#!/usr/bin/python                                                                                                                                                                                                                                     
# -*- coding: utf-8                                                                                                                                                                                                                                 
import httplib
import re
from time import gmtime, strftime
import sqlite3

filepath = '/home/vilts/devel/EMHI-temperature/'
logfile_name = 'emhi_temp.log'
tempfile_name = 'emhi_temp.txt'
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
    pattern = re.compile(row["regexp"])
    city_obj = re.search(pattern, weather_data)
    city_temp = float(city_obj.group(1))
    print u"[{0}] {1}".format(row["name"], city_temp)

tallinn_obj = re.search( r'<div style="position: absolute; left: 247px; top: 82px; width:70px; height:13px; color:#993300;" class="kaarditekst">(-?\d+\.?\d+)</div>', weather_data)
tallinn_temp = float(tallinn_obj.group(1))

tyri_obj = re.search( r'<div style="position: absolute; left: 322px; top: 187px; width:70px; height:13px; color:#993300;" class="kaarditekst">(-?\d+\.?\d+)</div>', weather_data)
tyri_temp = float(tyri_obj.group(1))

if tallinn_obj and tyri_obj:
    current_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
    print "[{0}]: {1}".format(current_time, tallinn_temp)
    print "[{0}]: {1}".format(current_time, tyri_temp)
else:
    print "Didn't find temperature in web page."

# old_temp = last_db_temp()

#if old_temp != degC:
#    print "Inserting new temp to DB: " + str(degC)
#    insert_db_temp(degC)
#else:
#    print "Old temp matches current: " + str(old_temp) + " = " + str(degC)

dbconn.close()
