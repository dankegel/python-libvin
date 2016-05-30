"""
Copyright (C) 2016 Dan Kegel
Look up EPA mileage given make, model, and year.
License: LGPL
"""

# See "Practical Data Science Cookbook" for a nice look at this data in Python.
# Also, several students did writeups of how to look at this data in R, e.g.
# https://rpubs.com/jeknov/auto-eda
# https://rpubs.com/agz1117/ConnectedCar

import csv
import os
from collections import namedtuple

epa_loaded = False
epa_table = {}

def epa_mmy_lookup(make, model, year):
    '''Return a tuple of EPA fuel economy data, including especially
       UCity -- city MPG
       UHighway -- highway MPG
       co2TailpipeGpm -- grams per mile co2 emissions
       See http://www.fueleconomy.gov/feg/ws/index.shtml for definitions of other fields
       Not threadsafe
    '''
    global epa_loaded
    global epa_table
    if not epa_loaded:
        here = os.path.dirname(os.path.abspath(__file__)) 
        with open(here + '/epa/vehicles.csv') as f:
            csv_f = csv.reader(f)
            headers = next(csv_f)
            Row = namedtuple('Row', headers)
            for line in csv_f:
                row = Row(*line)
                mmy = row.make + "_" + row.model + "_" + str(row.year)
                print "%s: city %s, hwy %s, co2/mi %s" % (mmy, row.UCity, row.UHighway, row.co2TailpipeGpm)
                epa_table[mmy] = row
        epa_loaded = True

    return epa_table[make + "_" + model + "_" + str(year)]
