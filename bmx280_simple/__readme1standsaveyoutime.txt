A. Compatible with:
	s-Sense BME280 I2C temperature, pressure and humidity sensor breakout [PN: SS-BME280#I2C, SKU: ITBP-6002], info https://itbrainpower.net/sensors/BME280-TEMPERATURE-HUMIDITY-PRESSURE-I2C-sensor-breakout 
	s-Sense BMP280 I2C temperature and pressure sensor breakout [PN: SS-BMP280#I2C, SKU: ITBP-6001], info https://itbrainpower.net/sensors/BMP280-TEMPERATURE-PRESSURE-I2C-sensor-breakout 
	all Raspberry PI, using Python 2.7



B. s-Sense sensor wiring
    Mandatory wiring [bellow for RPi B/B+/II/3B/3B+/4/Zero/Zero W]:
        - sensor Vin            <------> RPI pin 1 [3V3 power] *
        - sensor I2C SDA        <------> RPI pin 3 [i2c-1 SDA]
        - sensor I2C SCL        <------> RPI pin 5 [i2c-1 SCL]
        - sensor GND            <------> RPI pin 9 [GND]

    Wiring notes:
        *    to spare 3V3 power - read about RPI I2C sensors 5V powering

    WIRING WARNING:
        Wrong wiring may damage your RaspberryPI or your sensor! Double check what you've done.





c. How to enable i2c on RPi and install requiered python packages and other utilities.

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


    Install required python packages:
        a. sudo apt-get install python-setuptools
        b. wget https://files.pythonhosted.org/packages/6a/06/80a6928e5cbfd40c77c08e06ae9975c2a50109586ce66435bd8166ce6bb3/smbus2-0.3.0.tar.gz
        c. expand archive
        d. chdir smbus2-0.3.0
        e. sudo python setup.py install




Bellow, how to run sensor software:
	a. check / update sensors parameters in bmx280_param.py
	b. each time you edit python files, execute "sudo ./clear"
	c. python bmx280_simple.py



Enjoy!
Dragos Iosub, Bucharest 2020.
https://itbrainpower.net
