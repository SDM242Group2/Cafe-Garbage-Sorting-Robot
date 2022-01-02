from test3 import*
import time
import socket
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.113', 6666))  #绑定ip和端口号（IP为发送数据的树莓派ip，端口号自己指定）
print("a")
s.listen(5)
print("b")
c, address = s.accept()      #等待别的树莓派接入
print("c")
a=test3()
a.Capture_Init()
a.Servo_Init()
while True:
            
            (x, y) = a.Face_Detect()
            
            # 识别到人脸
            if  (x!=0 and y!=0):
                # 2 PID舵机控制
                a.PID_Servo_Control(x, y)
                a.Robot_servo()
                

                
            # 多线程处理（舵机控制）
            servo_tid = threading.Thread(target=a.Robot_servo) 
            #                                   函数               参数
            servo_tid.setDaemon(True)   # 设置守护线程，防止程序无限挂起
            servo_tid.start()           # 开启线程
            #xh=int(float(a.getservoX()))
            #yh=int(float(a.getservoY()))
            #rea=int(float(a.getarea()))
            msg=a.getservoX()
            c.send(msg.encode('utf-8'))   #编码
            if cv2.waitKey(1)=='q':
                break
            
a.close()
s.close()    
    

    