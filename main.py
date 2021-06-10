from time import sleep
import machine

# ESP32 - Pin assignment
pin14 = machine.Pin(14, machine.Pin.OUT)
high_low_flag = True

def gpio_irq_handler(gpio):
    global high_low_flag, pin14
    high_low_flag = not high_low_flag
    pin14.value(high_low_flag)

pin5 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin5.irq(handler=gpio_irq_handler, trigger=machine.Pin.IRQ_RISING)
while True:
    print("main loop")
    sleep(5)
