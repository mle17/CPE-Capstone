import sys
import struct
import pandas as pd
import numpy as np
import csv

BIT = '1'
KEY = '1'
TRIG_VOLT = 3        # Cutoff voltage for a trigger high
BIT_1_THRESH = 100   # Cutoff threshold for number of points in a 0 bit model

# Converts waveform captured from each trigger of the encryption cycle 
# into their own .csv to be later converted into a model
def main():
   if KEY == '1':
      result_csv = open('outputKey.csv', 'w')
   else:
      result_csv = open('outputBit' + BIT + '.csv', 'w')
      # Data for the delays are captured as well
      delay_csv = open('delayBit' + BIT + '.csv', 'w')

   if KEY == '1':
      # Key model
      for counter in range(31, 61):
         filename = 'Key/scope_' + str(counter) + '.csv'
         add_bit_data_to_csv(filename, result_csv, None)
   elif BIT == '0':
      # Bit 0 model
      for counter in range(41, 91):
         filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
         add_bit_data_to_csv(filename, result_csv, delay_csv)
   else:
      # Bit 1 model
      for counter in range(0, 41):
         filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
         add_bit_data_to_csv(filename, result_csv, delay_csv)

   result_csv.close()
   delay_csv.close()

def add_bit_data_to_csv(source_file, result_csv, delay_csv):
   src_csv = pd.read_csv(source_file)
   wr_result = csv.writer(result_csv, delimiter=',')
   if delay_csv:
   wr_delay = csv.writer(delay_csv, delimiter=',')

   src_vout = list(src_csv["1"])[1:]
   src_trigger = list(src_csv["2"])[1:]
   src_vout = [float(i) for i in src_vout]
   src_trigger = [float(i) for i in src_trigger]

   bit_data = []
   delay_data = []
   is_triggered = False
   for vout_data, trigger_data in zip(src_vout, src_trigger):
      # Start of a trigger
      if not is_triggered and trigger_data > TRIG_VOLT:
         is_triggered = True
         if KEY != '1':
            wr_delay.writerows([delay_data])
            delay_data = []
      # End of a trigger
      elif is_triggered and trigger_data < TRIG_VOLT:
         is_triggered = False
         if BIT == '1' or KEY == '1':
               if len(bit_data) > BIT_1_THRESH:
                  wr_result.writerows([bit_data])
         else:
               if len(bit_data) < BIT_1_THRESH:
                  wr_result.writerows([bit_data])
         bit_data = []

      # Trigger high means data for the bit
      if is_triggered:
         bit_data.append(vout_data)
      # Trigger low means data for the delay
      else:
         delay_data.append(vout_data)

if __name__== "__main__":
    main()
