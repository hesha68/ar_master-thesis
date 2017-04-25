from math import pi, sin, cos 

from direct.showbase.ShowBase import ShowBase 
from direct.task import Task 
from direct.actor.Actor import Actor 
from direct.interval.IntervalGlobal import Sequence 
from panda3d.core import Point3 

from ctypes import *

import sys
import socket

class MyApp(ShowBase):
   def __init__(self): 
      ShowBase.__init__(self) 
     
      #Load the environment model
      self.environ = self.loader.loadModel("models/environment") 
      #Reparent the model to render.
      self.environ.reparentTo(self.render) 
      #Apply scale and position transforms on the model
      self.environ.setScale(0.25, 0.25, 0.25) 
      self.environ.setPos(-8, 42, 0) 
      
      #Add the spinCamera procedure to the task manage
      self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")  

      #Load and transform the panda actor
      self.pandaActor = Actor ("models/panda-model", 
                         {"walk":  "models/panda-walk4"}) 
      self.pandaActor.setScale(0.005, 0.005, 0.005) 
      self.pandaActor.reparentTo(self.render)
      #Loop its animation
      self.pandaActor.loop("walk")
      #print("Press Enter to quit ....")
      #chr=sys.stdin.read(1)
      #exit(0)
      

   def spinCameraTask(self,task):
       #Call Phidget data
       #spatial.setOnSpatialDataHandler(SpatialGyro)
    
       HOST = "127.0.0.1"
       PORT= 5000

       ## set up a UDP server
       mySocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

       #Listen on port 
       # to all IP address on this system
       mySocket.bind (( HOST, PORT ))

       packet, address = mySocket.recvfrom(1024)

       ## receive packet
       print "Packet received:"
       print "From host:", address[ 0 ]
       print "Host port:", address[ 1 ]
       print "Length:", len( packet )
       print "Containing:"
       print "\t" + packet


       orientationData=packet.split()
       print(orientationData)
       P=orientationData[1]
       R=orientationData[2]
       H=orientationData[0]
       X=orientationData[3]
       Y=orientationData[4]
       Z=orientationData[5]

       H=float(H)
       P=float(P)
       R=float(R)
       X=float(X)
       Y=float(Y)

       print "\nEcho data to client...",
       mySocket.sendto( packet, address )
       print "Packet sent\n"

       mySocket.close()
       
       angleDegreesPitch=P
       angleDegreesRoll=R
       angleDegreesHeading=H
       self.camera.setPos(X,Y,3)
       self.camera.setHpr(angleDegreesHeading,angleDegreesPitch,angleDegreesRoll)
       return Task.cont
       
app = MyApp()
app.run()
