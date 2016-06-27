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
from pprint import pprint
import itertools
import json
import xmltodict

# Local
from decoding import Vin
from nhtsa import *

def epa_get_models(year, make):
    '''
    Return list of models for given year of given make.
    The models are those needed by epa_get_vehicle_ids().
    '''

    models = []
    url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=%s&make=%s' % (year, make)
    try:
        r = requests.get(url)
    except requests.Timeout:
        print "epa: connection timed out"
        return None
    except requests.ConnectionError:
        print "epa: connection failed"
        return None
    try:
        content = r.content
        # You can't make this stuff up.  I love xml.
        for item in xmltodict.parse(content).popitem()[1].items()[0][1]:
           models.append(item.popitem()[1])
    except ValueError:
        print "epa: could not parse result"
        return None
    pprint(models)
    return models

def epa_get_vehicle_ids(year, make, model):
    '''
    Return dictionary of id -> vehicle trim string from fueleconomy.gov, or None on error.
    The id's are those needed by epa_get_vehicle_economy().
    '''

    id2trim = dict()
    url = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=%s&make=%s&model=%s' % (year, make, model)
    try:
        r = requests.get(url)
    except requests.Timeout:
        print "epa: connection timed out"
        return None
    except requests.ConnectionError:
        print "epa: connection failed"
        return None
    try:
        content = r.content
        # You can't make this stuff up.  I love xml.
        print("Content is %s" % content)
        parsed = xmltodict.parse(content)
        pprint(parsed)
        for item in xmltodict.parse(content).popitem()[1].items()[0][1]:
           id = item.popitem()[1]
           trim = item.popitem()[1]
           id2trim[id] = trim
    except ValueError:
        print "epa: could not parse result"
        return None
    return id2trim

def epa_get_vehicle_economy(id):
    '''
    Return dictionary of a particular vehicle's economy data from fueleconomy.gov, or None on error.
    id is from epa_get_vehicle_ids().
    '''

    url = 'http://www.fueleconomy.gov/ws/rest/vehicle/%s' % id
    try:
        r = requests.get(url)
    except requests.Timeout:
        print "epa: connection timed out"
        return None
    except requests.ConnectionError:
        print "epa: connection failed"
        return None
    try:
        content = r.content
        return xmltodict.parse(content).popitem()[1]
    except ValueError:
        print "epa: could not parse result"
        return None
    return None

def epa_get_model(vin, nhtsa):
    '''
    Given a decoded vin and its nhtsa data, look up its epa model name
    '''
    models = epa_get_models(vin.year, vin.make)
    model = nhtsa['Model']

    # Try it without modifiers first
    if model in models: 
        return model

    # Get candidate modifier strings
    modifiers = []
    driveType = nhtsa['DriveType']
    if 'Front' in driveType or 'FWD' in driveType or '4x2' in driveType:
        modifiers.append("2WD")
        modifiers.append("FWD")
    if 'Trim' in nhtsa and nhtsa['Trim'] != "":
        modifiers.append(nhtsa['Trim'])
    if 'BodyClass' in nhtsa and nhtsa['BodyClass'] != "":
        modifiers.append(nhtsa['BodyClass'])

    # Throw them against the wall and see what sticks
    for L in range(0, len(modifiers)+1):
        for subset in itertools.permutations(modifiers, L):
            modified_model = model + " " + " ".join(subset) 
            print "Checking %s" % modified_model
            if modified_model in models: 
                return modified_model

    print "Failed to find model"
    pprint(nhtsa)
    return None

