# socket client
from PID import PID
import socket
import time
import datetime
import xlwt
import pymysql
from selfcontrol7550 import selfsail
db = pymysql.connect("192.168.0.105","root","root","star")#uncommon for database

ip_port=('192.168.31.63',7786)

# 封装协议（对象）
s = socket.socket()

# 向服务端建立连接
s.connect(ip_port)

pid = PID(0.2,0.1,0)
pid.SetPoint = 60
print('conected')

    
while True:
    Mode = input('選擇模式>>: ')
    send_data = str(Mode)
    s.send(bytes(str(send_data),encoding='utf8'))
    print('Mode:',Mode)
    if Mode == 'Mode1':
        # Set Boundary points
        x_init = 920#int(input('x_initial>>:'))#870 200
        y_down = 270#int(input('y_initial>>:'))
        #x = int(input('x>>')) #test
        #y = int(input('y>>')) #test
        x_right = x_init + 190 #right bound width 150, for tacking
        x_left = x_init - 230 #left bound width 460,for tailing wind
        y_up = y_down + 580 #y length,600
        # Initial Command
        C_LM = 1500 # Left Moter
        C_RM = 1500 # Right Moter
        C_R = 62 # Rudder
        C_S = 80 # Sail
        Initialization = 1
        sailmode = 1#sailmode for tacking
        # Creat a table and write the head of the table
        wb= xlwt.Workbook()
        ws=wb.add_sheet('Test')
        ws.write(0,0,'heading');ws.write(0,1,'x-axis');ws.write(0,2,'y-axis');
        ws.write(0,3,'speed_left');ws.write(0,4,'speed_right');ws.write(0,5,'sail angle');
        ws.write(0,6,'rudder angle');ws.write(0,7,'Bus Voltage');ws.write(0,8,'Bus Current');
        ws.write(0,9,'Power');ws.write(0,10,'Shunt Voltage');ws.write(0,11,'Time-hour');
        ws.write(0,12,'Time-minute');ws.write(0,13,'Time-second');
        i = 1
        try:
            while True:
                print('start')
                try:
                    #Read real location (x,y)
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM data WHERE id=1")#uncommon for database
                    data = cursor.fetchone()
                    x = int(data[5])#实时获取船x坐标
                    y = int(data[4])#实时获取船y坐标
                    while x==0 and y==0:
                        x = int(data[5])#实时获取船x坐标
                        y = int(data[4])#实时获取船y坐标
                        #print('location: x'+str(x)+' y'+str(y))

                    if Initialization == 1:
                        Initialization = 0
                    else:
                        pid.SetPoint, C_S, C_R, C_LM, C_RM, sailmode = selfsail(x,y,x_init,x_right,x_left,y_down,y_up,feedback,pid.SetPoint,C_LM,C_RM,C_R,pid.output,sailmode)

##                    if C_LM == 1500:
##                        C_LM_send = 0
##                    elif C_LM == 1560:
##                        C_LM_send = 1
##
##                    if C_RM == 1500:
##                        C_RM_send = 0
##                    elif C_RM == 1560:
##                        C_RM_send = 1
                        
                    # 发送消息
                    send_data = str(C_LM)+' '+str(C_RM)+' '+str(C_R)+' '+str(C_S)
                    s.send(bytes(str(send_data),encoding='utf8'))
                    #print('Command:',str(send_data))
                    #if send_data == 'exit': break  # 如果输入exit，则退出
                    
                    # 接收消息
                    recv_data = s.recv(1024) #接受船角度信息
                    feedback, LeftSpeed, RightSpeed, SailAngle, RudderAngle, BusVoltage, BusCurrent, Power, ShuntVoltage = (str(recv_data,encoding='utf8').split(' '))
                    feedback, LeftSpeed, RightSpeed, SailAngle, RudderAngle, BusVoltage, BusCurrent, Power, ShuntVoltage = float(feedback),float(LeftSpeed), float(RightSpeed), float(SailAngle), float(RudderAngle), float(BusVoltage), float(BusCurrent), float(Power), float(ShuntVoltage)
                    pid.update(feedback)
                    print('IMU angle:',feedback)
                    print(x,y,LeftSpeed,RightSpeed,RudderAngle)
                    # Print everything out.
                    ws.write(i,0,'{0:0.2F}'.format(feedback))
                    ws.write(i,1,str(x))
                    ws.write(i,2,str(y))
                    ws.write(i,3,'{0:0.2F}'.format(LeftSpeed))
                    ws.write(i,4,'{0:0.2F}'.format(RightSpeed))
                    ws.write(i,5,'{0:0.2F}'.format(SailAngle))
                    ws.write(i,6,'{0:0.2F}'.format(RudderAngle))
                    ws.write(i,7,'{0:0.2f}V'.format(BusVoltage))
                    ws.write(i,8,'{0:0.2f}mA'.format(BusCurrent))
                    ws.write(i,9,'{0:0.2f}mW'.format(Power))
                    ws.write(i,10,'{0:0.2f}mV'.format(ShuntVoltage))
                    t=datetime.datetime.now()
                    ws.write(i,11,str(t.hour))
                    ws.write(i,12,str(t.minute))
                    ws.write(i,13,str(t.second))

                    #print('(Voltage, Current): (',round(BusVoltage,3),',', round(BusCurrent,3),')')
                    i+=1
                except:
                    time.sleep(0.5)
                    print('\nSaving data...')
                    wb.save('%s .xls' % str(t).replace(':',','))
                    print('\nSaving successfully')
        except KeyboardInterrupt:
            time.sleep(0.5)
            print('\nSaving data...')
            wb.save('%s .xls' % str(t).replace(':',','))
            print('\nSaving successfully')

    elif Mode == 'Mode2':
        try:
            while True:
                # Input Command
                data = input('Command>>: ').strip()
                # 发送消息
                send_data = str(data)
                s.send(bytes(str(send_data),encoding='utf8'))
        except KeyboardInterrupt:
            time.sleep(0.5)
    
# 结束连接
s.close()

