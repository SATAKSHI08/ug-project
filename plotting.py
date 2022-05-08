from matplotlib import pyplot as plt
file = open("E://UG//SpeedRecord.txt","r")
count=0
entrytime=[]
exittime=[]

for line in file:
    count+=1
    if count<=2:
        continue
    x=line.split("\t")
    if(x[3]<x[2]):
        continue
    
    entrytime.append(x[2])
    exittime.append(x[3])
print(entrytime,exittime)

for i in range (0,len(entrytime)):
    x=[float(entrytime[i]),float(exittime[i])]
    y=[float(10),float(40)]
    plt.plot(x,40
    plt.plot(x, y)
plt.show()
