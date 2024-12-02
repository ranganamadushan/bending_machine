import tkinter as tk
import csv
import time
import pyvisa as visa
import serial
from datetime import datetime

ser = serial.Serial('COM19', 9600)  # Replace 'COM17' with the name of your serial port and 9600 with the baud rate of your serial device

# Open the connection to the DMM
rm = visa.ResourceManager()
dmm = rm.open_resource('USB0::0x05E6::0x2100::1373334::INSTR')
dmm.timeout = 10000  # Set timeout to 10 seconds

# Open the CSV file for writing
with open('conc_1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Resistance'])

    data = ""  # Initialize the data variable
    try:
        # Read and display the data continuously
        while True:
            if ser.in_waiting > 0:  # Check if there is data in the serial buffer
                data = ser.readline().decode('utf-8').rstrip()  # Read data from serial port and decode it from bytes to UTF-8 string format

            # Take a measurement and parse the result
            reading = dmm.query_ascii_values('READ?')
            if reading and data:  # Check if both data and reading are not empty
                reading = reading[0]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Get the current timestamp with milliseconds
                data_row = [timestamp, reading, data]

                # Write the data to the CSV file
                writer.writerow(data_row)

            # Wait for 100 milliseconds before taking the next measurement
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Close the connection to the DMM
        dmm.close()
