# Flash test

# 221018 - Started

from time import sleep
from machine import Pin, Timer

led = Pin(15)

gamma = [0, 256, 768, 2304, 5120, 9216, 15616, 23808, 34560, 47616, 65535]

class Flash():
    def __init__(self, p, conf=1000):
        self.conf = conf
        self.i = 0
        self.pin = p
        self.pin.init(Pin.OUT)
        self.pin.on()
        tim = Timer(period=self.conf[0], mode=Timer.ONE_SHOT, callback = self.nex)

    def nex(self, t):
        self.i += 1
        if self.i >= len(self.conf):
            self.i = 0
        if self.conf[self.i] != 0:
            self.pin.toggle()
            tim = Timer(period=self.conf[self.i], mode=Timer.ONE_SHOT, callback = self.nex)

f = Flash(led, [300, 300, 1000, 300, 0])

while True:
    sleep(10)
    
