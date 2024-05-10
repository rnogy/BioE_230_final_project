#This script is to create timer when create animation in chimera
from chimera import runCommand
if mdInfo['frame'] == 1:
    #Create timer at step =1. Since script is re-ran at each frame, no "memory" can be created.
    #Using try and except to avoid error
    try:
        #Create label called timer at left bottom corner. 
        runCommand("2dlabels create timer text '0 ns' size 40 color white xpos 0 ypos 0")
    except:
        #100 ps per frame, each frame is in ps. 
        runCommand("2dlabels change timer text" + " " + str(100 * (mdInfo["frame"] / 1000.0)) + 'ns')
else:
    runCommand("2dlabels change timer text" + " " + str(100 * (mdInfo["frame"] / 1000.0)) + 'ns')