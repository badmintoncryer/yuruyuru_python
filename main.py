from time import sleep
import machine

BOOLIAN_FLAG = False

# ESP32 - Pin assignment
pin14 = machine.Pin(14, machine.Pin.OUT)
if (BOOLIAN_FLAG):
    high_low_flag = True
else:
    high_low_flag = 0x01

while True:
    if (BOOLIAN_FLAG):
        high_low_flag = not high_low_flag
    else:
        high_low_flag = ~high_low_flag & 0x01

    pin14.value(high_low_flag)
    sleep(1)
