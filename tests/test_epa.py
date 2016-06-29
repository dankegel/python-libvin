# -*- coding: utf-8 -*-
from nose.tools import assert_equals, assert_true, raises

# To run tests that depend on network, do e.g. 'NETWORK_OK=1 nose2'
import os
if not 'NETWORK_OK' in os.environ:
    print "skipping network tests; set NETWORK_OK=1 to run"
else:
    from libvin.epa import EPAVin
    from libvin.static import *
    from . import TEST_DATA

    # Cache responses for 7 days to be kind to EPA's and nhtsa's servers
    import requests_cache
    requests_cache.install_cache('libvin_tests_cache', expire_after=7*24*60*60)

    class TestEPA(object):

        def test_model(self):
            for test in TEST_DATA:
                v = EPAVin(test['VIN'])
                if not 'nhtsa.model' in test:
                    continue
                print "Testing nhtsaModel of %s - %s" % (test['VIN'], v.nhtsaModel)
                assert_equals(v.nhtsaModel, test['nhtsa.model'])
                if not 'epa.model' in test:
                    continue
                print "Testing model of %s - %s" % (test['VIN'], v.model)
                assert_equals(v.model, test['epa.model'])

        def test_co2(self):
            for test in TEST_DATA:
                v = EPAVin(test['VIN'])
                if not 'epa.co2TailpipeGpm' in test:
                    continue
                co2 = v.eco['co2TailpipeGpm']
                print "Testing co2 of %s - %s" % (test['VIN'], co2)
                assert_equals(co2, test['epa.co2TailpipeGpm'])
