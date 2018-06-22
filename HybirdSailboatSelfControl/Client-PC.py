# socket client
from PID import PID
import socket
import time
import pymysql
from selfcontrol import selfsail
db = pymysql.connect("192.168.0.105","root","root","star")

cursor = db.cursor()
cursor.execute("SELECT * FROM data WHERE id=1")
data = cursor.fetchone()
#
ip_port=('192.168.31.63',7786)

# 封装协议（对象）
s = socket.socket()

# 向服务端建立连接
s.connect(ip_port)

##x_int = data[5]#实时获取船x坐标
##y_int = data[4]#实时获取船y坐标
##x_ter = x_ini - 400
##y_ter = y_ini + 600
##print(x_int,y_int,x_ter,y_ter)


pid = PID(0.2,0.1,0)
pid.SetPoint = 60
print('conected')

    
while True:
    Mode = input('選擇模式>>: ')
    send_data = str(Mode)
    s.send(bytes(str(send_data),encoding='utf8'))
    print('Mode:',Mode)
    if Mode == 'Mode1':
        x_init = int(input('x_initial>>:'))
        y_down = int(input('y_initial>>:'))
        x_right = x_init + 230
        x_left = x_init - 460
        y_up = y_down + 600
        #print(x_init,x_r,x_l,y_init,y_u)
        C_LM = 1500 # Left Moter
        C_RM = 1500 # Right Moter
        C_R = 62 # Rudder
        C_S = 80 # Sail
        Initialization = 1
        sailmode = 1
        try:
            while True:
                # 设定方向
                cursor = db.cursor()
                cursor.execute("SELECT * FROM data WHERE id=1")
                data = cursor.fetchone()
                x = int(data[5])#实时获取船x坐标
                y = int(data[4])#实时获取船y坐标
                print('location: x'+str(x)+' y'+str(y))

                if Initialization == 1:
                    Initialization = 0
                else:
                    pid.SetPoint, C_S, C_R, C_LM, C_RM, sailmode = selfsail(x,y,x_init,x_right,x_left,y_down,y_up,feedback,pid.SetPoint,C_LM,C_RM,C_R,pid.output,sailmode)

                # 发送消息
                send_data = str(C_LM)+' '+str(C_RM)+' '+str(C_R)+' '+str(C_S)
                s.send(bytes(str(send_data),encoding='utf8'))
                print('Command:',str(send_data))
                #if send_data == 'exit': break  # 如果输入exit，则退出
                
                # 接收消息
                recv_data = s.recv(1024) #接受船角度信息
                feedback = float(str(recv_data,encoding='utf8'))
                pid.update(feedback)
                print('IMU angle:',feedback)
        except KeyboardInterrupt:
            time.sleep(0.5)

    elif Mode == 'Mode2':
        try:
            while True:
                # 设定方向
                data = input('Cammand>>: ').strip()
                # 发送消息
                send_data = str(data)
                s.send(bytes(str(send_data),encoding='utf8'))
        except KeyboardInterrupt:
            time.sleep(0.5)
    
# 结束连接
s.close()

