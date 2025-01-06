import gc
import time
import math
import random
from pimoroni import Button, Analog, AnalogMux
from servo import servo2040, ServoCluster, Servo


gc.collect()    # Collect garbage to free up memory 


# Initialize variables
current_sum = 0
current_count = 0
rolling_average = 0


UPDATES = 60            # Number of updates per second
TIME_FOR_EACH_MOVE = 1  # Set the time for each move in seconds
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES
N = 900  # Number of seconds in rolling average window (15 mins)
SERVO_EXTENT = 14   # How far from the center to limit the servo (15 degrees in this case)


def save_to_storage(average):
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
        save_to_storage(rolling_average)  # Store the average


# cluster_pins = [servo2040.SERVO_1, servo2040.SERVO_2,servo2040.SERVO_3,servo2040.SERVO_4]
# Create a servo cluster with the pins we want to use
# s = ServoCluster(0, 0, cluster_pins)

s1 = Servo(servo2040.SERVO_1)
s2 = Servo(servo2040.SERVO_2)

# Set the frequency of the servos
s1.frequency(333)  # good servo to 333Hz
s2.frequency(50)   # bad servo to 50Hz

# Initialize the sensors on the shared ADC
sen_adc = Analog(servo2040.SHARED_ADC)
vol_adc = Analog(servo2040.SHARED_ADC, servo2040.VOLTAGE_GAIN)
cur_adc = Analog(servo2040.SHARED_ADC, servo2040.CURRENT_GAIN,
                 servo2040.SHUNT_RESISTOR, servo2040.CURRENT_OFFSET)

# Create an analog multiplexer to select the current sensor pin
mux = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2)
mux.select(servo2040.CURRENT_SENSE_ADDR)


# Get the initial value and create a random end value between the extents
start_value = s1.mid_value()
end_value = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)

# Create the user button
user_sw = Button(servo2040.USER_SW)

outputs = []  # Create a list to store the rolling averages
update = 0  # Initialize the update (time) counter


# Continually move the servo until the user button is pressed
while not user_sw.raw():
    # Calculate how far along this movement we are
    percent_along = update / UPDATES_PER_MOVE

    # Use Cosine to simulate reduceing jerk on control surfaces
    s1.to_percent(math.cos(percent_along * math.pi), 1.0, -1.0, start_value, end_value)
    s2.to_percent(math.cos(percent_along * math.pi), 1.0, -1.0, start_value, end_value)
    
    update_rolling_average(int(cur_adc.read_current()*1000)) # Update the rolling average
    
    update += 1   # Move along in time

    # Have we reached the end of this movement?
    if update >= UPDATES_PER_MOVE:
        # Reset time
        update = 0

        # Set the start as the last end and create a new random end value
        start_value = end_value
        end_value = random.uniform(-SERVO_EXTENT, SERVO_EXTENT)

    time.sleep(1.0 / UPDATES)

# Disable the servo
s1.disable()
s2.disable()

# Save the rolling average to storage
with open('outputs.txt', 'w') as f:
    for x in outputs:
        f.write(f"{x}\n")