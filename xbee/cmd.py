import Xbee_raspberry as Xbee
import time

Xbee = Xbee.Xbee()

board_addr = 2
dongle_addr = 1



try :

	Xbee.check_serial()

	while True:
			res = False
			cmd = raw_input("{0} --> {1} : ".format(dongle_addr, board_addr))
			Xbee.send(cmd, board_addr)

			delayRef = time.time()
			delay = 0.5
			while time.time() < delayRef + delay:
				try :
					src,rcv = Xbee.read(src_exp = board_addr, timeout = 0.1)

					if rcv[len(rcv)-1] == '\n':
						delayRef = time.time()
						res = True
						delay = 0.2

						if rcv != "ack\n":
							print "{0} <-- {1} : {2}".format(dongle_addr, board_addr, rcv[:-1])

				except TypeError:
					pass	
			if not res :		
				print "Coffee machine does not respond"

except IOError as e:
	print e
	#print "Serial error, no Xbee"
	print "Be sure you have root privilege"
	quit()
except KeyboardInterrupt :
	print ""
	quit()
