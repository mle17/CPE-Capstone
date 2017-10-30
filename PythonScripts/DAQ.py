import numpy as np
import pandas as pd
import visa, time

SCOPE_VISA_ADDR = "USB0::0x0957::0x1797::MY55140223::0::INSTR"

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
    
    while True:
        osc_daq.write("MEASURE:FREQ? ")  # have DAQ read in data
        Freq = float(osc_daq.read())          # record data DAQ acquired
        osc_daq.write("MEASURE:VPP? ")
        Vout = float(osc_daq.read())
        print(str(Freq) + " Hz\t" + str(Vout) + " V")
        #osc_daq.clear()
        time.sleep(1)
        if(Freq > 1 * MHZ):
           osc_daq.write(":AUTOSCALE")


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

    # print(scope.query("*IDN?")) # what are you?
    # print(scope.resource_info) # oscilloscope information

    ## Set Global Timeout
    ## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
    scope.timeout = GLOBAL_TOUT

    ## Clear the instrument bus
    scope.clear()

    ## Clear all registers and errors
    ## Always stop scope when making any changes.
    scope.query(":STOP;*CLS;*OPC?")

    return scope

# Random crap from source file
##############################################################################################################################################################################
##############################################################################################################################################################################
## Define 2 functions to synchronize InfiiVision Oscilloscopes
##############################################################################################################################################################################
##############################################################################################################################################################################

#######################################################################################################
## Define a simple and fast function utilizing the blocking :DIGitize command in conjunction with *OPC?
def blocking_method():

    KsInfiniiVisionX.timeout =  SCOPE_ACQUISITION_TIME_OUT # Time in milliseconds (PyVisa uses ms) to wait for the scope to arm, trigger, finish acquisition, and finish any processing.
        ## Note that this is a property of the device interface, KsInfiniiVisionX.
	## If doing repeated acquisitions, this should be done BEFORE the loop, and changed again after the loop if the goal is to achieve best throughput.

    print("Acquiring signal(s)...\n")
    try: # Set up a try/except block to catch a possible timeout and exit.
        KsInfiniiVisionX.query(":DIGitize;*OPC?") # Acquire the signal(s) with :DIGItize (blocking) and wait until *OPC? comes back with a one. There is no need to issue a *CLS before issuing the :DIGitize command as :DIGitize actually takes care of this for you.
        print("Signal acquired.\n")
        KsInfiniiVisionX.timeout =  GLOBAL_TOUT # Reset timeout back to what it was, GLOBAL_TOUT.
    except Exception: # Catch a possible timeout and exit.
        print("The acquisition timed out, most likely due to no trigger, or improper setup causing no trigger. Properly closing scope connection and exiting script.\n")
        KsInfiniiVisionX.clear() # Clear scope communications interface; a device clear aborts a digitize and clears the scope's IO interface..
        ## Don't do a *CLS.  If you do, you won't be able to do a meaningful :SYSTem:ERRor? query as *CLS clears the error queue
        KsInfiniiVisionX.close() # Close communications interface to scope
        sys.exit("Exiting script.")

    ## Benefits of this method:
        ## Fastest, compact
        ## Only way for Average Acquisition type:
            ## The :SINGle command does not do a complete average.
            ## Counting triggers with :RUN is much too slow
        ## Allows for easy synchronization with math functions
        ## Don't have to deal with the status registers, which can be confusing
        ## Potentially faster than polling_method(), for better throughput
        ## Because it's faster one can retrieve more accurate acquisition times than with a polling method.
        ## Works best for segmented memory if any post processing is done on the scope, e.g. measurements, lister, math, as this does not come back until the processing is all done
            ## In this scenario, :DIGitize does not reduce the sample rate or memory depth.
    ## Drawbacks of this method:
        ## Usually does not fill acquisition memory tot eh maximum available, usually only on-screen data.
        ## May not be at the highest sample rate (compared with the polling_method)
        ## Requires a well-chosen, hard-set timeout that will cover the time to arm, trigger,
            ## and finish acquisition.
        ## Requires Exception handling and a device_clear() for a possible timeout (no trigger event).
            ## Socket connection cannot do device_clear()
        ## Since :DIGitize is a "specialized form of the :RUN" command, on these scope, that results in:
            ## the sample rate MAY be reduced from using :SINGle - usually at longer time scales -
            ## typically only acquires what is on screen, though at the fastest time scales, more than on screen data may be acquired
            ## Thus, for max memory and max sample rate, use the polling_method(), which uses :SINGle.
    ## How it works:
        ## The :DIGitize command is a blocking command, and thus, all other SCPI commands are blocked until
            ## :DIGitize is completely done.  This includes any subsequent processing that is already set up,
            ## such as math, jitter separation, and measurements.  Key Point: When the *OPC? query is appended to
            ## :DIGitize with a semi-colon (;), which essentially ties it to the same thread in the parser,
            ## it is immediately dealt with when :DIGitize finishes and gives a “1” back to the script, allowing the script to move on.
    ## Other Notes:
        ## If you DO NOT know when a trigger will occur, you will need to (should) set a very long time out.
        ## The timeout will need to be (should be) adjusted before and after the :DIGitize operation,
            ## though this is not absolutely required.
        ## A :DIGitize can be aborted with a device clear, whcih also stops the scope: KsInfiniiVisionX.clear()
        ## :DIGItize disables the anti-aliasing feature (sample rate dither) on all InfiniiVision and InfiniiVision-X scopes.
        ## :DIGitize temporarily blocks the front panel, and all front panel presses are queued until :DIGitize is done.  So if you change the vertical scale, it will not happen until the acquisition is done.
            ## The exception is that the Run/Stop button on the front panel is NOT blocked (unless the front panel is otherwise locked by :SYSTem:LOCK 1).

