"""
This module implements drivers for Xbee serie one wireless modules.
Xbee modules should be configure first (network ID, modules ID and 
serial link baudrate). Communications with the module choosed as 
sensor network passerel is done trought USB link using serial interface
offered by pySerial lib. This module should have "1" as ID and 
"115200" as baudrate.
"""
import serial
import time


                                        
def add_checksum(frame):
    """
    Calculated a new checksum based on given frame.
    The result is store in the last field of the frame.
    
    **parameters**
    
    Initial frame
    
    **returns**
    
    Same frame with checksum in the last field
    
    """    
    add = 0x00
    for i in range (3,3+frame[2]):
        add += frame[i] 
    frame[frame[2]+3] = (0xFF - add) & 0xFF
    return frame

        


class Xbee :
    
    """
    Xbee class. Use a serial object.

    """        
    
    def __init__(self):
        """
        Constructor. 
        Could be used to configure serial Link.

        """
        self.serial = serial.Serial()
        
        self.serial.baudrate = 38400 #111111   # Xbee communication link is closer of 111111baud than 115200baud
                                        # due to his clock and PLL. In strict 115200baud computer configuration
                                        # frame are regularly lost. 
                                        
        self.serial.port =     '/dev/ttyAMA0'
        
        self.serial.timeout =  0.1      # 100ms default timeout for pySerial call

                
    def open_serial(self):
        """
        Try to open serial link with self parameters.
        Rise IOError if field.
        """
        try: 
            self.serial.open()
        except serial.serialutil.SerialException:
            raise IOError('Error open Xbee serial, cannot go further')

                        
    def try_open(self):
        """
        Test if serial link is open and open it if not.
        Return final serial link state.
        This function is used in chaski object definition 
        to obtain dongle statu.
        
        **returns**
        serial link state
        
        """       
        if self.serial.isOpen():
            return True
        else :
            try:
                self.open_serial()
            except IOError:
                return False
            else:
                return True
   
   
    def check_serial(self):
        """
        Test if serial link is open and if wanted baudrate
        si used. 
        This function is used at each driver call to force
        serial link in xbee particular configuration in case
        the serial link is used for two different devices
        (IR and Xbee ?).
        
        """       
        if not self.serial.isOpen() or self.serial.baudrate != 111111:
            if self.serial.isOpen():
                self.serial.close()
            self.open_serial()      # default config -> baudrate set at 111111
                
                
                
    def flushInput(self):
        """
        Flush pySerial input buffer (remove any data on it).        
        """      
        self.check_serial()
        self.serial.flushInput()

                
                
    def flushOutput(self):
        """
        Flush pySerial Output buffer (send data immediately).        
        """      
        self.check_serial()
        self.serial.flushOutput()
                
 
 
    def IR_wake_up_trought_Xbee(self):
        """
        Use serial link with Xbee to trig infrared led.
        38KHz needed infrared signal is obtain thanks a
        sequence of one hundred 0xAA characters transmit
        at 111111baud.
        
        """
        self.check_serial()

        frame = bytearray(100)    
        for i in range(100):
            frame[i] = 0xAA
            
        try :
            self.serial.write(str(frame))
            self.serial.flushInput()
            self.serial.flushOutput()
            
        except OSError as e:  # bug fix python before 2.7
            raise IOError(e)

        
        
    def send(self, data, dest = 0xFFFF):
        """
        Send data thanks Xbee module. Data to send are packet in a new Xbee<->host 
        protocole commnication frame. Then, the frame is send to hosted Xbee module
        thanks pySerial <write> function. Ending frame checksum is build thanks
        <add_checksum> function.
        
        """
        self.check_serial()

        string_lenght = len(data)
        assert string_lenght <= 100                     # max data size
        assert dest <= 0xFFFF                           # 16bits addr max
        frame = bytearray(string_lenght + 9)
        frame[0] = 0x7E                                 # start ident
        frame[1] = 0x00                                 # taille de la frame MSB
        frame[2] = string_lenght + 5                    # taille de la frame LSB 
        frame[3] = 0x01                                 # API TX addr 16bits ident
        frame[4] = 0x00                                 # UART Ack disable
        frame[5] = dest >> 8                            # dest MSB
        frame[6] = dest & 0xFF                          # dest LSB
        frame[7] = 0x00                                 # Options
        for i in range(string_lenght) :
            frame[8+i] = ord(data[i])                   # data
        try :
            self.serial.write(str(add_checksum(frame))) # checksum
     
        except OSError as e:                            # bug fix python before 2.7
            raise IOError(e)

                
    def read_frame_NB(self):  # default 0.1 ms timeout
        """
        Look for new frame in serial link received buffer and try 
        to decode it as it came from hosted Xbee module.
        One hundred millisecond timeout is used to acheived 
        non blocking behaviour.
        If no data have been received, raise TypeError as 
        timeout signal.
       
        **returns**
        Source of the data from Xbee point of view, data contain in
        the received frame.
        
        """
        self.check_serial()
        
        try:
            while True:
                a = self.serial.read()
                a = ord(a)
                if a == 0x7E:
                    a = (ord(self.serial.read()) << 8 ) + ord(self.serial.read())
                    frame = bytearray(a+1)
                    check = 0
                    for i in range(a+1):
                        frame[i] = ord(self.serial.read())
                        check += frame[i]
                    if (check & 0xFF) != 0xFF:
                        continue                # Bad checksum
                    if frame[0] != 0x81:
                        continue                # it's not a 16bits addr RF packet
                    src  = (frame[1] << 8) + frame[2]
                    data = ""
                    for i in range(5,a):
                        data += chr(frame[i])
                    return src,data

        except TypeError:
            raise TypeError         # time out, no available data in receive buffer but time += 0,1 !
        except OSError:
            pass                    # bug fix on mini pc

                        
                
    def read(self, src_exp = 0xFFFF, timeout = -1):
        """
        Used <read_frame_NB> to read data from wireless link.
        This function allowed to wait for data from a particular 
        source (from a particular Smart Board Xbee module).
        Time to wait could be configure trought timeout 
        argument. TypeError is rise when delay expired. The minimal 
        timeout is the serial link timeout (default 100ms).
        
        **returns**
        
        Expected data.
        
        """
        
        start_time = time.time()
        while True:
            try :
                src, data = self.read_frame_NB()
                if src_exp == 0xFFFF or src_exp == src :
                    return src,data
            except TypeError:
                if time.time() - start_time > timeout and timeout != -1:
                    raise TypeError
                else:
                    continue

        
 
if __name__ == '__main__':
    pass

