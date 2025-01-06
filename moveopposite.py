import gc
import time
import math
import random
from pimoroni import Button, Analog, AnalogMux
from servo import Servo, servo2040, ServoCluster

SERVO_EXTENT = 14      # How far from zero to move the servo
        
gc.collect()        
user_sw = Button(servo2040.USER_SW)

s1 = Servo(servo2040.SERVO_1)
s18 = Servo(servo2040.SERVO_18)



def move_opposite(val):
    global s1, s18
    if val > -15 and val < 15:
        s1.value(val)
        s18.value(-val) 
        
        
newUpdate = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)
step = s1.value() - newUpdate    
i=0
while not user_sw.raw():
    i += 1
    # (s1.value())
    move_opposite(s1.value()-step)
    
    if i > 20:
        newUpdate = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)
        step = s1.value() - newUpdate
        i=0
    time.sleep(0.2)