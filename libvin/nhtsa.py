"""
Fetch a VIN record from NHTSA
(c) Copyright 2016 Dan Kegel <dank@kegel.com>
License: AGPL v3.0
"""

# Note: client app may wish to 'import requests_cache' and install a cache
# to avoid duplicate fetches
import requests
import requests_cache
import time

def nhtsa_decode(vin, verbosity=0):
    '''
    Return vpic.nhtsa.dot.gov's interpretation of the VIN in a dictionary, or None on error.

    ErrorCode member of dictionary is a string starting with '0'
    if NHTSA thinks it has good data for that vin.

    Fields set seem to depend on the manufacturer.
    Here's which fields seem to be set for a few makes:

    BodyClass, Make, Model, ModelYear, GVWR: all
    Doors: most
    EngineModel: Honda, Acura
    EngineCylinders: Dodge
    DisplacementCC: Infiniti, BMW, Dodge
    DriveType: Infiniti, Dodge, Mitsubishi
    Series: BMW, Dodge, Mitsubishi
    Trim: BMW, Dodge
    '''

    tries = 5
    jresult = None
    results = None

    while tries > 0:
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/' + vin + '?format=json'
        if (verbosity > 0):
            print("nhtsa_decode: url is %s" % url)
        try:
            if tries < 2:
                with requests_cache.disabled():
                    r = requests.get(url)
            else:
                r = requests.get(url)
        except requests.Timeout:
            if verbosity > 0:
                print "nhtsa: connection timed out"
            continue
        except requests.ConnectionError:
            if verbosity > 0:
                print "nhtsa: connection failed"
            continue
        try:
            jresult = r.json()
            results = jresult['Results'][0]
        except ValueError:
            if (verbosity > 0):
                print("nhtsa: could not parse result %s" % r.text)
            return None

        if jresult['Message'] != "Execution Error":
            break
        if (verbosity > 0):
            print("nhtsa: execution error; sleeping then retrying without cache")
        tries -= 1
        time.sleep(1)

    if tries == 0:
       if (verbosity > 0):
           print("error: nhtsa: Make not found in results %s" % r.text)
       return None

    # Sanity-check
    if 'Make' not in results:
       if (verbosity > 0):
           print("error: nhtsa: Make not found in results %s" % r.text)
       return None

    # Strip trailing spaces (as in 'Hummer ')
    for key in results:
        results[key] = results[key].rstrip()

    # Add missing decodes
    if results['Make'] == 'HONDA' and results['Turbo'] == '':
        # NHTSA does not yet decode turbo for some models, e.g.
        # 2016 Civic EX-L Sedan 19XFC1F7XGE028370
        # 2016 Civic EX-T Coupe 2HGFC3B37GH354325
        # FC1 and FC3 don't show up in older VIN guides:
        # 2014: https://vpic.nhtsa.dot.gov/mid/home/displayfile/29820
        # 2015: https://vpic.nhtsa.dot.gov/mid/home/displayfile/29821
        # FC1 first showed up in
        # 2016: https://vpic.nhtsa.dot.gov/mid/home/displayfile/29039
        # FC3 is on sale in 2016 (early?), NHTSA can't decode it yet at all
        vds = vin[3:6]
        if vds == 'FC1' or vds == 'FC3':
            results['Turbo'] = 'Yes'

    return results
