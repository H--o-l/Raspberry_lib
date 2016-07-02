
import serial



ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
liste_char = list()

while True:
	c = ser.read()
	if c == '\n':
		print "".join(liste_char)
		liste_char = []
	else:
		liste_char.append(c)

		
		