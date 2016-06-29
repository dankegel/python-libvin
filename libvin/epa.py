"""
Fetch data from fueleconomy.gov
(c) Copyright 2016 Dan Kegel <dank@kegel.com>
License: AGPL v3.0
"""

# Note: client app may wish to 'import requests_cache' and install a cache
# to avoid duplicate fetches
import requests
import requests_cache
# Cache responses for 7 days to be kind to nhtsa's server
requests_cache.install_cache('libvin_tests_cache', expire_after=7*24*60*60)
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
        self.__model = self.__get_model()
        self.__id    = self.__get_id()
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
        return self.__id

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

    def __get_possible_models(self):
        '''
        Return list of possible models for given year of given make.
        The models are those needed by get_vehicle_ids().
        '''

        models = []
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
               models.append(item.popitem()[1])
        except AttributeError:
            print "epa:__get_possible_models: no models for year %s, make %s" % (self.year, self.make)
            return None
        except ValueError:
            print "epa:__get_possible_models: could not parse result"
            return None
        return models

    def __get_model(self):
        '''
        Given a decoded vin and its nhtsa data, look up its epa model name
        '''
        models = self.__get_possible_models()
        if models == None:
            return None

        # Get candidate modifier strings
        modifiers = []
        driveType = self.nhtsa['DriveType']
        if 'AWD' in driveType or '4WD' in driveType or '4x4' in driveType:
            modifiers.append("4WD")
            modifiers.append("AWD")
            # Special cases
            if self.make == 'GMC' and self.nhtsaModel == 'Sierra':
                modifiers.append("K15")
        elif 'Front' in driveType or 'FWD' in driveType or '4x2' in driveType:
            modifiers.append("2WD")
            modifiers.append("FWD")
            # Special cases
            if self.make == 'GMC' and self.nhtsaModel == 'Sierra':
                modifiers.append("C15")
        else:
            # special cases
            if self.make == 'Ford' and self.nhtsaModel == 'Focus':
                modifiers.append("FWD")
        if 'Trim' in self.nhtsa and self.nhtsa['Trim'] != "":
            modifiers.append(self.nhtsa['Trim'])
        if 'BodyClass' in self.nhtsa and self.nhtsa['BodyClass'] != "":
            modifiers.append(self.nhtsa['BodyClass'])
        if 'Series' in self.nhtsa and self.nhtsa['Series'] != "":
            modifiers.append(self.nhtsa['Series'])

        # Throw them against the wall and see what sticks
        # FIXME: pick model with highest number of matches regardless of order
        for L in range(len(modifiers)+1, 0, -1):
            for subset in itertools.permutations(modifiers, L):
                modified_model = self.nhtsaModel + " " + " ".join(subset)
                if modified_model in models:
                    return modified_model

        if self.nhtsaModel in models:
            return self.nhtsaModel

        print "epa:__get_model: Failed to find model for %s" % self.vin
        return None

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

    def __get_id(self):
        '''
        Given a decoded vin, look up its epa id, or return None on failure
        '''
        if self.model == None:
            return None
        id2trim = self.__get_possible_ids()

        # If only one choice, return it
        if (len(id2trim) == 1):
            key, value = id2trim.popitem()
            return key

        # Filter by engine displacement
        displacement = '%s L' % self.nhtsa['DisplacementL']
        matches = [key for key, value in id2trim.items() if displacement in value.upper()]
        if (len(matches) == 1):
            return matches[0]

        # Filter by transmission
        tran = None
        if 'Manual' in self.nhtsa['TransmissionStyle']:
            tran = 'MAN'
        if 'Auto' in self.nhtsa['TransmissionStyle']:
            tran = 'AUTO'
        if tran != None:
            matches = [key for key, value in id2trim.items() if tran in value.upper()]
            if (len(matches) == 1):
                return matches[0]

        print "epa:__get_id: Failed to match trim for %s" % self.vin
        return None

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
