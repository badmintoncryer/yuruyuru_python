from time import sleep
import machine

# ESP32 - Pin assignment
pin14 = machine.Pin(14, machine.Pin.OUT)
high_low_flag = True

def super_heavy_task():
    print("start super heavy task")
    sleep(5)
    print("finish super heavy task")

def timer_irq_handler(timer):
    global high_low_flag, pin14
    high_low_flag = not high_low_flag
    pin14.value(high_low_flag)

timer = machine.Timer(0)
timer.init(mode=machine.Timer.PERIODIC, period=1000, callback=timer_irq_handler)
while True:
    super_heavy_task()
    sleep(1)
