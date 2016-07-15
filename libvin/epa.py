"""
Fetch data from fueleconomy.gov
(c) Copyright 2016 Dan Kegel <dank@kegel.com>
License: AGPL v3.0
"""

# Note: client app may wish to 'import requests_cache' and install a cache
# to avoid duplicate fetches
import json
import requests
import sys
import xmltodict
from pprint import pprint

# Local
from decoding import Vin
from nhtsa import *

class EPAVin(Vin):

    # Public interfaces

    def __init__(self, vin, verbosity=0, yearoffset=0):
        '''
        Decode the given vin and gather data about it from fueleconomy.gov.
        Verbosity above 0 adds logging to stdout.
        Set yearoffset = -1 to use the previous year's EPA data
        (for when EPA has a hole in its database).
        '''
        super(EPAVin, self).__init__(vin)

        self.verbosity = verbosity
        self.yearoffset = yearoffset
        if self.verbosity > 0 and self.yearoffset != 0:
            print "Setting yearoffset to %d" % yearoffset
        # Use the anonymized vin for privacy, and because it'll make lookups of
        # lots of identical-ish cars faster when using a web cache
        self.__nhtsa = nhtsa_decode(self.anonvin(), verbosity)
        if (self.__nhtsa == None):
            return
        self.__attribs = self.__get_attributes()
        self.__model = self.__get_model()
        if (self.__model != None):
            self.__ids, self.__trims = self.__get_ids()
            self.__eco   = [self.__get_vehicle_economy(id) for id in self.__ids]

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

    def nhtsaGVWRClass(self):
        '''
        FHWA GVWR class for this vehicle.
        1 - 0-6000 lbs
        2 - 6001-10000 lbs
        '''
        if self.nhtsa['GVWR'].startswith('Class'):
             # 'Class 3: 10,001 - 14,000 lb (4,536 - 6,350 kg)'
             return self.nhtsa['GVWR'].split(':')[0].split()[1]
        return None

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
    def ids(self):
        '''
        List of likely EPA ids for this vehicle.
        '''
        return self.__ids

    @property
    def trim(self):
        '''
        EPA trim for this vehicle.
        '''
        # FIXME: If we don't know which trim exactly, just pick the
        # first one.  We're guessing anyway, what with the fuzzy matching and all...
        return self.__trims[0]

    @property
    def trims(self):
        '''
        List of likely EPA trim for this vehicle.
        '''
        return self.__trims

    @property
    def eco(self):
        '''
        EPA fuel economy info dictionary for this vehicle.
        Fields of interest:
        - co2TailpipeGpm - present for most vehicles
        - co2TailpipeAGpm - present for some vehicles, matches EPA website
        In case of ambiguity, just one record is returned.
        '''
        return self.__eco[0]

    @property
    def ecos(self):
        '''
        List of EPA fuel economy info dictionaries for this vehicle.
        Fields of interest:
        - co2TailpipeGpm - present for most vehicles
        - co2TailpipeAGpm - present for some vehicles, matches EPA website
        In case of ambiguity, all possible records are returned.
        '''
        return self.__eco

    # Private interfaces

    def __remodel(self):
        '''
        Return model name translated from NHTSA-ese into EPA-ese
        '''
        m = self.nhtsa['Model']
        if self.make == 'Dodge':
            if m == 'Caravan/Grand Caravan':
                return 'Grand Caravan'
        elif self.make == 'Fiat':
            if m.endswith("00L"):
                return m.replace("00L", "00 L")
            if m.endswith("00X"):
                return m.replace("00X", "00 X")
        elif self.make == 'Ford':
            if m.startswith('F-150'):
                return m.replace('F-', 'F', 1)
        elif self.make == 'Infiniti':
            # L is a slightly longer version...
            if m == "Q70L":
                return "Q70"
            elif self.year == 2013 and m == 'EX35':
                # Rebadged, and NHTSA didn't notice
                return 'EX37'
        elif self.make == 'Mazda':
            if m.startswith('Mazda'):
                return m.replace('Mazda', '')
        elif self.make == 'Mercedes-Benz':
            if m.endswith('-Class'):
                # Rest of model name is in nhtsa['Series'], kind of
                return m.replace('-Class', '')
        elif self.make == 'MINI':
            if m.endswith('Hardtop'):
                return m.replace(' Hardtop', '')
        elif self.make == 'Nissan':
            if m == 'Versa Note':
                # Note is just the hatchback
                return 'Versa'
            elif m == 'NV200, City Express':
                # NHTSA's Make for this is 'Nissan, Chevrolet'!
                return 'NV200'
        elif self.make == 'Toyota':
            if m == 'Corolla Matrix':
                # Nobody has ever heard the official name 'Corolla Matrix'
                return 'Matrix'
            elif m == '4-Runner':
                return '4Runner'
        elif self.make == 'Volkswagen':
            if m == 'New Beetle':
                # EPA has just 'Beetle' for some years
                return 'Beetle'
        elif self.make == 'Volvo':
            if m.endswith("0CC"):
                return m.replace("0CC", "0 CC")
            if m == "S60/S60I":
                return "S60"
        return m

    def __get_attributes(self):
        '''
        Returns a list of adjectives for this vehicle that might help identify it in EPA model or trim names
        '''
        # Strongest attribute: the model name!
        attributes = [self.__remodel()]

        driveType = self.nhtsa['DriveType']
        if 'AWD' in driveType:
            attributes.append("AWD")
        elif '4WD' in driveType or '4x4' in driveType:
            attributes.append("4WD")
        elif 'Front' in driveType or 'FWD' in driveType:
            attributes.append("FWD")
            attributes.append("2WD")
        elif 'Rear' in driveType or 'RWD' in driveType:
            attributes.append("RWD")
            attributes.append("2WD")
        elif '4x2' in driveType or '2WD' in driveType:
            attributes.append("2WD")
        else:
            # 3FA6P0G76ER244757 has no drivetype listed at all, but is FWD.
            # FIXME: make this special case more specific somehow?
            # This guesses wrong for e.g. JM1DKBD74G0111725, can we improve that?
            if self.year > 1990:
                attributes.append("FWD")
                attributes.append("2WD")
                if self.verbosity > 1:
                    print("No drive type given, defaulting to FWD")

        if 'Trim' in self.nhtsa and self.nhtsa['Trim'] != "":
            for word in self.nhtsa['Trim'].split():
                attributes.append(word)
            # Special cases
            s = self.nhtsa['Trim']
            # Chevrolet: 1500=1/2ton, 2500=3/4ton, 3500=1 ton?
            if self.make == 'Chevrolet':
                if "1/2 ton" in s:
                    attributes.append('1500')
                if "3/4 ton" in s:
                    attributes.append('2500')
                if "1 ton" in s:
                    attributes.append('3500')
        if 'BodyClass' in self.nhtsa and self.nhtsa['BodyClass'] != "":
            for word in self.nhtsa['BodyClass'].split("/"):
                attributes.append(word)
        if 'Doors' in self.nhtsa and self.nhtsa['Doors'] != "":
            attributes.append(self.nhtsa['Doors']+'Dr')
            attributes.append(self.nhtsa['Doors']+'-Door')
        if 'Series' in self.nhtsa and self.nhtsa['Series'] != "":
            s = self.nhtsa['Series']
            if len(s) < 2:
                attributes.append(" " + s)
            else:
                attributes.append(s)
            # Handle Chevy Spark, where Series is e.g. "EV, 2LT"
            words = self.nhtsa['Series'].replace(",", "").split()
            if len(words) > 1:
                for word in words:
                    attributes.append(word)
            # Special cases
            # Chevrolet: 1500=1/2ton, 2500=3/4ton, 3500=1 ton?
            if self.make == 'Chevrolet':
                if "1/2 ton" in s:
                    attributes.append('1500')
                if "3/4 ton" in s:
                    attributes.append('2500')
                if "1 ton" in s:
                    attributes.append('3500')
            if self.make == 'Mercedes-Benz':
                # e.g. WDBTJ65JX5F126044: NHTSA calls it CLK320C, but EPA expects CLK320
                if s.endswith('0C'):
                    attributes.append(s[:-1])
            # sDrive 28i -> sDrive28i
            attributes.append(self.nhtsa['Series'].replace(" ", ""))

        if 'Series2' in self.nhtsa and self.nhtsa['Series2'] != "":
            attributes.append(self.nhtsa['Series2'])
            # https://vpic.nhtsa.dot.gov/mid/home/displayfile/29218
            # shows 2016 Lexus NX has Series2 of NX 200t / NX200t ... AWD
            # unfortunately, the AWD there is just a possibility
            for words in self.nhtsa['Series2'].split("/"):
                for word in words.split():
                    # FIXME: make this special case specific to Lexus?
                    if word != 'AWD':
                        attributes.append(word)

        if 'DisplacementL' in self.nhtsa and self.nhtsa['DisplacementL'] != '':
            attributes.append('%s L' % self.nhtsa['DisplacementL'])
            # EPA sometimes likes to go all precise
            if '.' not in self.nhtsa['DisplacementL']:
               attributes.append('%s.0 L' % self.nhtsa['DisplacementL'])
        if 'EngineCylinders' in self.nhtsa and self.nhtsa['EngineCylinders'] != '':
            attributes.append('%s cyl' % self.nhtsa['EngineCylinders'])

        if 'FuelTypePrimary' in self.nhtsa:
            # FIXME: also check FuelTypeSecondary?
            ftp = self.nhtsa['FuelTypePrimary']
            if 'FFV' in ftp or 'E85' in ftp:
                attributes.append('FFV')

        if 'BatteryKWh' in self.nhtsa and self.nhtsa['BatteryKWh'] != '':
            attributes.append('%s kW-hr' % self.nhtsa['BatteryKWh'])

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
        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=%s&make=%s' % (self.year + self.yearoffset, self.make)
        if self.verbosity > 0:
            print "epa:__get_possible_models: URL is %s" % url
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
        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=%s&make=%s&model=%s' % (self.year + self.yearoffset, self.make, self.model)
        if self.verbosity > 0:
            print "epa:__get_possible_ids: URL is %s" % url
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
                if attrib == "":
                    continue
                u = val.upper()
                if ((attrib.upper() in u)
                 or (attrib == '2WD' and ('FWD' in u or 'RWD' in u))):
                    if chars_matched == 0:
                        chars_matched = len(attrib)
                    else:
                        chars_matched += len(attrib) + 1  # for space

            if self.verbosity > 1:
                print "chars_matched %d, for %s" % (chars_matched, val)
            if (chars_matched > best_matched):
                best_ids = [key]
                best_len = len(val)
                best_matched = chars_matched
            elif (chars_matched > 0 and chars_matched == best_matched):
                if len(val) < best_len:
                    if self.verbosity > 1:
                       print "chars %d == %d, len %d < %d, breaking tie in favor of shorter trim" % (chars_matched, best_matched, len(val), best_len)
                    best_ids = [key]
                    best_len = len(val)
                    best_matched = chars_matched
                elif len(val) == best_len:
                    if self.verbosity > 1:
                        print "chars %d == %d, len %d == %d, marking tie" % (chars_matched, best_matched, len(val), best_len)
                    best_ids.append(key)
        if len(best_ids) == 0:
            if self.verbosity > 0:
                print "epa:__fuzzy_match: no match found for vin %s" % self.vin
            if self.verbosity > 1:
                pprint(mustmatch)
                pprint(attributes)
                pprint(choices)
        elif len(best_ids) > 1:
            if self.verbosity > 0:
                print "epa:__fuzzy_match: multiple matches for vin %s: " % self.vin + " / ".join(best_ids)
            if self.verbosity > 1:
                pprint(mustmatch)
                pprint(attributes)
                pprint(choices)
        return best_ids

    def __get_model(self):
        '''
        Given a decoded vin and its nhtsa data, look up its epa model name
        '''
        # Get candidate modifier strings
        id2models = self.__get_possible_models()
        if id2models == None:
            return None
        if self.verbosity > 0:
            print "Finding model for vin %s" % self.vin
        ids = self.__fuzzy_match(self.__remodel(), self.__attribs, id2models)
        if len(ids) != 1:
            if self.verbosity > 0:
                print "epa:__get_model: Failed to find model for vin %s" % self.vin
                pprint(id2models)
                pprint(self.__attribs)
                if self.verbosity > 1:
                    pprint(self.nhtsa)
            return None

        modelname = ids[0]  # key same as val
        if self.verbosity > 0:
            print "VIN %s has model %s" % (self.vin, modelname)
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
        if len(id2trim.items()) == 1:
            # No point in filtering if there's only one choice
            return [id2trim.keys(), id2trim.values()]
        if self.verbosity > 0:
            print "Finding trims for vin %s" % self.vin
        ids = self.__fuzzy_match(None, self.__attribs, id2trim)
        if len(ids) == 0:
            # Sometimes (e.g. Toyota Matrix) there is very little info
            # in the NHTSA decode, and filtering comes up empty.
            # So return unfiltered view.
            ids = id2trim.keys()
        trims = map(lambda x: id2trim[x], ids)
        if self.verbosity > 0:
            print("VIN %s has trim names %s" % (self.vin, " / ".join(trims)))
        return [ids, trims]

    def __get_vehicle_economy(self, id):
        '''
        Return dictionary of a particular vehicle's economy data from fueleconomy.gov, or None on error.
        id is from __get_vehicle_ids().
        '''

        url = 'http://www.fueleconomy.gov/ws/rest/vehicle/%s' % id
        if self.verbosity > 0:
            print "epa:__get_vehicle_economy: URL is %s" % url
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

