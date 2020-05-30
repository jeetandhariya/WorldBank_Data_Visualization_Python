# WorldBank_Data_Visualization_Python
 World Bank Data visualization using python and SQLite Database

 Hello All!

 This is my first project using python(or any language) that I have uploaded to github.(First ever project on github as well!!)
 I made this project after a cousrse specialization on python by University of Michigan on Coursera as part of its Capstone Project. It was my stepping stone to learning python.

 I have worked on Data Visualization on World Bank Data Indicators. You can find the csv file here: https://datacatalog.worldbank.org/dataset/world-development-indicators. YOU WILL NEED WDIData.csv from the zip file of csv downloaded from this location. SO, COPY THIS FILE AND ALL THE FILES in repository IN YOUR DIRECTORY.

 WDIData.csv file has data from 1960 to 2019 for 264 different regions such as Arab World, India, the US, etc for 1429 different indicators such as GDP, population etc.

 I decided to make a database from this csv file so that data can be properly managed. I made an SQLite file for regions and indicators separately. So it had two tables for regions and indicators in which I stored regions and indicators giving them Primary Keys.

 So, FIRST STEP is to run indicators.py. This would create indicator.sqlite database from WDIData.csv

 For data ranging from 1960 to 2019, I made another SQLite file. I pondered a lot about how to store this data. This was the first time I am actually making a database, so suggestions are welcomed. I made different tables for each year's data. So this file has a total of 60 tables. Each table has foreign keys for Regions and Indicators and data for that respective year only for which data is available in the csv file. I am not sure this is the most efficient way to store data.

 So, 2nd STEP is to run yearwise.py. This would generate yearwise.sqlite database.

For, visualization I have made 'choose.py'. You can choose any number of regions for any ONE particular indicator. It will make data.js file which will have array of data for regions and indicator selected. This javascript file is used in data.htm file which uses googlejsapi to visualize data.

So, 3rd STEP is to run choose.py. This would prompt you to select no. of regions and one indicator. This would also make data.js and data.htm file. You can open data.htm file in browser and visualize data.

Any suggestions are most welcome.
