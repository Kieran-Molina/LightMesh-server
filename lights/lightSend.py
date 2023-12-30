import serial, sys

ser = serial.Serial('/dev/ttyACM0', 115200)
ser.write((sys.argv[1]+'\n').encode())
line = ser.readline()
ser.close()
return line