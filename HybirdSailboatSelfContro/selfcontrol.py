#大角度开电机
def motor(heading,setting,C_LM,C_RM):
    deltaangle = heading-setting
    if deltaangle>180:
        deltaangle = deltaangle -360
    elif deltaangle<-180:
        deltaangle = deltaangle +360

    if deltaangle>60:
        if C_RM != 1560:
            C_RM = 1560#right
            C_LM = 1500
    elif deltaangle<-60:
        if C_LM != 1560:
            C_LM = 1560#left
            C_RM = 1500
    else:
        C_LM = 1500
        C_RM = 1500
    return C_LM, C_RM

def pidrudder(pidoutput,C_R):
    pidoutput=round(pidoutput,2)
    if pidoutput>0:
        if pidoutput<6:
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
        else:
            pidoutput=6
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
    elif pidoutput<0:
        if pidoutput>-6:
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
        else:
            pidoutput=-6
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
    return int(C_R)

def tailwind(x_now,x_left,heading,setting,C_LM,C_RM,pidoutput,C_R):
    if x_now < x_left and setting == -120:
        setting = 120
        print('Backward 2')
    C_S = 60
    C_R = pidrudder(pidoutput,C_R)
    C_LM, C_RM = motor(heading,setting,C_LM,C_RM)
    return setting, C_S, C_R, C_LM, C_RM

def tacking(heading,setting,x_now,x_init,x_right):
    changingangle=10
    C_LM=1500
    C_RM=1500
    C_R=62
    #rudder & close motor(by angle) 
    if setting==60:
        if heading>=changingangle:#condition to change rudder
            C_R=102
            C_LM=1500
            C_RM=1500
            print('正常右tacking')
        elif heading<changingangle:
            C_R=22
            print('刚刚右tacking')
    elif setting==-60:
        if heading<=-changingangle:
            C_R=22
            C_LM=1500
            C_RM=1500
            print('正常左tacking')
        else:
            C_R=102
            print('刚刚左tacking')

    #open motor (by location)
    if x_now>=x_right:
        setting=-60
        C_RM=1560
    elif x_now <= x_init:
        setting=60
        C_LM=1560
    C_S=80
    print('heading'+str(heading))
    return setting, C_S, C_R, C_LM, C_RM

def selfsail(x_now,y_now,x_init,x_right,x_left,y_down,y_up,heading,setting,C_LM,C_RM,C_R,pidoutput,sailmode):
    # 逆风折线
    #sailmode = 1 # tacking mode
    if y_now > y_up and sailmode == 1:
        sailmode = 0
        setting=-120
        print('Backward 1')
    elif y_now < y_down and sailmode == 0:
        sailmode = 1
        setting = 60

    if sailmode == 1:
        setting, C_S, C_R, C_LM, C_RM = tacking(heading,setting,x_now,x_init,x_right)
    elif sailmode ==0:
        setting, C_S, C_R, C_LM, C_RM = tailwind(x_now,x_left,heading,setting,C_LM,C_RM,pidoutput,C_R)

    return setting, C_S, C_R, C_LM, C_RM, sailmode
