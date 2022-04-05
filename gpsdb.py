import time
import serial
import RPi.GPIO as gpio
import re
import math
import mysql.connector
from haversine import haversine
from datetime import date, datetime, timedelta

gpio.setmode(gpio.BOARD)

port = "/dev/ttyACM0" #serial port to which the pi is connected

ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "pi",
    passwd = "irs5540",
    database = "mysql"
)
def get_gpsBus():
    mycursor = mydb.cursor()
    lat = ''
    lon = ''
    count = 0
    while True:
        try:
            data1 = ser.readline().decode('utf-8', errors = 'replace')
            data2 = str(data1)
        except:
            print("no detected")
        if data2.find("$GPGGA") != -1:
            loc = re.search('(.+),(.+),(.+),N,(.+),E',data2)

            lat = float(loc.group(3))
            lon = float(loc.group(4))
            ts = time.strftime('%Y-%m-%d %H:%M:%S')

            lat1 = math.floor(lat/100)
            lon1 = math.floor(lon/100)

            lat2 = ((lat/100)-lat1)*100/60
            lon2 = ((lon/100)-lon1)*100/60

            lat = str(lat1+lat2)
            lon = str(lon1+lon2)
            print("Location: "+lat+","+lon+","+ts)
            time.sleep(1)
            mycursor.execute("insert into gps_data(latitude, longitude) values(%s, %s)", (float(lat), float(lon)))
            mydb.commit()
            

get_gpsBus()

