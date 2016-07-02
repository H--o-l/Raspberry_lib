
import Xbee

Xbee = Xbee.Xbee()

board_addr = 1
dongle_addr = 0



while True:
	try :
		src,rcv = Xbee.read(src_exp = board_addr, timeout = -1)
		if rcv[len(rcv)-1] == '\n':
			print "{0} <-- {1} : {2}".format(dongle_addr, board_addr, rcv[:-1])
			
	except IOError as e:
		raise IOError("serial error : {0}".format(e))
	except TypeError:
		pass
	
	
