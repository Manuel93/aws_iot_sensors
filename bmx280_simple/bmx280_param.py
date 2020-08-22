# I2C channel used
channel = 1                                 #/dev/i2c-1

#  BME280/BMP280 defaults to address 0x76
BMx280_I2C_ADDRESS = 0x76                   #alt address 0x77



"""do not change definitions bellow"""
DevID_BMP280 = 0x58
DevID_BME280 = 0x60


#  Constants 
BMx280_TEMP_DIG_LENGTH      = 6
BMx280_PRESS_DIG_LENGTH     = 18
BMx280_HUM_DIG_ADDR1_LENGTH = 1
BMx280_HUM_DIG_ADDR2_LENGTH = 7
BMx280_DIG_LENGTH           = 32
BMx280_SENSOR_DATA_LENGTH   = 8

#  Define BMx280 Register Map
BMx280_CTRL_HUM_ADDR   = 0xF2
BMx280_CTRL_MEAS_ADDR  = 0xF4
BMx280_CONFIG_ADDR     = 0xF5
BMx280_PRESS_ADDR      = 0xF7
BMx280_TEMP_ADDR       = 0xFA
BMx280_HUM_ADDR        = 0xFD
BMx280_TEMP_DIG_ADDR   = 0x88
BMx280_PRESS_DIG_ADDR  = 0x8E
BMx280_HUM_DIG_ADDR1   = 0xA1
BMx280_HUM_DIG_ADDR2   = 0xE1
BMx280_ID_ADDR         = 0xD0

# Define sensor constants for measurements
# Mode
BMx280_Mode_Sleep  = 0
BMx280_Mode_Forced = 1
BMx280_Mode_Normal = 3
#OSR [over sample rate]
BMx280_OSRX1 =  1
BMx280_OSRX2 =  2
BMx280_OSRX4 =  3
BMx280_OSRX8 =  4
BMx280_OSRX16 = 5
#standby time
BMx280_StandbyTime_500us   = 0
BMx280_StandbyTime_62500us = 1
BMx280_StandbyTime_125ms   = 2
BMx280_StandbyTime_250ms   = 3
BMx280_StandbyTime_50ms    = 4
BMx280_StandbyTime_1000ms  = 5
BMx280_StandbyTime_10ms    = 6
BMx280_StandbyTime_20ms    = 7
#Filter
BMx280_Filter_Off = 0
BMx280_Filter_2   = 1
BMx280_Filter_4   = 2
BMx280_Filter_8   = 3
BMx280_Filter_16  = 4
