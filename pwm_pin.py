# PWM_Pin Class

# 221019 - Fade added.
# 221018 - Started.

from machine import Pin, PWM, Timer

class PWM_Pin():
    def __init__(self, pin, high=65535, low=0, freq=1000):
        self.pwm = PWM(pin)
        self.pwm.freq(freq)
        self.high = min(max(high,0), 65535)
        self.low = min(max(low,0), 65535)
        self._tim = Timer(period=0, mode=Timer.ONE_SHOT, callback=lambda t:print("PWM_Pin-Timer Setup."))

    def _min_max(self, v):
        return min(max(v,self.low), self.high)

    def _write_duty(self, v):
        self.pwm.duty_u16(v)

    def _read_duty(self):
        return self.pwm.duty_u16()

    def _tim_next(self, t):
        self._i += 2
        if self._i >= len(self._conf):
            self._i = 0
        self._write_duty(self._min_max(self._conf[self._i]))
        if self._conf[self._i + 1] != 0:
            self._tim = Timer(period=self._min_max(self._conf[self._i+1]), mode=Timer.ONE_SHOT, callback = self._tim_next)

    def sequence(self, conf=[65535,500, 0,500]):
        self._tim.deinit()
        if type(conf) is int:
            self._write_duty(self._min_max(conf))
        else:
            self._conf = conf
            if len(self._conf) % 2 > 0:
                self._conf.append(0)
            self._write_duty(self._min_max(self._conf[0]))
            self._i = 0
            self._tim = Timer(period=self._min_max(self._conf[1]), mode=Timer.ONE_SHOT, callback = self._tim_next)

    def _tim_fade(self, t):
        self._steps -= 1
        if self._steps > 0:
            self._now += self._step
            self._write_duty(int(self._now))
            self._tim = Timer(period=10, mode=Timer.ONE_SHOT, callback = self._tim_fade)
        else:
            Pin(25, Pin.OUT).off()
            self._write_duty(self._target)

    def fade(self, target=0, time=1): # target duty, time in seconds.
        self._tim.deinit()
        self._now = self._read_duty()
        if target == self._now:
            return
        self._target = self._min_max(target)
        self._steps = int(100 * min(max(time,0), 65535))
        self._step = (self._target - self._now) / self._steps
        if self._step == 0:
            self._write_duty(self._target)
        else:
            Pin(25, Pin.OUT).on()
            self._tim = Timer(period=10, mode=Timer.ONE_SHOT, callback = self._tim_fade)

    def on(self):
        self._tim.deinit()
        self._write_duty(self.high)
        
    def off(self):
        self._tim.deinit()
        self._write_duty(self.low)

    def value(self, *args):
        if len(args):
            self._tim.deinit()
            v = args[0]
            if v == -1 or v == 1:
                self._write_duty(self.high)
            else:
                self._write_duty(self._min_max(v))
        else:
            return self._read_duty()

class LED_Pin(PWM_Pin):
    def __init__(self, pin, high=65535, low=0):
        super().__init__(pin, high, low, freq=1000)

    def _write_duty(self, v):
        self.pwm.duty_u16(int(v ** 2.8 / 467400000))

    def _read_duty(self):
        return int((self.pwm.duty_u16() * 467400000) ** (1/2.8))

class Servo_Pin(PWM_Pin):
    def __init__(self, pin, high=65535, low=0):
        super().__init__(pin, high, low, freq=50)
