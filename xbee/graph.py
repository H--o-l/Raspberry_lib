# import numpy as np
# from matplotlib import pyplot as plt
# import serial




# ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
# liste_char = list()

# start = 0

# plt.ion()
# # tableau = [1,1,1]
# # image = plt.imshow(tableau)

# x = list()
# y = list()

# # x.append(100000)
# # y.append(0)
# plt.plot(x,y)


# def received(string):
# 	global start
# 	if string == "start":
# 		start = 1
# 	elif start:
# 		data = string.split("-")
# 		x.append(data[1])
# 		y.append(data[0])
# 		# y[0] = data[0] * 2
# 		plt.plot(x,y,'k')
# 		plt.draw()



# while True:
# 	c = ser.read()
# 	if c == '\n':
# 		received("".join(liste_char))
# 		liste_char = []
# 	else:
# 		liste_char.append(c)


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time


ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, timeout = 0.1)

window = 10000

def data_gen():
	liste_char = list()
	print "bouh"

	try :
		while True:
			if liste_char == []:
				sendTime = time.time()
				# print "send request at {0}".format(sendTime)
				ser.write('d')
			c = ser.read()
			if c == '\n':
				# print "treat"
				received = "".join(liste_char)
				liste_char = []
				data = received.split("-")
				print data
				yield float(data[1]),float(data[0])
			elif time.time() - sendTime > 0.1:
				# print "timeout"
				liste_char = []
				continue
			else:
				liste_char.append(c)

	except KeyboardInterrupt:
		ser.write('S')
		time.sleep(0.2)
		quit()




try :

	fig = plt.figure()
	ax = fig.add_subplot(111)
	line, = ax.plot([], [], lw=2)
	ax.set_ylim(-1, 1024)
	ax.set_xlim(0, window)
	ax.grid()
	xdata, ydata = [], []
	def run(data):
	    # update the data
	    t,y = data
	    xdata.append(t)
	    ydata.append(y)
	    xmin, xmax = ax.get_xlim()

	    print data

	    if t >= xmax:
	        ax.set_xlim(xmin + window, xmax + window)
	        ax.figure.canvas.draw()
	    # elif t < xmin:
	    # 	fig.clear()
	    #     ax.set_xlim(t, t + window)
	    #     ax.figure.canvas.draw()
	    line.set_data(xdata, ydata)


	    return line,

	ser.write('s')
	ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=40,
	    repeat=False)
	plt.show()


except KeyboardInterrupt:
	ser.write('S')
	time.sleep(0.2)
	quit()
