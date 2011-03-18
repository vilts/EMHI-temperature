#!/usr/bin/python                                                                                                                                                                                                                                     
# -*- coding: utf-8                                                                                                                                                                                                                                   

import httplib
import re
from time import gmtime, strftime
import sqlite3

filepath = '/home/vilts/'
logfile_name = 'emhi_temp.log'
tempfile_name = 'emhi_temp.txt'
dbname = 'emhi.db'

dbconn = sqlite3.connect(filepath + dbname)

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
conn.request("GET", "/")
resp = conn.getresponse()
weather_data = resp.read()

matchObj = re.search( r'<div style="position: absolute; left: 179px; top: 62px; width:37px; height:11px; color:#FFFFFF; background-color:#003399; text-align: center;" class="mintavatext">(-?\d+\.?\d+).?C</div>', weather_data, re.M)
degC = float(matchObj.group(1))

if matchObj:
    current_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
    print "[{0}]: {1}".format(current_time, degC)
else:
    print "Didn't find temperature in web page."

old_temp = last_db_temp()

if old_temp != degC:
    print "Inserting new temp to DB: " + str(degC)
    insert_db_temp(degC)
else:
    print "Old temp matches current: " + str(old_temp) + " = " + str(degC)

dbconn.close()
