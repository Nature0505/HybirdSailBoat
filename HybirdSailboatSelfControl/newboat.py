import RPi.GPIO as GPIO
import pigpio
import os
import time

ESC1 = 21
ESC2 = 20
Servopin1 = 16
Servopin2 = 26

speed1=1500
speed2=1500
os.system('sudo pigpiod')
os.system('sudo pigpiod')
pi=pigpio.pi()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(Servopin1, GPIO.OUT, initial=False)
GPIO.setup(Servopin2, GPIO.OUT, initial=False)
copy1=0
copy2=0

while True:
    try:
        pi.set_servo_pulsewidth(ESC1,speed1)
        pi.set_servo_pulsewidth(ESC2,speed2)
        data=str(input("Input the demand:"))
        if len(data)==1:
            if data=='a':
                speed1=1550
                speed2=1550
                print('run')
            elif data=='s':
                speed1+=10
            elif data=='x':
                speed1-=10
            elif data=='d':
                speed2+=10
            elif data=='c':
                speed2-=10
            elif data=='w':
                speed1=1550
            elif data=='e':
                speed2=1550
            else:
                speed1=1500
                speed2=1500
            time.sleep(0.02)
            print('speed1'+str(speed1))
            print('speed2'+str(speed2))
        else:
            if data[0]=='s':
                angle=float(data[1:])
                delay=5+(angle/180)*20
                if abs(copy1-angle)>100:
                    k=18
                elif 50<abs(copy1-angle)<=100:
                    k=12
                else:
                    k=6
                for i in range (1,k):
                    time.sleep(0.02)
                    GPIO.output(Servopin1,GPIO.HIGH)
                    time.sleep(0.0001*delay)
                    GPIO.output(Servopin1,GPIO.LOW)
                copy1=angle
            elif data[0]=='r':
                angle=float(data[1:])
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
            print('sail'+str(copy1))
            print('rudder'+str(copy2))            
                    
        continue
    except:
        print('ERROR')
