import numpy as np
import pandas as pd
import visa, time

SCOPE_VISA_ADDR = "USB0::0x0957::0x1797::MY55460257::INSTR"

rm = visa.ResourceManager()
resources = rm.list_resources()
print("Resources: ", resources)

osc_daq = rm.open_resource(SCOPE_VISA_ADDR)
print(osc_daq.query("*IDN?")) # what are you?
print(osc_daq.resource_info) # oscilloscope information

# osc_daq = visa.instrument("USB0::0x0957::0x1797::MY55140223::0::INSTR")
# power_supply = visa.instrument("[Insert port and protocol]")

results = pd.DataFrame()

# while True:
#     osc_daq.write("MEASURE:VBASE? ")  # have DAQ read in data
#     Vout = float(daq.read())                    # record data DAQ acquired
#     print(Vout)
#     time.sleep(1)
