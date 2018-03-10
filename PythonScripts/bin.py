import sys
import struct

BIT = '1'

def main():
   for counter in range(0, 51 if BIT == '0' else 41):
      filename = 'Bit' + BIT + '/scope_' + str(counter) + '.csv'
      print(filename)
   # Loop through files
      # Open current file
      # Loop through csv
         # Check when trigger is high, store in array
      # Output to another csv

if __name__== "__main__":
    main()