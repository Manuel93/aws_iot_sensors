# Reading bmp280 sensor

import sys
import logging
import numpy as np
import time
import json
import datetime
from bmx280 import *
import boto3
import csv

class bmp(object):
    
    def __init__(self):
        logging.basicConfig(filename='bmp.log',level=logging.DEBUG)
        logging.info("Initializing temperature and pressure sensor bmp 280")

        bmx280Begin()

        #self.test()

        data = self.get_data()
        self.write_csv(data)

        self.loop()

    def get_time_string(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y%m%d_%H_%M_%S")
        return dt_string

    def read_data(self):
        bmx280ReadData()

    def read_temperature(self):
        temperature = bmx280GetTemperature()
        print(temperature)
        return temperature

    def read_pressure(self):
        pressure = bmx280GetPressure()
        print(pressure)
        return pressure

    def read_humidity(self):
        sensorType = bmx280GetSensorType()
        if(sensorType == DevID_BME280):
            humidity = bmx280GetHumidity()
            print(humidity)
        return humidity

    def write_to_dynamoDB(self,timestamp,temperature,pressure,humidity,dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('plant_watering')
        response = table.put_item(
        Item={
                'data_number': timestamp,
                'temperature': temperature,
                'pressure': pressure,
                'humidity': humidity
            }
        )
        return response

    def get_data(self, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('plant_watering')
        scan_kwargs = {
            'ProjectionExpression': "data_number, temperature, pressure, humidity"
        }

        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = table.scan(**scan_kwargs)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return response.get('Items', [])

    def write_csv(self,items):
        """
        # Python 2 
        with open('measurements.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for item in items:
                csvwriter.writerow([item['data_number'], item['temperature'], item['pressure'],item['humidity']]) """

        # Python 3
        with open('measurements.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for item in items:
                csvwriter.writerow([item['data_number'], item['temperature'], item['pressure'],item['humidity']])


    def test(self):
        while(1):
            bmx280ReadData()
            temperature = bmx280GetTemperature()
            pressure = bmx280GetPressure()
            print("Timestamp: {0}".format(self.get_time_string()))
            print("Temperature: %.2f C" %temperature)
            print("Pressure: %.2f Pascals" %pressure)

            sensorType = bmx280GetSensorType()
            if(sensorType == DevID_BME280):
            #if(1):
                    humidity = bmx280GetHumidity()
                    print("Relative Humidity : %.2f %%" %humidity)
            sleep(10)

    def loop(self):
        while(1):
            self.read_data()
            resp = self.write_to_dynamoDB(self.get_time_string(),str(self.read_temperature()),str(self.read_pressure()),str(self.read_humidity()))
            print(resp)
            sleep(10)


bmp = bmp()
