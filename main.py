from time import sleep
import machine
import driver.BME280

BOOLIAN_FLAG = False

# ESP32 - Pin assignment
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)
pin14 = machine.Pin(14, machine.Pin.OUT)
if (BOOLIAN_FLAG):
    high_low_flag = True
else:
    high_low_flag = 0x01

while True:
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure

    # uncomment for temperature in Fahrenheit
    #temp = (bme.read_temperature()/100) * (9/5) + 32
    #temp = str(round(temp, 2)) + 'F'

    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)

    pin14.value(~high_low_flag)
    sleep(5)
