# Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Write in MicroPython by Warayut Poomiwatracanont JAN 2023

from MPU6050 import MPU6050
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C
from time import sleep_ms
import time
import framebuf

WIDTH  = 128                                            
HEIGHT = 64

VCC_oled = Pin(4, Pin.OUT)
GND_oled = Pin(5, Pin.OUT)
VCC_oled.value(1)
GND_oled.value(0)

VCC = Pin(13, Pin.OUT)
GND = Pin(12, Pin.OUT)
VCC.value(1)
GND.value(0)

time.sleep(0.2)

sda=Pin(2)
scl=Pin(3)

i2c = SoftI2C(sda=sda, scl=scl)

time.sleep(0.2)

devices = i2c.scan()
if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:', len(devices))

  for device in devices:
    print("i2c hexadecimal address: ", hex(device))

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

mpu = MPU6050()

print("Device Started")

while True:
        # Accelerometer Data
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    # Anything above 1.5 or below -1.5 movement on the Z axis, but the axis starts at 10 when in the correct orientation, trigger an alert, shocks are taking damage, otherwise just output the raw value
    if (aZ > 11.5 or aZ < -9.5):
        print("z: " + str(aZ) + " - SHOCKS ARE TAKING DAMAGE")
    else:
        print("z: " + str(aX))
    
    # Anything above 6 or below -6 movement on the Y axis, trigger an alert, truck is tipping over, otherwise just output the raw value
    if (aY > 6 or aY < -6):
        print("y: " + str(aY) + " - TRUCK IS TIPPING OVER")
    else:
        print("y: " + str(aY))
    #print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))
        # Gyroscope Data
    gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
   
    #print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))
    
    sleep_ms(100)   
    


