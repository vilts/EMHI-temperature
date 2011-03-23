#!/usr/bin/python
# -*- coding: utf-8                                                                                                                                                                                                                      

import httplib, re, sqlite3, sys, getopt, os
from time import gmtime, strftime

from pygooglechart import SimpleLineChart
from pygooglechart import Axis

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
dbname = 'emhi.db'

dbconn = sqlite3.connect(ROOT + dbname)
dbconn.row_factory = sqlite3.Row
print_text = 0

def main():
    global print_text
    init_db = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ihd", ["init", "help", "display"])
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-i", "--init"):
            init_db = 1
        elif o in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif o in ("-d", "--display"):
            print_text = 1

    conn = httplib.HTTPConnection('www.emhi.ee')
    conn.request("GET", "/?ide=21")
    resp = conn.getresponse()
    weather_data = resp.read()

    # Get all cities and their regexps from DB
    cur = dbconn.cursor()
    cur.execute("SELECT * FROM cities");
    for city in cur:
        current_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
        city_obj = re.search(re.compile(city["regexp"]), weather_data)
        if city_obj:
            city_temp = float(city_obj.group(1))
            if print_text:
                print u"[{0}] ({1}) {2} °C".format(current_time, city["name"], city_temp)
            if init_db:
                insert_db_temp(city["id"], city_temp)
            elif last_db_temp(city["id"]) != city_temp:
                insert_db_temp(city["id"], city_temp)
    dbconn.close()

def usage():
    print '''Usage: 
./emhi.py
./emhi.py -i [--init]    : Initialize DB with first values
./emhi.py -h [--help]    : Display this help message
./emhi.py -d [--display] : Display temperatures and other info'''

def last_db_temp(city_id):
    cur = dbconn.cursor()
    query = "SELECT temperature FROM emhi WHERE city_id = " + str(city_id) + " ORDER BY id DESC LIMIT 1"
    cur.execute(query)
    row = cur.fetchone()
    cur.close()
    return row[0]

def insert_db_temp(city_id, degC):
    cur = dbconn.cursor()
    if print_text:
        print "Inserting to DB"
    cur.execute("INSERT INTO emhi (city_id, temperature, timestamp) VALUES(" + str(city_id) + ", " + str(degC) + ", datetime('now'))")
    dbconn.commit()
    cur.close()

def simple_random():
    chart = SimpleLineChart(300, 100, y_range=(0, 100))
    max_y = 100
    list_data = [10, 90, 80, 10, 10, 20, 30, 20, 15, 45, 56, 42, 92]
    chart.add_data(list_data)
    chart.add_data(reversed(list_data))
    chart.set_axis_labels(Axis.LEFT, ['', max_y / 2, max_y])
    chart.set_axis_labels(Axis.BOTTOM, ['Sep', 'Oct', 'Nov', 'Dec'])
    chart.download('line-simple-random.png')


if __name__ == "__main__":
    main()
    # simple_random()
