# PWM_Pin Test

# 221018 - Started

from time import sleep
from machine import Pin, PWM, Timer
import pwm_pin

led = Pin(15)
onboard = Pin('LED')

gamma = [0, 256, 768, 2304, 5120, 9216, 15616, 23808, 34560, 47616, 65535]

f = pwm_pin.PWM_Pin(Pin(15))

f.sequence([65535,300, 0,300, 2000,1000, 0,100])

print("Main.")

sleep(4)
print("Slept.")

f.sequence([65535,500, 0,500])

print("Loop.")
try:
    while True:
        onboard.on()
        sleep(0.01)
        onboard.off()
        sleep(0.99)

except KeyboardInterrupt:
    print("Ctrl-C")
f.off()
onboard.off()
