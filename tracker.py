import math
import time
import numpy as np
import cv2

limit = 80
entryflag=1
entrytime=0
file = open("E://UG//SpeedRecord.txt","w")
#file.write("ID \t SPEED  \t CURRENT START TIME \t  \tCURRENT END TIME\t\t VEHICLE TYPE \n--------\t---------- \t----------------\t \t-----------------------\t \t-------------------------\n")
file.write("ID \t SPEED \t ENTRY TIME \t \t EXIT TIME \t CURRENT START TIME \t \tCURRENT END TIME\t \t VEHICLE TYPE \n--------\t----------\t----------------------\t \t----------------\t \t-----------------------\t \t-------------------------\n")

file.close()
class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        #self.start = 0
        #self.stop = 0
##        self.et=0
        self.s1 = np.zeros((1,1000)) #start time 
        self.s2 = np.zeros((1,1000)) ##time difference
        self.s = np.zeros((1,1000))  ## speed
        self.f = np.zeros(1000)
        self.capf = np.zeros(1000)
        self.count = 0
        self.exceeded =0
        self.startTime=""
        

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        flagg=1  ##using to start timer
        #intitally flagg 1 when new obejct detected is true we set flagg 1 and in
        # in start timer range we just stop by saving ist instant of time.
        
        
        global entryflag
        global entrytime
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            
            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                
                if dist < 35:
                    self.center_points[id] = (cx, cy)
                    #print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    
                #START TIMER......
                if (y >= 15 and y <= 50):
                    self.s1[0,id] = time.time()
                    if(flagg):
                        self.startTime=time.asctime(time.localtime(time.time()))
                        flagg=0
                    if(entryflag):
                        entrytime= time.time()
                        entryflag=0
                #STOP TIMER and FIND DIFFERENCE
                if (y >= 90 and y <= 150):
                    self.s2[0,id] = time.time()
                    self.s[0,id] = self.s2[0,id] - self.s1[0,id]
                    #print("start time" + str(self.s1[0,id]))
                    print(self.s[0,id])
                    print(time.asctime(time.localtime(time.time())))
                   
                    #startEnd_Time.append(time.asctime(time.localtime(time.time())))
                #CAPTURE FLAG
                if (y<60):
                    self.f[id]=1
            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                self.s[0,self.id_count]=0
                self.s1[0,self.id_count]=0
                self.s2[0,self.id_count]=0
                flagg=1
                
                
                
                
                
                    

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

#SPEEED FUNCTION
    def getsp(self,id):
        if (self.s[0,id]!=0):
            s =  20.0/ self.s[0, id]
        else:
            s = 0

        return int(s)

    #SAVE VEHICLE DATA
    def capture(self,img,x,y,h,w,sp,Vehicle_type,id):
        if(self.capf[id]==0):
            self.capf[id] = 1
            self.f[id]=0
            #crop_img = img[y-5:y + h+5, x-5:x + w+5]
            #n = str(id)+"_speed_"+str(sp)
            #file = 'E://UG//' + n + '.jpg'
            #cv2.imwrite(file, crop_img)
            self.count += 1
            filet = open("E://UG//SpeedRecord.txt", "a")
            if(sp>limit):
                #file2 = 'E://UG//exceeded//' + n + '.jpg'
                #cv2.imwrite(file2, crop_img)
                filet.write(str(id)+"\t"+str(24)+ "\t" + str(self.s1[0,id]-entrytime) +"\t" + str(self.s2[0,id]-entrytime)+"\t"+ str(self.startTime)+ "\t" + str(time.asctime(time.localtime(self.s2[0,id])))+"\t" +str(Vehicle_type)+ "\n")
                self.exceeded+=1
            else:
                filet.write(str(id) + "\t" + str(sp) + "\t" + str(self.s1[0,id]-entrytime) +"\t" + str(self.s2[0,id]-entrytime)+"\t" + str(self.startTime)+ "\t" + str(time.asctime(time.localtime(self.s2[0,id])))+"\t" +str(Vehicle_type) + "\n")
                #time.asctime(time.localtime(time.time()))
            filet.close()


    #SPEED_LIMIT
    def limit(self):
        return limit

    #TEXT FILE SUMMARY
    def end(self):
        file = open("E://UG//SpeedRecord.txt", "a")
        file.write("\n-------------\n")
        file.write("-------------\n")
        file.write("SUMMARY\n")
        file.write("-------------\n")
        file.write("Total Vehicles :\t"+str(self.count)+"\n")
        file.write("Exceeded speed limit :\t"+str(self.exceeded))
        file.close()

