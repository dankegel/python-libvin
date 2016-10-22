# To run tests that depend on network, do e.g. 'NETWORK_OK=1 nose2'
import os
if 'NETWORK_OK' in os.environ:
    import requests
    import requests_cache
    # Cache responses for 7 days to be kind to servers (and rerun quickly)
    requests_cache.install_cache('libvin_tests_cache', expire_after=7*24*60*60)

# Sorted alphabetically by VIN
TEST_DATA = [
    # http://www.fueleconomy.gov/ws/rest/vehicle/37077
    {'VIN': '19XFC2F58GE223856', 'WMI': '19X', 'VDS': 'FC2F58', 'VIS': 'GE223856',
     'MODEL': 'Civic', 'MAKE': 'Honda', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '223856', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37077', 'epa.co2TailpipeGpm': '262.0', 'epa.model' : 'Civic 4Dr', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 2.0 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/37075
    {'VIN': '19XFC1F7XGE028370', 'WMI': '19X', 'VDS': 'FC1F7X', 'VIS': 'GE028370',
     'MODEL': 'Civic', 'MAKE': 'Honda', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '028370', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37075', 'epa.co2TailpipeGpm': '252.0', 'epa.model' : 'Civic 4Dr', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 1.5 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=1C4RJEAG2EC476429&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/33496
    {'VIN': '1C4RJEAG2EC476429', 'WMI': '1C4', 'VDS': 'RJEAG2', 'VIS': 'EC476429',
     'MODEL': 'Grand Cherokee', 'MAKE':  'Jeep', 'YEAR': 2014, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '476429', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '33496', 'epa.co2TailpipeGpm': '444.0', 'epa.model' : 'Grand Cherokee 2WD', 'epa.trim' : 'Auto 8-spd, 6 cyl, 3.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1C6RR6GG1FS674987
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Ram
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Ram&model=1500%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/35741
    {'VIN': '1C6RR6GG1FS674987', 'WMI': '1C6', 'VDS': 'RR6GG1', 'VIS': 'FS674987',
     'MODEL': 'Ram', 'MAKE': 'Ram', 'YEAR': 2015, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '674987', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '1500-SLT', 'nhtsa.series': '',
     'epa.id' : '35741', 'epa.co2TailpipeGpm': '451.0', 'epa.model' : '1500 2WD', 'epa.trim' : 'Auto 8-spd, 6 cyl, 3.6 L',
    },

    # http://www.vindecoder.net/?vin=1D7RB1CP8BS798034&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/30456
    {'VIN': '1D7RB1CP8BS798034', 'WMI': '1D7', 'VDS': 'RB1CP8', 'VIS': 'BS798034',
     'MODEL': 'Ram 1500', 'MAKE':  'Dodge', 'YEAR': 2011, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '798034', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '30456', 'epa.co2TailpipeGpm': '592.5', 'epa.model' : 'Ram 1500 Pickup 2WD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 4.7 L',
    },

    # http://www.vindecoder.net/?vin=1D7RB1CT1BS488952&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/30457
    {'VIN': '1D7RB1CT1BS488952', 'WMI': '1D7', 'VDS': 'RB1CT1', 'VIS': 'BS488952',
     'MODEL': 'Ram 1500', 'MAKE':  'Dodge', 'YEAR': 2011, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '488952', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '30457', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'Ram 1500 Pickup 2WD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 5.7 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1FMCU59H48KB89898
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Ford
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Ford&model=Escape%20Hybrid%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/24113
    {'VIN': '1FMCU59H48KB89898', 'WMI': '1FM', 'VDS': 'CU59H4', 'VIS': '8KB89898',
     'MODEL': 'Escape', 'MAKE': 'Ford', 'YEAR': 2008, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'B89898', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '24113', 'epa.co2TailpipeGpm': '317.4', 'epa.model' : 'Escape Hybrid 4WD', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 2.3 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/37047
    # Note: EPA has option package names like
    #  F150 5.0L 2WD FFV GVWR>7599 LBS PAYLOAD PACKAGE
    #  F150 Pickup 4WD FFV
    #  F150 2.7L 4WD GVWR>6799 LBS PAYLOAD PACKAGE
    # and NHTSA has attributes like
    #  <GVWR>Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)</GVWR>
    # libvin/epa.py will need to handle GVWR intelligently to match those.
    # Not sure it's worth it yet.
    {'VIN': '1FTEW1EP7GKD77746', 'WMI': '1FT', 'VDS': 'EW1EP7', 'VIS': 'GKD77746',
     'MODEL': 'F-150', 'MAKE': 'Ford', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'D77746', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37047', 'epa.co2TailpipeGpm': '452.0', 'epa.model' : 'F150 Pickup 4WD', 'epa.trim' : 'Auto (S6), 6 cyl, 2.7 L, Turbo',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/37040
    {'VIN': '1FTEW1C80GKD23989', 'WMI': '1FT', 'VDS': 'EW1C80', 'VIS': 'GKD23989',
     'MODEL': 'F-150', 'MAKE': 'Ford', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'D23989', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37040', 'epa.co2TailpipeGpm': '454.0', 'epa.model' : 'F150 Pickup 2WD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GB0C4EGXGZ280783
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Chevrolet&model=Silverado%20C15%202WD
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/37007
    ## http://www.fueleconomy.gov/ws/rest/vehicle/37006
    ## http://www.fueleconomy.gov/ws/rest/vehicle/37008
    {'VIN': '1GB0C4EGXGZ280783', 'WMI': '1GB', 'VDS': '0C4EGX', 'VIS': 'GZ280783',
     'MODEL': 'Silverado', 'MAKE': 'Chevrolet', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '280783', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '37007', 'epa.co2TailpipeGpm': '492.0', 'epa.model' : 'Silverado C15 2WD', 'epa.trim' : 'Auto 8-spd, 8 cyl, 5.3 L, SIDI',
     #'epa.id' : '37006', 'epa.co2TailpipeGpm': '480.0', 'epa.model' : 'Silverado C15 2WD', 'epa.trim' : 'Auto 6-spd, 8 cyl, 5.3 L, SIDI',
     #'epa.id' : '37008', 'epa.co2TailpipeGpm': '527.0', 'epa.model' : 'Silverado C15 2WD', 'epa.trim' : 'Auto 8-spd, 8 cyl, 6.2 L, SIDI',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1G11D5RR7DF107260
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Chevrolet&model=Malibu%20eAssist
    # http://www.fueleconomy.gov/ws/rest/vehicle/32208
    {'VIN': '1G11D5RR7DF107260', 'WMI': '1G1', 'VDS': '1D5RR7', 'VIS': 'DF107260',
     'MODEL': 'Malibu', 'MAKE': 'Chevrolet', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '107260', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1LT Eco',
     'epa.id' : '32208', 'epa.co2TailpipeGpm': '310.0', 'epa.model' : 'Malibu eAssist', 'epa.trim' : 'Auto (S6), 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GCEK19B45E223906
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2005&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2005&make=Chevrolet&model=Silverado%201500%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/21155
    {'VIN': '1GCEK19B45E223906', 'WMI': '1GC', 'VDS': 'EK19B4', 'VIS': '5E223906',
     'MODEL': 'Silverado', 'MAKE': 'Chevrolet', 'YEAR': 2005, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '223906', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1500',
     'epa.id' : '21155', 'epa.co2TailpipeGpm': '592.5', 'epa.model' : 'Silverado 1500 4WD', 'epa.trim' : 'Auto 4-spd, 8 cyl, 5.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GNKRHKD2GJ223195
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Chevrolet&model=Traverse%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36351
    {'VIN': '1GNKRHKD2GJ223195', 'WMI': '1GN', 'VDS': 'KRHKD2', 'VIS': 'GJ223195',
     'MODEL': 'Traverse', 'MAKE': 'Chevrolet', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '223195', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '2LT',
     'epa.id' : '36351', 'epa.co2TailpipeGpm': '507.0', 'epa.model' : 'Traverse FWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GNSCHE00CR257349
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2012&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2012&make=Chevrolet&model=Suburban%201500%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/31472
    {'VIN': '1GNSCHE00CR257349', 'WMI': '1GN', 'VDS': 'SCHE00', 'VIS': 'CR257349',
     'MODEL': 'Suburban', 'MAKE': 'Chevrolet', 'YEAR': 2012, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '257349', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1/2 ton LS',
     'epa.id' : '31472', 'epa.co2TailpipeGpm': '522.8', 'epa.model' : 'Suburban 1500 2WD', 'epa.trim' : 'Auto 6-spd, 8 cyl, 5.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GNWCMEG8BR257377
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2011&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2011&make=Chevrolet&model=Suburban%202500%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/30523
    {'VIN': '1GNWCMEG8BR257377', 'WMI': '1GN', 'VDS': 'WCMEG8', 'VIS': 'BR257377',
     'MODEL': 'Suburban', 'MAKE': 'Chevrolet', 'YEAR': 2011, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '257377', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '3/4 ton', 'nhtsa.series': 'LT',
     'epa.id' : '30523', 'epa.co2TailpipeGpm': '740.6', 'epa.model' : 'Suburban 2500 2WD', 'epa.trim' : 'Auto 6-spd, 8 cyl, 6.0 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/35571
    {'VIN': '1GTN1TEC9FZ904179', 'WMI': '1GT', 'VDS': 'N1TEC9', 'VIS': 'FZ904179',
     'MODEL': 'Sierra', 'MAKE': 'GMC', 'YEAR': 2015, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '904179', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35571', 'epa.co2TailpipeGpm': '478.0', 'epa.model' : 'Sierra C15 2WD', 'epa.trim' : 'Auto 6-spd, 8 cyl, 5.3 L, SIDI',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1J8HR68T89C533504
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2009&make=Jeep
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2009&make=Jeep&model=Grand%20Cherokee%20SRT8%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/26181
    {'VIN': '1J8HR68T89C533504', 'WMI': '1J8', 'VDS': 'HR68T8', 'VIS': '9C533504',
     'MODEL': 'Grand Cherokee', 'MAKE': 'Jeep', 'YEAR': 2009, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '533504', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Overland', 'nhtsa.series': 'WK',
     'epa.id' : '26181', 'epa.co2TailpipeGpm': '740.6', 'epa.model' : 'Grand Cherokee SRT8 AWD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 6.1 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/37066
    {'VIN': '1N4AZ0CP6GC304290', 'WMI': '1N4', 'VDS': 'AZ0CP6', 'VIS': 'GC304290',
     'MODEL': 'Leaf', 'MAKE': 'Nissan', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '304290', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37066', 'epa.co2TailpipeGpm': '0.0', 'epa.model' : 'Leaf (24 kW-hr battery pack)', 'epa.trim' : 'Auto (A1)',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1N4BL3AP5DN508203
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Nissan
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Nissan&model=Altima
    # http://www.fueleconomy.gov/ws/rest/vehicle/32612
    {'VIN': '1N4BL3AP5DN508203', 'WMI': '1N4', 'VDS': 'BL3AP5', 'VIS': 'DN508203',
     'MODEL': 'Altima', 'MAKE': 'Nissan', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '508203', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '32612', 'epa.co2TailpipeGpm': '354.0', 'epa.model' : 'Altima', 'epa.trim' : 'Auto(AV-S6), 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=19UUA65694A043249&submit=Decode
    # http://acurazine.com/forums/vindecoder.php?vin=19UUA65694A043249
    # http://www.fueleconomy.gov/ws/rest/vehicle/19711
    {'VIN': '19UUA65694A043249', 'WMI': '19U', 'VDS': 'UA6569', 'VIS': '4A043249',
     'MODEL': 'TL', 'MAKE':  'Acura', 'YEAR': 2004, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '043249', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '19711', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : 'TL', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.2 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/19UUA9F53EA002754
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Acura
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Acura&model=TL%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/34342
    {'VIN': '19UUA9F53EA002754', 'WMI': '19U', 'VDS': 'UA9F53', 'VIS': 'EA002754',
     'MODEL': 'TL', 'MAKE': 'Acura', 'YEAR': 2014, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '002754', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SH-AWD TECH',
     'epa.id' : '34342', 'epa.co2TailpipeGpm': '421.0', 'epa.model' : 'TL 4WD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.7 L',
    },

    # http://www.vindecoder.net/?vin=19XFB4F24DE547421&submit=Decode says unknown
    # http://www.civicx.com/threads/2016-civic-vin-translator-decoder-guide.889/
    # http://honda-tech.com/forums/vindecoder.php?vin=19XFB4F24DE547421
    # http://www.fueleconomy.gov/ws/rest/vehicle/33507
    {'VIN': '19XFB4F24DE547421', 'WMI': '19X', 'VDS': 'FB4F24', 'VIS': 'DE547421',
     'MODEL': 'Civic Hybrid', 'MAKE':  'Honda', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '547421', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '33507', 'epa.co2TailpipeGpm': '200.0', 'epa.model' : 'Civic Hybrid', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 1.5 L',
    },

    # http://www.vindecoder.net/?vin=1FAHP3FN8AW139719&submit=Decode
    # multiple matches for vin 1FAHP3FN8AW139719: 29291 / 29292
    # http://www.fueleconomy.gov/ws/rest/vehicle/29291
    # http://www.fueleconomy.gov/ws/rest/vehicle/29292
    {'VIN': '1FAHP3FN8AW139719', 'WMI': '1FA', 'VDS': 'HP3FN8', 'VIS': 'AW139719',
     'MODEL': 'Focus', 'MAKE':  'Ford', 'YEAR': 2010, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '139719', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '29292', 'epa.co2TailpipeGpm': '317.4', 'epa.model' : 'Focus FWD', 'epa.trim' : 'Man 5-spd, 4 cyl, 2.0 L',
     #'epa.id' : '29291', 'epa.co2TailpipeGpm': '317.4', 'epa.model' : 'Focus FWD', 'epa.trim' : 'Auto 4-spd, 4 cyl, 2.0 L',
    },

    # http://www.vindecoder.net/?vin=1GKEV13728J123735&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/24114
    {'VIN': '1GKEV13728J123735', 'WMI': '1GK', 'VDS': 'EV1372', 'VIS': '8J123735',
     'MODEL': 'Acadia', 'MAKE':  'GMC', 'YEAR': 2008, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '123735', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '24114', 'epa.co2TailpipeGpm': '493.7', 'epa.model' : 'Acadia AWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1GKS1GEJXDR155600
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=GMC
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=GMC&model=Yukon%20Denali%201500%20Hybrid%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/32652
    {'VIN': '1GKS1GEJXDR155600', 'WMI': '1GK', 'VDS': 'S1GEJX', 'VIS': 'DR155600',
     'MODEL': 'Yukon', 'MAKE': 'GMC', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '155600', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1/2 Ton Denali Hybrid',
     'epa.id' : '32652', 'epa.co2TailpipeGpm': '416.0', 'epa.model' : 'Yukon Denali 1500 Hybrid 4WD', 'epa.trim' : 'Auto (variable gear ratios), 8 cyl, 6.0 L',
    },

    # http://www.vindecoder.net/?vin=1GT020CG4EF828544&submit=Decode doesn't have model
    {'VIN': '1GT020CG4EF828544', 'WMI': '1GT', 'VDS': '020CG4', 'VIS': 'EF828544',
     'MODEL': 'Sierra 2500', 'MAKE':  'GMC', 'YEAR': 2014, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '828544', 'FEWER_THAN_500_PER_YEAR': False,
     # https://vpic.nhtsa.dot.gov/decoder/ says this is 6 liters, but epa doesn't have the 6 liter engine
    },

    # http://www.vindecoder.net/?vin=1GYFC56299R410242&submit=Decode didn't have model
    # http://www.vindecoderz.com/EN/check-lookup/1GYFC56299R410242 says Escalade ESV
    # http://www.ford-trucks.com/forums/vindecoder.php?vin=3GYVKMEF5AG416315 says Escalade EXT (and so does NHTSA)
    # https://www.fueleconomy.gov/feg/bymodel/2010_Cadillac_Escalade.shtml doesn't list EXT
    # So it's probably an ESV, but...
    {'VIN': '1GYFC56299R410242', 'WMI': '1GY', 'VDS': 'FC5629', 'VIS': '9R410242',
     'MODEL': 'Escalade ESV', 'MAKE':  'Cadillac', 'YEAR': 2009, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '410242', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # The EPA doesn't even have this vehicle for 2016 (as of July 2016); have to use yearoffset = -1 to get any epa data:
    # Can't tell whether this is flex-fuel from the vin
    # http://www.fueleconomy.gov/ws/rest/vehicle/35975
    ## http://www.fueleconomy.gov/ws/rest/vehicle/35974
    {'VIN': '1N6AA1F2XGN509474', 'WMI': '1N6', 'VDS': 'AA1F2X', 'VIS': 'GN509474',
     'MODEL': 'Titan', 'MAKE': 'Nissan', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '509474', 'FEWER_THAN_500_PER_YEAR': False,
     'yearoffset':'-1',
     'epa.id' : '35975', 'epa.co2TailpipeGpm': '588.0', 'epa.model' : 'Titan 2WD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 5.6 L, FFV',
     #'epa.id' : '35974', 'epa.co2TailpipeGpm': '591.0', 'epa.model' : 'Titan 2WD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 5.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1YVHZ8DH0C5M33844
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2012&make=Mazda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2012&make=Mazda&model=6
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/31223
    ## http://www.fueleconomy.gov/ws/rest/vehicle/31224
    {'VIN': '1YVHZ8DH0C5M33844', 'WMI': '1YV', 'VDS': 'HZ8DH0', 'VIS': 'C5M33844',
     'MODEL': 'Mazda6', 'MAKE': 'Mazda', 'YEAR': 2012, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'M33844', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Touring', 'nhtsa.series': '',
     'epa.id' : '31223', 'epa.co2TailpipeGpm': '355.5', 'epa.model' : '6', 'epa.trim' : 'Auto (S5), 4 cyl, 2.5 L',
     #'epa.id' : '31224', 'epa.co2TailpipeGpm': '370.3', 'epa.model' : '6', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/1ZVBP8CF4E5242560
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Ford
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Ford&model=Mustang
    # http://www.fueleconomy.gov/ws/rest/vehicle/33431
    {'VIN': '1ZVBP8CF4E5242560', 'WMI': '1ZV', 'VDS': 'BP8CF4', 'VIS': 'E5242560',
     'MODEL': 'Mustang', 'MAKE': 'Ford', 'YEAR': 2014, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '242560', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'GT Coupe', 'nhtsa.series': '',
     'epa.id' : '33431', 'epa.co2TailpipeGpm': '473.0', 'epa.model' : 'Mustang', 'epa.trim' : 'Man 6-spd, 8 cyl, 5.0 L',
    },

    # http://www.vindecoder.net/?vin=19VDE2E5XEE644230&submit=Decode unchecked
    # http://acurazine.com/forums/vindecoder.php?vin=19VDE2E5XEE644230
    # https://vpic.nhtsa.dot.gov/decoder/ says it has errors
    #{'VIN': '19VDE2E5XEE644230', 'WMI': '19V', 'VDS': 'DE2E5X', 'VIS': 'EE644230',
    # 'MODEL': 'ILX', 'MAKE':  'Acura', 'YEAR': 2014, 'COUNTRY': 'United States',
    # 'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '644230', 'FEWER_THAN_500_PER_YEAR': False,
    # 'epa.co2TailpipeGpm': '387',
    #},

    # http://www.vindecoder.net/?vin=2A4GM684X6R632476&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/22368
    {'VIN': '2A4GM684X6R632476', 'WMI': '2A4', 'VDS': 'GM684X', 'VIS': '6R632476',
     'MODEL': 'Pacifica', 'MAKE':  'Chrysler', 'YEAR': 2006, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '632476', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '22368', 'epa.co2TailpipeGpm': '522.8', 'epa.model' : 'Pacifica 2WD', 'epa.trim' : 'Auto 4-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=2B3KA43G27H825762&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/23609
    {'VIN': '2B3KA43G27H825762', 'WMI': '2B3', 'VDS': 'KA43G2', 'VIS': '7H825762',
     'MODEL': 'Charger', 'MAKE':  'Dodge', 'YEAR': 2007, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '825762', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '23609', 'epa.co2TailpipeGpm': '444.4', 'epa.model' : 'Charger', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=2C3CDYAGXDH825982&submit=Decode doesn't have good info
    # http://dodgeforum.com/forum/vindecoder.php?vin=2C3CDYAGXDH825982
    # http://www.fueleconomy.gov/ws/rest/vehicle/32977
    {'VIN': '2C3CDYAGXDH825982', 'WMI': '2C3', 'VDS': 'CDYAGX', 'VIS': 'DH825982',
     'MODEL': 'Challenger', 'MAKE':  'Dodge', 'YEAR': 2013, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '825982', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32977', 'epa.co2TailpipeGpm': '426.0', 'epa.model' : 'Challenger', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.6 L',
     },

    # http://www.fueleconomy.gov/ws/rest/vehicle/35462
    {'VIN': '2C4RDGBG1FR710120', 'WMI': '2C4', 'VDS': 'RDGBG1', 'VIS': 'FR710120',
     'MODEL': 'Caravan/Grand Caravan', 'MAKE': 'Dodge', 'YEAR': 2015, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '710120', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35462', 'epa.co2TailpipeGpm': '445.0', 'epa.model' : 'Grand Caravan', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/2C4RC1BG8GR193643
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Chrysler
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Chrysler&model=Town%20and%20Country
    # http://www.fueleconomy.gov/ws/rest/vehicle/36488
    {'VIN': '2C4RC1BG8GR193643', 'WMI': '2C4', 'VDS': 'RC1BG8', 'VIS': 'GR193643',
     'MODEL': 'Town & Country', 'MAKE': 'Chrysler', 'YEAR': 2016, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '193643', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Touring', 'nhtsa.series': 'RT',
     'epa.id' : '36488', 'epa.co2TailpipeGpm': '445.0', 'epa.model' : 'Town and Country', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # http://www.vindecoder.net/?vin=2D4RN6DX5AR939562&submit=Decode
    # https://vpic.nhtsa.dot.gov/decoder/ gives this as Caravan/Grand Caravan, 4 L, 6 cyl,
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2010&make=Dodge was tough for my fuzzy match, at first it liked Nitro 2WD better
    {'VIN': '2D4RN6DX5AR939562', 'WMI': '2D4', 'VDS': 'RN6DX5', 'VIS': 'AR939562',
     'MODEL': 'Grand Caravan', 'MAKE':  'Dodge', 'YEAR': 2010, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '939562', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # http://www.vindecoder.net/?vin=2FTCF15F2ECA55516&submit=Decode
    # NHTSA says 'ErrorCode': u'8 - No detailed data available currently',
    {'VIN': '2FTCF15F2ECA55516', 'WMI': '2FT', 'VDS': 'CF15F2', 'VIS': 'ECA55516',
     'MODEL': 'F-150', 'MAKE':  'Ford', 'YEAR': 1984, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'A55516', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/2GCEC13C981202392
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Chevrolet&model=Silverado%20C15%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/24510
    {'VIN': '2GCEC13C981202392', 'WMI': '2GC', 'VDS': 'EC13C9', 'VIS': '81202392',
     'MODEL': 'Silverado', 'MAKE': 'Chevrolet', 'YEAR': 2008, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '202392', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1/2 ton Work Truck / LS',
     'epa.id' : '24510', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'Silverado C15 2WD', 'epa.trim' : 'Auto 4-spd, 8 cyl, 4.8 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/2GNFLPE55C6105926
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2012&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2012&make=Chevrolet&model=Equinox%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/31467
    {'VIN': '2GNFLPE55C6105926', 'WMI': '2GN', 'VDS': 'FLPE55', 'VIS': 'C6105926',
     'MODEL': 'Equinox', 'MAKE': 'Chevrolet', 'YEAR': 2012, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '105926', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '2LT (FWD)',
     'epa.id' : '31467', 'epa.co2TailpipeGpm': '444.4', 'epa.model' : 'Equinox FWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.0 L, SIDI',
    },

    # http://www.gmforum.com/vindecoder.php?vin=2G61W5S83E9422251
    # ftp://safercar.gov/MfrMail/ORG7595.pdf "General Motors LLC 2013 Vehicle Identification Numbering Standard"
    # http://www.fueleconomy.gov/ws/rest/vehicle/33852
    {'VIN': '2G61W5S83E9422251', 'WMI': '2G6', 'VDS': '1W5S83', 'VIS': 'E9422251',
     'MODEL': 'XTS', 'MAKE':  'Cadillac', 'YEAR': 2014, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '422251', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '33852', 'epa.co2TailpipeGpm': '475.0', 'epa.model' : 'XTS AWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.6 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/2HJYK16566H509774
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2006&make=Honda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2006&make=Honda&model=Ridgeline%20Truck%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/22281
    {'VIN': '2HJYK16566H509774', 'WMI': '2HJ', 'VDS': 'YK1656', 'VIS': '6H509774',
     'MODEL': 'Ridgeline', 'MAKE': 'Honda', 'YEAR': 2006, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '509774', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'RTL',
     'epa.id' : '22281', 'epa.co2TailpipeGpm': '522.8', 'epa.model' : 'Ridgeline Truck 4WD', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=2HNYD18975H033218&submit=Decode
    # http://acurazine.com/forums/vindecoder.php?vin=2HNYD18975H033218
    # http://www.fueleconomy.gov/ws/rest/vehicle/21351
    {'VIN': '2HNYD18975H033218', 'WMI': '2HN', 'VDS': 'YD1897', 'VIS': '5H033218',
     'MODEL': 'MDX', 'MAKE':  'Acura', 'YEAR': 2005, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '033218', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '21351', 'epa.co2TailpipeGpm': '522.8', 'epa.model' : 'MDX 4WD', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=2LMHJ5AT9CB565906&submit=Decode
    # Note: some disagreement about model.
    # https://vindecoder.eu/check-vin/2LMHJ5AT9CB565906 says FWD
    # http://www.vindecoderz.com/EN/check-lookup/2LMHJ5AT9CB565906 says AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/31533
    {'VIN': '2LMHJ5AT9CB565906', 'WMI': '2LM', 'VDS': 'HJ5AT9', 'VIS': 'CB565906',
     'MODEL': 'MKT', 'MAKE':  'Lincoln', 'YEAR': 2012, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '565906', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31533', 'epa.co2TailpipeGpm': '493.7', 'epa.model' : 'MKT AWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L, Turbo',
    },

    # http://www.toyodiy.com/parts/q?vin=2t1kr32e26c557497 says ATM 4-SPEED FLOOR SHIFT (how's it know?)
    # http://www.fueleconomy.gov/ws/rest/vehicle/22123
    {'VIN': '2T1KR32E16C583752', 'WMI': '2T1', 'VDS': 'KR32E1', 'VIS': '6C583752',
     'MODEL': 'Matrix', 'MAKE': 'Toyota', 'YEAR': 2006, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '583752', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '22123', 'epa.co2TailpipeGpm': '329.1', 'epa.model' : 'Matrix', 'epa.trim' : 'Auto 4-spd, 4 cyl, 1.8 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/2T2BGMCA0GC004299
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Lexus
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Lexus&model=RX%20450h%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/37111
    {'VIN': '2T2BGMCA0GC004299', 'WMI': '2T2', 'VDS': 'BGMCA0', 'VIS': 'GC004299',
     'MODEL': 'RX', 'MAKE': 'Lexus', 'YEAR': 2016, 'COUNTRY': 'Canada',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '004299', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'G grade', 'nhtsa.series': 'GYL25L/GGL25L/GGL20L/GYL20L',
     'epa.id' : '37111', 'epa.co2TailpipeGpm': '299.0', 'epa.model' : 'RX 450h AWD', 'epa.trim' : 'Auto(AV-S6), 6 cyl, 3.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3A8FY68818T213031
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Chrysler
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Chrysler&model=PT%20Cruiser
    # http://www.fueleconomy.gov/ws/rest/vehicle/24590
    {'VIN': '3A8FY68818T213031', 'WMI': '3A8', 'VDS': 'FY6881', 'VIS': '8T213031',
     'MODEL': 'PT Cruiser', 'MAKE': 'Chrysler', 'YEAR': 2008, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '213031', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Limited', 'nhtsa.series': 'PT',
     'epa.id' : '24590', 'epa.co2TailpipeGpm': '404.0', 'epa.model' : 'PT Cruiser', 'epa.trim' : 'Man 5-spd, 4 cyl, 2.4 L, Turbo',
    },

    # http://www.vin-decoder.org/details?vin=3C3CFFCR9FT528063
    # http://www.fiat500usa.com/2013/08/decoding-fiat-500-vin.html
    # Chrysler Passenger Car Vehicle Identification Number Code Guide
    # ftp://ftp.nhtsa.dot.gov/MfrMail/ORG9653.pdf
    # Note: Can't tell what transmission it has?!
    # http://www.fueleconomy.gov/ws/rest/vehicle/35154  'Auto 6-spd, 4 cyl, 1.4 L'
    # http://www.fueleconomy.gov/ws/rest/vehicle/35156  'Man 5-spd, 4 cyl, 1.4 L'
    {'VIN': '3C3CFFCR9FT528063', 'WMI': '3C3', 'VDS': 'CFFCR9', 'VIS': 'FT528063',
     'MODEL': '500', 'MAKE':  'Fiat', 'YEAR': 2015, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '528063', 'FEWER_THAN_500_PER_YEAR': False,
     #'epa.id' : '35154', 'epa.co2TailpipeGpm': '295.0', 'epa.model' : '500', 'epa.trim' : 'Auto 6-spd, 4 cyl, 1.4 L',
     'epa.id' : '35156', 'epa.co2TailpipeGpm': '265.0', 'epa.model' : '500', 'epa.trim' : 'Man 5-spd, 4 cyl, 1.4 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/34122
    {'VIN': '3C4PDCBG3ET296933', 'WMI': '3C4', 'VDS': 'PDCBG3', 'VIS': 'ET296933',
     'MODEL': 'Journey', 'MAKE': 'Dodge', 'YEAR': 2014, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '296933', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '34122', 'epa.co2TailpipeGpm': '457.0', 'epa.model' : 'Journey FWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # http://www.vindecoder.net/?vin=3C6JD7CT4CG104778&submit=Decode
    # ftp://safercar.gov/MfrMail/ORG7565.pdf
    # http://www.fueleconomy.gov/ws/rest/vehicle/31451
    {'VIN': '3C6JD7CT4CG104778', 'WMI': '3C6', 'VDS': 'JD7CT4', 'VIS': 'CG104778',
     'MODEL': 'Ram 1500 Pickup', 'MAKE':  'Dodge', 'YEAR': 2012, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '104778', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31451', 'epa.co2TailpipeGpm': '592.5', 'epa.model' : 'Ram 1500 Pickup 4WD', 'epa.trim' : 'Auto 6-spd, 8 cyl, 5.7 L',
    },

    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3CZRU5H35GM739695
    # http://www.fueleconomy.gov/ws/rest/vehicle/35999
    {'VIN': '3CZRU5H35GM739695', 'WMI': '3CZ', 'VDS': 'RU5H35', 'VIS': 'GM739695',
     'MODEL': 'HR-V', 'MAKE': 'Honda', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '739695', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35999', 'epa.co2TailpipeGpm': '290.0', 'epa.model' : 'HR-V 2WD', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 1.8 L',
    },

    # http://www.vindecoder.net/?vin=3D4PH6FV5AT152960&submit=Decode
    # http://www.rambodybuilder.com/2010/docs/intro/vin.pdf
    # http://www.fueleconomy.gov/ws/rest/vehicle/28788
    {'VIN': '3D4PH6FV5AT152960', 'WMI': '3D4', 'VDS': 'PH6FV5', 'VIS': 'AT152960',
     'MODEL': 'Journey', 'MAKE':  'Dodge', 'YEAR': 2010, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '152960', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '28788', 'epa.co2TailpipeGpm': '493.7', 'epa.model' : 'Journey  AWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=3D4PH7FG1BT808130&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/31059
    {'VIN': '3D4PH7FG1BT808130', 'WMI': '3D4', 'VDS': 'PH7FG1', 'VIS': 'BT808130',
     'MODEL': 'Journey', 'MAKE':  'Dodge', 'YEAR': 2011, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '808130', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31059', 'epa.co2TailpipeGpm': '467.7', 'epa.model' : 'Journey AWD', 'epa.trim' : 'Auto 6-spd, 6 cyl, 3.6 L',
    },

    # http://www.vindecoder.net/?vin=3D73Y3CL0BG113805&submit=Decode
    # Edmunds has this as Dodge up to 2010, RAM thereafter,
    # but EPA confused; https://www.fueleconomy.gov/feg/EPAGreenGuide/txt/all_alpha_11.txt has it as Dodge still
    # ftp://safercar.gov/MfrMail/ORG7565.pdf bit confused too
    # ftp://safercar.gov/MfrMail/ORG5870.pdf is for 2011, but calls it Dodge still
    # Heck, http://www.rambodybuilder.com/2012/docs/intro/vin.pdf is 2012, and still calls it Dodge
    # Screw it, let's go with Dodge, as I have no way of getting this right
    # And NHTSA gives an engine size that EPA doesn't have...?
    {'VIN': '3D73Y3CL0BG113805', 'WMI': '3D7', 'VDS': '3Y3CL0', 'VIS': 'BG113805',
     'MODEL': 'Ram 3500', 'MAKE':  'Dodge', 'YEAR': 2011, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '113805', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/34088
    {'VIN': '3FA6P0G76ER244757', 'WMI': '3FA', 'VDS': '6P0G76', 'VIS': 'ER244757',
     'MODEL': 'Fusion', 'MAKE': 'Ford', 'YEAR': 2014, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '244757', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '34088', 'epa.co2TailpipeGpm': '342.0', 'epa.model' : 'Fusion FWD', 'epa.trim' : 'Auto (S6), 4 cyl, 2.5 L',
    },


    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3FA6P0PU0HR122230
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Ford
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Ford&model=Fusion%20Energi%20Plug-in%20Hybrid
    # http://www.fueleconomy.gov/ws/rest/vehicle/37470
    {'VIN': '3FA6P0PU0HR122230', 'WMI': '3FA', 'VDS': '6P0PU0', 'VIS': 'HR122230',
     'MODEL': 'Fusion', 'MAKE': 'Ford', 'YEAR': 2017, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '122230', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SE PHEV',
     'epa.id' : '37470', 'epa.co2TailpipeGpm': '112.0', 'epa.model' : 'Fusion Energi Plug-in Hybrid', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 2.0 L',
    },

    # A Fusion Titanium.  It's AWD, but NHTSA mistakenly identifies it as FWD,
    # and EPA uses FWD or AWD in the model name, so we can't even look up EPA data correctly.
    {'VIN': '3FA6P0K95GR305754', 'WMI': '3FA', 'VDS': '6P0K95', 'VIS': 'GR305754',
     'MODEL': 'Fusion', 'MAKE': 'Ford', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '305754', 'FEWER_THAN_500_PER_YEAR': False,
     # FIXME: if NHTSA ever fixes their database, add epa data here.
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3GCEC13078G157479
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Chevrolet&model=Silverado%20C15%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/24511
    {'VIN': '3GCEC13078G157479', 'WMI': '3GC', 'VDS': 'EC1307', 'VIS': '8G157479',
     'MODEL': 'Silverado', 'MAKE': 'Chevrolet', 'YEAR': 2008, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '157479', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1/2 ton Work Truck / LS',
     'epa.id' : '24511', 'epa.co2TailpipeGpm': '522.8', 'epa.model' : 'Silverado C15 2WD', 'epa.trim' : 'Auto 4-spd, 8 cyl, 5.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3GNAL2EK5ES582413
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Chevrolet&model=Captiva%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/34120
    {'VIN': '3GNAL2EK5ES582413', 'WMI': '3GN', 'VDS': 'AL2EK5', 'VIS': 'ES582413',
     'MODEL': 'Captiva Sport', 'MAKE': 'Chevrolet', 'YEAR': 2014, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '582413', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '2LS',
     'epa.id' : '34120', 'epa.co2TailpipeGpm': '347.0', 'epa.model' : 'Captiva FWD', 'epa.trim' : 'Auto 6-spd, 4 cyl, 2.4 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/23047
    {'VIN': '3GNFK16387G115163', 'WMI': '3GN', 'VDS': 'FK1638', 'VIS': '7G115163',
     'MODEL': 'Suburban', 'MAKE':  'Chevrolet', 'YEAR': 2007, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '115163', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '23047', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'Suburban 1500 4WD', 'epa.trim' : 'Auto 4-spd, 8 cyl, 5.3 L',
    },

    # http://www.vindecoder.net/?vin=3GYVKMEF5AG416315&submit=Decode
    # https://www.fueleconomy.gov/feg/bymodel/2010_Cadillac_Escalade.shtml doesn't list EXT
    # So it's probably an ESV, but...
    {'VIN': '3GYVKMEF5AG416315', 'WMI': '3GY', 'VDS': 'VKMEF5', 'VIS': 'AG416315',
     'MODEL': 'Escalade', 'MAKE':  'Cadillac', 'YEAR': 2010, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '416315', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3G1BE6SM1HS511968
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Chevrolet&model=Cruze%20Hatchback
    # http://www.fueleconomy.gov/ws/rest/vehicle/37909
    {'VIN': '3G1BE6SM1HS511968', 'WMI': '3G1', 'VDS': 'BE6SM1', 'VIS': 'HS511968',
     'MODEL': 'Cruze', 'MAKE': 'Chevrolet', 'YEAR': 2017, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '511968', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'LT',
     'epa.id' : '37909', 'epa.co2TailpipeGpm': '278.0', 'epa.model' : 'Cruze Hatchback', 'epa.trim' : 'Auto (S6), 4 cyl, 1.4 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3KPFL4A8XHE050680
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Kia
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Kia&model=Forte
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/37555
    ## http://www.fueleconomy.gov/ws/rest/vehicle/37556
    {'VIN': '3KPFL4A8XHE050680', 'WMI': '3KP', 'VDS': 'FL4A8X', 'VIS': 'HE050680',
     'MODEL': 'Forte', 'MAKE': 'Kia', 'YEAR': 2017, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '050680', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SX, EX',
     'epa.id' : '37555', 'epa.co2TailpipeGpm': '301.0', 'epa.model' : 'Forte', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L',
     #'epa.id' : '37556', 'epa.co2TailpipeGpm': '314.0', 'epa.model' : 'Forte', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L',
    },

    # http://www.vindecoder.net/?vin=3LNHL2GC1BR262548&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/30367
    {'VIN': '3LNHL2GC1BR262548', 'WMI': '3LN', 'VDS': 'HL2GC1', 'VIS': 'BR262548',
     'MODEL': 'MKZ', 'MAKE':  'Lincoln', 'YEAR': 2011, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '262548', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '30367', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : 'MKZ FWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3MYDLBYV0HY148317
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Toyota
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Toyota&model=Yaris
    # http://www.fueleconomy.gov/ws/rest/vehicle/37971
    # FIXME: can't tell Yaris from Yaris iA, can't tell auto from manual.
    # Choosing one at random (sort of).
    {'VIN': '3MYDLBYV0HY148317', 'WMI': '3MY', 'VDS': 'DLBYV0', 'VIS': 'HY148317',
     'MODEL': 'Yaris', 'MAKE': 'Toyota', 'YEAR': 2017, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '148317', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '37971', 'epa.co2TailpipeGpm': '271.0', 'epa.model' : 'Yaris', 'epa.trim' : 'Man 5-spd, 4 cyl, 1.5 L',
    },

    # Can't tell transmission from vin, so pick one at random :-(
    # https://vpic.nhtsa.dot.gov/mid/home/displayfile/6089
    # http://www.fueleconomy.gov/ws/rest/vehicle/36534
    ## http://www.fueleconomy.gov/ws/rest/vehicle/36535
    {'VIN': '3MZBM1K72GM303265', 'WMI': '3MZ', 'VDS': 'BM1K72', 'VIS': 'GM303265',
     'MODEL': 'Mazda3', 'MAKE': 'Mazda', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '303265', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '36534', 'epa.co2TailpipeGpm': '275.0', 'epa.model' : '3 5-Door', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L, SIDI',
     #'epa.id' : '36535', 'epa.co2TailpipeGpm': '270.0', 'epa.model' : '3 5-Door', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L, SIDI',
    },

    # http://www.downtownnissan.com/inventory/New-2016-Nissan-Versa_Note-SR-3N1CE2CP0GL391251/ says this is a CVT
    # but https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3N1CE2CP0GL391251/ doesn't indicate transmission type
    # We normally just guess shortest epa trim in that case, but that gives the wrong answer here,
    # so leave off epa info.
    # FIXME: add notion of XFAIL to tests
    {'VIN': '3N1CE2CP0GL391251', 'WMI': '3N1', 'VDS': 'CE2CP0', 'VIS': 'GL391251',
     'MODEL': 'Versa Note', 'MAKE': 'Nissan', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '391251', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/37237
    {'VIN': '3N6CM0KN0GK696126', 'WMI': '3N6', 'VDS': 'CM0KN0', 'VIS': 'GK696126',
     'MODEL': 'NV200, City Express', 'MAKE': 'Nissan', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '696126', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '37237', 'epa.co2TailpipeGpm': '353.0', 'epa.model' : 'NV200 NYC Taxi', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/3TMCZ5AN2GM040551
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Toyota
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Toyota&model=Tacoma%204WD
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/36925
    ## http://www.fueleconomy.gov/ws/rest/vehicle/36924
    {'VIN': '3TMCZ5AN2GM040551', 'WMI': '3TM', 'VDS': 'CZ5AN2', 'VIS': 'GM040551',
     'MODEL': 'Tacoma', 'MAKE': 'Toyota', 'YEAR': 2016, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '040551', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SR5 Grade', 'nhtsa.series': 'GRN305L',
     'epa.id' : '36925', 'epa.co2TailpipeGpm': '470.0', 'epa.model' : 'Tacoma 4WD', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.5 L',
     #'epa.id' : '36924', 'epa.co2TailpipeGpm': '444.0', 'epa.model' : 'Tacoma 4WD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/31173
    {'VIN': '3VWVA7AT5CM635721', 'WMI': '3VW', 'VDS': 'VA7AT5', 'VIS': 'CM635721',
     'MODEL': 'New Beetle', 'MAKE': 'Volkswagen', 'YEAR': 2012, 'COUNTRY': 'Mexico',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '635721', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31173', 'epa.co2TailpipeGpm': '355.5', 'epa.model' : 'Beetle', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=4A31K3DT4CE403200&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/31170
    {'VIN': '4A31K3DT4CE403200', 'WMI': '4A3', 'VDS': '1K3DT4', 'VIS': 'CE403200',
     'MODEL': 'Eclipse', 'MAKE':  'Mitsubishi', 'YEAR': 2012, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '403200', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31170', 'epa.co2TailpipeGpm': '444.4', 'epa.model' : 'Eclipse', 'epa.trim' : 'Auto (S5), 6 cyl, 3.8 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/4JGDA6DB9GA764832
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Mercedes-Benz&model=GLE550e%204matic
    # http://www.fueleconomy.gov/ws/rest/vehicle/37526
    {'VIN': '4JGDA6DB9GA764832', 'WMI': '4JG', 'VDS': 'DA6DB9', 'VIS': 'GA764832',
     'MODEL': 'GLE', 'MAKE': 'Mercedes-Benz', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '764832', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'GLE550e-4M',
     'epa.id' : '37526', 'epa.co2TailpipeGpm': '294.0', 'epa.model' : 'GLE550e 4matic', 'epa.trim' : 'Auto 7-spd, 6 cyl, 3.0 L, Turbo',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/36406
    {'VIN': '4S3BNAH62G3049699', 'WMI': '4S3', 'VDS': 'BNAH62', 'VIS': 'G3049699',
     'MODEL': 'Legacy', 'MAKE': 'Subaru', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '049699', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '36406', 'epa.co2TailpipeGpm': '302.0', 'epa.model' : 'Legacy AWD', 'epa.trim' : 'Auto(AV-S6), 4 cyl, 2.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/55SWF4JB6GU104745
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Mercedes-Benz&model=C300
    # http://www.fueleconomy.gov/ws/rest/vehicle/36739
    {'VIN': '55SWF4JB6GU104745', 'WMI': '55S', 'VDS': 'WF4JB6', 'VIS': 'GU104745',
     'MODEL': 'C-Class', 'MAKE': 'Mercedes-Benz', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '104745', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'C300',
     'epa.id' : '36739', 'epa.co2TailpipeGpm': '318.0', 'epa.model' : 'C300', 'epa.trim' : 'Auto 7-spd, 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/58ABK1GG4GU016219
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Lexus
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Lexus&model=ES%20350
    # http://www.fueleconomy.gov/ws/rest/vehicle/36750
    {'VIN': '58ABK1GG4GU016219', 'WMI': '58A', 'VDS': 'BK1GG4', 'VIS': 'GU016219',
     'MODEL': 'ES', 'MAKE': 'Lexus', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '016219', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '350', 'nhtsa.series': 'GSV60L/AVV60L',
     'epa.id' : '36750', 'epa.co2TailpipeGpm': '363.0', 'epa.model' : 'ES 350', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=5FRYD3H26GB020813&submit=Decode unchecked
    # Note: can't tell if it has stop-start
    # http://www.fueleconomy.gov/ws/rest/vehicle/36119 'Auto (S9), 6 cyl, 3.5 L, SIDI; Stop-Start'
    # http://www.fueleconomy.gov/ws/rest/vehicle/36120 'Auto (S9), 6 cyl, 3.5 L, SIDI'
    # Only 10 grams/mile diff, tho
    {'VIN': '5FRYD3H26GB020813', 'WMI': '5FR', 'VDS': 'YD3H26', 'VIS': 'GB020813',
     'MODEL': 'MDX', 'MAKE':  'Acura', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '020813', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '36120', 'epa.co2TailpipeGpm': '406.0', 'epa.model' : 'MDX 2WD', 'epa.trim' : 'Auto (S9), 6 cyl, 3.5 L, SIDI',
    },

    # http://www.vindecoder.net/?vin=5GADS13S072592644&submit=Decode
    # https://service.gm.com/dealerworld/vincards/
    # https://service.gm.com/dealerworld/vincards/pdf/vincard07.pdf
    # ftp://www-nrd.nhtsa.dot.gov/MfrMail/ORG5807.pdf
    # http://www.fueleconomy.gov/ws/rest/vehicle/22947
    {'VIN': '5GADS13S072592644', 'WMI': '5GA', 'VDS': 'DS13S0', 'VIS': '72592644',
     'MODEL': 'Ranier', 'MAKE':  'Buick', 'YEAR': 2007, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '592644', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '22947', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'Rainier 2WD', 'epa.trim' : 'Auto 4-spd, 6 cyl, 4.2 L',
    },

    # http://www.vindecoder.net/?vin=5GNRNGEE9A8215904&submit=Decode
    # http://www.gmforum.com/vindecoder.php?vin=5GNRNGEE9A8215904 claims the H3T had a 5 cylinder engine
    # http://www.tflcar.com/2013/03/modern-collectibles-revealed-2010-hummer-h3t/ agrees!
    # NOTE: Can't tell which engine or transmission from what NHTSA gives us
    # so we should either pick one or average.
    # I'm going with 'skip' for now.
    {'VIN': '5GNRNGEE9A8215904', 'WMI': '5GN', 'VDS': 'RNGEE9', 'VIS': 'A8215904',
     'MODEL': 'H3T', 'MAKE':  'Hummer', 'YEAR': 2010, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '215904', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # http://www.vindecoder.net/?vin=5J6TF1H33CL339137&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/31913
    {'VIN': '5J6TF1H33CL339137', 'WMI': '5J6', 'VDS': 'TF1H33', 'VIS': 'CL339137',
     'MODEL': 'Crosstour', 'MAKE':  'Honda', 'YEAR': 2012, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '339137', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31913', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : 'Crosstour 2WD', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=5J8TB1H27CA348655&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/31946
    {'VIN': '5J8TB1H27CA348655', 'WMI': '5J8', 'VDS': 'TB1H27', 'VIS': 'CA348655',
     'MODEL': 'RDX', 'MAKE':  'Acura', 'YEAR': 2012, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '348655', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31946', 'epa.co2TailpipeGpm': '467.7', 'epa.model' : 'RDX 4WD', 'epa.trim' : 'Auto (S5), 4 cyl, 2.3 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5KBCP36869B501904
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2009&make=Honda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2009&make=Honda&model=Accord
    # http://www.fueleconomy.gov/ws/rest/vehicle/26007
    {'VIN': '5KBCP36869B501904', 'WMI': '5KB', 'VDS': 'CP3686', 'VIS': '9B501904',
     'MODEL': 'Accord', 'MAKE': 'Honda', 'YEAR': 2009, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '501904', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'EX-L-V6', 'nhtsa.series': '',
     'epa.id' : '26007', 'epa.co2TailpipeGpm': '404.0', 'epa.model' : 'Accord', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5NMZT3LB2HH016192
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Hyundai
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Hyundai&model=Santa%20Fe%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/37228
    {'VIN': '5NMZT3LB2HH016192', 'WMI': '5NM', 'VDS': 'ZT3LB2', 'VIS': 'HH016192',
     'MODEL': 'Santa Fe', 'MAKE': 'Hyundai', 'YEAR': 2017, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '016192', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Base',
     'epa.id' : '37228', 'epa.co2TailpipeGpm': '427.0', 'epa.model' : 'Santa Fe FWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5N1AL0MM1DC339116
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Infiniti&model=JX35%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/32314
    {'VIN': '5N1AL0MM1DC339116', 'WMI': '5N1', 'VDS': 'AL0MM1', 'VIS': 'DC339116',
     'MODEL': 'JX35', 'MAKE': 'Infiniti', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '339116', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '32314', 'epa.co2TailpipeGpm': '432.0', 'epa.model' : 'JX35 FWD', 'epa.trim' : 'Auto(AV-S6), 6 cyl, 3.5 L',
    },

    # http://www.vindecoder.net/?vin=5N1CR2MN6EC875492&submit=Decode
    # NOTE: Disagreement between NHTSA and EPA about engine size, so skipping
    {'VIN': '5N1CR2MN6EC875492', 'WMI': '5N1', 'VDS': 'CR2MN6', 'VIS': 'EC875492',
     'MODEL': 'Pathfinder', 'MAKE':  'Nissan', 'YEAR': 2014, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '875492', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5N3AA08C68N906008
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Infiniti&model=QX56%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/24115
    {'VIN': '5N3AA08C68N906008', 'WMI': '5N3', 'VDS': 'AA08C6', 'VIS': '8N906008',
     'MODEL': 'QX56', 'MAKE': 'Infiniti', 'YEAR': 2008, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '906008', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '24115', 'epa.co2TailpipeGpm': '634.8', 'epa.model' : 'QX56 4WD', 'epa.trim' : 'Auto 5-spd, 8 cyl, 5.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5NPE24AF8HH000000
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Hyundai
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Hyundai&model=Sonata
    # http://www.fueleconomy.gov/ws/rest/vehicle/37432
    {'VIN': '5NPE24AF8HH000000', 'WMI': '5NP', 'VDS': 'E24AF8', 'VIS': 'HH000000',
     'MODEL': 'Sonata', 'MAKE': 'Hyundai', 'YEAR': 2017, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '000000', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SE, Eco',
     'epa.id' : '37432', 'epa.co2TailpipeGpm': '307.0', 'epa.model' : 'Sonata', 'epa.trim' : 'Auto (S6), 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5NPE24AF6GH269479
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Hyundai
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Hyundai&model=Sonata
    # http://www.fueleconomy.gov/ws/rest/vehicle/36477
    {'VIN': '5NPE24AF6GH269479', 'WMI': '5NP', 'VDS': 'E24AF6', 'VIS': 'GH269479',
     'MODEL': 'Sonata', 'MAKE': 'Hyundai', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '269479', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SE / SE w/Popular Pkg / Eco / Eco w/Tech Pkg',
     'epa.id' : '36477', 'epa.co2TailpipeGpm': '307.0', 'epa.model' : 'Sonata', 'epa.trim' : 'Auto (S6), 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5NPEC4AB5DH717264
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Hyundai
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Hyundai&model=Sonata
    # http://www.fueleconomy.gov/ws/rest/vehicle/32340
    {'VIN': '5NPEC4AB5DH717264', 'WMI': '5NP', 'VDS': 'EC4AB5', 'VIS': 'DH717264',
     'MODEL': 'Sonata', 'MAKE': 'Hyundai', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '717264', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SE / SE NAVI / Limited / Limited NAVI',
     'epa.id' : '32340', 'epa.co2TailpipeGpm': '342.0', 'epa.model' : 'Sonata', 'epa.trim' : 'Auto 6-spd, 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=5UMDU93436L421092&submit=Decode
    # NOTE: confusion about model.  Fuzzy matching may need improvement, too.
    {'VIN': '5UMDU93436L421092', 'WMI': '5UM', 'VDS': 'DU9343', 'VIS': '6L421092',
     'MODEL': 'M', 'MAKE':  'BMW', 'YEAR': 2006, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '421092', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5UXKR0C52H0U50460
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=BMW&model=X5%20xDrive35i
    # http://www.fueleconomy.gov/ws/rest/vehicle/37795
    {'VIN': '5UXKR0C52H0U50460', 'WMI': '5UX', 'VDS': 'KR0C52', 'VIS': 'H0U50460',
     'MODEL': 'X5', 'MAKE': 'BMW', 'YEAR': 2017, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'U50460', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': '35i',
     'epa.id' : '37795', 'epa.co2TailpipeGpm': '434.0', 'epa.model' : 'X5 xDrive35i', 'epa.trim' : 'Auto (S8), 6 cyl, 3.0 L, Turbo',
    },

    # BMW 2010-2015
    # Cover letter: "Update - Vehicle Identification Number (VIN) Decipherments for 2010, 2011, 2012, 2013, 2014 & 2015 Model Year BMW Vehicles"
    # Table: "BMW Model Year 2015 Decipherment of VINs in Accordance with Part 565"
    # https://vpic.nhtsa.dot.gov/mid/home/displayfile/6197

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5UXWZ7C56H0T43955
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=BMW&model=X3%20sDrive%2028i
    # http://www.fueleconomy.gov/ws/rest/vehicle/37343
    {'VIN': '5UXWZ7C56H0T43955', 'WMI': '5UX', 'VDS': 'WZ7C56', 'VIS': 'H0T43955',
     'MODEL': 'X3', 'MAKE': 'BMW', 'YEAR': 2017, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'T43955', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': 'sDrive28i',
     'epa.id' : '37343', 'epa.co2TailpipeGpm': '374.0', 'epa.model' : 'X3 sDrive 28i', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=5UXXW5C54F0791433&submit=Decode
    # http://www.partesymas.com/VIN-Interpretation-Tables-2026.pdf showed 4-7 were the model,body,engine code
    # http://www.autoredbook.com/ distinguished between the two X4 models
    # http://www.fueleconomy.gov/ws/rest/vehicle/35241
    {'VIN': '5UXXW5C54F0791433', 'WMI': '5UX', 'VDS': 'XW5C54', 'VIS': 'F0791433',
     'MODEL': 'X4 xDrive35i', 'MAKE':  'BMW', 'YEAR': 2015, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '791433', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35241', 'epa.co2TailpipeGpm': '415.0', 'epa.model' : 'X4 xDrive35i', 'epa.trim' : 'Auto (S8), 6 cyl, 3.0 L, Turbo',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/34949
    {'VIN': '5XXGM4A7XFG459047', 'WMI': '5XX', 'VDS': 'GM4A7X', 'VIS': 'FG459047',
     'MODEL': 'Optima', 'MAKE': 'Kia', 'YEAR': 2015, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '459047', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '34949', 'epa.co2TailpipeGpm': '334.0', 'epa.model' : 'Optima', 'epa.trim' : 'Auto (S6), 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5XYPK4A57GG169415
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Kia
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Kia&model=Sorento%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/35987
    {'VIN': '5XYPK4A57GG169415', 'WMI': '5XY', 'VDS': 'PK4A57', 'VIS': 'GG169415',
     'MODEL': 'Sorento', 'MAKE': 'Kia', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '169415', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'SX / SX Limited',
     'epa.id' : '35987', 'epa.co2TailpipeGpm': '436.0', 'epa.model' : 'Sorento FWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5XYZT3LB5GG318570
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Hyundai
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Hyundai&model=Santa%20Fe%20Sport%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36208
    {'VIN': '5XYZT3LB5GG318570', 'WMI': '5XY', 'VDS': 'ZT3LB5', 'VIS': 'GG318570',
     'MODEL': 'Santa Fe', 'MAKE': 'Hyundai', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '318570', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Sport', 'nhtsa.series': '',
     'epa.id' : '36208', 'epa.co2TailpipeGpm': '387.0', 'epa.model' : 'Santa Fe Sport FWD', 'epa.trim' : 'Auto (S6), 4 cyl, 2.4 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/35500
    {'VIN': '5YFBURHE9FP280940', 'WMI': '5YF', 'VDS': 'BURHE9', 'VIS': 'FP280940',
     'MODEL': 'Corolla', 'MAKE':  'Toyota', 'YEAR': 2015, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '280940', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35500', 'epa.co2TailpipeGpm': '285.0', 'epa.model' : 'Corolla', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.8 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5Y2SP67069Z433697
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2009&make=Pontiac
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2009&make=Pontiac&model=Vibe
    # http://www.fueleconomy.gov/ws/rest/vehicle/25302
    {'VIN': '5Y2SP67069Z433697', 'WMI': '5Y2', 'VDS': 'SP6706', 'VIS': '9Z433697',
     'MODEL': 'Vibe', 'MAKE': 'Pontiac', 'YEAR': 2009, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': '433697', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '25302', 'epa.co2TailpipeGpm': '370.3', 'epa.model' : 'Vibe', 'epa.trim' : 'Auto (S5), 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5YJSA1AG1DFP08689
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Tesla
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Tesla&model=Model%20S%20(60%20kW-hr%20battery%20pack)
    # http://www.fueleconomy.gov/ws/rest/vehicle/33367
    {'VIN': '5YJSA1AG1DFP08689', 'WMI': '5YJ', 'VDS': 'SA1AG1', 'VIS': 'DFP08689',
     'MODEL': 'Model S', 'MAKE': 'Tesla', 'YEAR': 2013, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'P08689', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '33367', 'epa.co2TailpipeGpm': '0.0', 'epa.model' : 'Model S (60 kW-hr battery pack)', 'epa.trim' : 'Auto (A1)',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/5YMKT6C52G0R79418
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=BMW&model=X5%20M
    # http://www.fueleconomy.gov/ws/rest/vehicle/36774
    {'VIN': '5YMKT6C52G0R79418', 'WMI': '5YM', 'VDS': 'KT6C52', 'VIS': 'G0R79418',
     'MODEL': 'X5', 'MAKE': 'BMW', 'YEAR': 2016, 'COUNTRY': 'United States',
     'REGION': 'north_america', 'SEQUENTIAL_NUMBER': 'R79418', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': 'M',
     'epa.id' : '36774', 'epa.co2TailpipeGpm': '551.0', 'epa.model' : 'X5 M', 'epa.trim' : 'Auto (S8), 8 cyl, 4.4 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=JA4AD2A3XEZ426420&submit=Decode didn't have model
    # https://www.mitsubishicars.com/owners/support/vin-information
    # NHTSA complains  u'ErrorCode': u'4 - VIN corrected, error in one position only (indicated by ! in Suggested VIN), multiple matches found.',
    {'VIN': 'JA4AD2A3XEZ426420', 'WMI': 'JA4', 'VDS': 'AD2A3X', 'VIS': 'EZ426420',
     'MODEL': 'Outlander ES', 'MAKE':  'Mitsubishi', 'YEAR': 2014, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '426420', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JC1NFAEK5H0103072
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Fiat
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Fiat&model=124%20Spider
    # http://www.fueleconomy.gov/ws/rest/vehicle/37528
    {'VIN': 'JC1NFAEK5H0103072', 'WMI': 'JC1', 'VDS': 'NFAEK5', 'VIS': 'H0103072',
     'MODEL': '124 Spider', 'MAKE': 'Fiat', 'YEAR': 2017, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '103072', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '37528', 'epa.co2TailpipeGpm': '298.0', 'epa.model' : '124 Spider', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.4 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JF1GPAY67G8331894
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Subaru
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Subaru&model=Impreza%20Wagon%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36827
    {'VIN': 'JF1GPAY67G8331894', 'WMI': 'JF1', 'VDS': 'GPAY67', 'VIS': 'G8331894',
     'MODEL': 'Impreza', 'MAKE': 'Subaru', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '331894', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Sport-Ltd + NAVI + EyeSight', 'nhtsa.series': '',
     'epa.id' : '36827', 'epa.co2TailpipeGpm': '318.0', 'epa.model' : 'Impreza Wagon AWD', 'epa.trim' : 'Man 5-spd, 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JF1VA2Y63G9804991
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Subaru
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Subaru&model=WRX
    # http://www.fueleconomy.gov/ws/rest/vehicle/36092
    {'VIN': 'JF1VA2Y63G9804991', 'WMI': 'JF1', 'VDS': 'VA2Y63', 'VIS': 'G9804991',
     'MODEL': 'WRX', 'MAKE': 'Subaru', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '804991', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'STI Limited + MR + KA + NAVI(H/K) + BSD', 'nhtsa.series': '',
     'epa.id' : '36092', 'epa.co2TailpipeGpm': '458.0', 'epa.model' : 'WRX', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JF1ZCAB12G9604896
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Subaru
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Subaru&model=BRZ
    # http://www.fueleconomy.gov/ws/rest/vehicle/36150
    {'VIN': 'JF1ZCAB12G9604896', 'WMI': 'JF1', 'VDS': 'ZCAB12', 'VIS': 'G9604896',
     'MODEL': 'BRZ', 'MAKE': 'Subaru', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '604896', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Base', 'nhtsa.series': '',
     'epa.id' : '36150', 'epa.co2TailpipeGpm': '360.0', 'epa.model' : 'BRZ', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JF1ZNAA19G8708660
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Scion
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Scion&model=FR-S
    # http://www.fueleconomy.gov/ws/rest/vehicle/36194
    {'VIN': 'JF1ZNAA19G8708660', 'WMI': 'JF1', 'VDS': 'ZNAA19', 'VIS': 'G8708660',
     'MODEL': 'Scion FR-S', 'MAKE': 'Scion', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '708660', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'STD', 'nhtsa.series': '',
     'epa.id' : '36194', 'epa.co2TailpipeGpm': '317.0', 'epa.model' : 'FR-S', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JF2SJGVC3GH555328
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Subaru
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Subaru&model=Forester%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36148
    {'VIN': 'JF2SJGVC3GH555328', 'WMI': 'JF2', 'VDS': 'SJGVC3', 'VIS': 'GH555328',
     'MODEL': 'Forester', 'MAKE': 'Subaru', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '555328', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Touring + MR + H/K Premium + KA', 'nhtsa.series': '',
     'epa.id' : '36148', 'epa.co2TailpipeGpm': '357.0', 'epa.model' : 'Forester AWD', 'epa.trim' : 'Auto(AV-S8), 4 cyl, 2.0 L, Turbo',
    },


    # http://www.vindecoder.net/?vin=JH4CW2H53BC567925&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/34758
    {'VIN': 'JH4CW2H53BC567925', 'WMI': 'JH4', 'VDS': 'CW2H53', 'VIS': 'BC567925',
     'MODEL': 'TSX', 'MAKE':  'Acura', 'YEAR': 2011, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '567925', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '34758', 'epa.co2TailpipeGpm': '370.3', 'epa.model' : 'TSX Wagon', 'epa.trim' : 'Auto (S5), 4 cyl, 2.4 L',
    },

    # ftp://safercar.gov/MfrMail/ORG7377.pdf "MY12 Nissan VIN Coding System"

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JN1BJ0HP3DM430419
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Infiniti&model=EX37
    # http://www.fueleconomy.gov/ws/rest/vehicle/33276
    # Note: Wikipedia mentioned this was rebadged.  Looks like EPA noticed and NHTSA didn't.
    {'VIN': 'JN1BJ0HP3DM430419', 'WMI': 'JN1', 'VDS': 'BJ0HP3', 'VIS': 'DM430419',
     'MODEL': 'EX35', 'MAKE': 'Infiniti', 'YEAR': 2013, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '430419', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '33276', 'epa.co2TailpipeGpm': '438.0', 'epa.model' : 'EX37', 'epa.trim' : 'Auto (S7), 6 cyl, 3.7 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JN1CV6FE4EM164066
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Infiniti&model=Q60%20Convertible
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/34134
    ## http://www.fueleconomy.gov/ws/rest/vehicle/34133
    {'VIN': 'JN1CV6FE4EM164066', 'WMI': 'JN1', 'VDS': 'CV6FE4', 'VIS': 'EM164066',
     'MODEL': 'Q60', 'MAKE': 'Infiniti', 'YEAR': 2014, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '164066', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '34134', 'epa.co2TailpipeGpm': '464.0', 'epa.model' : 'Q60 Convertible', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.7 L',
     #'epa.id' : '34133', 'epa.co2TailpipeGpm': '434.0', 'epa.model' : 'Q60 Convertible', 'epa.trim' : 'Auto (S7), 6 cyl, 3.7 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JN1AJ0HP7CM401080
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2012&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2012&make=Infiniti&model=EX35
    # http://www.fueleconomy.gov/ws/rest/vehicle/31820
    {'VIN': 'JN1AJ0HP7CM401080', 'WMI': 'JN1', 'VDS': 'AJ0HP7', 'VIS': 'CM401080',
     'MODEL': 'EX35', 'MAKE': 'Infiniti', 'YEAR': 2012, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '401080', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '31820', 'epa.co2TailpipeGpm': '444.4', 'epa.model' : 'EX35', 'epa.trim' : 'Auto (S7), 6 cyl, 3.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JN1AY1PP4FM170016
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Infiniti&model=Q70
    # http://www.fueleconomy.gov/ws/rest/vehicle/35712
    # NOTE: EPA doesn't seem to have separate data for the L, it's slightly longer
    {'VIN': 'JN1AY1PP4FM170016', 'WMI': 'JN1', 'VDS': 'AY1PP4', 'VIS': 'FM170016',
     'MODEL': 'Q70L', 'MAKE': 'Infiniti', 'YEAR': 2015, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '170016', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '35712', 'epa.co2TailpipeGpm': '463.0', 'epa.model' : 'Q70', 'epa.trim' : 'Auto (S7), 8 cyl, 5.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JN1AZ44EX9M403788
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2009&make=Nissan
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2009&make=Nissan&model=370z
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/26324
    ## http://www.fueleconomy.gov/ws/rest/vehicle/26323
    {'VIN': 'JN1AZ44EX9M403788', 'WMI': 'JN1', 'VDS': 'AZ44EX', 'VIS': '9M403788',
     'MODEL': '370Z', 'MAKE': 'Nissan', 'YEAR': 2009, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '403788', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '26324', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : '370z', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.7 L',
     #'epa.id' : '26323', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : '370z', 'epa.trim' : 'Auto (S7), 6 cyl, 3.7 L',
    },

    # http://www.vindecoder.net/?vin=JN8BS1MW7EM920252&submit=Decode
    # NHTSA has 4WD, EPA and world have AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/33883
    {'VIN': 'JN8BS1MW7EM920252', 'WMI': 'JN8', 'VDS': 'BS1MW7', 'VIS': 'EM920252',
     'MODEL': 'QX70', 'MAKE':  'Infiniti', 'YEAR': 2014, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '920252', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '33883', 'epa.co2TailpipeGpm': '549.0', 'epa.model' : 'QX70 AWD', 'epa.trim' : 'Auto (S7), 8 cyl, 5.0 L',
    },

    # http://www.vindecoder.net/?vin=JN8CS1MU0DM236239&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/32818
    {'VIN': 'JN8CS1MU0DM236239', 'WMI': 'JN8', 'VDS': 'CS1MU0', 'VIS': 'DM236239',
     'MODEL': 'FX37', 'MAKE':  'Infiniti', 'YEAR': 2013, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '236239', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32818', 'epa.co2TailpipeGpm': '460.0', 'epa.model' : 'FX37 RWD', 'epa.trim' : 'Auto (S7), 6 cyl, 3.7 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JTEBU5JR5G5340695
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Toyota
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Toyota&model=4Runner%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36858
    {'VIN': 'JTEBU5JR5G5340695', 'WMI': 'JTE', 'VDS': 'BU5JR5', 'VIS': 'G5340695',
     'MODEL': '4-Runner', 'MAKE': 'Toyota', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '340695', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Base Grade', 'nhtsa.series': 'GRN280L/GRN285L',
     'epa.id' : '36858', 'epa.co2TailpipeGpm': '478.0', 'epa.model' : '4Runner 4WD', 'epa.trim' : 'Auto (S5), 6 cyl, 4.0 L, Part-time 4WD',
    },

    # http://www.vindecoder.net/?vin=JTHBW1GG7D2369737&submit=Decode has no model
    # http://www.autocalculator.org/VIN/WMI.aspx agrees JTH is Lexus
    # http://www.clublexus.com/forums/vindecoder.php?vin=JTHBW1GG7D2369737
    # http://www.fueleconomy.gov/ws/rest/vehicle/32711
    {'VIN': 'JTHBW1GG7D2369737', 'WMI': 'JTH', 'VDS': 'BW1GG7', 'VIS': 'D2369737',
     'MODEL': 'ES 300h', 'MAKE':  'Lexus', 'YEAR': 2013, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '369737', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32711', 'epa.co2TailpipeGpm': '224.0', 'epa.model' : 'ES 300h', 'epa.trim' : 'Auto(AV-S6), 4 cyl, 2.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JTJYARBZ3G2042318
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Lexus
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Lexus&model=NX%20200t
    # http://www.fueleconomy.gov/ws/rest/vehicle/37058
    {'VIN': 'JTJYARBZ3G2042318', 'WMI': 'JTJ', 'VDS': 'YARBZ3', 'VIS': 'G2042318',
     'MODEL': 'NX', 'MAKE': 'Lexus', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '042318', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Luxury', 'nhtsa.series': 'AGZ10L/AGZ15L/AYZ10L/AYZ15L',
     'epa.id' : '37058', 'epa.co2TailpipeGpm': '357.0', 'epa.model' : 'NX 200t', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=JTJHY7AX4D4667505&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/32226
    {'VIN': 'JTJHY7AX4D4667505', 'WMI': 'JTJ', 'VDS': 'HY7AX4', 'VIS': 'D4667505',
     'MODEL': 'LX 570', 'MAKE':  'Lexus', 'YEAR': 2013, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '667505', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32226', 'epa.co2TailpipeGpm': '623.0', 'epa.model' : 'LX 570', 'epa.trim' : 'Auto (S6), 8 cyl, 5.7 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JTNKARJEXGJ522381
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Scion
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Scion&model=iM
    # http://www.fueleconomy.gov/ws/rest/vehicle/36902
    {'VIN': 'JTNKARJEXGJ522381', 'WMI': 'JTN', 'VDS': 'KARJEX', 'VIS': 'GJ522381',
     'MODEL': 'Scion iM', 'MAKE': 'Scion', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '522381', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'ZRE186L',
     'epa.id' : '36902', 'epa.co2TailpipeGpm': '294.0', 'epa.model' : 'iM', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.8 L',
    },

    ## Breadcrumbs for how libvin/epa.py looks up the epa results:
    ## https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JM1BM1W39E1175532
    ## http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Mazda
    ## http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Mazda&model=3%204-Door
    ### http://www.fueleconomy.gov/ws/rest/vehicle/34274
    ## The Vin info isn't enough, this has the i-ELOOP thingy.  Disable until we can decode it.
    ## Not likely to be fixed, given https://vpic.nhtsa.dot.gov/mid/home/displayfile/5442 doesn't mention it.
    ## Fortunately, it almost doesn't matter.
    ## http://www.fueleconomy.gov/ws/rest/vehicle/34275
    {'VIN': 'JM1BM1W39E1175532', 'WMI': 'JM1', 'VDS': 'BM1W39', 'VIS': 'E1175532',
     'MODEL': 'Mazda3', 'MAKE': 'Mazda', 'YEAR': 2014, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '175532', 'FEWER_THAN_500_PER_YEAR': False,
    # 'nhtsa.trim': 'Grand Touring/GT', 'nhtsa.series': '',
    # #'epa.id' : '34274', 'epa.co2TailpipeGpm': '277.0', 'epa.model' : '3 4-Door', 'epa.trim' : 'Auto (S6), 4 cyl, 2.5 L, SIDI',
    # 'epa.id' : '34275', 'epa.co2TailpipeGpm': '275.0', 'epa.model' : '3 4-Door', 'epa.trim' : 'Auto (S6), 4 cyl, 2.5 L, SIDI; with i-ELOOP Technology Package',
    },

    # http://www.vindecoder.net/?vin=JM1BL1SF3A1267720&submit=Decode
    # NOTE: Can't tell transmission type, just pick one
    # http://www.fueleconomy.gov/ws/rest/vehicle/26372 'Man 5-spd, 4 cyl, 2.0 L,
    # http://www.fueleconomy.gov/ws/rest/vehicle/26373 'Auto (S5), 4 cyl, 2.0 L'
    {'VIN': 'JM1BL1SF3A1267720', 'WMI': 'JM1', 'VDS': 'BL1SF3', 'VIS': 'A1267720',
     'MODEL': 'MAZDA3', 'MAKE':  'Mazda', 'YEAR': 2010, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '267720', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '26373', 'epa.co2TailpipeGpm': '329.1', 'epa.model' : '3', 'epa.trim' : 'Auto (S5), 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JM1DE1KZ2E0182845
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Mazda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Mazda&model=2
    # http://www.fueleconomy.gov/ws/rest/vehicle/34162
    {'VIN': 'JM1DE1KZ2E0182845', 'WMI': 'JM1', 'VDS': 'DE1KZ2', 'VIS': 'E0182845',
     'MODEL': 'Mazda2', 'MAKE': 'Mazda', 'YEAR': 2014, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '182845', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Sport/GX', 'nhtsa.series': '',
     'epa.id' : '34162', 'epa.co2TailpipeGpm': '286.0', 'epa.model' : '2', 'epa.trim' : 'Man 5-spd, 4 cyl, 1.5 L',
    },

    # https://vpic.nhtsa.dot.gov/mid/home/displayfile/29702 "2016 Model Year Vin Coding" for cx-9 and cx-3
    # Note: DKA and DKB didn't encode 2WD vs 4WD, but DKC-DKF do.
    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JM1DKDD75G0135172
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Mazda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Mazda&model=CX-3%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36219
    {'VIN': 'JM1DKDD75G0135172', 'WMI': 'JM1', 'VDS': 'DKDD75', 'VIS': 'G0135172',
     'MODEL': 'CX-3', 'MAKE': 'Mazda', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '135172', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Grand Touring/GT',
     'epa.id' : '36219', 'epa.co2TailpipeGpm': '288.0', 'epa.model' : 'CX-3 2WD', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/JM1DKFD76G0130140
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Mazda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Mazda&model=CX-3%204WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36220
    {'VIN': 'JM1DKFD76G0130140', 'WMI': 'JM1', 'VDS': 'DKFD76', 'VIS': 'G0130140',
     'MODEL': 'CX-3', 'MAKE': 'Mazda', 'YEAR': 2016, 'COUNTRY': 'Japan',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '130140', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Grand Touring/GT',
     'epa.id' : '36220', 'epa.co2TailpipeGpm': '305.0', 'epa.model' : 'CX-3 4WD', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/KL1TD5DE9BB162132
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2011&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2011&make=Chevrolet&model=Aveo
    # http://www.fueleconomy.gov/ws/rest/vehicle/30314
    {'VIN': 'KL1TD5DE9BB162132', 'WMI': 'KL1', 'VDS': 'TD5DE9', 'VIS': 'BB162132',
     'MODEL': 'Aveo', 'MAKE': 'Chevrolet', 'YEAR': 2011, 'COUNTRY': 'Korea (South)',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '162132', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1LS/1LT',
     'epa.id' : '30314', 'epa.co2TailpipeGpm': '306.4', 'epa.model' : 'Aveo', 'epa.trim' : 'Man 5-spd, 4 cyl, 1.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/KL4CJASB9GB686238
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Buick
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Buick&model=Encore
    # http://www.fueleconomy.gov/ws/rest/vehicle/36490
    {'VIN': 'KL4CJASB9GB686238', 'WMI': 'KL4', 'VDS': 'CJASB9', 'VIS': 'GB686238',
     'MODEL': 'Encore', 'MAKE': 'Buick', 'YEAR': 2016, 'COUNTRY': 'Korea (South)',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '686238', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '36490', 'epa.co2TailpipeGpm': '320.0', 'epa.model' : 'Encore', 'epa.trim' : 'Auto (S6), 4 cyl, 1.4 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/KL7CJPSB2GB657170
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Chevrolet
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Chevrolet&model=Trax%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36769
    {'VIN': 'KL7CJPSB2GB657170', 'WMI': 'KL7', 'VDS': 'CJPSB2', 'VIS': 'GB657170',
     'MODEL': 'Trax', 'MAKE': 'Chevrolet', 'YEAR': 2016, 'COUNTRY': 'Korea (South)',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '657170', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '1LT AWD',
     'epa.id' : '36769', 'epa.co2TailpipeGpm': '330.0', 'epa.model' : 'Trax AWD', 'epa.trim' : 'Auto (S6), 4 cyl, 1.4 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=KNDJT2A54D7883468&submit=Decode
    # Note: can't tell transmission
    # http://www.fueleconomy.gov/ws/rest/vehicle/32802 'Auto 6-spd, 4 cyl, 1.6 L'
    # http://www.fueleconomy.gov/ws/rest/vehicle/32803 'Man 6-spd, 4 cyl, 1.6 L'
    {'VIN': 'KNDJT2A54D7883468', 'WMI': 'KND', 'VDS': 'JT2A54', 'VIS': 'D7883468',
     'MODEL': 'Soul', 'MAKE':  'Kia', 'YEAR': 2013, 'COUNTRY': 'Korea (South)',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '883468', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32803', 'epa.co2TailpipeGpm': '331.0', 'epa.model' : 'Soul', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.6 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/36940
    {'VIN': 'KNMAT2MT0GP672329', 'WMI': 'KNM', 'VDS': 'AT2MT0', 'VIS': 'GP672329',
     'MODEL': 'Rogue', 'MAKE': 'Nissan', 'YEAR': 2016, 'COUNTRY': 'Korea (South)',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '672329', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '36940', 'epa.co2TailpipeGpm': '318.0', 'epa.model' : 'Rogue FWD', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 2.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/LRBFXBSA5HD005141
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Buick
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Buick&model=Envision%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/37784
    {'VIN': 'LRBFXBSA5HD005141', 'WMI': 'LRB', 'VDS': 'FXBSA5', 'VIS': 'HD005141',
     'MODEL': 'Envision', 'MAKE': 'Buick', 'YEAR': 2017, 'COUNTRY': 'China',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '005141', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Essence',
     'epa.id' : '37784', 'epa.co2TailpipeGpm': '356.0', 'epa.model' : 'Envision FWD', 'epa.trim' : 'Auto 6-spd, 4 cyl, 2.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/LYV402FK0GB112042
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Volvo
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Volvo&model=S60%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36224
    {'VIN': 'LYV402FK0GB112042', 'WMI': 'LYV', 'VDS': '402FK0', 'VIS': 'GB112042',
     'MODEL': 'S60/S60I', 'MAKE': 'Volvo', 'YEAR': 2016, 'COUNTRY': 'China',
     'REGION': 'asia', 'SEQUENTIAL_NUMBER': '112042', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SV33 Premier', 'nhtsa.series': '',
     'epa.id' : '36224', 'epa.co2TailpipeGpm': '292.0', 'epa.model' : 'S60 FWD', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SADCM2BV5HA056855
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Jaguar
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Jaguar&model=F-Pace
    # http://www.fueleconomy.gov/ws/rest/vehicle/37394
    {'VIN': 'SADCM2BV5HA056855', 'WMI': 'SAD', 'VDS': 'CM2BV5', 'VIS': 'HA056855',
     'MODEL': 'F-Pace', 'MAKE': 'Jaguar', 'YEAR': 2017, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '056855', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'S',
     'epa.id' : '37394', 'epa.co2TailpipeGpm': '446.0', 'epa.model' : 'F-Pace', 'epa.trim' : 'Auto (S8), 6 cyl, 3.0 L, Sup Charg',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SAJWA0HP7FMU61983
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Jaguar
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Jaguar&model=XF%20FFV
    # http://www.fueleconomy.gov/ws/rest/vehicle/34948
    {'VIN': 'SAJWA0HP7FMU61983', 'WMI': 'SAJ', 'VDS': 'WA0HP7', 'VIS': 'FMU61983',
     'MODEL': 'XF', 'MAKE': 'Jaguar', 'YEAR': 2015, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '61983', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Supercharged', 'nhtsa.series': '',
     'epa.id' : '34948', 'epa.co2TailpipeGpm': '500.0', 'epa.model' : 'XF FFV', 'epa.trim' : 'Auto (S8), 8 cyl, 5.0 L, Sup Charg',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SAJWJ6HL9HMK36791
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Jaguar
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Jaguar&model=F-Type%20R%20AWD%20Convertible
    # http://www.fueleconomy.gov/ws/rest/vehicle/37312
    {'VIN': 'SAJWJ6HL9HMK36791', 'WMI': 'SAJ', 'VDS': 'WJ6HL9', 'VIS': 'HMK36791',
     'MODEL': 'F-Type', 'MAKE': 'Jaguar', 'YEAR': 2017, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '36791', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'R',
     'epa.id' : '37312', 'epa.co2TailpipeGpm': '500.0', 'epa.model' : 'F-Type R AWD Convertible', 'epa.trim' : 'Auto (S8), 8 cyl, 5.0 L, Sup Charg',
    },

    # http://www.vindecoder.net/?vin=SCBEC9ZA1EC225243&submit=Decode
    # https://www.vinaudit.com/vin-search?vin=SCBEC9ZA1EC225243 got model slightly wrong
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Bentley confirms model name
    # 'ErrorCode': u'8 - No detailed data available currently',
    {'VIN': 'SCBEC9ZA1EC225243', 'WMI': 'SCB', 'VDS': 'EC9ZA1', 'VIS': 'EC225243',
     'MODEL': 'Flying Spur', 'MAKE':  'Bentley', 'YEAR': 2014, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '225243', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SCCLMDTU9DHA10803
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Lotus
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Lotus&model=Evora
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/33309
    ## http://www.fueleconomy.gov/ws/rest/vehicle/33312
    ## http://www.fueleconomy.gov/ws/rest/vehicle/33311
    ## http://www.fueleconomy.gov/ws/rest/vehicle/33310
    {'VIN': 'SCCLMDTU9DHA10803', 'WMI': 'SCC', 'VDS': 'LMDTU9', 'VIS': 'DHA10803',
     'MODEL': 'Evora', 'MAKE': 'Lotus', 'YEAR': 2013, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '0803', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '33309', 'epa.co2TailpipeGpm': '420.0', 'epa.model' : 'Evora', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.5 L',
     #'epa.id' : '33312', 'epa.co2TailpipeGpm': '402.0', 'epa.model' : 'Evora', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L, Sup Charg',
     #'epa.id' : '33311', 'epa.co2TailpipeGpm': '390.0', 'epa.model' : 'Evora', 'epa.trim' : 'Auto (S6), 6 cyl, 3.5 L',
     #'epa.id' : '33310', 'epa.co2TailpipeGpm': '433.0', 'epa.model' : 'Evora', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.5 L, Sup Charg',
    },

    # http://www.vindecoder.net/?vin=SCFAD01A65G199359&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2005&make=Aston%20Martin verifies spelling
    # 'ErrorCode': u'8 - No detailed data available currently',
    {'VIN': 'SCFAD01A65G199359', 'WMI': 'SCF', 'VDS': 'AD01A6', 'VIS': '5G199359',
     'MODEL': 'DB9', 'MAKE':  'Aston Martin', 'YEAR': 2005, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '99359', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SCFBF04B38GD08385
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2008&make=Aston%20Martin
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2008&make=Aston%20Martin&model=V8%20Vantage
    # http://www.fueleconomy.gov/ws/rest/vehicle/24742
    # Note short SEQUENTIAL_NUMBER!

    {'VIN': 'SCFBF04B38GD08385', 'WMI': 'SCF', 'VDS': 'BF04B3', 'VIS': '8GD08385',
     'MODEL': 'V8 Vantage', 'MAKE': 'Aston Martin', 'YEAR': 2008, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '08385', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '24742', 'epa.co2TailpipeGpm': '592.5', 'epa.model' : 'V8 Vantage', 'epa.trim' : 'Man 6-spd, 8 cyl, 4.3 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SHHFK7H56HU400265
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Honda
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Honda&model=Civic%205Dr
    # http://www.fueleconomy.gov/ws/rest/vehicle/38256
    {'VIN': 'SHHFK7H56HU400265', 'WMI': 'SHH', 'VDS': 'FK7H56', 'VIS': 'HU400265',
     'MODEL': 'Civic', 'MAKE': 'Honda', 'YEAR': 2017, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '400265', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'EX',
     'epa.id' : '38256', 'epa.co2TailpipeGpm': '260.0', 'epa.model' : 'Civic 5Dr', 'epa.trim' : 'Auto (variable gear ratios), 4 cyl, 1.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/SJKCH5CPXHA016639
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=Infiniti
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=Infiniti&model=QX30
    # http://www.fueleconomy.gov/ws/rest/vehicle/38053
    {'VIN': 'SJKCH5CPXHA016639', 'WMI': 'SJK', 'VDS': 'CH5CPX', 'VIS': 'HA016639',
     'MODEL': 'QX30', 'MAKE': 'Infiniti', 'YEAR': 2017, 'COUNTRY': 'United Kingdom',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '016639', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '38053', 'epa.co2TailpipeGpm': '324.0', 'epa.model' : 'QX30', 'epa.trim' : 'Auto(AM7), 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=TRUSC28N711268458&submit=Decode
    # NOTE: displacement is 1781cc, but EPA only has 1.8L, hard to match.
    {'VIN': 'TRUSC28N711268458', 'WMI': 'TRU', 'VDS': 'SC28N7', 'VIS': '11268458',
     'MODEL': 'TT', 'MAKE':  'Audi', 'YEAR': 2001, 'COUNTRY': 'Hungary',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '268458', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # http://www.vindecoder.net/?vin=VNKJTUD36FA838549&submit=Decode
    # Note: can't tell transmission
    # http://www.fueleconomy.gov/ws/rest/vehicle/35297
    # http://www.fueleconomy.gov/ws/rest/vehicle/35298
    {'VIN': 'VNKJTUD36FA838549', 'WMI': 'VNK', 'VDS': 'JTUD36', 'VIS': 'FA838549',
     'MODEL': 'Yaris', 'MAKE':  'Toyota', 'YEAR': 2015, 'COUNTRY': 'France',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '838549', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35298', 'epa.co2TailpipeGpm': '271.0', 'epa.model' : 'Yaris', 'epa.trim' : 'Man 5-spd, 4 cyl, 1.5 L',
    },

    # http://www.vindecoder.net/?vin=W04GW5EV0B1603732&submit=Decode
    # http://gmvindecoder.net/vins/W04GW5EV0B1603732
    # Note: can't tell transmission
    # http://www.fueleconomy.gov/ws/rest/vehicle/31008
    # http://www.fueleconomy.gov/ws/rest/vehicle/31009
    {'VIN': 'W04GW5EV0B1603732', 'WMI': 'W04', 'VDS': 'GW5EV0', 'VIS': 'B1603732',
     'MODEL': 'Regal', 'MAKE':  'Buick', 'YEAR': 2011, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '603732', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '31009', 'epa.co2TailpipeGpm': '370.3', 'epa.model' : 'Regal', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WA1C2AFP1GA058862
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Audi
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Audi&model=Q5
    # http://www.fueleconomy.gov/ws/rest/vehicle/36421
    {'VIN': 'WA1C2AFP1GA058862', 'WMI': 'WA1', 'VDS': 'C2AFP1', 'VIS': 'GA058862',
     'MODEL': 'Q5', 'MAKE': 'Audi', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '058862', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'quattro', 'nhtsa.series': '2.0T Premium / Hybrid Prestige / TDI Premium Plus / SQ5 Premium Plus',
     'epa.id' : '36421', 'epa.co2TailpipeGpm': '395.0', 'epa.model' : 'Q5', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # http://www.vindecoder.net/?vin=WA1EY74LX9D205644&submit=Decode
    # https://vindecoder.eu/check-vin/WA1EY74LX9D205644
    # NOTE: NHTSA has 3.596000 L, EPA has 3.6 L
    {'VIN': 'WA1EY74LX9D205644', 'WMI': 'WA1', 'VDS': 'EY74LX', 'VIS': '9D205644',
     'MODEL': 'Q7', 'MAKE':  'Audi', 'YEAR': 2009, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '205644', 'FEWER_THAN_500_PER_YEAR': False,
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBA1L9C54GV325753
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=BMW&model=228i%20xDrive%20Convertible
    # http://www.fueleconomy.gov/ws/rest/vehicle/36640
    {'VIN': 'WBA1L9C54GV325753', 'WMI': 'WBA', 'VDS': '1L9C54', 'VIS': 'GV325753',
     'MODEL': '228i', 'MAKE': 'BMW', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '325753', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'xDrive SULEV', 'nhtsa.series': '2-series',
     'epa.id' : '36640', 'epa.co2TailpipeGpm': '338.0', 'epa.model' : '228i xDrive Convertible', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBAVM1C50EVW50347
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=BMW&model=X1%20sDrive28i
    # http://www.fueleconomy.gov/ws/rest/vehicle/33552
    {'VIN': 'WBAVM1C50EVW50347', 'WMI': 'WBA', 'VDS': 'VM1C50', 'VIS': 'EVW50347',
     'MODEL': 'X1', 'MAKE': 'BMW', 'YEAR': 2014, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'W50347', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': 'sDrive 28i',
     'epa.id' : '33552', 'epa.co2TailpipeGpm': '332.0', 'epa.model' : 'X1 sDrive28i', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBA3C1C53FK119625
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=BMW&model=328i
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/35331
    ## http://www.fueleconomy.gov/ws/rest/vehicle/35330
    {'VIN': 'WBA3C1C53FK119625', 'WMI': 'WBA', 'VDS': '3C1C53', 'VIS': 'FK119625',
     'MODEL': '328i', 'MAKE': 'BMW', 'YEAR': 2015, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '119625', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SULEV', 'nhtsa.series': '3-Series',
     'epa.id' : '35331', 'epa.co2TailpipeGpm': '341.0', 'epa.model' : '328i', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L, Turbo',
     #'epa.id' : '35330', 'epa.co2TailpipeGpm': '324.0', 'epa.model' : '328i', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBA3F9C50DF483691
    # http://www.fueleconomy.gov/ws/rest/vehicle/32907
    ## http://www.fueleconomy.gov/ws/rest/vehicle/33054
    {'VIN': 'WBA3F9C50DF483691', 'WMI': 'WBA', 'VDS': '3F9C50', 'VIS': 'DF483691',
     'MODEL': '335i', 'MAKE': 'BMW', 'YEAR': 2013, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '483691', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'ActiveHybrid 3 Sedan', 'nhtsa.series': '3-Series',
     'epa.id' : '32907', 'epa.co2TailpipeGpm': '385.0', 'epa.model' : '335i', 'epa.trim' : 'Man 6-spd, 6 cyl, 3.0 L, Turbo',
     #'epa.id' : '33054', 'epa.co2TailpipeGpm': '341.0', 'epa.model' : '335i', 'epa.trim' : 'Auto (S8), 6 cyl, 3.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBSWL9C54AP786013
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2010&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2010&make=BMW&model=M3%20Convertible
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/29697
    ## http://www.fueleconomy.gov/ws/rest/vehicle/29806
    {'VIN': 'WBSWL9C54AP786013', 'WMI': 'WBS', 'VDS': 'WL9C54', 'VIS': 'AP786013',
     'MODEL': 'M3', 'MAKE': 'BMW', 'YEAR': 2010, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '786013', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '3 - Series',
     'epa.id' : '29697', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'M3 Convertible', 'epa.trim' : 'Auto (S7), 8 cyl, 4.0 L',
     #'epa.id' : '29806', 'epa.co2TailpipeGpm': '555.4', 'epa.model' : 'M3 Convertible', 'epa.trim' : 'Man 6-spd, 8 cyl, 4.0 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBXHT3C30G5E55046
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=BMW&model=X1%20xDrive28i
    # http://www.fueleconomy.gov/ws/rest/vehicle/36936
    {'VIN': 'WBXHT3C30G5E55046', 'WMI': 'WBX', 'VDS': 'HT3C30', 'VIS': 'G5E55046',
     'MODEL': 'X1', 'MAKE': 'BMW', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'E55046', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': 'xDrive28i',
     'epa.id' : '36936', 'epa.co2TailpipeGpm': '346.0', 'epa.model' : 'X1 xDrive28i', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBXHT3C30H5F67928
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2017&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2017&make=BMW&model=X1%20xDrive28i
    # http://www.fueleconomy.gov/ws/rest/vehicle/37930
    {'VIN': 'WBXHT3C30H5F67928', 'WMI': 'WBX', 'VDS': 'HT3C30', 'VIS': 'H5F67928',
     'MODEL': 'X1', 'MAKE': 'BMW', 'YEAR': 2017, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'F67928', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SAV', 'nhtsa.series': '28i Br',
     'epa.id' : '37930', 'epa.co2TailpipeGpm': '349.0', 'epa.model' : 'X1 xDrive28i', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBY1Z2C51GV556326
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=BMW&model=i3%20BEV
    # http://www.fueleconomy.gov/ws/rest/vehicle/37216
    {'VIN': 'WBY1Z2C51GV556326', 'WMI': 'WBY', 'VDS': '1Z2C51', 'VIS': 'GV556326',
     'MODEL': 'i3', 'MAKE': 'BMW', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '556326', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '37216', 'epa.co2TailpipeGpm': '0.0', 'epa.model' : 'i3 BEV', 'epa.trim' : 'Auto (A1)',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WBY1Z4C5XGV505984
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=BMW
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=BMW&model=i3%20REX
    # http://www.fueleconomy.gov/ws/rest/vehicle/37222
    {'VIN': 'WBY1Z4C5XGV505984', 'WMI': 'WBY', 'VDS': '1Z4C5X', 'VIS': 'GV505984',
     'MODEL': 'i3', 'MAKE': 'BMW', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '505984', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Range Extender',
     'epa.id' : '37222', 'epa.co2TailpipeGpm': '37.0', 'epa.model' : 'i3 REX', 'epa.trim' : 'Auto (A1), 2 cyl, 0.6 L',
    },

    # http://www.fueleconomy.gov/ws/rest/vehicle/20623
    {'VIN': 'WDBTJ65JX5F126044', 'WMI': 'WDB', 'VDS': 'TJ65JX', 'VIS': '5F126044',
     'MODEL': 'CLK-Class', 'MAKE': 'Mercedes-Benz', 'YEAR': 2005, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '126044', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '20623', 'epa.co2TailpipeGpm': '423.2', 'epa.model' : 'CLK320', 'epa.trim' : 'Auto 5-spd, 6 cyl, 3.2 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WDCYC3HF7EX225710
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Mercedes-Benz&model=G550
    # http://www.fueleconomy.gov/ws/rest/vehicle/34514
    {'VIN': 'WDCYC3HF7EX225710', 'WMI': 'WDC', 'VDS': 'YC3HF7', 'VIS': 'EX225710',
     'MODEL': 'G-Class', 'MAKE': 'Mercedes-Benz', 'YEAR': 2014, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '225710', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '4-MATIC', 'nhtsa.series': 'G550',
     'epa.id' : '34514', 'epa.co2TailpipeGpm': '680.0', 'epa.model' : 'G550', 'epa.trim' : 'Auto 7-spd, 8 cyl, 5.5 L',
    },

    # http://www.vindecoder.net/?vin=WDCYC7DF3FX109287&submit=Decode
    # http://www.vindecoderz.com/EN/check-lookup/WDCYC7DF3FX109287
    # http://www.autocalculator.org/VIN/WMI.aspx says WDC is Mercedes-Benz, hmm
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/make?year=2015 spells it Mercedes-Benz, too, let's go with that
    # http://www.fueleconomy.gov/ws/rest/vehicle/35839
    {'VIN': 'WDCYC7DF3FX109287', 'WMI': 'WDC', 'VDS': 'YC7DF3', 'VIS': 'FX109287',
     'MODEL': 'G63', 'MAKE':  'Mercedes-Benz', 'YEAR': 2015, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '109287', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '35839', 'epa.co2TailpipeGpm': '696.0', 'epa.model' : 'G63 AMG', 'epa.trim' : 'Auto 7-spd, 8 cyl, 5.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WDC0G4KB8GF033296
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Mercedes-Benz&model=GLC300%204matic
    # http://www.fueleconomy.gov/ws/rest/vehicle/37160
    {'VIN': 'WDC0G4KB8GF033296', 'WMI': 'WDC', 'VDS': '0G4KB8', 'VIS': 'GF033296',
     'MODEL': 'GLC', 'MAKE': 'Mercedes-Benz', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '033296', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'Base-4M', 'nhtsa.series': 'GLC300',
     'epa.id' : '37160', 'epa.co2TailpipeGpm': '377.0', 'epa.model' : 'GLC300 4matic', 'epa.trim' : 'Auto 9-spd, 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WDDGF4HB6DA760028
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=Mercedes-Benz&model=C250
    # http://www.fueleconomy.gov/ws/rest/vehicle/32780
    {'VIN': 'WDDGF4HB6DA760028', 'WMI': 'WDD', 'VDS': 'GF4HB6', 'VIS': 'DA760028',
     'MODEL': 'C-Class', 'MAKE': 'Mercedes-Benz', 'YEAR': 2013, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '760028', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'C250',
     'epa.id' : '32780', 'epa.co2TailpipeGpm': '352.0', 'epa.model' : 'C250', 'epa.trim' : 'Auto 7-spd, 4 cyl, 1.8 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WDDLJ7GB9EA113284
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Mercedes-Benz
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Mercedes-Benz&model=CLS63%20AMG%204matic
    # http://www.fueleconomy.gov/ws/rest/vehicle/33815
    # Oh, well.  Can't handle this yet.
    #{'VIN': 'WDDLJ7GB9EA113284', 'WMI': 'WDD', 'VDS': 'LJ7GB9', 'VIS': 'EA113284',
    # 'MODEL': 'CLS-Class', 'MAKE': 'Mercedes-Benz', 'YEAR': 2014, 'COUNTRY': 'Germany',
    # 'REGION': 'europe', 'SEQUENTIAL_NUMBER': '113284', 'FEWER_THAN_500_PER_YEAR': False,
    # 'nhtsa.trim': '4-Matic', 'nhtsa.series': 'CLS63 AMG-S',
    # 'epa.id' : '33815', 'epa.co2TailpipeGpm': '495.0', 'epa.model' : 'CLS63 AMG 4matic', 'epa.trim' : 'Auto 7-spd, 8 cyl, 5.5 L, Turbo',
    #},

    # http://www.vindecoder.net/?vin=WDDNG7BB4AA522219&submit=Decode
    # ftp://safercar.gov/MfrMail/ORG4488.pdf
    # http://www.fueleconomy.gov/ws/rest/vehicle/29413
    {'VIN': 'WDDNG7BB4AA522219', 'WMI': 'WDD', 'VDS': 'NG7BB4', 'VIS': 'AA522219',
     'MODEL': 'S550', 'MAKE':  'Mercedes-Benz', 'YEAR': 2010, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '522219', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '29413', 'epa.co2TailpipeGpm': '493.7', 'epa.model' : 'S550', 'epa.trim' : 'Auto 7-spd, 8 cyl, 5.5 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WMWSV3C56DT393104
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=MINI
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2013&make=MINI&model=Cooper%20S
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/32877
    ## http://www.fueleconomy.gov/ws/rest/vehicle/32876
    {'VIN': 'WMWSV3C56DT393104', 'WMI': 'WMW', 'VDS': 'SV3C56', 'VIS': 'DT393104',
     'MODEL': 'Cooper S Hardtop', 'MAKE': 'MINI', 'YEAR': 2013, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '393104', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Cooper S',
     'epa.id' : '32877', 'epa.co2TailpipeGpm': '301.0', 'epa.model' : 'Cooper S', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.6 L, Turbo',
     #'epa.id' : '32876', 'epa.co2TailpipeGpm': '310.0', 'epa.model' : 'Cooper S', 'epa.trim' : 'Auto (S6), 4 cyl, 1.6 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WMWXM5C52F3A57895
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=MINI
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=MINI&model=Cooper%20(3-doors)
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/35794
    ## http://www.fueleconomy.gov/ws/rest/vehicle/35793
    {'VIN': 'WMWXM5C52F3A57895', 'WMI': 'WMW', 'VDS': 'XM5C52', 'VIS': 'F3A57895',
     'MODEL': 'Cooper Hardtop', 'MAKE': 'MINI', 'YEAR': 2015, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'A57895', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Cooper',
     'epa.id' : '35794', 'epa.co2TailpipeGpm': '272.0', 'epa.model' : 'Cooper (3-doors)', 'epa.trim' : 'Man 6-spd, 3 cyl, 1.5 L, Turbo',
     #'epa.id' : '35793', 'epa.co2TailpipeGpm': '287.0', 'epa.model' : 'Cooper (3-doors)', 'epa.trim' : 'Auto (S6), 3 cyl, 1.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WMWXM7C58ET986724
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=MINI
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=MINI&model=Cooper%20S%20(3-doors)
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/34792
    ## http://www.fueleconomy.gov/ws/rest/vehicle/34858
    {'VIN': 'WMWXM7C58ET986724', 'WMI': 'WMW', 'VDS': 'XM7C58', 'VIS': 'ET986724',
     'MODEL': 'Cooper S Hardtop', 'MAKE': 'MINI', 'YEAR': 2014, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '986724', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Cooper S',
     'epa.id' : '34792', 'epa.co2TailpipeGpm': '316.0', 'epa.model' : 'Cooper S (3-doors)', 'epa.trim' : 'Man 6-spd, 4 cyl, 2.0 L, Turbo',
     #'epa.id' : '34858', 'epa.co2TailpipeGpm': '300.0', 'epa.model' : 'Cooper S (3-doors)', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WMWXP5C50G3B76912
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=MINI
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=MINI&model=Cooper%20Hardtop%202%20door
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/36790
    ## http://www.fueleconomy.gov/ws/rest/vehicle/36843
    {'VIN': 'WMWXP5C50G3B76912', 'WMI': 'WMW', 'VDS': 'XP5C50', 'VIS': 'G3B76912',
     'MODEL': 'Cooper Hardtop', 'MAKE': 'MINI', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'B76912', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Cooper',
     'epa.id' : '36790', 'epa.co2TailpipeGpm': '292.0', 'epa.model' : 'Cooper Hardtop 2 door', 'epa.trim' : 'Auto (S6), 4 cyl, 1.5 L, Turbo',
     #'epa.id' : '36843', 'epa.co2TailpipeGpm': '277.0', 'epa.model' : 'Cooper Hardtop 2 door', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WMWXU1C50G2E16676
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=MINI
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=MINI&model=Cooper%20Hardtop%204%20door
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/36791
    ## http://www.fueleconomy.gov/ws/rest/vehicle/36719
    {'VIN': 'WMWXU1C50G2E16676', 'WMI': 'WMW', 'VDS': 'XU1C50', 'VIS': 'G2E16676',
     'MODEL': 'Cooper', 'MAKE': 'MINI', 'YEAR': 2016, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'E16676', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'Cooper',
     'epa.id' : '36791', 'epa.co2TailpipeGpm': '292.0', 'epa.model' : 'Cooper Hardtop 4 door', 'epa.trim' : 'Auto (S6), 4 cyl, 1.5 L, Turbo',
     #'epa.id' : '36719', 'epa.co2TailpipeGpm': '272.0', 'epa.model' : 'Cooper Hardtop 4 door', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WP1AE2A20FLA52901
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Porsche
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Porsche&model=Cayenne%20S%20e-Hybrid
    # http://www.fueleconomy.gov/ws/rest/vehicle/35896
    {'VIN': 'WP1AE2A20FLA52901', 'WMI': 'WP1', 'VDS': 'AE2A20', 'VIS': 'FLA52901',
     'MODEL': 'Cayenne', 'MAKE': 'Porsche', 'YEAR': 2015, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'A52901', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'E-Hybrid', 'nhtsa.series': 'S',
     'epa.id' : '35896', 'epa.co2TailpipeGpm': '260.0', 'epa.model' : 'Cayenne S e-Hybrid', 'epa.trim' : 'Auto(AM8), 6 cyl, 3.0 L, Sup Charg',
    },

    # http://www.vindecoder.net/?vin=WUADUAFG6AN410499&submit=Decode
    # http://www.fueleconomy.gov/ws/rest/vehicle/28523
    {'VIN': 'WUADUAFG6AN410499', 'WMI': 'WUA', 'VDS': 'DUAFG6', 'VIS': 'AN410499',
     'MODEL': 'R8', 'MAKE':  'Audi', 'YEAR': 2010, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '410499', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '28523', 'epa.co2TailpipeGpm': '592.5', 'epa.model' : 'R8', 'epa.trim' : 'Man 6-spd, 8 cyl, 4.2 L',
    },

    # http://www.vindecoder.net/?vin=WVGAV7AX9BW549850&submit=Decode unchecked
    # http://acurazine.com/forums/vindecoder.php?vin=WVGAV7AX9BW549850
    # http://www.fueleconomy.gov/ws/rest/vehicle/30536
    {'VIN': 'WVGAV7AX9BW549850', 'WMI': 'WVG', 'VDS': 'AV7AX9', 'VIS': 'BW549850',
     'MODEL': 'Tiguan', 'MAKE':  'Volkswagen', 'YEAR': 2011, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '549850', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '30536', 'epa.co2TailpipeGpm': '404.0', 'epa.model' : 'Tiguan', 'epa.trim' : 'Auto (S6), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/WVGEP9BP7FD004530
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Volkswagen
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Volkswagen&model=Touareg
    # http://www.fueleconomy.gov/ws/rest/vehicle/35484
    {'VIN': 'WVGEP9BP7FD004530', 'WMI': 'WVG', 'VDS': 'EP9BP7', 'VIS': 'FD004530',
     'MODEL': 'Touareg', 'MAKE': 'Volkswagen', 'YEAR': 2015, 'COUNTRY': 'Germany',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '004530', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'V6 FSI / TDI / Hybrid',
     'epa.id' : '35484', 'epa.co2TailpipeGpm': '462.0', 'epa.model' : 'Touareg', 'epa.trim' : 'Auto (S8), 6 cyl, 3.6 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/YH4K14AA5CA000763
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2012&make=Fisker
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2012&make=Fisker&model=Karma
    # http://www.fueleconomy.gov/ws/rest/vehicle/32516
    # Note: commented out until nhtsa fixes Make to be Fisker, not Karma.
    #{'VIN': 'YH4K14AA5CA000763', 'WMI': 'YH4', 'VDS': 'K14AA5', 'VIS': 'CA000763',
    # 'MODEL': 'Karma', 'MAKE': 'Fisker', 'YEAR': 2012, 'COUNTRY': 'Finland',
    # 'REGION': 'europe', 'SEQUENTIAL_NUMBER': '000763', 'FEWER_THAN_500_PER_YEAR': False,
    # 'nhtsa.trim': 'Volume Build', 'nhtsa.series': 'ECO Sport',
    # 'epa.id' : '32516', 'epa.co2TailpipeGpm': '169.0', 'epa.model' : 'Karma', 'epa.trim' : 'Auto (A1), 4 cyl, 2.0 L, Turbo',
    #},

    #------- Volvo --------
    # https://vpic.nhtsa.dot.gov/mid/home/displayfile/32205 "Volvo MY 2016 VIN decoder - USA/Canada"

    # http://www.vindecoder.net/?vin=YV1902FH5D1796335&submit=Decode doesn't have model
    # http://www.vindecoderz.com/EN/check-lookup/YV1902FH5D1796335
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2013&make=Volvo confirms XC60
    # http://www.fueleconomy.gov/ws/rest/vehicle/32588
    {'VIN': 'YV1902FH5D1796335', 'WMI': 'YV1', 'VDS': '902FH5', 'VIS': 'D1796335',
     'MODEL': 'XC60', 'MAKE':  'Volvo', 'YEAR': 2013, 'COUNTRY': 'Sweden',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '796335', 'FEWER_THAN_500_PER_YEAR': False,
     'epa.id' : '32588', 'epa.co2TailpipeGpm': '425.0', 'epa.model' : 'S60 AWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/YV126MFK7G2412996
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Volvo
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Volvo&model=S60%20FWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36224
    {'VIN': 'YV126MFK7G2412996', 'WMI': 'YV1', 'VDS': '26MFK7', 'VIS': 'G2412996',
     'MODEL': 'S60/S60I', 'MAKE': 'Volvo', 'YEAR': 2016, 'COUNTRY': 'Sweden',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '412996', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SV33 Premier', 'nhtsa.series': '',
     'epa.id' : '36224', 'epa.co2TailpipeGpm': '292.0', 'epa.model' : 'S60 FWD', 'epa.trim' : 'Auto (S8), 4 cyl, 2.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/YV1A92TS3G1394112
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Volvo
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Volvo&model=S60%20PoleStar%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36226
    {'VIN': 'YV1A92TS3G1394112', 'WMI': 'YV1', 'VDS': 'A92TS3', 'VIS': 'G1394112',
     'MODEL': 'S60/S60I', 'MAKE': 'Volvo', 'YEAR': 2016, 'COUNTRY': 'Sweden',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '394112', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'SVP9 Polestar Special Edition', 'nhtsa.series': '',
     'epa.id' : '36226', 'epa.co2TailpipeGpm': '412.0', 'epa.model' : 'S60 PoleStar AWD', 'epa.trim' : 'Auto (S6), 6 cyl, 3.0 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/YV4612UM8G2001277
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Volvo
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Volvo&model=S60%20CC%20AWD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36247
    {'VIN': 'YV4612UM8G2001277', 'WMI': 'YV4', 'VDS': '612UM8', 'VIS': 'G2001277',
     'MODEL': 'S60CC', 'MAKE': 'Volvo', 'YEAR': 2016, 'COUNTRY': 'Sweden',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '001277', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': '',
     'epa.id' : '36247', 'epa.co2TailpipeGpm': '383.0', 'epa.model' : 'S60 CC AWD', 'epa.trim' : 'Auto (S6), 5 cyl, 2.5 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/ZACCJABH0FPB66736
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Jeep
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Jeep&model=Renegade%202WD
    # http://www.fueleconomy.gov/ws/rest/vehicle/36124
    # NOTE: invalid but real: https://vpic.nhtsa.dot.gov/mid/home/displayfile/29290
    #{'VIN': 'ZACCJABH0FPB66736', 'WMI': 'ZAC', 'VDS': 'CJABH0', 'VIS': 'FPB66736',
    # 'MODEL': 'Renegade', 'MAKE': 'Jeep', 'YEAR': 2015, 'COUNTRY': 'Italy',
    # 'REGION': 'europe', 'SEQUENTIAL_NUMBER': 'B66736', 'FEWER_THAN_500_PER_YEAR': False,
    # 'nhtsa.trim': 'Latitude (US-Mex.), North(Can)', 'nhtsa.series': '',
    # 'epa.id' : '36124', 'epa.co2TailpipeGpm': '333.0', 'epa.model' : 'Renegade 2WD', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.4 L, Turbo',
    #},

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/ZAM56PPA0E1082014
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2014&make=Maserati
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2014&make=Maserati&model=Quattroporte%20GTS
    # http://www.fueleconomy.gov/ws/rest/vehicle/34100
    {'VIN': 'ZAM56PPA0E1082014', 'WMI': 'ZAM', 'VDS': '56PPA0', 'VIS': 'E1082014',
     'MODEL': 'Quattroporte', 'MAKE': 'Maserati', 'YEAR': 2014, 'COUNTRY': 'Italy',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '082014', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': '', 'nhtsa.series': 'M156',
     'epa.id' : '34100', 'epa.co2TailpipeGpm': '548.0', 'epa.model' : 'Quattroporte GTS', 'epa.trim' : 'Auto 8-spd, 8 cyl, 3.8 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/ZFBCFADH0FZ036733
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Fiat
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Fiat&model=500%20L
    # There is ambiguity, so all possibly matching epa variants for this epa model are listed:
    # http://www.fueleconomy.gov/ws/rest/vehicle/35306
    ## http://www.fueleconomy.gov/ws/rest/vehicle/35307
    {'VIN': 'ZFBCFADH0FZ036733', 'WMI': 'ZFB', 'VDS': 'CFADH0', 'VIS': 'FZ036733',
     'MODEL': '500L', 'MAKE': 'Fiat', 'YEAR': 2015, 'COUNTRY': 'Italy',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '036733', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'TREKKING', 'nhtsa.series': '',
     'epa.id' : '35306', 'epa.co2TailpipeGpm': '327.0', 'epa.model' : '500 L', 'epa.trim' : 'Auto(AM6), 4 cyl, 1.4 L, Turbo',
     #'epa.id' : '35307', 'epa.co2TailpipeGpm': '312.0', 'epa.model' : '500 L', 'epa.trim' : 'Man 6-spd, 4 cyl, 1.4 L, Turbo',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/ZFBCFXBT2GP392995
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2016&make=Fiat
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2016&make=Fiat&model=500%20X
    # http://www.fueleconomy.gov/ws/rest/vehicle/36200
    {'VIN': 'ZFBCFXBT2GP392995', 'WMI': 'ZFB', 'VDS': 'CFXBT2', 'VIS': 'GP392995',
     'MODEL': '500X', 'MAKE': 'Fiat', 'YEAR': 2016, 'COUNTRY': 'Italy',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '392995', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'EASY(US-Mex), SPORT (CAN)', 'nhtsa.series': '',
     'epa.id' : '36200', 'epa.co2TailpipeGpm': '350.0', 'epa.model' : '500 X', 'epa.trim' : 'Auto 9-spd, 4 cyl, 2.4 L',
    },

    # Breadcrumbs for how libvin/epa.py looks up the epa results:
    # https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/ZFBERFAT7F6978883
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=2015&make=Ram
    # http://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=2015&make=Ram&model=Promaster%20City
    # http://www.fueleconomy.gov/ws/rest/vehicle/35911
    {'VIN': 'ZFBERFAT7F6978883', 'WMI': 'ZFB', 'VDS': 'ERFAT7', 'VIS': 'F6978883',
     'MODEL': 'Promaster City', 'MAKE': 'Ram', 'YEAR': 2015, 'COUNTRY': 'Italy',
     'REGION': 'europe', 'SEQUENTIAL_NUMBER': '978883', 'FEWER_THAN_500_PER_YEAR': False,
     'nhtsa.trim': 'ST', 'nhtsa.series': '',
     'epa.id' : '35911', 'epa.co2TailpipeGpm': '372.0', 'epa.model' : 'Promaster City', 'epa.trim' : 'Auto 9-spd, 4 cyl, 2.4 L',
    },
]
