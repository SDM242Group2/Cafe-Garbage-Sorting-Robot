from __future__ import division
import importlib,sys
importlib.reload(sys)
from multiprocessing import Pool
import cv2
import time  
import numpy as np
import Adafruit_PCA9685
import threading
import os
class test3(object):
   
    #global error_x, error_y, last_error_x, last_error_y, pid_X_P, pid_Y_P

    error_x=500            #当前误差值
    last_error_x=100       #上一次误差值
    error_y=500
    last_error_y=100
    # 舵机的转动角度(初始转动角度)
    pid_Y_P = 100
    pid_X_P = 300 
    area=0
            
    
        # 初始化PCA9685和舵机
    def Servo_Init(self):
        
        self.servo_pwm = Adafruit_PCA9685.PCA9685()  # 实例话舵机云台
        
        # 设置舵机初始值，可以根据自己的要求调试
        self.servo_pwm.set_pwm_freq(50)  # 设置频率为60HZ
        self.servo_pwm.set_pwm(5,0,350)  # 底座舵机
        self.servo_pwm.set_pwm(4,0,330)  # 倾斜舵机
        time.sleep(1)
    
    
      # 摄像头初始化
    def Capture_Init(self):
        #初始化摄像头并设置阙值
        
        
        self.capture = cv2.VideoCapture(0)


        
        # 设置显示的分辨率，设置为320×240 px（即摄像头大小）
        self.capture.set(3, 320)
        self.capture.set(4, 240)
        
    # 舵机旋转
    def Robot_servo(self):


        self.servo_pwm.set_pwm(5,0,540 - self.pid_X_P)
        self.servo_pwm.set_pwm(4,0,430 - self.pid_Y_P)
    
    def getservoX(self):
        a=540-self.pid_X_P
        b=' '
        if(a>154 and a<225):
            b="102"
        elif(a>224 and a<276):
            b='101'
        elif(a>275 and a<310):
            b='000'
        elif(a>309 and a<370):
            b='001'
        elif(a>369 and a<431):
            b='002'
    
        return(b)

    def getarea(self):
        return(str(self.area/404))
    
    def getservoY(self):
        c=430-self.pid_Y_P
        d=0
        if(c<414 and c>390):
            d=1
        elif(c<391 and c>375):
            d=2
        elif(c<376 and c>335):
            d=3
        elif(c<336 and c>275):
            d=4
        elif(c<276 and c>258):
            d=5
        elif(c<259):
            d=6
        return(str(d))
    # 1 识别人脸
    def Face_Detect(self):
        # 1 实例化官方训练好的人脸识别器
        face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/PCA9685/haarcascades/haarcascade_frontalface_default.xml')
    
        # 2 获取每帧图像
        ret,frame = self.capture.read()
        #cv2.imshow('frame', frame)
        image = frame
        
        # 3 转灰度图

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray', gray)
        
        # 4 人脸检测
        faces = face_cascade.detectMultiScale(gray, 1.3, 1)
        
        # 5 获取人脸坐标并在图像上框出人脸
        try:
            x,y,w,h = faces[0]
            #print(x,y)
            cv2.rectangle(image, (x,y),(x+w,y+h), (255,0,255),3)
            cv2.imshow('image',image)
            self.area=w*h
            return (x+w/2, y+h/2)
        except:
            return (0, 0)
  
    # 2 PID舵机控制（这里分别设置使用PID和不用PID的情况）
    def PID_Servo_Control(self,x, y):
        
        # 下面开始pid算法：
        # pid总公式：PID = Uk + KP*【E(k)-E(k-1)】 + KI*E(k) + KD*【E(k)-2E(k-1)+E(k-2)】 
        # 这里只用到了p，所以公式为：P = Uk + KP*【E(k)-E(k-1)】
        # uk:原值   E(k):当前误差   KP:比例系数   KI:积分系数   KD:微分系数
        
        # 使用PID（可以发现舵机云台运动比较稳定）
        
        # 1 获取误差(x和y方向)（分别计算距离x、y轴中点的误差）
        error_x = -x + 160   # width:160
        error_y = y - 120   # height:120
        #define die region
        if abs(error_x)<5:
            error_x=0
        if abs(error_y)<5:
            error_y=0
        # 2 PID控制参数
        pwm_x = error_x*2 + (error_x - self.last_error_x)*13
        pwm_y = error_y*3 + (error_y - self.last_error_y)*13
        
        # 这里pwm（p分量） = 当前误差*3 + 上次的误差增量*1
    
        # 3 保存本次误差，以便下一次运算
        self.last_error_x = error_x
        self.last_error_y = error_y
        
        # 4 最终PID值（舵机旋转角度）
        self.pid_X_P -= int(pwm_x/70)
        self.pid_Y_P -= int(pwm_y/70)
        
        #print(pid_X_P,pid_Y_P)
        # p(pid的p) = 原值 + p分量
        

        
        # 5 限值(0~650)
        if self.pid_X_P>385:
            self.pid_X_P=385
        if self.pid_X_P<110:
            self.pid_X_P=110
        if self.pid_Y_P>330:
            self.pid_Y_P=330
        if self.pid_Y_P<15:
            self.pid_Y_P=15
    '''
    def run(self):
        # 摄像头初始化
        self.Capture_Init()
        # 舵机初始化
        self.Servo_Init()
        while True:
            (x, y) = self.Face_Detect()
            
            # 识别到人脸
            if  (x!=0 and y!=0):
                # 2 PID舵机控制
                self.PID_Servo_Control(x, y)
                self.Robot_servo()
                

                
            # 多线程处理（舵机控制）
            servo_tid = threading.Thread(target=self.Robot_servo) 
            #                                   函数               参数
            servo_tid.setDaemon(True)   # 设置守护线程，防止程序无限挂起
            servo_tid.start()           # 开启线程
            if cv2.waitKey(1)=='q':
                break
    

        capture.release()
        cv2.destroyAllWindows()
        '''
    def close(self):
        self.capture.release()
        cv2.destroyAllWindows()