import sqlite3
import serial
import time
import platform

#
con = sqlite3.connect('Test Database.db')
cur = con.cursor()
# Create table Scheme-MESSDATA
#
# Table names cannot be passed to parameters You will have to hard code them

cur.execute('''CREATE TABLE IF NOT EXISTS Main_Sensors
                (MESSID TEXT NOT NULL,gps_date TEXT NOT NULL,latitude REAL NOT NULL ,longitude REAL NOT NULL,alt REAL NOT NULL,actual_date TEXT NOT NULL,standard_pm1_0 INTEGER,standard_pm2_5 REAL,standard_pm10 REAL,atmospheric_pm1_0 REAL,atmospheric_pm2_5 REAL,atmospheric_pm10 REAL ,pm1_gt_3 REAL,pm1_gt_5 REAL,pm1_gt_10 REAL,pm1_gt_25 REAL,pm1_gt_50 REAL,pm1_gt_100 REAL,Temperature REAL, Humidity NUB,Pressure REAL ,Voc NUB)''')
con.commit()

# What System is this? Serial Port Identification
if platform == "linux" or platform == "linux2":
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
    )
else:
    ser = serial.Serial(
        port='COM3',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

while True:
    try:
        ser.flushInput()
        podDdataIn: bytes = ser.readline()
        print(podDdataIn)
        if podDdataIn[:9] == "MESSKIT0R":
            print(podDdataIn)
        if podDdataIn[:9] == "MESSKIT02":
            print(podDdataIn)
        cur.execute(
            '''INSERT INTO Main_Sensors (MESSID ,gps_date ,latitude,longitude,alt ,actual_date ,standard_pm1_0,standard_pm2_5,standard_pm10,atmospheric_pm1_0,atmospheric_pm2_5,atmospheric_pm10,pm1_gt_3,pm1_gt_5,pm1_gt_10,pm1_gt_25,pm1_gt_50 ,pm1_gt_100,Temperature, Humidity,Pressure,Voc) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')
        con.commit()
        time.sleep(1)
        ser.flushInput()
        ser.write(podDdataIn)
    except KeyboardInterrupt:
        ser.close()
        break
con.commit()
#
con.close()
