import sys
import struct
import pandas as pd
import numpy as np
import csv

BIT = '1'
TRIG_VOLT = 3

def main():
   for counter in range(0, 51 if BIT == '0' else 41):
      filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
      print(filename)
   # Loop through files
      # Open current file
      # Loop through csv
         # Check when trigger is high, store in array
      # Output to another csv

def add_bit_data_to_csv(source_file):
    src_csv = pd.read_csv(source_file)
    result_csv = open('outputBit' + BIT + '.csv', 'w')
    wr = csv.writer(result_csv, delimiter=',')

    src_vout = list(src_csv["1"])[1:]
    src_trigger = list(src_csv["2"])[1:]
    src_vout = [float(i) for i in src_vout]
    src_trigger = [float(i) for i in src_trigger]

    bit_data = []
    is_triggered = False
    for vout_data, trigger_data in zip(src_vout, src_trigger):
        if not is_triggered and trigger_data > TRIG_VOLT:
            is_triggered = True
        elif is_triggered and trigger_data < TRIG_VOLT:
            is_triggered = False
            wr.writerows([bit_data])
            bit_data = []

        if is_triggered:
            bit_data.append(vout_data)

if __name__== "__main__":
    add_bit_data_to_csv("Bit0/scope_0.csv")
