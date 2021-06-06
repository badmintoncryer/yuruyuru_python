from time import sleep
import machine
import BME280, ST7032i

BOOLIAN_FLAG = True

# ESP32 - Pin assignment
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)
pin14 = machine.Pin(14, machine.Pin.OUT)

if (BOOLIAN_FLAG):
    high_low_flag = True
else:
    high_low_flag = 0x01

bme = BME280.BME280(i2c=i2c)
lcd = ST7032i.ST7032i(i2c=i2c)

while True:
    if (BOOLIAN_FLAG):
        high_low_flag = not high_low_flag
    else:
        high_low_flag = ~high_low_flag & 0x01
    pin14.value(high_low_flag)

    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure

    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)

    lcd.reset_display()
    lcd.set_cursor(0, 0)
    lcd.print('Temp is ' + str(temp))
    lcd.set_cursor(0, 1)
    lcd.print('hum is ' + str(hum))

    sleep(1)
