import numpy as np
import matplotlib.pyplot as plt

# Function to read the data from the file
def read_data(file_path):
    # Load the data into a numpy array from the text file, assuming the values are separated by commas
    data = np.loadtxt(file_path, delimiter=',')
    return data

# Read the data from the file
file_path = 'random_valuesfirst.txt'  # Replace with your actual file path
data = read_data(file_path)

# Assuming each line in data contains a pair of values, we use the first column for plotting
values = data # First column (x-axis values)

# Calculate the gradient of the x_values (here, just using absolute values for simplicity)
gradient_x = np.abs(values)

# Create the x-axis labels as time in minutes, then convert to hours
time_minutes = np.arange(0, len(values) * 15, 15)
time_hours = time_minutes / 60  # Convert minutes to hours

# Plot the data in two separate line graphs
plt.figure(figsize=(10, 6))

# First plot: gradient of the x_values
plt.subplot(2, 1, 1)  # Two rows, one column, first plot
plt.plot(time_hours, gradient_x, label='Current 15 Minute Rolling Average', color='blue')

plt.xlabel('Time (Hours)')
plt.ylabel('Current 15 Minute Rolling Average')
plt.title('Plot of Current (15 Minute Rolling Average)')
plt.grid(True)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
