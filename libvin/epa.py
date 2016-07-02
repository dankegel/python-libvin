"""
Fetch data from fueleconomy.gov
(c) Copyright 2016 Dan Kegel <dank@kegel.com>
License: AGPL v3.0
"""

# Note: client app may wish to 'import requests_cache' and install a cache
# to avoid duplicate fetches
import requests
import itertools
import json
import xmltodict

# Local
from decoding import Vin
from nhtsa import *

class EPAVin(Vin):

    # Public interfaces

    def __init__(self, vin):
        super(EPAVin, self).__init__(vin)

        self.__nhtsa = nhtsa_decode(vin)
        self.__attribs = self.__get_attributes()
        self.__model = self.__get_model()
        if (self.__model != None):
            self.__ids, self.__trims = self.__get_ids()
            self.__eco   = self.__get_vehicle_economy()

    @property
    def nhtsa(self):
        '''
        NHTSA info dictionary for this vehicle.
        '''
        return self.__nhtsa

    @property
    def nhtsaModel(self):
        '''
        NHTSA model name for this vehicle.
        '''
        return self.nhtsa['Model']

    @property
    def model(self):
        '''
        EPA model name for this vehicle.
        '''
        return self.__model

    @property
    def id(self):
        '''
        EPA id for this vehicle.
        '''
        # FIXME: If we don't know which trim exactly, just pick the
        # first one.  We're guessing anyway, what with the fuzzy matching and all...
        return self.__ids[0]

    @property
    def trim(self):
        '''
        EPA trim for this vehicle.
        '''
        # FIXME: If we don't know which trim exactly, just pick the
        # first one.  We're guessing anyway, what with the fuzzy matching and all...
        return self.__trims[0]

    @property
    def eco(self):
        '''
        EPA fuel economy info dictionary for this vehicle.
        Fields of interest:
        - co2TailpipeGpm - present for most vehicles
        - co2TailpipeAGpm - present for some vehicles, matches EPA website
        '''
        return self.__eco

    # Private interfaces

    def __get_attributes(self):
        '''
        Returns a list of adjectives for this vehicle that might help identify it in EPA model or trim names
        '''
        # Strongest attribute: the model name!
        attributes = [self.nhtsa['Model']]

        driveType = self.nhtsa['DriveType']
        if 'AWD' in driveType:
            attributes.append("AWD")
        elif '4WD' in driveType or '4x4' in driveType:
            attributes.append("4WD")
        elif '4x2' in driveType:
            attributes.append("2WD")
        elif 'Front' in driveType or 'FWD' in driveType:
            attributes.append("FWD")
            attributes.append("2WD")

        if 'Trim' in self.nhtsa and self.nhtsa['Trim'] != "":
            attributes.append(self.nhtsa['Trim'])
        if 'BodyClass' in self.nhtsa and self.nhtsa['BodyClass'] != "":
            attributes.append(self.nhtsa['BodyClass'])
        if 'Series' in self.nhtsa and self.nhtsa['Series'] != "":
            attributes.append(self.nhtsa['Series'])
        if 'Series2' in self.nhtsa and self.nhtsa['Series2'] != "":
            attributes.append(self.nhtsa['Series2'])

        if 'DisplacementL' in self.nhtsa and self.nhtsa['DisplacementL'] != '':
            attributes.append('%s L' % self.nhtsa['DisplacementL'])
            # EPA sometimes likes to go all precise
            if '.' not in self.nhtsa['DisplacementL']:
               attributes.append('%s.0 L' % self.nhtsa['DisplacementL'])
        if 'EngineCylinders' in self.nhtsa and self.nhtsa['EngineCylinders'] != '':
            attributes.append('%s cyl' % self.nhtsa['EngineCylinders'])

        if 'Manual' in self.nhtsa['TransmissionStyle']:
            attributes.append('MAN')
        elif 'Auto' in self.nhtsa['TransmissionStyle']:
            attributes.append('AUTO')
        elif 'CVT' in self.nhtsa['TransmissionStyle']:
            attributes.append('CVT')
            attributes.append('Variable')

        # Twin turbo is "Yes, Yes"!
        if 'Turbo' in self.nhtsa and 'Yes' in self.nhtsa['Turbo']:
            attributes.append('Turbo')

        return attributes

    def __get_possible_models(self):
        '''
        Return dict of possible models for given year of given make.
        The key and value are the same, and are the values needed by get_vehicle_ids().
        '''

        key2model = dict()
        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=%s&make=%s' % (self.year, self.make)
        try:
            r = requests.get(url)
        except requests.Timeout:
            print "epa:__get_possible_models: connection timed out"
            return None
        except requests.ConnectionError:
            print "epa:__get_possible_models: connection failed"
            return None
        try:
            content = r.content
            # You can't make this stuff up.  I love xml.
            for item in xmltodict.parse(content).popitem()[1].items()[0][1]:
               model = item.popitem()[1]
               key2model[model] = model
        except AttributeError:
            print "epa:__get_possible_models: no models for year %s, make %s" % (self.year, self.make)
            return None
        except ValueError:
            print "epa:__get_possible_models: could not parse result"
            return None
        return key2model

    def __get_possible_ids(self):
        '''
        Return dictionary of id -> vehicle trim string from fueleconomy.gov, or None on error.
        The id's are those needed by get_vehicle_economy().
        '''

        id2trim = dict()
        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=%s&make=%s&model=%s' % (self.year, self.make, self.model)
        try:
            r = requests.get(url)
        except requests.Timeout:
            print "epa:__get_possible_ids: connection timed out"
            return None
        except requests.ConnectionError:
            print "epa:__get_possible_ids: connection failed"
            return None
        try:
            content = r.content
            # You can't make this stuff up.  I love xml.
            parsed = xmltodict.parse(content)
            innards = parsed.popitem()[1].items()[0][1]
            # special case for N=1
            if not isinstance(innards, list):
               innards = [ innards ]
            for item in innards:
               id = item.popitem()[1]
               trim = item.popitem()[1]
               id2trim[id] = trim
        except ValueError:
            print "epa:__get_possible_ids: could not parse result"
            return None
        return id2trim

    def __fuzzy_match(self, mustmatch, attributes, choices):
        '''
        Given a base name and a bunch of attributes, find the choice that matches them the best.
        mustmatch : string
        attributes : string[]
        choices : dict mapping id to string
        Returns: array of ids of best matching choices
        '''

        best_ids = []     # id of best matching trims
        best_len = 0      # len of best matching trims
        best_matched = 0
        for (key, val) in choices.iteritems():
            # optional mandatory attribute
            # to prevent [Q60 AWD] from matching Q85 AWD instead of Q60 AWD Coupe
            if mustmatch != None and mustmatch.upper() not in val.upper():
                continue
            # Find choice that matches most chars from attributes.
            # In case of a tie, prefer shortest choice.
            chars_matched = 0
            for attrib in attributes:
                if attrib != "" and attrib.upper() in val.upper():
                    if chars_matched == 0:
                        chars_matched = len(attrib)
                    else:
                        chars_matched += len(attrib) + 1  # for space
            #print "chars_matched %d, for %s" % (chars_matched, val)
            if (chars_matched > best_matched):
                best_ids = [key]
                best_len = len(val)
                best_matched = chars_matched
            elif (chars_matched > 0 and chars_matched == best_matched):
                if len(val) < best_len:
                    #print "chars %d == %d, len %d < %d, breaking tie in favor of shorter trim" % (chars_matched, best_matched, len(val), best_len)
                    best_ids = [key]
                    best_len = len(val)
                    best_matched = chars_matched
                elif len(val) == best_len:
                    #print "chars %d == %d, len %d == %d, marking tie" % (chars_matched, best_matched, len(val), best_len)
                    best_ids.append(key)
        if len(best_ids) == 0:
            print "epa:__fuzzy_match: no match found for vin %s" % self.vin
        elif len(best_ids) > 1:
            print "epa:__fuzzy_match: multiple matches for vin %s: " % self.vin + " / ".join(best_ids)
        return best_ids

    def __get_model(self):
        '''
        Given a decoded vin and its nhtsa data, look up its epa model name
        '''
        # Get candidate modifier strings
        id2models = self.__get_possible_models()
        if id2models == None:
            return None
        #print "Finding model for vin %s" % self.vin
        # Special case for Mercedes-Benz, which puts the real model in Series
        oldmodel = self.nhtsa['Model']
        model = oldmodel.replace('-Class', '')
        ids = self.__fuzzy_match(model, self.__attribs, id2models)
        if len(ids) != 1:
            # Second chance for alternate spellings
            if '4WD' in self.__attribs:
                tribs = self.__attribs
                tribs.append('AWD')
                print "Searching again with AWD"
                ids = self.__fuzzy_match(self.nhtsa['Model'], tribs, id2models)
            elif '2WD' in self.__attribs and 'FWD' not in self.__attribs:
                tribs = self.__attribs
                tribs.append('RWD')
                print "Searching again with RWD"
                ids = self.__fuzzy_match(self.nhtsa['Model'], tribs, id2models)
            elif 'Mazda' in self.nhtsa['Model']:
                oldmodel = self.nhtsa['Model']
                model = oldmodel.replace('Mazda', '')
                tribs = self.__attribs
                tribs.append(model)
                print "Searching again with %s instead of %s" % (model, oldmodel)
                ids = self.__fuzzy_match(model, tribs, id2models)

        if len(ids) != 1:
            print "epa:__get_model: Failed to find model for vin %s" % self.vin
            return None

        modelname = ids[0]  # key same as val
        #print "VIN %s has model %s" % (self.vin, modelname)
        return modelname

    def __get_ids(self):
        '''
        Given a decoded vin, look up the matching epa id(s) and trims, or return None on failure
        '''
        if self.model == None:
            return None
        id2trim = self.__get_possible_ids()
        if id2trim == None:
            return None
        #print "Finding trims for vin %s" % self.vin
        ids = self.__fuzzy_match(None, self.__attribs, id2trim)
        if len(ids) == 0:
            print "epa:__get_id: No trims found for vin %s" % self.vin
            return None
        trims = map(lambda x: id2trim[x], ids)
        #print("VIN %s has trim names %s" % (self.vin, " / ".join(trims)))
        return [ids, trims]

    def __get_vehicle_economy(self):
        '''
        Return dictionary of a particular vehicle's economy data from fueleconomy.gov, or None on error.
        id is from __get_vehicle_ids().
        '''

        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/%s' % self.id
        try:
            r = requests.get(url)
        except requests.Timeout:
            print "epa:__get_vehicle_economy: connection timed out"
            return None
        except requests.ConnectionError:
            print "epa:__get_vehicle_economy: connection failed"
            return None
        try:
            content = r.content
            return xmltodict.parse(content).popitem()[1]
        except ValueError:
            print "epa:__get_vehicle_economy: could not parse result"
            return None
        return None
