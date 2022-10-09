# Logging GPS Receiver
 Stores GPS data and SDR Signal Levels versus time.
Other features: AM/WBFM/USB/LSB/NBFM Monitor Receiver with AGC and S-meter.
				Offset averaging for S meter for logging.
				Logging Bandwidth is programmable to increase sensitivity.
				You can type on the keyboard while running and the note will show up in the CSV file in the 6th column

This program requires that a GPS receiver and a SDR receiver for Hardware. For software GNU Radio and gpsd are required. It was tested on Ubuntu 22.04.

The GPS receiver should be started along with the gpsd program or equivalent. The gpsd program sends data to ip:127.0.0.1 port 2947 which is picked up by the program. The program also runs gnuradio with a receiver tuned into a narrow frequency range. GUI Screens enable tuning in the signal so as to center it in the filter bandwidth. This bandwidth is heavely averaged and is then combined with the gps data for storage. The output is in a standard CSV format - Lattitude, Longitude, Signal Level, Elevation and GPS_Time and Notes. Notes can be added manually by typing them in while the program is running.

Two almost identical versions are included: 
1) Logging_Receiver_B205.grc , logging_receiver_b205.py and logging_receiver_b205_epy_block_0_0.py are used with the ETTUS B205mini SDR
2) Logging_Receiver_RTLSDR.grc, logging_receiver_rtlsdr.py and logging_receiver_rtlsdr_epy_block_0_0.py are used with a RTL-SDR.
Other SDR's can be used by modifing the GRC files.

The 2 programs may be run from the command line ex: python3 logging_receiver_b205.py
Parameters may be changed from the command line. ex: logging_receiver_rtlsdr.py -h    will list the parameters available to change. 

For a detailed description and screen shots see the logging_receiver.pdf file