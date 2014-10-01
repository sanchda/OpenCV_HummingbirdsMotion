#Following Swinnen (2014) from:
###A Novel Method to Reduce Time Investment When Processing Videos from Camera Trap Studies###

#Import Libraries
import cv2 
import numpy as np
import argparse
import os
from shapely.ops import cascaded_union
import shapely.geometry as sg
import SwinnenSource


#Define command line arguments
parser = argparse.ArgumentParser()

#Video file
parser.add_argument("-f", help="path of single video",type=str,default="C:/Program Files (x86)/MotionMeerkat/PlotwatcherTest.tlv")
#threshold for variance
parser.add_argument("-t", help="threshold",type=int)

#f="C:/Program Files (x86)/MotionMeerkat/PlotwatcherTest.tlv"
#f ='C:/Users/Ben/Documents/OpenCV_HummingbirdsMotion/ReviewDocuments/tinyshark.avi'
#f='C:\Users\Ben\Dropbox\Thesis\Automated_Monitering\sharkpass2.avi'
f ='C:/Users/Ben/Desktop/MotionMeerkatTest/Rees.avi'

#read in video file
cap=cv2.VideoCapture(f)

#get info of file
#read in frame 
_,img=cap.read()

##Initiate two background subtractors
motion=SwinnenSource.MotionM(f,5,0.25)
mog=SwinnenSource.MOG(f,1000,15)

cap=cv2.VideoCapture(f)

##Output location
#file destination folder
dest="C:/MotionMeerkat/"

#make folder to hold output using the file name
flname=os.path.splitext(os.path.basename(f))[0]
outdr=os.path.join(dest,flname)   

#make folder
if not os.path.exists(outdr): os.mkdir(outdr)
    
vidname=os.path.join(dest,flname,"Comparison.avi")

height=np.size(img,1)
width=np.size(img,0)

codec=cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter(vidname,codec,20,(height,width),True)    
                         
##Capture next frame, if there is no next frame; break.
counter=0
while (1):
    counter=counter+1    
    print(counter)
    ret,i = cap.read()
    if not ret:
        break
    m=motion.accAvg(img=i,towrite=i)
    g=mog.run(img=i,towrite=m)
    p=os.path.join(outdr,str(counter) +".jpg")
    cv2.imwrite(p, g)
    out.write(g)

out.release()
cv2.destroyAllWindows()        
