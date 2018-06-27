from boatclass import sailboat
import RPi.GPIO as GPIO
import pigpio
import os
import time

newboat = sailboat(21,20,1500,1500,16,26,100,60)
print(newboat.getspeed())
newboat.initialization
print(newboat.getspeed())
#newboat.motorruning(21,1550) #left

time.sleep(1)
newboat.motorruning(21,1500)
print(newboat.getspeed())
