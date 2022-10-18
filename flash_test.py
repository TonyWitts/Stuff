# Flash test

# 221018 - Started

from time import sleep
from machine import Pin, PWM, Timer

led = Pin(15)
onboard = Pin('LED')

gamma = [0, 256, 768, 2304, 5120, 9216, 15616, 23808, 34560, 47616, 65535]

class Flash():
    def __init__(self, pin, conf=1000):
        self.conf = conf
        if len(self.conf) % 2 > 0:
            self.conf.append(0)
        self.i = 0
        #self.pin= pin
        #self.pin.init(Pin.OUT)
        self.pin = PWM(pin)
        self.pin.freq(1000)
        self.tim = ''
        if type(conf) is int:
            self.pin.duty_u16(conf)
        else:
            self.pin.duty_u16(self.conf[0])
            self.tim = Timer(period=self.conf[1], mode=Timer.ONE_SHOT, callback = self.nex)

    def nex(self, t):
        self.i += 2
        if self.i >= len(self.conf):
            #print("Cycle")
            self.i = 0
        self.pin.duty_u16(self.conf[self.i])
        if self.conf[self.i + 1] != 0:
            self.tim = Timer(period=self.conf[self.i+1], mode=Timer.ONE_SHOT, callback = self.nex)
    
    def deinit(self):
        self.tim.deinit()
        
f = Flash(led, [65535,300, 0,300, 2000,1000, 0,100])

print("Main.")

sleep(3)
print("Slept.")
f.deinit()
f = Flash(led, [65535,500, 0,500])
print("Loop.")
while True:
    pass
