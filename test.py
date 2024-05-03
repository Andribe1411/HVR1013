import serial
import time
import signal
import sys
import threading
from adafruit_servokit import ServoKit  # Set channels to the number of servo channels on your kit.
from smbus import SMBus
kit = ServoKit(channels=8) # 8 servo connectors on the robot
kit.frequency = 50

distance = 30


serialPort = serial.Serial(port = "/dev/ttyS0", baudrate=38400,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

def sigint_handler(sig, frame):
    serialPort.write(b'((AR000))')
    serialPort.close()
    sys.exit(0)


def drive_forward(time_running=999999999):
    serialPort.write(b'((AF100))') #Both motors forward at 40% duty cycle
    time.sleep(time_running)
    stop()
def drive_reverse(time_running=999999999):
    serialPort.write(b'((AR100))') #Both motors forward at 40% duty cycle
    time.sleep(time_running)
    stop()

def drive_right(time_running=10):
    serialPort.write(b'((LF100))') #Both motors forward at 40% duty cycle
    serialPort.write(b'((RR100))') #Both motors forward at 40% duty cycle
    time.sleep(time_running)
    stop()

def drive_left(time_running=10):
    serialPort.write(b'((LR100))') #Both motors forward at 40% duty cycle
    serialPort.write(b'((RF100))') #Both motors forward at 40% duty cycle
    time.sleep(time_running)
    stop()

def stop():
    serialPort.write(b'((AR000))') # Stop both motors


signal.signal(signal.SIGINT, sigint_handler)

def drive():
    
    while True:
        global distance
        print(distance,"lowest")
        if distance < 20:
            stop()
            drive_reverse(0.2)
            drive_left(0.1)

        else:
            drive_forward(0.1)


def move_servo():
    while 1:
        counter = 144
        for x in range(72,144):
            kit.servo[0].angle = x  # Servo in slot 1 on robot
            kit.servo[1].angle = x  # Servo in slot 1 on robot
            time.sleep(0.01)
        for x in range(72,144):
            counter -=1
            kit.servo[0].angle = counter  # Servo in slot 1 on robot
            kit.servo[1].angle = counter  # Servo in slot 1 on robot
            time.sleep(0.01)


def find_distance():

    global distance

    i2c_bus = SMBus(1)
    i2c_address1 = 0x70
    i2c_address2 = 0x71

    while 1:
        i2c_bus.write_byte_data(i2c_address1, 0, 0x51)  # Tell sensor to scan in cm
        time.sleep(0.05)
        i2c_bus.write_byte_data(i2c_address2, 0, 0x51)  # Tell sensor to scan in cm
        time.sleep(0.05)

        high1 = i2c_bus.read_byte_data(i2c_address1, 2)  # Read the high byte of the value
        time.sleep(0.05)
        high2 = i2c_bus.read_byte_data(i2c_address2, 2)  # Read the high byte of the value
        time.sleep(0.05)
        #print(high) # print the value of High byte

        low1 = i2c_bus.read_byte_data(i2c_address1, 3)  # Read the low byte of the value
        time.sleep(0.05)
        low2 = i2c_bus.read_byte_data(i2c_address2, 3)  # Read the low byte of the value
        time.sleep(0.05)
        #print(low) # print the value of low byte

        current_value1 = high1 * 256 + low1 
        current_value2 = high2 * 256 + low2

        print(current_value1," ", current_value2)

        time.sleep(0.05)  # Sleep for some

        if current_value1 < current_value2:
            distance = current_value1
        elif current_value2 < current_value1:
            distance = current_value2




if __name__ =="__main__":
    t1 = threading.Thread(target=drive, args=())
    t2 = threading.Thread(target=move_servo, args=())
    t3 = threading.Thread(target=find_distance, args=())
 
    t1.start()
    t2.start()
    t3.start()
 
    t1.join()
    t2.join()
    t3.join()
 
    print("Done!")