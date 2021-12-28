import time
import serial

SERIAL_GAP = 0.1 # Seconds between sending two messages. Avoiding Crashing.
ACCELERATION = 660 # value change per second
TOP_SPEED = 660
HIGH_SPEED = 440
MID_SPEED = 330
LOW_SPEED = 200

class Serialing:
    # varibles for all instances here
    instCnt = 0

    def __init__(self) -> None:
        Serialing.instCnt += 1

        # instance varibles here:
        self.spdNow = [0, 0, 0]

        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout = 5)
        pass

    def get_instCnt():
        return Serialing.instCnt

    def get_spdNow(self):
        return self.spdNow

    def update_spdNow(self, y, x, turn):
        self.spdNow[0] = y
        self.spdNow[1] = x
        self.spdNow[2] = turn

    def read_string_message(self):
        read_str = self.ser.readline()
        self.ser.reset_input_buffer()
        return read_str.decode("utf-8").strip()

    def to_string_message(self, y, x, turn):
        # convert to "XXXX"
        y4Char = ("00" + str(abs(y)))[-3:] # trim the last 3 digits, making sure it is 3 digits by filling 0s.
        x4Char = ("00" + str(abs(x)))[-3:]
        turn4Char = ("00" + str(abs(turn)))[-3:]

        yStr = ("0" if y >= 0 else "1") + y4Char
        xStr = ("0" if x >= 0 else "1") + x4Char
        turnStr = ("0" if turn >= 0 else "1") + turn4Char

        # concate to "XXXX XXXX XXXX" by adding spaces in between
        return yStr + " " + xStr + " " + turnStr
    
    def send_speed(self, y, x, turn):
        self.ser.write(self.to_string_message(y, x, turn).encode())
        self.update_spdNow(y, x, turn)

    def send_speed_t(self, y, x, turn, t): # t for second
        # startTime = time.time()
        # while(time.time() - startTime <= t):
        #     self.ser.write(self.to_string_message(y, x, turn).encode())
        #     self.update_spdNow(y, x, turn)
        #     time.sleep(SERIAL_GAP)
        # self.stop()

        self.ser.write(self.to_string_message(y, x, turn).encode())
        self.update_spdNow(y, x, turn)
        time.sleep(t)
        self.stop()

    def go_y(self, y):
        self.send_speed(y, 0, 0)

    def go_y_t(self, y, t):
        self.send_speed_t(y, 0, 0, t)
    
    def go_x(self, x):
        self.send_speed(0, x, 0)

    def go_x_t(self, x, t):
        self.send_speed_t(x, 0, 0, t)

    def turn(self, turn):
        # negative for left, positive for right
        self.send_speed(0, 0, turn)

    def stop(self):
        self.ser.write(self.to_string_message(0, 0, 0).encode())
        self.update_spdNow(0, 0, 0)
        time.sleep(0.1)

    def emergency_stop(self):
        self.stop()
        time.sleep(SERIAL_GAP)
        self.stop()
        time.sleep(SERIAL_GAP)
        self.stop()

    def isRamping():
        return True

    def set_speed(self, y, x, turn):
        startTime = time.time()
        while(self.isRamping()):
            pass
        self.send_speed(self, y, x, turn)