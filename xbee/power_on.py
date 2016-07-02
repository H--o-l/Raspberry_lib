import Xbee
import time

Xbee = Xbee.Xbee()

board_addr = 2

cmd = "ON"

try :
	Xbee.send(cmd, board_addr)
	print "{0} : {1} --> {2} : {3}".format("Coffee_cmd", 1, board_addr, cmd)
	
except AssertionError as e:
	raise AssertionError("send {0} assert error : {1}".format("Echo", e)) #fatal error ...
except IOError as e:
	raise IOError("serial error : {0}".format(e))
