# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import sys
import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import logging
import numpy as np
import datetime
from bmx280_simple import *
import boto3
import csv

class aws_publisher(object):
    def __init__(self):
        # Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
        ENDPOINT = "a2peyl32kymk7i-ats.iot.eu-central-1.amazonaws.com"
        CLIENT_ID = "RaspberryPi_plant_watering"
        PATH_TO_CERT = "../Downloads/094c5e9dc2-certificate.pem.crt"
        PATH_TO_KEY = "../Downloads/094c5e9dc2-private.pem.key"
        PATH_TO_ROOT = "../Downloads/root.pem"
        #MESSAGE = "Hello World"
        #TOPIC = "room/temperature"
        #RANGE = 5

        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
        self.myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
        self.myAWSIoTMQTTClient.connect()

    def send_sensor_data(self,temp,pressure,humidity):
        message = {"temperature [\N{DEGREE SIGN}C]" : temp, "pressure [Pa]":pressure, "humidity [%]":humidity}
        topic = "room/sensordata"
        self.myAWSIoTMQTTClient.publish(topic, json.dumps(message), 1) 


class bmp(object):
    
    def __init__(self):
        logging.basicConfig(filename='bmp.log',level=logging.DEBUG)
        logging.info("Initializing temperature and pressure sensor bmp 280")

        bmx280Begin()

        #data = self.get_data()

        self.aws_publisher = aws_publisher()

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
            #resp = self.write_to_dynamoDB(self.get_time_string(),str(self.read_temperature()),str(self.read_pressure()),str(self.read_humidity()))
            #print(resp)
            self.aws_publisher.send_sensor_data(self.read_temperature(),self.read_pressure(),self.read_humidity())
            sleep(10)


bmp = bmp()
