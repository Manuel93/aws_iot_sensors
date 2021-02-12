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
import Adafruit_ADS1x15
import Adafruit_BME280
import boto3
import csv

import configuration

class aws_publisher(object):
    def __init__(self):

        aws_config_file = "/configuration/aws.json"
        self.aws_config = configuration.aws_configuration(aws_config_file)

        print(self.aws_config.get_endpoint())

        # Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
        ENDPOINT = self.aws_config.get_endpoint()
        CLIENT_ID = self.aws_config.get_client_id()
        PATH_TO_CERT = self.aws_config.get_path_to_cert()
        PATH_TO_KEY = self.aws_config.get_path_to_key()
        PATH_TO_ROOT = self.aws_config.get_path_to_root()
        #MESSAGE = "Hello World"
        #TOPIC = "room/temperature"
        #RANGE = 5

        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
        self.myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
        self.myAWSIoTMQTTClient.connect()

    def send_room_sensor_data(self,user_id,datetime,temp,pressure,humidity):
        message = {"user_id":user_id,"datetime":datetime,"temperature" : temp, "pressure":pressure, "humidity":humidity}
        topic = "room/sensordata"
        self.myAWSIoTMQTTClient.publish(topic, json.dumps(message), 1) 

    def send_plant_sensor_data(self,user_id,datetime,moisture):
        message = {"user_id":user_id,"datetime":datetime,"moisture":[{"plant_1":moisture}]}
        topic = "room/sensordata"
        self.myAWSIoTMQTTClient.publish(topic, json.dumps(message), 1) 

    def send_sensor_data(self,user_id,datetime,temp,pressure,humidity,moisture):
        message = {"user_id":user_id,"datetime":datetime,"temperature" : temp, "pressure":pressure, "humidity":humidity, "moisture":[{"plant_1":moisture}]}
        topic = "room/sensordata"
        try:
            self.myAWSIoTMQTTClient.publish(topic, json.dumps(message), 1) 
        except:
            print("Exception during publishing of message to aws.")


class bmp(object):
    
    def __init__(self):
        logging.basicConfig(filename='bmp.log',level=logging.DEBUG)
        logging.info("Initializing temperature and pressure sensor bmp 280")

        self.sensor = Adafruit_BME280.BME280(t_mode=Adafruit_BME280.BME280_OSAMPLE_8, p_mode=Adafruit_BME280.BME280_OSAMPLE_8, h_mode=Adafruit_BME280.BME280_OSAMPLE_8)

        #data = self.get_data()

        self.aws_publisher = aws_publisher()

        self.loop()

    def get_time_string(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y%m%d_%H_%M_%S")
        return dt_string

    def read_temperature(self):
        temperature = self.sensor.read_temperature()
        print(temperature)
        return temperature

    def read_pressure(self):
        pressure = self.sensor.read_pressure()
        print(pressure)
        return pressure

    def read_humidity(self):
        humidity = self.sensor.read_humidity()
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
        sensor = Adafruit_BME280.BME280(t_mode=Adafruit_BME280.BME280_OSAMPLE_8, p_mode=Adafruit_BME280.BME280_OSAMPLE_8, h_mode=Adafruit_BME280.BME280_OSAMPLE_8)
        while(1):
            print("Timestamp: {0}".format(self.get_time_string()))
            degrees = sensor.read_temperature()
            pascals = sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = sensor.read_humidity()

            print('Temp      = {0:0.3f} deg C'.format(degrees))
            print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
            print('Humidity  = {0:0.2f} %'.format(humidity))

            sleep(10)

    def loop(self):
        while(1):
            #resp = self.write_to_dynamoDB(self.get_time_string(),str(self.read_temperature()),str(self.read_pressure()),str(self.read_humidity()))
            #print(resp)
            user_id = "000000001_Manuel_Belke"
            self.aws_publisher.send_room_sensor_data(user_id,self.get_time_string(),self.read_temperature(),self.read_pressure(),self.read_humidity())
            sleep(60)

class moisture(object):

    def __init__(self):
        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        self.aws_publisher = aws_publisher()

    def read_moisture(self,id):
        try:
	        value = self.adc.read_adc(id, gain=self.GAIN)
        except OSError as err:
            print("OS Error: {0}".format(err))

    def loop(self):
        while(1):
            self.read_sensor()
            user_id = "000000001_Manuel_Belke"
            self.aws_publisher.send_plant_sensor_data(user_id,self.get_time_string(),self.read_moisture(0))
            sleep(60)

class sensordata(object):

    def __init__(self):
        logging.basicConfig(filename='bmp.log',level=logging.DEBUG)
        logging.info("Initializing sensors")

        self.sensor = Adafruit_BME280.BME280(t_mode=Adafruit_BME280.BME280_OSAMPLE_8, p_mode=Adafruit_BME280.BME280_OSAMPLE_8, h_mode=Adafruit_BME280.BME280_OSAMPLE_8)

        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1

        self.aws_publisher = aws_publisher()

        self.loop()

    def get_time_string(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y%m%d_%H_%M_%S")
        return dt_string

    def read_temperature(self):
        temperature = 0
        for i in range(5):
            temperature += self.sensor.read_temperature()
        temperature /= 5
        print(temperature)
        return temperature

    def read_pressure(self):
        pressure = 0
        for i in range(5):
            pressure += self.sensor.read_pressure()
        pressure /= 5
        print(pressure)
        return pressure

    def read_humidity(self):
        humidity = 0
        for i in range(5):
            humidity += self.sensor.read_humidity()
        humidity /= 5
        print(humidity)
        return humidity

    def read_moisture(self,id):
        value = 0
        try:
            for i in range(5):
	            value += self.adc.read_adc(id, gain=self.GAIN)
            value /= 5
        except OSError as err:
            print("OS Error: {0}".format(err))

        return value

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

    def loop(self):
        while(1):
            #resp = self.write_to_dynamoDB(self.get_time_string(),str(self.read_temperature()),str(self.read_pressure()),str(self.read_humidity()))
            #print(resp)
            user_id = "000000001_Manuel_Belke"
            self.aws_publisher.send_sensor_data(user_id,self.get_time_string(),self.read_temperature(),self.read_pressure(),self.read_humidity(),self.read_moisture(0))
            sleep(60)


sensordata = sensordata()
