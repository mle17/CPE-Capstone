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

    for _ in range(1):
        # data = {}

        # osc_daq.write("MEASURE:FREQ? ")             # have DAQ read in data
        # data["Freq"] = float(osc_daq.read())        # record data DAQ acquired

        # osc_daq.write("MEASURE:VPP? ")
        # data["Vpp"] = float(osc_daq.read())

        # print(str(data["Freq"]) + " Hz\t" + str(data["Vpp"]) + " V")
        # results = results.append(data, ignore_index=True)
        # time.sleep(1)

        # if(data["Freq"] > 1 * MHZ):
        #    osc_daq.write(":AUTOSCALE")

       osc_daq.write(":WAVeform:POINts:MODE RAW")
       print(osc_daq.query(":WAVeform:POINts:MODE?"))

       osc_daq.write(":WAVeform:POINts 100")
       print(osc_daq.query(":WAVeform:POINts?"))

       osc_daq.write(":WAVeform:SOURce CHANnel1")
       print(osc_daq.query(":WAVeform:SOURce?"))

       osc_daq.write(":WAVeform:FORMat ASCII")
       print(osc_daq.query(":WAVeform:FORMat?"))

       sData = osc_daq.query(":WAVeform:DATA?")
    #    print(sData[1])
       wave_results = get_definite_length_block_data(sData)


    plt.plot(wave_results)
    plt.show()

##############################################################################################################################################################################
##############################################################################################################################################################################
## Helper Functions
##############################################################################################################################################################################
##############################################################################################################################################################################
def init_osc():
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print("Resources: ", resources)

    try:
        scope = rm.open_resource(SCOPE_VISA_ADDR)
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
def get_definite_length_block_data(sBlock):

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

if __name__== "__main__":
    main()
