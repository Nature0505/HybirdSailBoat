import RPi.GPIO as GPIO
import pigpio
import os
import time

class sailboat:
    def __init__ (self,ESC1,ESC2,initialspeed1,initialspeed2,Servo1,Servo2,initialangle1,initialangle2):
        self.__ESC1=ESC1#control left motor
        self.__ESC2=ESC2#right motor
        self.__initialspeed1=initialspeed1
        self.__initialspeed2=initialspeed2
        self.__Servo1=Servo1#left servo
        self.__Servo2=Servo2#right servo
        self.__initialangle1=initialangle1
        self.__initialangle2=initialangle2
##        os.system('sudo pigpiod')
##        os.system('sudo pigpiod')
        self.__pi=pigpio.pi()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__Servo1, GPIO.OUT, initial=False)
        GPIO.setup(self.__Servo2, GPIO.OUT, initial=False)
        self.__servocopy1=0#in order to check the angle difference of 2 sequencial requests
        self.__servocopy2=0
        self.__motorcopy1=0
        self.__motorcopy2=0
        
    def servoturning(self, servo, angle):
        try:
            if servo==self.__Servo1 or servo==self.__Servo2:
                if servo==self.__Servo1:
                    angle=float(angle)
                    delay= 5+(angle/180)*20
                    if abs(self.__servocopy1-angle)>100:
                            k=18
                    elif 50<abs(self.__servocopy1-angle)<=100:
                        k=12
                    else:
                        k=6
                    self.__servocopy1=angle
                elif servo==self.__Servo2:
                    angle=float(angle)
                    delay= 5+(angle/180)*20
                    if abs(self.__servocopy2-angle)>100:
                            k=18
                    elif 50<abs(self.__servocopy2-angle)<=100:
                        k=12
                    else:
                        k=6
                    self.__servocopy2=angle
                for i in range (1,k):
                    time.sleep(0.02)
                    GPIO.output(servo,GPIO.HIGH)
                    time.sleep(0.0001*delay)
                    GPIO.output(servo,GPIO.LOW)
            else:
                return False
        except:
            print('Error in TURNING')

    def rudderrunning(self, servo, angle):
        try:
            if servo==self.__Servo2:
                angle=float(angle)
                delay=5+(angle/180)*20
                if abs(copy2-angle)>100:
                    k=18
                elif 50<abs(copy2-angle)<=100:
                    k=12
                else:
                    k=6
                for i in range (1,k):
                    time.sleep(0.02)
                    GPIO.output(Servopin2,GPIO.HIGH)
                    time.sleep(0.0001*delay)
                    GPIO.output(Servopin2,GPIO.LOW)
                copy2=angle
            else:
                return False
        except:
            print('Error in TURNING')
    
    def motorruning(self, ESC, speed):
        try:
            if ESC==self.__ESC1 or ESC==self.__ESC2:
                if ESC==self.__ESC1:
                    self.__motorcopy1=speed
                else:
                    self.__motorcopy2=speed
                self.__pi.set_servo_pulsewidth(ESC,speed)     
            else:
                return False
        except:
            print('Error in CHANGING SPEED')
    def initialization(self):
        self.servoturning(self.__Servo1,self.__initialangle1)
        self.servoturning(self.__Servo2,self.__initialangle2)
        self.motorruning(self.__ESC1,self.__initialspeed1)
        self.motorruning(self.__ESC2,self.__initialspeed2)
    def getangle(self):
        return round(self.__servocopy1,3),round(self.__servocopy2,3)
    def getspeed(self):
        return self.__motorcopy1,self.__motorcopy2

if __name__=='__main__':
    k=sailboat(21,20,1000,1000,16,26,90,90)
    k.initialization()
    print('speed:'+str(k.getspeed()))
    print('angle:'+str(k.getangle()))
    
