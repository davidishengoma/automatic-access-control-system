import serial
import time

arduino = None

try:
    arduino = serial.Serial(port='COM11', baudrate=9600, timeout=.1)
except:
    pass

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def open_door(flag: str):
    
    flag = str(flag)
    
    if arduino is not None:
        try:
            value = write_read(flag)
            print(f"log: {value}")
        except:
            print("Door System not connected")
            
        
        arduino.close()

# input = "1"
# open_door(input)

input = input('code: ')
open_door(input)