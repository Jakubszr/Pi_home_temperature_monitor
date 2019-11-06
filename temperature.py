import w1thermsensor
import w1thermsensor.errors
import time
from datetime import datetime
import pymysql.cursors
import pymysql
import Adafruit_DHT

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='PiTemperature',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# create tables to store data from sensors
with connection.cursor() as cursor:
    # create table outside_temperature if not exists
    sql = ('CREATE TABLE IF NOT EXISTS outside_temperature \
           (id int NOT NULL AUTO_INCREMENT, temperature double, \
            day date, hour time, PRIMARY KEY (id))')
    cursor.execute(sql)

    # create table inside_temperature if not exists
    sql = ('CREATE TABLE IF NOT EXISTS inside_temperature \
           (id int NOT NULL AUTO_INCREMENT, temperature double, \
            day date, hour time, PRIMARY KEY (id))')
    cursor.execute(sql)

    # create table inside_humidity if not exists
    sql = ('CREATE TABLE IF NOT EXISTS inside_humidity \
           (id int NOT NULL AUTO_INCREMENT, humidity double, \
           day date, hour time, PRIMARY KEY (id))')
    cursor.execute(sql)

# check temperature and write to database in interval
while True:

    # get date
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')

    # get hour
    hour = now.strftime('%H:%M')

    # get outside temperature from sensor
    try:
        sensor = w1thermsensor.W1ThermSensor()
        outside_temp = sensor.get_temperature()

    except w1thermsensor.errors:
        outside_temp = 'NULL'

    # get inside temperature and humidity from  sensor
    sensor = Adafruit_DHT.DHT11
    gpio = 17
    humidity, inside_temp = Adafruit_DHT.read_retry(sensor, gpio)

    # if measure is wrong, write NULL value to record
    if humidity is None:
        humidity = 'NULL'
    elif inside_temp is None:
        inside_temp = 'NULL'

    # write data to database
    try:
        with connection.cursor() as cursor:
            # write to outside_temperature table
            sql = "INSERT INTO outside_temperature VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(outside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: outside temperature:\
                {outside_temp}; date: {date}; time: {hour}")

            # write to inside_temperature table
            sql = "INSERT INTO inside_temperature VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(inside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside temperature:\
                {inside_temp}; date: {date}; time: {hour}")

            # write to inside_humidity table
            sql = "INSERT INTO inside_humidity VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(humidity), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside humidity:\
                {humidity}; date: {date}; time: {hour}")

            connection.commit()

    except Exception:
        pass

    # check temperature in interval
    time.sleep(300)

connection.close()
