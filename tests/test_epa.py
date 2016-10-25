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
                yearoffset = 0
                if 'yearoffset' in test:
                    yearoffset=int(test['yearoffset'])
                v = EPAVin(test['VIN'], verbosity=0, yearoffset=yearoffset)
                co2 = round(float(v.eco['co2TailpipeGpm']), 1)
                print("%s ; id %s, co2TailpipeGpm (want %s, got %s), make %s, model %s, trim %s" % (test['VIN'], v.id, test['epa.co2TailpipeGpm'], co2, v.make, v.model, v.trim))
                assert_almost_equals(float(co2), float(test['epa.co2TailpipeGpm']), places= -1)
