import pigpio
import time

class IRsensor:
    instCnt = 0

    def __init__(self, BCMpin) -> None:
        IRsensor.instCnt += 1

        self.BCMpin = BCMpin
        self.io = pigpio.pi()
        self.io.set_mode(self.BCMpin, pigpio.INPUT)
        self.io.set_pull_up_down(self.BCMpin, pigpio.PUD_DOWN)
        pass

    def get_instCnt():
        return IRsensor.instCnt

    def get_reading(self):
        return self.io.read(self.BCMpin)