def epa_get_id(vin, nhtsa, model):
    '''
    Given a decoded vin, look up its epa id, or return None on failure
    '''
    #nhtsa = nhtsa_decode(vin.decode())
    #model = epa_get_model(vin, nhtsa)
    if model == None:
        return None
    id2trim = epa_get_vehicle_ids(vin.year, vin.make, model)

    # If only one choice, return it
    if (len(id2trim) == 1):
        key, value = id2trim.popitem()
        return key

    # Filter by engine displacement
    displacement = '%s L' % nhtsa['DisplacementL']
    print "Filtering by displacement %s" % displacement
    matches = [key for key, value in id2trim.items() if displacement in value.upper()]
    if (len(matches) == 1):
        return matches[0]

    # Filter by transmission
    print "Filtering by transmission %s" % nhtsa['TransmissionStyle']
    tran = None
    if 'Manual' in nhtsa['TransmissionStyle']:
        tran = 'MAN'
    if 'Auto' in nhtsa['TransmissionStyle']:
        tran = 'AUTO'
    if tran != None:
        matches = [key for key, value in id2trim.items() if tran in value.upper()]
        if (len(matches) == 1):
            return matches[0]

    print "Failed to match"
    pprint(id2trim)
    pprint(nhtsa)
    return None

def main():
    #v = Vin('2A4GM684X6R632476')  fails!  NHTSA engine info wrong
    #'19XFB4F24DE547421',
    for vin in [
        '1C4RJEAG2EC476429',
        '1D7RB1CP8BS798034',
        '1D7RB1CT1BS488952',
        '19UUA65694A043249',
        '1FAHP3FN8AW139719',
        '1GKEV13728J123735',
        '1GT020CG4EF828544',
        '1GYFC56299R410242',
        '19VDE2E5XEE644230',
        '2A4GM684X6R632476',
        '2B3KA43G27H825762',
        '2C3CDYAGXDH825982',
        '2C4RDGBG4FR987134',
        '2D4RN6DX5AR939562',
        '2FTCF15F2ECA55516',
        '2G61W5S83E9422251',
        '2HNYD18975H033218',
        '2LMHJ5AT9CB565906',
        '3C3CFFCR9FT528063',
        '3C6JD7CT4CG104778',
        '3D4PH6FV5AT152960',
        '3D4PH7FG1BT808130',
        '3D73Y3CL0BG113805',
        '3GYVKMEF5AG416315',
        '3LNHL2GC1BR262548',
        '4A31K3DT4CE403200',
        '5FRYD3H26GB020813',
        '5GADS13S072592644',
        '5GNRNGEE9A8215904',
        '5J6TF1H33CL339137',
        '5J8TB1H27CA348655',
        '5N1CR2MN6EC875492',
        '5UMDU93436L421092',
        '5UXXW5C54F0791433',
        'JA4AD2A3XEZ426420',
        'JH4CW2H53BC567925',
        'JN1CV6FE4EM164066',
        'JN1AZ44EX9M403788',
        'JN8BS1MW7EM920252',
        'JN8CS1MU0DM236239',
        'JTHBW1GG7D2369737',
        'JTJHY7AX4D4667505',
        'JM1BL1SF3A1267720',
        'KNDJT2A54D7883468',
        'SCBEC9ZA1EC225243',
        'SCFAD01A65G199359',
        'TRUSC28N711268458',
        'VNKJTUD36FA838549',
        'W04GW5EV0B1603732',
        'WA1EY74LX9D205644',
        'WBSWL9C54AP786013',
        'WDCYC7DF3FX109287',
        'WDDNG7BB4AA522219',
        'WUADUAFG6AN410499',
        'WVGAV7AX9BW549850',
        'YV1902FH5D1796335']:
        v = Vin(vin)
        nhtsa = nhtsa_decode(v.decode())
        model = epa_get_model(v, nhtsa)
        id = epa_get_id(v, nhtsa, model)
        print "VIN %s, Make: %s, Model: %s, Year: %s, id: %s" % (vin, v.make, model, v.year, id)
        if id == None:
            print("Could not find EPA id for vin %s" % vin)
        else:
            eco = epa_get_vehicle_economy(id)
            co2 = eco['co2TailpipeGpm']     # This value doesn't quite match what's on website
            #co2 = eco['co2TailpipeAGpm']   # This one does, but isn't always present
            print "VIN %s, Make: %s, Model: %s, Year: %s, Grams co2 per mile: %s" % (vin, v.make, model, v.year, co2)
            if co2 == 0.0:
                pprint(eco)

if __name__ == "__main__":
    main()
