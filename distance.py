import smbus # sudo apt-get install python-smbus
import datetime
import time
import serial
import signal
import sys
ADDRESS = 0x70 # i2c device address, https://www.dfrobot.com/wiki/index.php/SRF02_Ultrasonic_sensor_(SKU:SEN0005)

bus = smbus.SMBus(1)
dist_lpf = 0.0
serialPort = serial.Serial(port = "/dev/ttyS0", baudrate=38400,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
def turn(degrees):
    TIME_RUNNING=degrees*0.01444444444
    serialPort.write(b'((RF100))')
    serialPort.write(b'((LF100))')
    time.sleep(TIME_RUNNING)

# loop
while True:
    # initialize sensor to measure in centimeters
    bus.write_byte_data(ADDRESS, 0x00, 0x51)
    time.sleep(0.07) # wait around 65 ms
    # read distance
    data = bus.read_i2c_block_data(ADDRESS, 0x02, 2)
    dist_raw = ((data[0] << 8) |  data[1]) # raw data
    dist_lpf = (dist_lpf * 0.8) + (dist_raw * 0.2) # low pass filter
    # grab time stamp
    dt = datetime.datetime.now()
    if dist_raw <=100:
        turn(90)
    time.sleep(0.01) # 10hz