"""
This module implements a Stub for Xbee module
"""



import LINC.transport.Smart_board.Stub


# Xbee communication lib
import LINC.transport.Smart_board.Xbee



class ProtocolBagStub(LINC.transport.Smart_board.Stub.ProtocolBagStub):
    """
    Stub for Sensor, time stamp and actuator bag on Arduino.

    """

    def __init__(self, access_pattern):
        """
        Constructor


        **parameters**

        -acccessPattern:

        """
        LINC.transport.Smart_board.Stub.ProtocolBagStub.__init__(self, access_pattern)
        
        # Xbee drivers acces
        self.Xbee = LINC.transport.Smart_board.Xbee.Xbee()
        
        # upper stub level retry delay
        self.default_retry_delay = 0.3
        # low level commmunication timeout 
        self.com_timeout = 0.3
        
        # Trace options
        self.debug_board = True
        self.debug_stub  = True
        self.smart_board_addr = 3 
        self.stub_name = "Arduino"
        
        # address used for Xbee communication with Arduino
        self.smart_board_addr = 3 
        

        
        
    def try_send(self, args):
        """
        Implement communication protocol with Arduino based smart boards.
        Gived Data are send trought Xbee modules wireless link.
        Arduino board generate many frame as respond composed by debug traces
        and the coordination protocol reply. 
        Each arduino emmited frames is send trought XBee modules and are received one-by-one.
        How long as protocol coordination reply hasn't yet been received, debug
        trace could be print. When it's received, it is return to upper Stub level.
        It usually takes forty millesecond at Arduino to wake up and reply.
        
        An IOError is raised in usual error case. Retry should be executed at 
        upper Stub level.
        In critical error case, an AssertionError is raised but this case should
        never hapen if following conditions are met :
        - objects' name and bags' name are well defined.
        - communication protocol and encoding are the same on both sides.
        
        **parameters**

        -args: dictionary with encoded coordination protocol's call store in 
            <SString> field.
        
        **returns**
        
        Reply from Smart Board for coordinator. The reply, store in dictionary,
        should be decode by upper stub level.

        
        """   
        if self.debug_stub:
            print "{0}_stub : ------- : ".format(self.stub_name)
        

        
        # send IR wake up 
        try :
            if self.debug_stub:
                print "{0}_stub : {1} --> {2} : IR".format(self.stub_name, self.dongle_addr, self.smart_board_addr)
            self.Xbee.IR_wake_up_trought_Xbee()
            
        except IOError:
            raise IOError("send IR wake up serial error")

            

        # send the chaski cmd    
        try :
            self.Xbee.send(args['SString'], self.smart_board_addr)
            if self.debug_stub :
                print "{0}_stub : {1} --> {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr, args['SString'])
                
        except AssertionError as e:
            raise AssertionError("send {0} assert error : {1}".format(self.stub_name, e)) #fatal error ...
        except IOError:
            raise IOError("{0} serial error".format(self.stub_name))
            

            
        # wait for cmd reply with "return" ident. Treat debug reply. 
        try :
            while True:
                src,rcv = self.Xbee.read(src_exp = self.smart_board_addr, timeout = self.com_timeout)
                if rcv[len(rcv)-1] == '\n' and self.debug_board:
                     print "{0}_stub : {1} <-- {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr, rcv[:-1])
                if rcv[:5] == "reply":
                    reply = rcv[6:-1]
                    break
                    
        except IOError:
            raise IOError("{0} serial error".format(self.stub_name))
        except TypeError:
	    self.Xbee.flushInput()      
	    self.Xbee.flushOutput()      
	    raise IOError("received {0} timeout error".format(self.stub_name))
     
            
        
        return {'error':None, 'reply':reply, 'op':args['op']}
            
        

        
