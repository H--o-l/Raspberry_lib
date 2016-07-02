
import Xbee
import time

Xbee = Xbee.Xbee()

board_addr = 2
com_timeout = 1




while True:

	try :
		Xbee.send("bouh", board_addr)
		print "{0} : {1} --> {2} : {3}".format("Echo", 1, board_addr, "bouh")
		
	except AssertionError as e:
		raise AssertionError("send {0} assert error : {1}".format("Echo", e)) #fatal error ...
	except IOError as e:
		raise IOError("serial error : {0}".format(e))


	
	try :
		while True:
			src,rcv = Xbee.read(src_exp = board_addr, timeout = com_timeout)
			if rcv[len(rcv)-1] == '\n':
				print "{0} : {1} <-- {2} : {3}".format("Echo", 1, board_addr, rcv[:-1])
				break
			
	except IOError:
		raise IOError("serial error : {0}".format(e))
	except TypeError:
		continue
	
	
	time.sleep(com_timeout)
