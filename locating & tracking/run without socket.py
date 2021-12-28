from test3 import*

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
         
          
            if cv2.waitKey(1)=='q':
                break
            
a.close()
 
    

    