def myquote(s):
    return s.replace(" ", "%20")

def main():
    verbosity = 0
    yearoffset = 0
    if len(sys.argv) > 1:
        verbosity = int(sys.argv[1])
    if len(sys.argv) > 2:
        yearoffset = int(sys.argv[2])
    for line in sys.stdin:
        vin = line.strip()
        v = EPAVin(vin, verbosity=verbosity, yearoffset=yearoffset)
        url1 = myquote("http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=%s&make=%s" % (v.year, v.make))
        url2 = myquote("http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=%s&make=%s&model=%s" % (v.year, v.make, v.model))
        print("    # Breadcrumbs for how libvin/epa.py looks up the epa results:")
        print("    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/%s" % v.decode())
        print("    # %s" % url1)
        print("    # %s" % url2)
        if len(v.ecos) > 1:
            print("    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:")
        for i in range(0, len(v.ecos)):
            print("    # http://www.fueleconomy.gov/ws/rest/vehicle/%s" % v.ids[i])
        print("    {'VIN': '%s', 'WMI': '%s', 'VDS': '%s', 'VIS': '%s'," % (v.decode(), v.wmi, v.vds, v.vis))
        print("     'MODEL': '%s', 'MAKE': '%s', 'YEAR': %d, 'COUNTRY': '%s'," % (v.nhtsaModel, v.make, v.year, v.country))
        print("     'REGION': '%s', 'SEQUENTIAL_NUMBER': '%s', 'FEWER_THAN_500_PER_YEAR': %s," % (v.region, v.vsn, v.less_than_500_built_per_year))
        print("     'nhtsa.trim': '%s', 'nhtsa.series': '%s'," % (v.nhtsa['Trim'], v.nhtsa['Series']))
        for i in range(0, len(v.ecos)):
            print("     'epa.id' : '%s', 'epa.co2TailpipeGpm': '%s', 'epa.model' : '%s', 'epa.trim' : '%s'," %
                  (v.ids[i], round(float(v.ecos[i]['co2TailpipeGpm']), 1), v.model, v.trims[i]))
        print("    },")

if __name__ == "__main__":
    main()
