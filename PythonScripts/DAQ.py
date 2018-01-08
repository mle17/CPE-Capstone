import numpy as np
import pandas as pd
import visa, time
import sys
import struct
import matplotlib.pyplot as plt

SCOPE_VISA_ADDR = "USB0::0x0957::0x1797::MY55460257::0::INSTR"

GLOBAL_TOUT = 10000
TIME_TO_TRIGGER = 10
TIME_BTWN_TRIGGERS = 0.025
MHZ = 1e6

##############################################################################################################################################################################
##############################################################################################################################################################################
## main
##############################################################################################################################################################################
##############################################################################################################################################################################

def main():
    osc_daq = init_osc()

    results = pd.DataFrame()
    osc_daq.write(":RUN")
    # osc_daq.write(":SINGLE") # acquires one waveform (pg. 790)

    for _ in range(2):
        wave_data = take_waveform(osc_daq)
        results = results.append(wave_data)

    first_waveform = results.iloc[0]
    sec_waveform = results.iloc[1]
    first_waveform.plot(kind="line")
    sec_waveform.plot(kind="line")

    plt.show()

##############################################################################################################################################################################
##############################################################################################################################################################################
## Helper Functions
##############################################################################################################################################################################
##############################################################################################################################################################################
def take_waveform(scope):
  scope.write(":AUTOSCALE")
  scope.write(":WAVeform:POINts:MODE RAW")
  scope.write(":WAVeform:POINts 100")
  scope.write(":WAVeform:SOURce CHANnel1")
  scope.write(":WAVeform:FORMat ASCII")

  sData = scope.query(":WAVeform:DATA?")
  wave_results = format_wave_data(sData)
  df = pd.DataFrame([wave_results])
  return df

def init_osc():
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print("Resources: ", resources)

    try:
        device_addr = get_device_addr("USB0", resources) ## oscilloscope first address
        scope = rm.open_resource(device_addr)
    except Exception:
        print("Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDR) + ". Aborting script.\n")
        sys.exit()

    print(scope.query("*IDN?")) # what are you?
    print(scope.resource_info) # oscilloscope information

    ## Set Global Timeout
    ## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
    scope.timeout = GLOBAL_TOUT

    ## Clear the instrument bus
    scope.clear()

    ## Clear all registers and errors
    ## Always stop scope when making any changes.
    scope.query(":STOP;*CLS;*OPC?")

    return scope

def do_command(command, scope, hide_params=False):
    if hide_params:
        (header, data) = string.split(command, " ", 1)

    scope.write("%s\n" % command)
    if hide_params:
        check_instrument_errors(header)
    else:
        check_instrument_errors(command)

# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query, InfiniiVision):
   result = InfiniiVision.query("%s\n" % query)
   check_instrument_errors(query, InfiniiVision)
   return result

# =========================================================
# Send a query, check for errors, return values:
# =========================================================
def do_query_values(query, InfiniiVision):
   results = InfiniiVision.ask_for_values("%s\n" % query)
   check_instrument_errors(query, InfiniiVision)
   return results

# =========================================================
# Check for instrument errors:
# =========================================================
def check_instrument_errors(command, InfiniiVision):
   while True:
      error_string = InfiniiVision.query(":SYSTem:ERRor?\n")
      if error_string: # If there is an error string value.
         if error_string.find("+0,", 0, 3) == -1: # Not "No error".
            print("ERROR: %s, command: '%s'" % (error_string, command))
            print("Exited because of error.")
            sys.exit(1)
         else: # "No error"
            break
      else: # :SYSTem:ERRor? should always return string.
         print ("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
         print ("Exited because of error.")
         sys.exit(1)

# =========================================================
# Returns data from definite-length block.
# =========================================================
def format_wave_data(sBlock):

   # First character should be "#".
   pound = sBlock[0:1]
   if pound != "#":
      print("PROBLEM: Invalid binary block format, pound char is '%s'." % pound)
      print("Exited because of problem.")
      sys.exit(1)

   # Second character is number of following digits for length value.
   digits = sBlock[1]

   # Get the data out of the block and return it.
   sData = sBlock[int(digits) + 2:]
   list_data = sData.split(",")
   list_data = [float(i) for i in list_data]
   return list_data

def get_device_addr(port_type, resource_list):
    device_addr = ""
    for device in resource_list:
        if port_type in device:
            device_addr = device
            return device_addr

if __name__== "__main__":
    main()
