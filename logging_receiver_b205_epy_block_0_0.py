"""
Embedded Python Blocks: REv D

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt
import time
import requests
import json
import warnings
from datetime import datetime
warnings.simplefilter("ignore", np.ComplexWarning)
from gps import *


# import date.time  NG in Raspberry PI
#from datetime import date
# datetime object containing current date and time
now = datetime.now()
#print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Start Collection at: ", dt_string)


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block, sync_block
    """Embedded Python Block test case - count number and a simple multiply const"""

    def __init__(self, file_name='log_my_rcvr_gps.csv',Freq=104.5e6,Gain=30,Offset= 39):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='GPS Python Block', 
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
            #out_sig=[np.float32, np.byte]
        self.rcvr_file_name = file_name #rcvr_file_name
        rcvr_file_name = file_name 
        self.message_port_register_in(pmt.intern('msg_in_attach'))
        self.message_port_register_in(pmt.intern('gps_nmea_in'))        
        portName1 = 'gps_msg_out'
        self.message_port_register_out(pmt.intern(portName1))
        portName2 = 'time_and_dBm_out'
        self.message_port_register_out(pmt.intern(portName2))
        self.set_msg_handler(pmt.intern('msg_in_attach'), self.handle_msg)
        self.set_msg_handler(pmt.intern('gps_nmea_in'), self.handle_gps_msg)
                
        self.message_port_register_out(pmt.intern('clear_input'))
        self.portName1 = portName1
        self.portName2 = portName2        
        self.dt_string = dt_string
        self.msg = "Hello"
        self.gps_msg = "There" 
        self.nmea = self.gps_msg
        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)  #WATCH_NEWSTYLE forces JSON streaming
        self.gpsd = gpsd
#        print("gpsd_TOP =", gpsd)
        #ipadr= "127.0.0.1", myport= "2947",        
#        self.ipadr = ipadr
#        self.myport = myport
        print("logFREQ=", Freq, "Gain=", Gain, "Offset=", Offset, "start time=", dt_string)
        #header_message = "logFREQ= "+ str(Freq)+ " Gain= " + str(Gain)+ " Offset= "+ str(Offset)+ " start time= "+ str(dt_string)
        
        with open(rcvr_file_name, "a") as f:
            
            f.write(", , , , ,logFREQ:" + str(Freq)+ " Gain:" + str(Gain)+ " Offset:" + str(Offset)+ " start time:" + str(dt_string) + "\n")
            f.write("Lattitude ,  Longitude,  Signal Level (dB), Elevation, gps Time, notes" + "\n")
       
        self.value = 1
#        self.url = 'http://192.168.0.123:2947'

        
    def handle_msg(self, msg):   # added input text notes to the file !
        global textboxValue
        textboxValue = pmt.symbol_to_string (msg)
        self.textboxValue = textboxValue
#        print (pmt.serialize_str (msg))       
         
    def handle_gps_msg(self, gps_msg):   # added input text notes to the file !
        global nmea
        nmea = pmt.deserialize_str (gps_msg)
        self.gps_msg = nmea
        self.nmea = nmea
#        print("NMEA Message = ", nmea)
#        global PMT_msg
  #@      PMT_msg = pmt.to_pmt([self.local_save])
        
    def work(self, input_items, output_items):
        """example output"""
        global textboxValue
        msg = self.msg
        gps_msg = self.gps_msg
        portName1 = self.portName1
        portName2 = self.portName2
        textboxValue = self.textboxValue   # a string type
        rcvr_file_name = self.rcvr_file_name
        nmea = self.nmea
        gpsd = self.gpsd
#        print("gpsd_MID =", gpsd)
#        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
#        print('latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb') # '\t' = TAB to try and output the data in columns.
        report = gpsd.next() #
#        print(report) # prints the raw data NOT in NEMA format !

        if report['class'] == 'TPV':
# typical 2022-09-11T15:52:20.000Z 	 114.5752 	 38.884 	 0.005 	 0.167 	 0.058 	 42.460212246 	 -71.530672654 
#            print("TPV found")
            nmea = self.nmea #"print("nmea received", "textboxValue = ", textboxValue) "
   #         print(getattr(report,'lat',0.0),"\t", end=" ")
    #        print(getattr(report,'lon',0.0),"\t", end=" ")
#            print(getattr(report,'time',''),"\t") #, end=" ")
#            print(getattr(report,'alt','nan'),"\t", end=" ")
#            print(getattr(report,'epv','nan'),"\t", end=" ")
#            print(getattr(report,'ept','nan'),"\t", end=" ")
 #           print(getattr(report,'speed','nan'),"\t")
#            print(getattr(report,'climb','nan'),"\t", end=" ")
#        time.sleep(.5)        

 
        with open(rcvr_file_name, "a") as f:


            for index in range(len(input_items[0])):     #value = 22.7712   # from the receiver and offset
                self.value = (input_items[0][index])   # get the dB value
                value = self.value

                
                a1 = getattr(report,'time', ' ')
                a2 = getattr(report,'lat',0.0)
                a3 = getattr(report,'lon',0.0)
                a4 = value
                a5 = getattr(report,'alt','nan')
                print(a2,  a3, "  ", a4)
#                print("   ", str(a4))
                gps_msg_to_send = str(a2) + ", " + str(a3) + ", " + str(a4) + ", " + str(a5) + ", " + str(a1)
                # (getattr(report,'time', ' '), getattr(report,'lat',0.0)," ", getattr(report,'lon',0.0)," "), getattr(report,'alt','nan' #, "{:.2f}".format(value), "dB")
#                print(gps_msg_to_send)               
                msg_to_send = gps_msg_to_send 
                              
                if len(textboxValue) >=1 :
                    f.write(gps_msg_to_send + "\n" + ", , , , ," + textboxValue + "\n")
                    print(textboxValue)

                else:
                    f.write(gps_msg_to_send + "\n")
#                    print("un-changed", textboxValue)
                    
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                dt_dBm_string = dt_string + " dB=" + str("{:.2f}".format(value))
 ###               print(dt_dBm_string)
##                dt_dBm_bytes = str.encode(dt_dBm_string)       # # my_str_as_bytes = str.encode(my_str)
##                print("byte stream: ", dt_dBm_bytes)
                if len(textboxValue) >=1 :
                    self.message_port_pub(pmt.intern(portName1), pmt.intern(msg_to_send + "\n" + textboxValue))              
                    self.message_port_pub(pmt.intern(portName2), pmt.intern(dt_dBm_string + "\n" + textboxValue))

                else:
                    self.message_port_pub(pmt.intern(portName1), pmt.intern(msg_to_send))
                    self.message_port_pub(pmt.intern(portName2), pmt.intern(dt_dBm_string))
                    #output_items[0][index] = dt_dBm_bytes

      
        output_items[0][:] = input_items[0]
#        output_items[1][:] = msg_to_send_bytes
        # clear input line
        textboxValue = ""
        self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
        return len(output_items[0])
 

