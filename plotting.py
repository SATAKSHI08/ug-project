from matplotlib import pyplot as plt
import numpy as np
file = open("E://UG//SpeedRecord.txt","r")
count=0
entrytime=[]
exittime=[]
speed=[]
flow=[]
vehicle=1
linss = np.linspace(0,600,1000)
for line in file:
    count+=1
    if count<=2:
        continue
    x=line.split("\t")
    if(x[3]<x[2]):
        continue
    speed.append(x[1])
    entrytime.append(x[2])
    exittime.append(x[3])
print(entrytime,exittime)

for i in range (0,len(entrytime)):
    x=[float(entrytime[i]),float(exittime[i])]
    y=[float(10),float(40)]
    
    plt.plot(x, y)
#plt.plot(linss,0*linss+ 40,'-r')
plt.xlabel('Time', color='#1C2833')
plt.ylabel('Distance', color='#1C2833')
plt.title('Time Space Diagram', fontweight='bold')
plt.show()
##########flow################

for i in range (0, len(entrytime)):
    flow.append(vehicle/(float(exittime[i])-float(entrytime[0])))
    vehicle+=1
print(flow)
for i in range (0,len(entrytime)):
    plt.scatter(flow[i], float(speed[i]))
plt.xlabel('FLOW', color='#1C2833')
plt.ylabel('SPEED', color='#1C2833')
plt.title('FLOW SPEED Diagram', fontweight='bold')
plt.show()

##################Density########################


