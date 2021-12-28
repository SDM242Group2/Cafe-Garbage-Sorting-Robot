from sys import modules
import pigpio # sudo pigpiod 
import time
import threading
import vlc
import socket

import PAJ7620U2
import VL53L0X
import Serialing
import Ultrasonic
import IRsensor

#bcm
TRIG = 18
ECHO = 23

IR_LEFT = 13
IR_MID = 19
IR_RIGHT = 26

# in cm
ULT_FAR_LIMIT = 800
ULT_VALID_LIMIT = 2
ULT_NEAR_LIMIT = 30

TOF_VALID_LIMIT = 10
TOF_NEAR_LIMIT = 30

SAFE_COOL_TIME = 1
AVOID_TIME = 1

FACE_LEFT_LIMIT = -1
FACE_RIGHT_LIMIT = 1

global ir_left_near
ir_left_near = 0
global ir_mid_near
ir_mid_near = 0
global ir_right_near
ir_right_near = 0
global ir_all_near
ir_all_near = False
global ir_near
ir_near = False

global ult_d
ult_d = 0
global ult_near
ult_near = False

global tof_d
tof_d = 0
global tof_near
tof_near = False

global gesture
gesture = ""

global mode # manual, straight, auto.
mode = 'm'

global angle
angle = 0

global face_left
face_left = False
global face_right
face_right = True

global ges_wave_flag
ges_wave_flag = False

automode_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/automode.mp3")
excuseme_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/excuseme.mp3")
manualmode_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/manualmode.mp3")
seeyounextime_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/seeyounexttime.mp3")
startsorting_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/startsorting.mp3")
straightlinemode_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/straightlinemode.mp3")
thankyou_audio = vlc.MediaPlayer("file:///home/pi/Desktop/xiaoai/thankyou.mp3")

def average(list):
    sum = 0
    for i in list:
        sum += i
    return sum / len(list)

def compare_count(list, compare, value):
    sum = 0
    if compare == '=':
        for i in list:
            if i == value:
                sum += 1
    if compare == '>':
        for i in list:
            if i > value:
                sum += 1
    if compare == '<':
        for i in list:
            if i < value:
                sum += 1
    if compare == '>=':
        for i in list:
            if i >= value:
                sum += 1
    if compare == '<=':
        for i in list:
            if i <= value:
                sum += 1
    return sum

class ultThread(threading.Thread):
    # def _init_(self):
    #     threading.Thread._init_(self)
    #     # self.threadID = threadID
    #     # self.name = name
    #     # self.counter = counter
    
    def run(self):
        global ult_d
        global ult_near

        self.ult = Ultrasonic.Ultrasonic(TRIG, ECHO)
        
        interval_length  = 5
        interval = []
        ult_near_false_threshold = 5
        for i in range(0, interval_length):
            interval.append(self.ult.get_distance() * 100)
        while True:
            ult_d = self.ult.get_distance() * 100.0
            del interval[0]
            interval.append(ult_d)
            
            if compare_count(interval, '>', ULT_NEAR_LIMIT) >= ult_near_false_threshold:
                ult_near = False
            if ult_d <= ULT_NEAR_LIMIT:
                ult_near = True

class tofThread(threading.Thread):
    def run(self):
        global tof_d
        global tof_near

        tof = VL53L0X.VL53L0X()
        tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        timing = tof.get_timing()
        if (timing < 20000):
            timing = 20000
        print ("Timing %d ms" % (timing/1000))


        # defining interval
        interval_length  = 5
        interval = []
        tof_near_false_threshold = 5
        # get initial filling for the interval
        for i in range(0, interval_length):
            tof_d = tof.get_distance() / 10.0
            time.sleep(timing/1000000.00)
            interval.append(tof_d)
            time.sleep(0.1)
        while True:
            tof_d = tof.get_distance() / 10.0
            time.sleep(timing/1000000.00)
            del interval[0]
            interval.append(tof_d)

            # update tof_near
            if compare_count(interval, '>', TOF_NEAR_LIMIT) >= tof_near_false_threshold:
                tof_near = False
            if tof_d <= TOF_NEAR_LIMIT:
                tof_near = True
            if tof_d <= TOF_VALID_LIMIT:
                tof_near = False
            time.sleep(0.1)

class irThread(threading.Thread):
    def run(self):
        global ir_left_near
        global ir_mid_near
        global ir_right_near
        global ir_all_near
        global ir_near
        # reversed
        irL = IRsensor.IRsensor(IR_LEFT)
        irM = IRsensor.IRsensor(IR_MID)
        irR = IRsensor.IRsensor(IR_RIGHT)

        interval_length = 4
        interval = []
        ir_near_false_threshold = 4
        # initrial read for interval filling
        for i in range(0, interval_length):
            ir_left_near = irL.get_reading()
            ir_mid_near = irM.get_reading()
            ir_right_near = irR.get_reading()
            if ir_left_near == 0 or ir_mid_near == 0 or ir_right_near == 0:
                interval.append(True)
            else:
                interval.append(False)

        while True:
            # read 3 sensors
            ir_left_near = irL.get_reading()
            ir_mid_near = irM.get_reading()
            ir_right_near = irR.get_reading()
            # judge if any of ir get near
            if ir_left_near == 0 or ir_mid_near == 0 or ir_right_near == 0:
                ir_all_near = True
            else:
                ir_all_near = False
            
            # add status of ir_all_near
            del interval[0]
            interval.append(ir_all_near)  

            # set ir_near = False, if number of false int the interval reaches thershold
            if interval.count(False) >= ir_near_false_threshold:
                # set global ir_near = False, OK to go
                ir_near = False
            if ir_all_near == True:
                # set global ir_near = True, stop
                ir_near = True
            
            time.sleep(0.1)

