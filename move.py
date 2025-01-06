import gc
import time
import math
import random
from pimoroni import Button, Analog, AnalogMux
from servo import Servo, servo2040, ServoCluster


        
gc.collect()        


# Initialize variables
current_sum = 0
current_count = 0
rolling_average = 0
N = 10000  # Replace with the desired window size


def save_to_memory(average):
    print(f"Rolling average saved: {average}")
    outputs.append(average)


def update_rolling_average(current_reading):
    global current_sum, current_count, rolling_average
    
    current_sum += current_reading
    current_count += 1

    if current_count == N:  # Check if we've reached the window size
        rolling_average = current_sum / N
        current_sum = 0
        current_count = 0
        save_to_memory(rolling_average)  # Store the average


UPDATES = 50            # How many times to update Servos per second
TIME_FOR_EACH_MOVE = 1  # The time to travel between each random value
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES

SERVO_EXTENT = 14      # How far from zero to move the servo
USE_COSINE = True       # Whether or not to use a cosine path between values

LIMIT_FROM_CENTER = 14
cluster_pins = [servo2040.SERVO_1, servo2040.SERVO_2,servo2040.SERVO_3,servo2040.SERVO_4,servo2040.SERVO_5]
# Create a servo on pin 0
s = ServoCluster(0, 0, cluster_pins)
# s = Servo(servo2040.SERVO_1)

sen_adc = Analog(servo2040.SHARED_ADC)
vol_adc = Analog(servo2040.SHARED_ADC, servo2040.VOLTAGE_GAIN)
cur_adc = Analog(servo2040.SHARED_ADC, servo2040.CURRENT_GAIN,
                 servo2040.SHUNT_RESISTOR, servo2040.CURRENT_OFFSET)

mux = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2)
mux.select(servo2040.CURRENT_SENSE_ADDR)


# Get the initial value and create a random end value between the extents
start_value = s.mid_value(cluster_pins[1])
end_value = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)

# Create the user button
user_sw = Button(servo2040.USER_SW)


update = 0

count = 1

outputs = []
# Continually move the servo until the user button is pressed
while not user_sw.raw():
    # Calculate how far along this movement to be
    percent_along = update / UPDATES_PER_MOVE

    if USE_COSINE:
        # Move the servo between values using cosine
        s.all_to_percent(math.cos(percent_along * math.pi), 1.0, -1.0, start_value, end_value)
    else:
        # Move the servo linearly between values
        s.all_to_percent(percent_along, 0.0, 1.0, start_value, end_value)
    # outputs.append((s.value(cluster_pins[0]),int(cur_adc.read_current()*1000)))
    update_rolling_average(int(cur_adc.read_current()*1000))
    # Print out the value the servo is now at
    if count % 3 == 0:
        # print("Current =", cur_adc.read_current()*1000, "mA")
        count=0
        
    # print("Value = ", round(s.value(cluster_pins[1]), 3), sep="")
    count += 1
    # Move along in time
    update += 1

    # Have we reached the end of this movement?
    if update >= UPDATES_PER_MOVE:
        # Reset the counter
        update = 0

        # Set the start as the last end and create a new random end value
        start_value = end_value
        end_value = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)

    time.sleep(1.0 / UPDATES)

# Disable the servo
s.disable_all()

with open('outputs.txt', 'w') as f:
    for x in outputs:
        f.write(f"{x}\n")