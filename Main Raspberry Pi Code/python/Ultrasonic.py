import pigpio # sudo pigpiod 
import time

class Ultrasonic:
    instCnt = 0
    
    def __init__(self, trig, echo) -> None:
        Ultrasonic.instCnt += 1

        self.trig = trig
        self.echo = echo

        self.io = pigpio.pi()
        self.io.set_mode(self.trig, pigpio.OUTPUT)
        self.io.set_mode(self.echo, pigpio.INPUT)
        self.io.set_pull_up_down(self.echo, pigpio.PUD_DOWN)

        # varibles for instance:
        self.distance = 0
        self.high_tick = None

        self.cbf = self.io.callback(echo, pigpio.EITHER_EDGE, self.callbackFunc)
        pass

    def get_instCnt():
        return Ultrasonic.instCnt

    def callbackFunc(self, gpio, level, tick):
        if level == 0: # echo line changed from high to low.
            if self.high_tick is not None:
                echoTick = pigpio.tickDiff(self.high_tick, tick)
                #  cms = (echoTick / 1000000.0) * 34030 / 2
                self.distance = (echoTick / 1000000.0) * 340.30 / 2
                #  print("echo was {} micros long ({:.1f} cms)".format(echoTick, cms))
        else:
            self.high_tick = tick

    def get_distance(self):
        self.io.gpio_trigger(self.trig, 15)
        time.sleep(0.1)
        return self.distance

# while True:
#     print(radarDis())
#     time.sleep(0.5)


# cbf.cancel()
# io.stop()