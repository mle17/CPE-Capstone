import sys
import struct
import pandas as pd
import numpy as np
import csv

BIT = '0'
TRIG_VOLT = 3
BIT_1_THRESH = 100

def main():
   if BIT == '0':
      for counter in range(41, 91):
         filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
         add_bit_data_to_csv(filename)
   else:
      for counter in range(0, 41):
         filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
         add_bit_data_to_csv(filename)

def add_bit_data_to_csv(source_file):
    src_csv = pd.read_csv(source_file)
    result_csv = open('outputBit' + BIT + '.csv', 'a')
    wr_result = csv.writer(result_csv, delimiter=',')
    delay_csv = open('delayBit' + BIT + '.csv', 'a')
    wr_delay = csv.writer(delay_csv, delimiter=',')

    src_vout = list(src_csv["1"])[1:]
    src_trigger = list(src_csv["2"])[1:]
    src_vout = [float(i) for i in src_vout]
    src_trigger = [float(i) for i in src_trigger]

    bit_data = []
    delay_data = []
    is_triggered = False
    for vout_data, trigger_data in zip(src_vout, src_trigger):
        if not is_triggered and trigger_data > TRIG_VOLT:
            is_triggered = True
            wr_delay.writerows([delay_data])
            delay_data = []
        elif is_triggered and trigger_data < TRIG_VOLT:
            is_triggered = False
            if BIT == '1':
                if len(bit_data) > BIT_1_THRESH:
                    wr_result.writerows([bit_data])
            else:
                if len(bit_data) < BIT_1_THRESH:
                    wr_result.writerows([bit_data])
            bit_data = []

        if is_triggered:
            bit_data.append(vout_data)
         else:
            delay_data.append(vout_data)

    result_csv.close()
    delay_csv.close()

if __name__== "__main__":
    main()
