#!/usr/bin/python                                                                                                                                                                                                                                     
# -*- coding: utf-8                                                                                                                                                                                                                                 
import httplib, re, sqlite3, sys
from time import gmtime, strftime

if sys.argv[1] == 'init':
    print "Init indeed"
    sys.exit()

filepath = '/home/vilts/devel/EMHI-temperature/'
dbname = 'emhi.db'

dbconn = sqlite3.connect(filepath + dbname)
dbconn.row_factory = sqlite3.Row

def last_db_temp():
    cur = dbconn.cursor()
    cur.execute('''SELECT temperature FROM emhi ORDER BY id DESC LIMIT 1''')
    row = cur.fetchone()
    cur.close()
    return row[0]

def insert_db_temp(degC):
    cur = dbconn.cursor()
    print "Inserting to DB"
    cur.execute("INSERT INTO emhi VALUES(NULL, " + str(degC) + ", datetime('now'))")
    dbconn.commit()
    cur.close()

conn = httplib.HTTPConnection('www.emhi.ee')
conn.request("GET", "/?ide=21")
resp = conn.getresponse()
weather_data = resp.read()

# Get all cities and their regexps from DB
cur = dbconn.cursor()
cur.execute("SELECT * FROM cities");
for row in cur:
    current_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
    pattern = re.compile(row["regexp"])
    city_obj = re.search(pattern, weather_data)
    city_temp = float(city_obj.group(1))
    print u"[{0}] ({1}) {2} °C".format(current_time, row["name"], city_temp)

# old_temp = last_db_temp()

#if old_temp != degC:
#    print "Inserting new temp to DB: " + str(degC)
#    insert_db_temp(degC)
#else:
#    print "Old temp matches current: " + str(old_temp) + " = " + str(degC)

dbconn.close()
