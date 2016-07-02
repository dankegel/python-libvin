# -*- coding: utf-8 -*-
from nose.tools import assert_almost_equals

# To run tests that depend on network, do e.g. 'NETWORK_OK=1 nose2'
import os
if not 'NETWORK_OK' in os.environ:
    print "skipping network tests; set NETWORK_OK=1 to run"
else:
    from libvin.epa import EPAVin
    from libvin.static import *
    from . import TEST_DATA

    class TestEPA(object):

        def test_co2(self):
            for test in TEST_DATA:
                if not 'epa.co2TailpipeGpm' in test:
                    continue
                print("Testing co2 of %s:" % test['VIN'])
                v = EPAVin(test['VIN'])
                if v.model == None:
                    print "Model unknown, skipping"
                    continue
                co2 = v.eco['co2TailpipeGpm']
                print("%s ; id %s, model %s, co2TailpipeGpm %s" % (test['VIN'], v.id, v.model, co2))
                # Prints to help when extending the test matrix
                #print("    # http://www.fueleconomy.gov/ws/rest/vehicle/%s" % v.id)
                #print("     'epa.id' : '%s', 'epa.co2TailpipeGpm': '%s', 'epa.model' : '%s', 'epa.trim' : '%s'," %
                #      (v.id, round(float(co2), 1), v.model, v.trim))
                #print("")
                assert_almost_equals(float(co2), float(test['epa.co2TailpipeGpm']), places=0)
