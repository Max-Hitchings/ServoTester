import numpy as np
#  490 - 630

# 345 - 440

goodlower_bound = 490
goodupper_bound = 630
badlower_bound = 345
badupper_bound = 440


# 29.873 days
# first bad servo 23.24525 hours
# good servo does not break

# polls every half hour
rate = 15 /60
no_of_polls =   29.873 *24 / rate
# no_of_polls =  no_of_polls-(23.24525 / rate)
print(rate)
print(no_of_polls)




GOOD_SERVO_CURRENT = 53
GOOD_SERVO_RANGES = 10

BAD_SERVO_CURRENT = 19





def generate_random_values(lower_bound, upper_bound, count=2774):
    # Calculate a reasonable mean and standard deviation based on bounds
    mean = (upper_bound + lower_bound) / 2  # Center of the bounds
    std_dev = (upper_bound - lower_bound) / 6  # Approx. 99.7% within bounds

    # Generate normally distributed values
    values = np.random.normal(loc=mean, scale=std_dev, size=count)

    # Clip values to ensure they stay within bounds
    values = np.clip(values, lower_bound, upper_bound)

    return values

random_values = generate_random_values(goodlower_bound, goodupper_bound)

# Save values to a txt file
file_name = "random_values.txt"
np.savetxt(file_name, random_values, fmt='%.2f', header='Random Values', comments='')

print(f"Random values saved to {file_name}")
