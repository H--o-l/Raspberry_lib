import Xbee
import time

Xbee = Xbee.Xbee()

board_addr = 2
dongle_addr = 1




fichier = open("/home/mint/Bureau/log", "w")
start_time = time.time()

while True:
	try :
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
						fichier.write("{0}   -   {1}\n".format(rcv[:-1], int(time.time() - start_time)))

			except TypeError:
				pass	
		if not res :		
			print "Coffee machine does not respond"

	except IOError as e:
		print "Serial error, no Xbee"
		fichier.close()
		quit()
	except KeyboardInterrupt :
		print ""
		fichier.close()
		quit()
