import matplotlib.pyplot as plt
import pandas as pd

startSpeed=40 #mph
finalSpeed=68 #mph
shiftTime=0.3 #secs
redline=9000 #max RPM
dtLoss=0.18
numPoints=90

gearRatios = [3.166, 2.05, 1.481, 1.166, 0.916, 0.725]
C60 = 4.529
C56 = 4.312
finalDrive = C60
effGearRatios = [ratio*finalDrive for ratio in gearRatios] #ratio of input to output of trans (>1)
gearTopSpeedsC60 = [42.96, 66.35, 91.84, 116.65, 148.49, 187.60]
gearTopSpeeds = [gear*C60/finalDrive for gear in gearTopSpeedsC60] 
wheelRad = 0.94652 #ft

def calcTorq(rpm, dyno):
    print("RPM: ", rpm)
    if (rpm>dyno.RPM[0]):
        torq = (dyno.Torque[0]-dyno.Torque[1])/(dyno.RPM[0]-dyno.RPM[1])\
                    *(rpm-dyno.RPM[0])+dyno.Torque[0]
        #print("Above the max")
        #print(torq)
        print("Torque: ", torq)
        return torq
    elif (rpm<dyno.RPM.iloc[-1]):
        #print("Lower than min")
        torq = (dyno.Torque.iloc[-2]-dyno.Torque.iloc[-1])/(dyno.RPM.iloc[-2]-dyno.RPM.iloc[-1])\
                    *(rpm-dyno.RPM.iloc[-1])+dyno.Torque.iloc[-1]
        print("Torque: ", torq)
        return torq
    for i in range(0,dyno.RPM.size-1):
        if (rpm<=dyno.RPM[i]) & (rpm>dyno.RPM[i+1]):
            #print("between", dyno.RPM[i], " and ", dyno.RPM[i+1])
            torq = (dyno.Torque[i]-dyno.Torque[i+1])/(dyno.RPM[i]-dyno.RPM[i+1])\
                    *(rpm-dyno.RPM[i])+dyno.Torque[i]
            #print(torq)
            print("Torque: ", torq)
            return torq

rho = 0.002377#air density in slug/ft3
heightMR2 = 4.0833
widthMR2 = 5.5833
areaMR2 = heightMR2*widthMR2
weightMR2 = 2200
c_dMR2 = 0.353
g=32.2 #ft/s
tireSlip_g = 0.5

def calcAccel(torque, gearRatio, speed, loss, rad, weight, c_d, frontArea, launch_g):
    speed_ftpersec = (speed*1.46667)
    drag = 0.5*rho*(speed_ftpersec**2)*c_d*frontArea
    #print("Rho: ", rho)
    print("Speed (mph): ", speed)
    '''print("C_d: ", c_d)
    print("front area (ft^2): ", frontArea)
    print("Drag (lbf): ", drag)
    print("Drag (hp): ", speed_ftpersec*drag/550)'''
    
    thrust = torque*(1-loss)*(gearRatio/rad)
    #print("Thrust: (lbs)", thrust)
    
    accel_g = (thrust-drag)/weight #in
    #Accounting for a launch
    if (accel_g<tireSlip_g)&(speed<20):
        accel_g = tireSlip_g
    
    accel = accel_g*g*3600/5280 #ft/s/s converted to m/h/s aka mph/s
    print("Accel g:", accel_g)
    return accel

## Read in the dyno data for the toyota MR2
torqLookup = pd.read_csv("MR2dyno.csv", usecols=range(0,4))
#print(torqLookup)

#initialize variables for sim
t = 0.0 #time in seconds
t_inc = 0.02 #time increment
curRPM=0 #rpm
curSpeed=startSpeed #in mph
curGear=0
curDist=0 #recorded in feet
distLog = []
mph2fps=1.4667 #1mph = 1.4667 fps
speedLog = []
timeLog = []
gearLog = []
lastShiftTime = 0
shiftTransition = False
forceGear = False
gearForced = 2 #remember to subtract 1

#start numerical based simulation
while curSpeed<finalSpeed:
    print("Time :", t)
    timeLog.append(t)
    speedLog.append(curSpeed)
    gearLog.append(curGear)
    distLog.append(curDist)
    if curSpeed<gearTopSpeeds[0]: curGear=0
    elif curSpeed>gearTopSpeeds[-1]: curGear=len(gearTopSpeeds)-1
    else:
        for i in range(0, len(gearTopSpeeds)-1):
            if (curSpeed>gearTopSpeeds[i]) & (curSpeed<gearTopSpeeds[i+1]):
                curGear=i+1
                break
    if (len(gearLog)>3):
        if (curGear<gearLog[-1]):
            curGear=gearLog[-1]
    print("Current gear (irl index): ", curGear+1)
    #if minimum gear is being forced
    if forceGear == True:
        if curGear<gearForced:
            curGear = gearForced
            
    if (len(gearLog)>3)&(curGear != gearLog[-1]):
        lastShiftTime = t
        print("Shifted Gears at:", t, " seconds")
        shiftTransition = True
        trq=0
    elif ((t-lastShiftTime)<shiftTime)&(shiftTransition==True):
        trq=0
    elif ((t-lastShiftTime)>shiftTime)&(shiftTransition==True):
        shiftTransition = False
    else:
        trq=calcTorq(curRPM, torqLookup)

    accel = calcAccel(trq, effGearRatios[curGear],curSpeed,dtLoss,wheelRad,weightMR2,c_dMR2,areaMR2, tireSlip_g)
    curSpeed = curSpeed+accel*t_inc 
    curDist = (curDist+curSpeed*t_inc*mph2fps)
    curRPM=(curSpeed/gearTopSpeeds[curGear])*redline
    t=t+t_inc



# Section that calculates the torque curve based on the values from the csv
rpmVals=[(i+1)*redline/numPoints for i in range(0,numPoints)]
torqCurve = [0]*numPoints
hpCurve = [0]*numPoints
for i in range(0,numPoints):
    torqCurve[i] = calcTorq(rpmVals[i],torqLookup)
    hpCurve[i] = torqCurve[i]*rpmVals[i]/5252


#plot results from all (including the drag race)
print(startSpeed, "mph - ", finalSpeed, "mph Time: ", timeLog[-1])

#make first graph
plt.figure(1)
plt.plot(rpmVals, torqCurve, 'b.')
plt.plot(rpmVals, hpCurve, 'r.')
plt.ylim(0,torqLookup.HP.max()+15)
plt.grid()
plt.legend(["Torque","Power"])
    
plt.figure(2)
plt.plot(timeLog, speedLog, "g*")
plt.show()

