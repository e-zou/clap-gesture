import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np


#phyphox configuration
PP_ADDRESS = "http://192.168.1.99:8080" # replace with your address shown in the phyphox app!!!
PP_CHANNELS = ["dB", "time"]

# global array to save amplitude data
dB =[]
times = []

def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS)) + "=full"
    data = requests.get(url=url).json()
    dB = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    times = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    return [dB, times]
        
def getData():
    [n_db, n_time] = getSensorData() # get nth sample
    dB.append(n_db)
    times.append(n_time)
    return [n_db, n_time]
    
# tracking number of claps
def main():
    analyze = [] #list
    clap_count = 0
    
    # stores claps recorded per 3 second interval
    claps = clap_count;

    # time since clap count was updated 
    last_time = 0.0
    
    # time since clap count was reset 
    reset_time = 0.0
    
    # time since action was updated 
    action_time = 0.0
    
    action = ""
    last_action = ""
    
    while True:
        [n_db, n_time] = getData()
        # prints out data collected every 3 seconds
        # if(n_time > last_time + 3):
        # print('time: ', n_time, '  dB: ', n_db, ' clap_count: ', clap_count)

        analyze.append(float(n_db))
        nums = analyze[-2:-1]

        if len(nums) >= 1:
            # was having trouble with the high resolution of this sensor... it detected 1 clap 10+ times...
            # " n_time > last_time + 0.5 "  #  -> updates clap count every 0.5 seconds - (to prevent excess detection)
            # works for single and double claps... although may not be 100% accurate 
            if nums[0] > -40  and (n_time > last_time + 0.5): # -40 is a threshold value that works 
                clap_count += 1
                last_time = float(n_time)
            
            # resets the clap counter every 3.0 seconds
            # stores the total number of claps detected each 3.0 seconds
            # determine which action based on number of claps detected
            if (n_time > reset_time + 3.0):
                reset_time = float(n_time) 
                claps = clap_count
                clap_count = 0; 
                if (claps == 1): # 1  - clap -> play/pause
                    if (action == "play"):
                        action = "pause"
                        last_action = "play"
                        # print('claps: ', claps, ' action: ', action)
                    else:
                        action = "play"
                        last_action = "pause"
                        # print('claps: ', claps, ' action: ', action)
                if (claps == 2): # 2  - clap -> rewind
                        action = "rewind"
                        last_action = "play"
                        # print('claps: ', claps, ' action: ', action)
                if (claps > 2): # 3+ - clap -> FastForward
                        action = "forward"
                        last_action = "play"
                        # print('claps: ', claps, ' action: ', action)
            
            # when a new action is determined, the video is manipulated based on that action
            while (last_action != action):  
                #Jess's Code
                action = last_action = "play"            
if __name__ == '__main__':
    main()