##################################################################################################################
## Define a function using the non-blocking :SINGle command and polling on the Operation Status Condition Register
def polling_method():

    MAX_TIME_TO_WAIT = SCOPE_ACQUISITION_TIME_OUT/float(1000) # Time in seconds to wait for the scope to arm, trigger, and finish acquisition.
        ## Note that this is NOT a property of the device interface, KsInfiniiVisionX, but rather some constant in the script to be used later with
            ## the Python module "time," and will be used as time.clock().

    ## Define "mask" bits and completion criterion.
    ## Mask condition for Run state in the Operation Status Condition (and Event) Register
         ## This can be confusing.  In general, refer to Programmer's Guide chapters on Status Reporting, and Synchronizing Acquisitions
         ## Also see the annotated screenshots included with this sample script.
    RUN_BIT = 3 # The run bit is the 4th bit (see next set of comments @ Completion Criteria).
    RUN_MASK = 1<<RUN_BIT  # This basically means:  2^3 = 8, or rather, in Python 2**3 (<< is a left shift; left shift is fastest); this is used later to
        ## "unmask" the result of the Operation Status Event Register as there is no direct access to the RUN bit.

    ## Completion criteria
    ACQ_DONE = 0 # Means the scope is stopped
    ACQ_NOT_DONE = 1<<RUN_BIT # Means the scope is running; value is 8
        ## This is the 4th bit of the Operation Status Condition (and Event) Register.
        ## The registers are binary and start counting at zero, thus the 4th bit (4th position in a binary representation of decimal 8 = 2^3 = (1 left shift 3).
        ## This is either High (running = 8) or low (stopped and therefore done with acquisition = 0).

    print("Acquiring signal(s)...\n")
    StartTime = time.clock() # Define acquisition start time; This is in seconds.
    KsInfiniiVisionX.write("*CLS;:SINGle") # Beigin Acquisition with *CLS and the non-blocking :SINGle command, concatenated together. The *CLS clears all (non-mask) registers & sets them to 0;

    ## Initialize the loop entry condition (assume Acq. is not done).
    Acq_State = ACQ_NOT_DONE

    ## Poll the scope until Acq_State is a one. (This is NOT a "Serial Poll.")
    while Acq_State == ACQ_NOT_DONE and (time.clock() - StartTime <= MAX_TIME_TO_WAIT):
        Status = int(KsInfiniiVisionX.query(":OPERegister:CONDition?")) # Ask scope if it is done with the acquisition via the Operation Status Condition (not Event) Register.
            ## The Condition register reflects the CURRENT state, while the EVENT register reflects the first event that occurred since it was cleared or read, thus the CONDITION register is used.
            ## DO NOT do: KsInfiniiVisionX.query("*CLS;SINGle;OPERegister:CONDition?") as putting :OPERegister:CONDition? rigth after :SINgle doesn't work reliably
                ## The scope SHOULD trigger, but it sits there with the Single hard key on the scope lit yellow; hitting this key causes a trigger.
        Acq_State = (Status & RUN_MASK) # Bitwise AND of the Status and RUN_MASK.  This exposes ONLY the 4th bit, which is either High (running = 8) or low (stopped and therefore done with acquisition = 0)
        if Acq_State == ACQ_DONE:
            break # Break out of while loop so that the 100 ms pause below is not incurred if done.
        time.sleep(.1) # Pause 100 ms to prevent excessive queries
            ## This can actually be set a little faster, at 0.045.  The point here is that
                ## 1. if there are other things being controlled, going too fast can tie up the bus.
                ## 2. going faster does not work on all scopes.  The symptom of this not working is:
                    ## The scope SHOULD trigger, but it sits there with the Single hard key on the scope lit yellow; hitting this key causes a trigger.
            ## The pause should be at the end of the loop, so that the scope is immediately asked if it is done.
        ## Loop exits when Acq_State != NOT_DONE, that is, it exits the loop when it is DONE or if the max wait time is exceeded.

    if Acq_State == ACQ_DONE: # Acquisition fully completed
        print("Signal acquired.\n")
    else: # Acquisition failed for some reason
        print("Max wait time exceeded.")
        print("This happens if there was no trigger event.")
        print("Adjust settings accordingly.\n")
        print("Properly closing scope connection and exiting script.\n")
        KsInfiniiVisionX.clear() # Clear scope communications interface
        KsInfiniiVisionX.query(":STOP;*OPC?") # Stop the scope
        KsInfiniiVisionX.close() # Close communications interface to scope
        sys.exit("Exiting script.")
        ## Or do something else...

    ## Benefits of this method:
        ## Don't have to worry about interface timeouts
        ## Easy to expand to know when scope is armed, and triggered
        ## MAY result in a higher sample rate than the blocking method
        ## Always fills max available memory
        ## Can use with a socket connection if desired
    ## Drawbacks of this method:
        ## Slow
        ## Does NOT work for Average Acquisition type
            ## :SINGle does not do a complete average
                ## It does a single acquisition as if it were in NORMal acq. type
                ## Counting triggers in :RUN is much too slow
        ## Works for Segmented Memory, BUT if any post processing is done on the scope, e.g. measurements, lister, math, as this reprotsa that the acquisition is done,
            ## which is correct, BUT  the processing is NOT done, and it willt ake an indefintie amoutn of time to wiat for that, though there is no way to tell if it is done.
            ## Use the blcoking_mthod for Segmented Memory.
        ## Can't be used effectively for synchronizing math functions
            ## It can be done by applying an additional hard coded wait after the acquisition is done.  At least 200 ms is suggested, more may be required.
            ## However, as long as the time out is not excessively short, the math happens fast enough that once :OPERegister:CONDition? comes back as done
                ## that one can just wait for it when it is time to pull the math waveform.  The exception would be for eye or jitter mode on an X6000A, where the processing time can be long.
        ## Still need some maximum timeout (here MAX_TIME_TO_WAIT), ideally, or the script will sit in the while loop forever if there is no trigger event
            ## Max time out (here MAX_TIME_TO_WAIT) must also account for any processing done (see comments on math above)
            ## Max time out (here MAX_TIME_TO_WAIT) must also account for time to arm the scope and finish the acquisition
                ## This arm/trigger/finish part is accounted for in the main script.
    ## How it works:
        ## Pretty well explained in line; see annotated screenshots. Basically:
            ## What really matters is the RUN bit in the Operation Condition (not Event) Register.  This bit changes based on the scope state.
            ## If the scope is running, it is high (8), and low (0) if it is stopped.
            ## The only (best) way to get at this bit is with the :OPERation:CONDition? query.  The Operation Condition Register can reflect states
            ## for other scope properties, for example, if the scope is armed, thus it can produce values other than 0 (stopped) or 8 (running).
            ## To handle that, the result of :OPERation:Condition? is bitwise ANDed (& in Python) with an 8.  This is called "unmasking."
            ## Here, the "unmasking" is done in the script.  On the other hand, it is possible to "mask" which bits get passed to the
            ## summary bit to the next register below on the instrument itself.  However, this method it typically only used when working with the Status Byte,
            ## and not used here.
            ## Why 8 = running = not done?
                ## The Run bit is the 4th bit of the Operation Status Condition (and Event) Registers.
                ## The registers are binary and start counting at zero, thus the 4th bit is bit number 3, and 2^3 = 8, and thus it returns an 8 for high and a 0 for low.
            ## Why the CONDITION and NOT the EVENT register?
                ## The Condition register reflects the CURRENT state, while the EVENT register reflects the first event that occurred since it was cleared or read (as in: has it EVER happened?),
                ## thus the CONDITION register is used.
    ## Note that with this method using :SINGle, for InfiniiVision-X scopes only, :SINGle itself forces the trigger sweep mode into NORMal.
        ## This does not happen with the blocking method, using :DIGitize or on the InfiniiVsion notXs.

if __name__== "__main__":
    main()