if __name__ == '__main__':
    pass

    
    
    #old try_send function is bellong. It implement a more stringent (synchronous) protocol which 
    # wait for "wake up" information before send data and block if "go sleep" information is received
    # before coordination protocol reply.
    # This protocole suffer from virtual errors. I supposed that is due to Xbee transmit and/or received buffers.
    
    
    
    #old

    #def try_send(self, args):
        #"""
        #Implement communication protocol with smart board. return error if primitive call don't go well.
        #Takes around 40ms with arduino based smart board.
        #If the board isn't, 200ms timeout will unlock the sending.
        
        #**parameters**

        #-args: dictionary with full sending parameters and data.
        
        #"""   
        #if self.debug_stub:
            #print "{0}_stub : ------- : ".format(self.stub_name)
        

        
        ## send IR wake up 
        #try :
            #if self.debug_stub:
                #print "{0}_stub : {1} --> {2} : IR".format(self.stub_name, self.dongle_addr, self.smart_board_addr)
            #LINC.transport.Smart_board.Xbee.IR_wake_up()
        ##except AssertionError as e:
            ##return {'error':"send IR wake up assert error" + str(e), 'reply':None, 'op':'ERROR'}
        #except IOError:
            #raise IOError("send IR wake up serial error")

            
            
        ## wait for "wake up" from the sensor. Also treat debug reply. 100ms timeout. If timeout raise it could mean that the sensor was already awake.
        ##try :
            ##while True:
                ##src,rcv = LINC.transport.Smart_board.Xbee.read(src_exp = self.smart_board_addr, timeout = 0)
                ##if rcv[len(rcv)-1] == '\n' and self.debug_board:
                         ##print "{0}_stub : {1} <-- {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr,rcv[:-1])
                ##if rcv[:7] == "wake up":
                        ##if self.debug_stub:
                             ##print "{0}_stub : {1}       : IR wake up ok, my turn to speak".format(self.stub_name, self.dongle_addr)
                        ##break
                ##continue
        ##except TypeError:
            ##if self.debug_stub:
                 ##print "{0}_stub : {1}       : IR no respond, try to speak".format(self.stub_name, self.dongle_addr)
        ##except IOError:
            ##raise IOError("IR wake up serial error")

            
            
        ## send the chaski cmd    
        #try :
            #LINC.transport.Smart_board.Xbee.send(args['SString'], self.smart_board_addr)
            #if self.debug_stub :
                #print "{0}_stub : {1} --> {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr, args['SString'])
        #except AssertionError as e:
            #raise AssertionError("send {0} assert error : {1}".format(self.stub_name, e)) #fatal error ...
        #except IOError:
            #raise IOError("{0} serial error".format(self.stub_name))
            
        ##LINC.transport.Smart_board.Xbee.flushInput()            
            

        ## wait for cmd reply with "return" ident. Treat debug reply. Early "go sleep" reply mean board detect an assert error.100s timeout mean board never answer.
        #try :
            #while True:
                #src,rcv = LINC.transport.Smart_board.Xbee.read(src_exp = self.smart_board_addr, timeout = self.com_timeout)
                #if rcv[len(rcv)-1] == '\n' and self.debug_board:
                     #print "{0}_stub : {1} <-- {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr, rcv[:-1])
                ##if rcv[:8] == "go sleep":
                    ##raise AssertionError("Sensor go sleep without treat the cmd, see sensor debug for intel")
                #elif rcv[:5] == "reply":
                    #reply = rcv[6:-1]
                    #break
        #except IOError:
            #raise IOError("{0} serial error".format(self.stub_name))
        #except TypeError:
            #LINC.transport.Smart_board.Xbee.flushInput()      
            #LINC.transport.Smart_board.Xbee.flushOutput()      
            #raise IOError("received {0} timeout error".format(self.stub_name))
     
            
        ## clear last debug reply until go sleep received or timeout. Reply had already been received -> ignore new errors
        ##try :
            ##while True:
                ##src,rcv = LINC.transport.Smart_board.Xbee.read(src_exp = self.smart_board_addr, timeout = 0.1)
                ##if rcv[len(rcv)-1] == '\n' and self.debug_board:
                     ##print "{0}_stub : {1} <-- {2} : {3}".format(self.stub_name, self.dongle_addr, self.smart_board_addr, rcv[:-1])
                ##if rcv == "go sleep\n":
                    ##break
        ##except TypeError:
            ##pass
        ##except IOError:
            ##pass

        ## finally, if we go thus far it's mean that everything went well and that we have the sensor return in reply string
        
        
        #return {'error':None, 'reply':reply, 'op':args['op']}
            
    #def get_assume_board_power_state(self):
        #return False


    
    