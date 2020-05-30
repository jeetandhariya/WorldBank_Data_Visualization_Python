#scrapping csv
import csv
import sqlite3


conn = sqlite3.connect('indicator.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Indicators''')
cur.execute('''DROP TABLE IF EXISTS Regions''')
cur.execute('''DROP TABLE IF EXISTS Ids''')

cur.execute('''CREATE TABLE IF NOT EXISTS Indicators
    (id INTEGER PRIMARY KEY, indicators TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Regions
    (id INTEGER PRIMARY KEY, regions TEXT UNIQUE, region_id TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Ids
    (region_id INTEGER, indicator_id INTEGER)''')

#making a separate list of both regions and indicators
with open('WDIData.csv','r') as indicator_file:
    reader = csv.reader(indicator_file)
    count = 0
    for row in reader:
        value_ind = row[2]
        if count>0:
            cur.execute('INSERT OR IGNORE INTO Indicators (indicators) VALUES ( ? )', ( value_ind, ) )
        if count%10000 == 1:
            print(value_ind)
            conn.commit()
        region = row[0]
        region_id = row[1]
        if count>0:
            cur.execute('INSERT OR IGNORE INTO Regions (regions,region_id) VALUES ( ?, ? )', ( region, region_id ) )
        count = count + 1
    print('Total rows:', count)
    conn.commit()

cur.execute('''SELECT id, indicators FROM Indicators''')
indicators = dict()
for row in cur:
    indicators[row[0]] = row[1]
#print(indicators)
cur.execute('''SELECT id, regions FROM Regions''')
regions = dict()
for row in cur:
    regions[row[0]] = row[1]
#print(regions)

#making a region_id indicator_id many to many table(for refernce only. turns out dont really need one.)
with open('WDIData.csv','r') as indicator_file:
    reader = csv.reader(indicator_file)
    j = 0
    i = 0
    count = 0
    yr = list()
    for row in reader:
        for key in indicators:
            if row[2] == indicators[key]:
                i = key
        for key in regions:
            if row[0] == regions[key]:
                j = key
        if count>0:
            cur.execute('INSERT OR IGNORE INTO Ids (region_id, indicator_id) VALUES ( ?, ? )', ( j, i ) )

        count = count + 1
    conn.commit()
    print('====END====')
