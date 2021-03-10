from time import sleep
import machine

# ESP32 - Pin assignment
pin14 = machine.Pin(14, machine.Pin.OUT)
high_low_flag = 1
pin14.value(high_low_flag)

while True:
    pin14.value(~high_low_flag)
    sleep(5)