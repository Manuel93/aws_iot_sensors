# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2peyl32kymk7i-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "RaspberryPi_plant_watering"
PATH_TO_CERT = "../Downloads/094c5e9dc2-certificate.pem.crt"
PATH_TO_KEY = "../Downloads/094c5e9dc2-private.pem.key"
PATH_TO_ROOT = "../Downloads/root.pem"
MESSAGE = "Hello World"
TOPIC = "room/temperature"
RANGE = 5

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
print('Begin Publish')
for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'room/temperature'")
    t.sleep(0.1)
print('Publish End')
myAWSIoTMQTTClient.disconnect()