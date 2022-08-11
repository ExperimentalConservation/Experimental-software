import serial
import time

arduino = serial.Serial(port = 'COM5', timeout=0)
time.sleep(2)

# while True:

#     print ("Enter '1' to turn 'on' the LED and '0' to turn LED 'off'")

#     var = str(input())
#     print ("You Entered :", var)

#     if(var == '1'):
#         arduino.write(str.encode('1'))
#         print("LED turned on")
#         time.sleep(1)

#     if(var == '0'):
#         arduino.write(str.encode('0'))
#         print("LED turned off")
#         time.sleep(1)

arduino.write(str.encode('1'))
time.sleep(5)
arduino.write(str.encode('0'))
time.sleep(5)
arduino.write(str.encode('1'))
time.sleep(5)
arduino.write(str.encode('0'))
time.sleep(5)
arduino.write(str.encode('1'))
time.sleep(5)
arduino.write(str.encode('0'))
time.sleep(5)
arduino.write(str.encode('1'))
time.sleep(5)
arduino.write(str.encode('0'))
time.sleep(5)
arduino.write(str.encode('1'))
time.sleep(5)
arduino.write(str.encode('0'))
time.sleep(5)