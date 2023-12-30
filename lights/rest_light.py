from flask import Flask, request, jsonify
import serial, sys, json, os

app = Flask(__name__)

def isValidJson(j):
	if len(j) == 0:
		return False
	try:
		json.loads(j)
	except ValueError as e:
		return False
	return True

def resetUsb():
	print('trying to restart usb device')
	os.system("sudo sh ~/lights/resetUsbEsp32.sh")

@app.route('/lightsend', methods=["POST"])
def home():
	tries = 3
	success = False
	toSend = request.json['send']
	print (toSend)

	while (not success) and tries > 0:
		print ('tries left', tries)
		try:
			ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 2)
			ser.write((json.dumps(toSend)+'\n').encode())
			line = ser.readline().decode()
			ser.close()
			success = isValidJson(line)
		except:
			if tries > 1:
				resetUsb()
			else:
				return '{"status": 444, "message": "Could not communicate with USB device"}', 444
		tries -=1

	if success:
		result = '{"status": 200, "message": ' + line + '}'
		resultCode = 200
	else:
		result = '{"status": 445, "message": "No response from USB device. If issue persists, try a hard reset"}'
		resultCode = 445
		resetUsb()
	result2 = ''.join(result.splitlines())
	print(result2)
	return result2 + '\n                     \n', resultCode


if __name__ == '__main__':
	app.run(host='::', port=5005)