# import numpy as np
# import matplotlib.pyplot as plt

# # Function to read the data from the file
# def read_data(file_path):
#     # Load the data into a numpy array from the text file, assuming the values are separated by commas
#     data = np.loadtxt(file_path, delimiter=',')
#     return data

# # Read the data from the file
# file_path = 'outputs.txt'  # Replace with your actual file path
# data = read_data(file_path)

# # Extract the two columns (assuming each line contains two float values)
# x_values = data[:, 0]  # First column (x-axis)
# y_values = data[:, 1]  # Second column (y-axis)

# # Plot the data in two separate line graphs
# plt.figure(figsize=(10, 6))

# # First plot
# plt.subplot(2, 1, 1)  # Two rows, one column, first plot
# plt.plot(x_values, label='X values', color='blue')
# plt.xlabel('Index')
# plt.ylabel('X values')
# plt.title('Plot of X values')
# plt.grid(True)
# plt.legend()

# # Second plot
# plt.subplot(2, 1, 2)  # Two rows, one column, second plot
# plt.plot(y_values, label='Y values', color='red')
# plt.xlabel('Index')
# plt.ylabel('Y values')
# plt.title('Plot of Y values')
# plt.grid(True)
# plt.legend()

# # Adjust the layout
# plt.tight_layout()

# # Show the plots
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Function to read the data from the file
def read_data(file_path):
    # Load the data into a numpy array from the text file, assuming the values are separated by commas
    data = np.loadtxt(file_path, delimiter=',')
    return data

# Read the data from the file
file_path = 'outputs2.txt'  # Replace with your actual file path
data = read_data(file_path)

# Extract the two columns (assuming each line contains two float values)
# x_values = np.abs(data[:, 0])  # First column (x-axis)
x_values = data[:, 0]  # First column (x-axis)
y_values = data[:, 1]  # Second column (y-axis)

# Calculate the gradient of the x_values
gradient_x = np.abs(np.gradient(x_values))

# Plot the data in two separate line graphs
plt.figure(figsize=(10, 6))

# First plot: gradient of the x_values
plt.subplot(2, 1, 1)  # Two rows, one column, first plot
plt.plot(gradient_x, label='Gradient of Movement', color='blue')
plt.xlabel('Time')
plt.ylabel('Gradient of Movement')
plt.title('Plot of Gradient of Movement')
plt.grid(True)
plt.legend()

# Second plot: plot of y_values
plt.subplot(2, 1, 2)  # Two rows, one column, second plot
plt.plot(y_values, label='Current', color='red')
plt.xlabel('Time')
plt.ylabel('Current')
plt.title('Plot of Current')
plt.grid(True)
plt.legend()

# Adjust the layout
plt.tight_layout()

# Show the plots
plt.show()
