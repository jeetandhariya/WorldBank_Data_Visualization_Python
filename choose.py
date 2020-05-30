import sqlite3
import csv
import json

conn = sqlite3.connect('yearwise.sqlite')
conn_1 = sqlite3.connect('indicator.sqlite')
cur = conn.cursor()
cur_1 = conn_1.cursor()

print('You can choose region from below:  \n\n')
#select and print regions from indicators.sqlite
cur_1.execute('''SELECT * FROM Regions''')
for row in cur_1:
    id = row[0]
    region = row[1]
    print(id, region)

print('\nLeave Blank and press Enter to leave the selection prompt for Regions_ID')
#choosing multiple regions
region_id_list = list()
while True:
    region_id = input('\nEnter Region_ID: ')
    if region_id == '': break
    region_id_list.append(region_id)

#making a dictionary so I can print region and region_id simultaniously
region_dict = dict()
for r in region_id_list:
    cur_1.execute('''SELECT * FROM Regions WHERE id = ?''', (r, ))
    for i in cur_1:
        region = i[1]
        region_dict[r] = region

#print(region_dict)

#select indicator and indicator_id from indicator.sqlite
cur_1.execute('''SELECT * FROM Indicators''')
for row in cur_1:
    id_1 = row[0]
    indicator = row[1]
    print(id_1, indicator)

#choosing indicator_id, only one indicator can be selected
indicator_id = input('\nEnter Indicator_ID: ')
cur_1.execute('''SELECT * FROM Indicators WHERE id = ?''', (indicator_id, ))
for i in cur_1:
    indicator = i[1]

#printing slected regions and indicator
for (r,i) in list(region_dict.items()):
    print('\nYour selected Region and ID are: ', r, i)
print('\nYour selected Indicator and ID are: ', indicator, indicator_id)

#making list of years from csv file. would like this to be generated from database itself. also want to strip 'C' from starting
with open('WDIData.csv','r') as indicator_file:
    reader = csv.reader(indicator_file)
    count = 0
    years = list()
    for row in reader:
        for i in range(4,64):
            if count == 0:
                x = row[i]
                y = 'C'
                z = y+x
                years.append(z)
        count = count +1
    #print(years)

#making a dictionary to store data
data = dict()
for yr in years:
    for r in region_id_list:
        cur.execute('SELECT * FROM %s WHERE region_id = ? AND indicator_id = ?' % yr,(r, indicator_id ))
        for i in cur:
            value_s = i[2]
            value = float(value_s)
            key = (yr, r) #(yr, r) indicates key is made of year and region_id
            data[key] = value
print(data) # data is of format {('c1960', '89'): 1.5,...}  where 1.5 is data value for respective year and region_id

#printing first line of js file
fhand = open('data.js','w')
fhand.write("datavis = [ ['Year'")
for (r,i) in list(region_dict.items()):
    fhand.write(",'"+i+"'")
fhand.write("]")

#converting None of python into null for javascript
p = None
js = json.dumps(p)

#printing rest of the lines of js file
for yr in years:
    fhand.write(",\n['"+yr+"'")
    for r in region_id_list:
        key = (yr, r)
        val = data.get(key,js) #makes val = js i.e. null if there is no data available
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

#writing html file
from string import Template
html = '''<html>
  <head>
    <script type="text/javascript" src="data.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable( datavis );

        var options = {
          interpolateNulls: true,
          title: '$i',
          chartArea: {left:'10%',top:'10%', width: '65%', height: '65%'}
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 1300px; height: 600px;"></div>
  </body>
</html>'''

#making title in line 117 variable and substituting it.
html_str = Template(html).substitute(i = indicator)
with open("data.htm", "w") as file:
    file.write(html_str)

print('html file ready')

print('JavaScript File Ready..')
