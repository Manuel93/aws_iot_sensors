"""
s-Sense BME280 by itbrainpower.net and s-Sense BME280 by itbrainpower.net I2C sensors breakout example - v1.0/20200218. 

Compatible with:
                s-Sense BME280 I2C temperature, pressure and humidity sensor breakout [PN: SS-BME280#I2C, SKU: ITBP-6002], info https://itbrainpower.net/sensors/BME280-TEMPERATURE-HUMIDITY-PRESSURE-I2C-sensor-breakout 
                s-Sense BMP280 I2C temperature and pressure sensor breakout [PN: SS-BMP280#I2C, SKU: ITBP-6001], info https://itbrainpower.net/sensors/BMP280-TEMPERATURE-PRESSURE-I2C-sensor-breakout 
		all Raspberry PI, using Python 2.7

Reading temperature, pressure [and humidity - only for BME6280] values example (pulling at 2sec) - based on Arduino BME280 library, 2016 version, written by Tyler Glenn.
Thank you Tyler! Great job! 
 
We've ported Tyler functions into python, patch them, add some variables, functions and functionalities.                


Mandatory wiring [bellow for RPi B/B+/II/3B/3B+/4/Zero/Zero W]:
        - sensor Vin            <------> RPI pin 1 [3V3 power] *
        - sensor I2C SDA        <------> RPI pin 3 [i2c-1 SDA]
        - sensor I2C SCL        <------> RPI pin 5 [i2c-1 SCL]
        - sensor GND            <------> RPI pin 9 [GND]

Wiring notes:
        *    to spare 3V3 power - read about RPI I2C sensors 5V powering

WIRING WARNING:
        Wrong wiring may damage your RaspberryPI or your sensor! Double check what you've done.


BME280 / BMP280 definitions are placed in bmx280_param.py


Bellow, how to set-up i2c on RPi and install requiered python packages and other utilities.

Enable I2C channel 1
        a. sudo raspi-config
                menu F5		=> 	enable I2C
                save, exit and reboot.
        
        
        b. edit /boot/config.txt and add/enable following directives:
               dtparam=i2c_arm=on
               dtparam=i2c_arm_baudrate=10000

           save and reboot.

Check i2c is loaded:
        run: ls /dev/*i2c*
        should return: /dev/i2c-1

Add i2c-tools packages:
        sudo apt-get install -y i2c-tools

Check sensor I2C connection:
        run: i2cdetect -y 1
        you should see listed the s-Sense BME280 / BMP280 I2C address [0x76]

Install additional python packages:
        a. sudo apt-get install python-setuptools
        b. wget https://files.pythonhosted.org/packages/6a/06/80a6928e5cbfd40c77c08e06ae9975c2a50109586ce66435bd8166ce6bb3/smbus2-0.3.0.tar.gz
        c. expand archive
        d. chdir smbus2-0.3.0
        e. sudo python setup.py install


You are legaly entitled to use this SOFTWARE ONLY IN CONJUNCTION WITH s-Sense BME280 or s-Sense BMP280 I2C sensors DEVICES USAGE. Modifications, derivates and
redistribution of this software must include unmodified this COPYRIGHT NOTICE. You can redistribute this SOFTWARE and/or modify it under the terms 
of this COPYRIGHT NOTICE. Any other usage may be permited only after written notice of Dragos Iosub / R&D Software Solutions srl.

This SOFTWARE is distributed is provide "AS IS" in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE.


itbrainpower.net invests significant time in design phase of our IoT products and in associated software and support resources.
Support us by purchasing our environmental and air quality sensors from here https://itbrainpower.net/order#s-Sense


Dragos Iosub, Bucharest 2020.
https://itbrainpower.net
"""

from time import sleep
from .bmx280 import *


#default settings       =>      BMx280_OSR_X1, BMx280_OSR_X1, BMx280_OSR_X1, BMx280_Mode_Forced, BMx280_StandbyTime_1000ms, BMx280_Filter_Off
bmx280Begin()                                                                   #start BMx280 w. default settings


#bmx280Begin()                                                                   #start BMx280 w. default settings
#bmx280SetSettings(_humOSR, _tempOSR, _presOSR, _mode, _standbyTime, _filter)    #set specific settings

while(1):
        bmx280ReadData()
        temperature = bmx280GetTemperature()
        pressure = bmx280GetPressure()
        print "Temperature: %.2f C" %temperature
        print "Pressure: %.2f Pascals" %pressure

        sensorType = bmx280GetSensorType()
        if(sensorType == DevID_BME280):
        #if(1):
                humidity = bmx280GetHumidity()
                print "Relative Humidity : %.2f %%" %humidity 
        sleep(2)
