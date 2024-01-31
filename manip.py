import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ikpy.chain import Chain
from pyquaternion import Quaternion

# Load the robot arm from the URDF file
my_chain = Chain.from_urdf_file("cobot_reassembled.urdf")

# Function to parse G-code
def parse_gcode(line):
    # Split the line into parts
    parts = line.split()

    # Extract the X and Y coordinates
    X = float(parts[1][1:]) 
    Y = float(parts[2][1:]) 
    Z = 0

    # Combine the coordinates into a point
    point = [X, Y, Z]

    return point

# Open the G-code file
with open('alphabet.gcode', 'r') as file:
    gcode_lines = file.readlines()

# Initialize plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for line in gcode_lines:
    # Parse G-code line
    x, y, z = parse_gcode(line)

    # Assume yaw, pitch, roll to be 0
    yaw, pitch, roll = 0, 0, 0

    # Perform inverse kinematics
    target_vector = [x, y, z]
    target_orientation = Quaternion(axis=[0, 1, 0], angle=yaw) * Quaternion(axis=[1, 0, 0], angle=pitch) * Quaternion(axis=[0, 0, 1], angle=roll)
    joint_angles = my_chain.inverse_kinematics(target_vector, target_orientation)

    # Visualize the robot's movements
    my_chain.plot(joint_angles, ax, target=target_vector)

plt.show()