class gesThread(threading.Thread):
    def run(self):
        global gesture
        ges = PAJ7620U2.PAJ7620U2()
        while True:
            gesture = ges.check_gesture()
            time.sleep(0.1)

class modeAudioThread(threading.Thread):
    def run(self):
        global mode
        mode_audio_flag = ""
        notification_audio_flag = ""
        while True:
            if mode == "s" and mode_audio_flag != "s":
                mode_audio_flag = "s"
                straightlinemode_audio.play()
                time.sleep(3)
                straightlinemode_audio.stop()
            elif mode == "m" and mode_audio_flag != "m":
                mode_audio_flag = "m"
                manualmode_audio.play()
                time.sleep(3)
                manualmode_audio.stop()
            elif mode == "a" and mode_audio_flag != "s":
                mode_audio_flag = "s"
                automode_audio.play()
                time.sleep(3)
                automode_audio.stop()

class notificationAudioThread(threading.Thread):
    def run(self):
        global ult_near
        global tof_near
        global ir_near
        global gesture
        global mode
        notification_audio_flag = ""

        while True:
            if (ult_near or tof_near) and mode == 's':
                excuseme_audio.play()
                time.sleep(4)
                excuseme_audio.stop()
            if gesture == "wave":
                thankyou_audio.play()
                time.sleep(2)
                thankyou_audio.stop()

class faceThread(threading.Thread):
     def run(self):
        global angle
        global face_left
        global face_right
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.1.113', 6666))   #链接刚刚绑定的ip和端口号
        while True:
            msg = s.recv(3)    #接收数据（字节数）
            msg = msg.decode('utf-8')   #解码
            if msg[0] == '0': # different from zyz
                angle = -int(msg[0:3])
            else:
                angle = int(msg[0:3]) # inverse form zyz
            
            if angle <= FACE_LEFT_LIMIT:
                face_left = True
                face_right = False
            elif angle >= FACE_RIGHT_LIMIT:
                face_left = False
                face_right = True
            else:
                face_left = False
                face_right = False

if __name__ == '__main__':
    srl = Serialing.Serialing()
    
    tofTrd = tofThread()
    tofTrd.start()
    # read sigal from ultrasonic sensors.
    ultTrd = ultThread()
    ultTrd.start()
    gesTrd = gesThread()
    gesTrd.start()
    # read signal from 3 IR sensors
    irTrd = irThread()
    irTrd.start()
    modeAudioTrd = modeAudioThread()
    modeAudioTrd.start()
    notificationAudioTrd = notificationAudioThread()
    notificationAudioTrd.start()
    faceTrd = faceThread()
    faceTrd.start()

    # read signal from facial recognition raspi
    
    # no "global" needed for accessing global vars.

    # for cooling down
    ir_near_flag = False
    d_near_flag = False

    # MAIN LOOP STARTS HERE
    while True:
        # read serial string threading
        mode = srl.read_string_message()

        if mode == 's': # straight line mode, joy stick up
            # play audio
            # if mode_audio_flag != "s":
            #     straightlinemode_audio.play()
            #     mode_audio_flag = "s"

            if ult_near or tof_near:
                # detect human, stop
                # if notification_audio_flag != "excuseme":
                #     excuseme_audio.play()
                #     notification_audio_flag = "excuseme"
                srl.stop()
                d_near_flag = True
            elif gesture != "" and gesture != None:
                print(gesture)
                # detect human gesture, stop
                srl.stop()
                d_near_flag = True # need to add and change to gestrue detected flag!
                gesture = ""
            else:
                # cool down
                if d_near_flag:
                    srl.stop()
                    time.sleep(SAFE_COOL_TIME)
                    d_near_flag = False
                    continue
                    
                # go right
                if ir_near:
                    srl.go_x(Serialing.LOW_SPEED)
                    ir_near_flag = True
                    continue

                # keep going right for a short amount of time
                if ir_near_flag:
                    srl.go_x_t(Serialing.LOW_SPEED, AVOID_TIME)
                    ir_near_flag = False
                    continue

                # not near, after after cool time or avoid time, go forward
                srl.go_y(Serialing.LOW_SPEED)
                time.sleep(0.05)
                
        elif mode == 'a': # auto mode, joy stick down
            # play audio
            # if mode_audio_flag != "a":
            #     automode_audio.play()
            #     mode_audio_flag = "a"

            # Facial Tracking
            # play audio
            # if mode_audio_flag != "m":
            #     manualmode_audio.play()
            #     mode_audio_flag = "m"
            if ult_near or tof_near:
                # detect human, stop
                # if notification_audio_flag != "excuseme":
                #     excuseme_audio.play()
                #     notification_audio_flag = "excuseme"
                srl.stop()
                d_near_flag = True

            if gesture == "wave":
                print(gesture)
                srl.stop()
                ges_wave_flag = True
                gesture = ""
                srl.go_y(-Serialing.LOW_SPEED)
                time.sleep(5)

            # cool down
            if d_near_flag:
                srl.stop()
                time.sleep(SAFE_COOL_TIME / 10)
                d_near_flag = False
                continue

            if face_left:
                srl.turn(-Serialing.LOW_SPEED - 100)
            elif face_right:
                srl.turn(Serialing.LOW_SPEED - 100)
            else:
                srl.go_y(Serialing.LOW_SPEED)
            time.sleep(0.05)
            pass

        elif mode == 'm': # manual mode, joy stick mid
            pass

        time.sleep(0.05)

# tof.stop_ranging()
# tof.close()