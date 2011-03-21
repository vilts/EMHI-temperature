#!/usr/bin/python                                                                                                                                                                                                                                     
# -*- coding: utf-8                                                                                                                                                                                                                                 
import httplib, re, sqlite3, sys, getopt
from time import gmtime, strftime

filepath = '/home/vilts/devel/EMHI-temperature/'
dbname = 'emhi.db'

dbconn = sqlite3.connect(filepath + dbname)
dbconn.row_factory = sqlite3.Row
init_db = 0

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    conn = httplib.HTTPConnection('www.emhi.ee')
    conn.request("GET", "/?ide=21")
    resp = conn.getresponse()
    weather_data = resp.read()

    # Get all cities and their regexps from DB
    cur = dbconn.cursor()
    cur.execute("SELECT * FROM cities");
    for city in cur:
        current_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
        pattern = re.compile(city["regexp"])
        city_obj = re.search(pattern, weather_data)
        city_temp = float(city_obj.group(1))
        print u"[{0}] ({1}) {2} °C".format(current_time, city["name"], city_temp)
        if init_db:
            insert_db_temp(city["id"], city_temp)

# old_temp = last_db_temp()
            
#if old_temp != degC:
#    print "Inserting new temp to DB: " + str(degC)
#    insert_db_temp(degC)
#else:
#    print "Old temp matches current: " + str(old_temp) + " = " + str(degC)

dbconn.close()


def last_db_temp():
    cur = dbconn.cursor()
    cur.execute('''SELECT temperature FROM emhi ORDER BY id DESC LIMIT 1''')
    row = cur.fetchone()
    cur.close()
    return row[0]

def insert_db_temp(city_id, degC):
    cur = dbconn.cursor()
    print "Inserting to DB"
    cur.execute("INSERT INTO emhi (city_id, temperature, timestamp) VALUES(" + str(city_id) + ", " + str(degC) + ", datetime('now'))")
    dbconn.commit()
    cur.close()

if __name__ == "__main__":
    main()
