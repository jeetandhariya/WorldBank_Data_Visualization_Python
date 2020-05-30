import csv
import sqlite3

with open('WDIData.csv','r') as indicator_file:
    reader = csv.reader(indicator_file)
    count = 0
    years = list()
    for row in reader:
        for i in range(4,64):
            if count == 0:
                x = row[i]
                y = 'C' #sqlite didnt accept only an integer value i.e.1960 as a column header or a table name, had to add an alphabetic character.
                z = y+x
                years.append(z)
        count = count +1
    print(years)

conn = sqlite3.connect('yearwise.sqlite')
conn_1 = sqlite3.connect('indicator.sqlite')
cur = conn.cursor()
cur_1 = conn_1.cursor()

column_id = 4 #starting with 1960 column in the csv file.
for yr in years:

    cur.execute("CREATE TABLE IF NOT EXISTS %s (region_id INTEGER, indicator_id INTEGER, %s INTEGER)" % (yr,yr)) # %s is a string placeholder.

    with open('WDIData.csv','r') as indicator_file:
        reader = csv.reader(indicator_file)
        count = 0
        for row in reader:
            if row[column_id] == '':continue #skip if there is no value in the year column in csv file.
            region_id = 0
            indicator_id = 0
            value = row[column_id]
            region = row[0]
            indicator = row[2]
            if count<10:
                print(region, value, indicator)
            cur_1.execute('''SELECT id FROM Regions WHERE regions = ?''', (region, )) #connecting with indicator.sqlite
            for i in cur_1:
                region_id = i[0]
                #print(region_id)
            cur_1.execute('''SELECT id FROM Indicators WHERE indicators = ?''', (indicator, ))
            for i in cur_1:
                indicator_id = i[0]
            if count > 0:
                cur.execute('INSERT OR IGNORE INTO %s (region_id, indicator_id, %s) VALUES ( ?, ?, ?)' % (yr,yr),(region_id, indicator_id, value))
            if count%1000 == 0:
                conn.commit()
            count = count + 1
        conn.commit()
        print(count)
    print(column_id)
    column_id = column_id + 1
