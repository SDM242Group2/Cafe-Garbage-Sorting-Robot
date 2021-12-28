import IRsensor
import time
import pigpio # sudo pigpiod 


irL = IRsensor.IRsensor(13)
irM = IRsensor.IRsensor(19)
irR = IRsensor.IRsensor(26)
while True:
    ir_left_near = irL.get_reading()
    ir_mid_near = irM.get_reading()
    ir_right_near = irR.get_reading()
    print(ir_left_near, ir_mid_near, ir_right_near)
    time.sleep(0.1)