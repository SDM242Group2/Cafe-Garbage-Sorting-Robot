import RPi.GPIO as GPIO
import pigpio
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pi=pigpio.pi()
servo0=20 #设定零号舵机的引脚编号 
servo1=4 #设定一号舵机的引脚编号
servo2=22 #设定二号舵机的引脚编号
servo3=25 #设定三号舵机的引脚编号
servo4=12 #设定四号舵机的引脚编号
senser=26 #设定传感器的引脚编号
ray=27 #设定红外对射模块的引脚编号

def conveyorServos(servoPin,dutycycle):
    pi.write(servoPin, 0) # BCM 将引脚设置为低电平
    pi.read(servoPin)
    pi.set_PWM_frequency(servoPin, 300)#设定引脚产生的pwm波形的频率为50Hz
    pi.set_PWM_range(servoPin, 2500)
    pi.set_PWM_dutycycle(servoPin,dutycycle)

def rodServo(servoPin,dutycycle):
    pi.write(servoPin, 0) # BCM 将引脚设置为低电平
    pi.read(servoPin)
    pi.set_PWM_frequency(servoPin, 50)#设定引脚产生的pwm波形的频率为50Hz
    pi.set_PWM_range(servoPin, 2000)
    pi.set_PWM_dutycycle(servoPin,dutycycle)
    time.sleep(0.5)

def senerAndRod(senserPin,servoPin):
    GPIO.setup(senserPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        status =GPIO.input(senserPin)
        print (status)
        if status==0:   
            # rodServo(servoPin,0)
            # time.sleep(0.2)  
            time.sleep(0.8)
            rodServo(servoPin,40) #舵机转到推杆能推出去的位置
            time.sleep(1)  
            rodServo(servoPin,0)
            time.sleep(0.2) 
            rodServo(servoPin,250) #舵机回到原来不推的位置
            time.sleep(0.2) 
            rodServo(servoPin,0)
            time.sleep(0.8)
        time.sleep(0.2)


def garbageDetection(rayPin):
    GPIO.setup(rayPin,GPIO.IN)
    while True:
        if GPIO.input(rayPin):
            return 1 #检测到垃圾，返回数字1
        else:
            return 0 #没检测到垃圾，返回数字0
        time.sleep(0.1)


def main():
    while True:
        GarbageIn=garbageDetection(ray)
        if GarbageIn==1: #检测到垃圾
            conveyorServos(servo1,600)
            conveyorServos(servo2,600)
            conveyorServos(servo3,600)
            time.sleep(0.2)
            conveyorServos(servo3,800)
            conveyorServos(servo4,2000)
            time.sleep(0.2)
            conveyorServos(servo4,1700)
            senerAndRod(senser,servo0)
        time.sleep(0.5)

         


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) Bye!\n")
        sys.exit(0)
