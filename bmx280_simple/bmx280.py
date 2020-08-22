"""
s-Sense BME280 by itbrainpower.net and s-Sense BME280 by itbrainpower.net python library v0.3 / 20200218
BME280 [temperature, pressure and humidity] and BMP280 [temperature and pressure] sensors are manufactured by Bosch Sensortec

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

from .bmx280_param import *

import smbus2 as smbus

from time import sleep


sensorType      = 0x00
m_dig = [0x00] * BMx280_DIG_LENGTH

humOSR                  = BMx280_OSRX1
tempOSR                 = BMx280_OSRX1
presOSR                 = BMx280_OSRX1
BMx280_mode             = BMx280_Mode_Forced
BMx280_standbyTime      = BMx280_StandbyTime_1000ms
BMx280_filter           = BMx280_Filter_Off

temp = 0.0
press = 0.0
hum = 0.0
        
        


def bmx280ReadNRegisters(address, length):
        global bus
        global BMx280_I2C_ADDRESS
        contents = bus.read_i2c_block_data(BMx280_I2C_ADDRESS, address, length)
        return contents


def bmx280ReadRegister(address):
        global bus
        global BMx280_I2C_ADDRESS

        contents = bus.read_i2c_block_data(BMx280_I2C_ADDRESS, address, 1)
        return contents[0]

def bmx280NWriteRegisters(address, data):
        global bus
        global BMx280_I2C_ADDRESS
        bus.write_i2c_block_data(BMx280_I2C_ADDRESS, address, data)

def bmx280WriteRegister(address, data):
        global bus
        global BMx280_I2C_ADDRESS

        bus.write_byte_data(BMx280_I2C_ADDRESS, address, data)




def bmx280WriteSettings():
        global humOSR
        global tempOSR
        global presOSR
        global BMx280_mode
        global BMx280_standbyTime
        global BMx280_filter
        
        #ctrlHum = humOSR
        ctrlHum = humOSR | 0x07        

        #ctrl_meas register. (ctrl_meas[7:5] = temperature oversampling rate, ctrl_meas[4:2] = pressure oversampling rate, ctrl_meas[1:0] = mode.)
        ctrlMeas = (tempOSR << 5) | (presOSR << 2) | BMx280_mode

        #config register. (config[7:5] = standby time, config[4:2] = filter, ctrl_meas[0] = spi enable.)
        config = (BMx280_standbyTime << 5) | (BMx280_filter << 2)
        
        bmx280WriteRegister(BMx280_CTRL_HUM_ADDR, ctrlHum)
        bmx280WriteRegister(BMx280_CTRL_MEAS_ADDR, ctrlMeas)
        bmx280WriteRegister(BMx280_CONFIG_ADDR, config)


def bmx280SetSettings(_humOSR, _tempOSR, _presOSR, _mode, _standbyTime, _filter):
        global humOSR
        global tempOSR
        global presOSR
        global BMx280_mode
        global BMx280_standbyTime
        global BMx280_filter

        humOSR = _humOSR
        tempOSR = _tempOSR
        presOSR = _presOSR
        BMx280_mode = _mode
        BMx280_standbyTime = _standbyTime
        BMx280_filter = _filter
        
        bmx280WriteSettings()


def bmx280SetDefaultSettings():                                 #set default settings
        bmx280SetSettings(BMx280_OSR_X1, BMx280_OSR_X1, BMx280_OSR_X1, BMx280_Mode_Forced, BMx280_StandbyTime_1000ms, BMx280_Filter_Off)

        

def bmx280Begin():
        global m_dig
        global temp
        global press
        global hum
        global sensorType
        global DevID_BME280
        global DevID_BMP280

        temp = 0.0
        press = 0.0
        hum = 0.0
        m_dig = [0x00] * BMx280_DIG_LENGTH


        contents = bmx280ReadRegister(BMx280_ID_ADDR)           #Hardware ID should be 0x58 or 0x60
        print("BMx280_HW_ID : 0x%02x " %contents)
 

        if (contents == DevID_BME280):                          #identify sensor type"
                sensorType = DevID_BME280
                print("BME280 found. Humidity available.")
        elif (contents == DevID_BMP280):
                sensorType = DevID_BMP280
                print("BMP280 found. No humidity available.")
        else:
                sensorType = 0
                print("BMx280 not found. Please check wiring.")
                return False

        pointer = 0
        cnt = 0

        #print "m-dig TEMP"

        lpointer = 0
        content = bmx280ReadNRegisters(BMx280_TEMP_DIG_ADDR, BMx280_TEMP_DIG_LENGTH)
        cnt += len(content)  
        while (lpointer < len(content)):
                m_dig[pointer] = content[lpointer]
                #print "m_dig [%d] : 0x%02x " %(pointer, m_dig[pointer])
                pointer += 1
                lpointer += 1
        
        #print "m-dig PRESS"
        
        lpointer = 0
        content = bmx280ReadNRegisters(BMx280_PRESS_DIG_ADDR, BMx280_PRESS_DIG_LENGTH)
        cnt += len(content)  
        while (lpointer < len(content)):
                m_dig[pointer] = content[lpointer]
                #print "m_dig [%d] : 0x%02x " %(pointer, m_dig[pointer])
                pointer += 1
                lpointer += 1
        
        #print "m-dig HUM1"

        lpointer = 0
        content = bmx280ReadNRegisters(BMx280_HUM_DIG_ADDR1, BMx280_HUM_DIG_ADDR1_LENGTH)
        cnt += len(content)  
        while (lpointer < len(content)):
                m_dig[pointer] = content[lpointer]
                #print "m_dig [%d] : 0x%02x " %(pointer, m_dig[pointer])
                pointer += 1
                lpointer += 1
        
        #print "m-dig HUM2"

        lpointer = 0
        content = bmx280ReadNRegisters(BMx280_HUM_DIG_ADDR2, BMx280_HUM_DIG_ADDR2_LENGTH)
        cnt += len(content)  
        while (lpointer < len(content)):
                m_dig[pointer] = content[lpointer]
                #print "m_dig [%d] : 0x%02x " %(pointer, m_dig[pointer])
                pointer += 1
                lpointer += 1

        if (cnt != BMx280_DIG_LENGTH):
                print("BMx280 dig registeres failed!")
                return False

        #pointer = 0
        #while (pointer < len(m_dig)):
        #        print "m_dig [%d] : 0x%02x " %(pointer, m_dig[pointer])
        #        pointer += 1


        #bmx280SetSettings(_humOSR, _tempOSR, _presOSR, _standbyTime, _filter)
        #bmx280SetDefaultSettings()                                      #set default settings

        bmx280WriteSettings()

        return 0  


        

def bmx280ReadData():
        global BMx280_mode
        global m_dig
        global temp
        global press
        global hum
        global sensorType

        error = 0

        if (BMx280_mode == BMx280_Mode_Forced):
                #print "forced mode ==> write settings"
                bmx280WriteSettings()

        data = bmx280ReadNRegisters(BMx280_PRESS_ADDR, BMx280_SENSOR_DATA_LENGTH)

        #temperature
        rawTemp   = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        
        dig_T1 = (m_dig[1] << 8) | m_dig[0]
        dig_T2 = (m_dig[3] << 8) | m_dig[2]
        dig_T3 = (m_dig[5] << 8) | m_dig[4]
        var1 = ((((rawTemp >> 3) - (dig_T1 << 1))) * (dig_T2)) >> 11
        var2 = (((((rawTemp >> 4) - (dig_T1)) * ((rawTemp >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1 + var2
        temp = (t_fine * 5 + 128) >> 8
        temp = temp / 100.0


        #pressure
        rawPressure = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

        dig_P1 = (m_dig[7]   << 8) | m_dig[6]
        dig_P2 = (m_dig[9]   << 8) | m_dig[8]
        dig_P3 = (m_dig[11] << 8) | m_dig[10]
        dig_P4 = (m_dig[13] << 8) | m_dig[12]
        dig_P5 = (m_dig[15] << 8) | m_dig[14]
        dig_P6 = (m_dig[17] << 8) | m_dig[16]
        dig_P7 = (m_dig[19] << 8) | m_dig[18]
        dig_P8 = (m_dig[21] << 8) | m_dig[20]
        dig_P9 = (m_dig[23] << 8) | m_dig[22]

        var1 = t_fine - 128000
        var2 = var1 * var1 * dig_P6
        var2 = var2 + ((var1 * dig_P5) << 17)
        var2 = var2 + (dig_P4 << 35)
        var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
        var1 = ((((1) << 47) + var1)) * (dig_P1) >> 33

        if (var1 != 0):                 #    Don't divide by zero.
                press = 1048576 - rawPressure
                press = int((((press << 31) - var2) * 3125)/var1)
                var1 = ((dig_P9) * (press >> 13) * (press >> 13)) >> 25
                var2 = ((dig_P8) * press) >> 19
                press = ((press + var1 + var2) >> 8) + ((dig_P7) << 4)

                press = (press)/256.0
        else:
                error = -2
                press = -100.0          #error
                print("pressure error - div zero")

        #humidity
        if sensorType == DevID_BME280:
        #if 1:
                rawHumidity = (data[6] << 8) | data[7]

                # Code based on calibration algorthim provided by Bosch.

                dig_H1 =   m_dig[24]
                dig_H2 = (m_dig[26] << 8) | m_dig[25]
                dig_H3 =   m_dig[27]
                dig_H4 = (m_dig[28] << 4) | (0x0F & m_dig[29])
                dig_H5 = (m_dig[30] << 4) | ((m_dig[29] >> 4) & 0x0F)
                dig_H6 =   m_dig[31]

                var1 = (t_fine - (76800))
                var1 = (((((rawHumidity << 14) - ((dig_H4) << 20) - ((dig_H5) * var1)) + (16384)) >> 15) * (((((((var1 * (dig_H6)) >> 10) * (((var1 * (dig_H3)) >> 11) + (32768))) >> 10) + (2097152)) * (dig_H2) + 8192) >> 14))

                var1 = (var1 - (((((var1 >> 15) * (var1 >> 15)) >> 7) * (dig_H1)) >> 4))
                if var1 < 0:
                        var1 = 0
                if var1 > 419430400:
                        var1 = 419430400
                hum = ((var1 >> 12))/1024.0
        else:
                hum = -100.0



def bmx280GetSensorType():
        global sensorType
        return sensorType


def bmx280GetTemperature():
        global temp
        return temp

def bmx280GetPressure():
        global press
        return press

def bmx280GetHumidity():
        global hum
        return hum


# Initialize I2C (SMBus)
try:
    configContents = bmx280ReadRegister(BMx280_ID_ADDR)
    print("I2C alredy loaded")
except:
    bus = smbus.SMBus(channel)

