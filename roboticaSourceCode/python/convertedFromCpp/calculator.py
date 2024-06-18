import math
import numpy as np

# Constants
DEGREES_TO_RADIANS = math.pi / 180.0  # Multiplication factor to turn degree values into radian values


"""
				ROBOT ASCII FOR VARIABLE EXPLANATION

			   base		   elbow	  camera	|  
				O--------------O-----------[]---O gripperbase
				|   humerus		 ulna			|
				|							   /\  gripper
				|
				|
			  __|__

			O = joint
			-,| = solid
			[] = special component
"""
# Variables
base_rotation_angle = 90  # Angle between base and humerus in degrees
elbow_rotation_angle = 0  # Angle between humerus and ulna in degrees

length_humerus = 40.5  # Length of the humerus in units (cm)
length_ulna = 32.0  # Length of the ulna in units (cm)
camera_position_on_ulna = 30.0  # Distance from elbow joint to camera on ulna in units
camera_height_from_ground = 49.0  # Height of the camera from the ground in units

# Camera specifications
camera_fov = 61.0  # Diagonal FOV in degrees
camera_width = 640  # Camera resolution width in pixels
camera_height = 480  # Camera resolution height in pixels

class Point:
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

# Calculate the real-life coordinates of the object
def calculate_real_life_coordinates(screen_x, screen_y):
	# Convert screen coordinates to normalized coordinates (-1 to 1)
	normalized_y = (2.0 * screen_x / camera_width) - 1.0
	normalized_x = 1.0 - (2.0 * screen_y / camera_height)

	# Calculate the camera's horizontal and vertical FOV in radians
	diagonal_fov_radians = camera_fov * DEGREES_TO_RADIANS
	aspect_ratio = camera_width / camera_height
	horizontal_fov_radians = 2 * math.atan(math.tan(diagonal_fov_radians / 2) / math.sqrt(1 + aspect_ratio * aspect_ratio))
	vertical_fov_radians = 2 * math.atan(math.tan(diagonal_fov_radians / 2) / math.sqrt(1 + (1 / aspect_ratio) * (1 / aspect_ratio)))

	# Calculate the real-life coordinates in the camera's frame of reference
	camera_x = 2 * normalized_x * math.tan(horizontal_fov_radians / 2) * camera_position_on_ulna
	camera_y = 2 * normalized_y * math.tan(vertical_fov_radians / 2) * camera_position_on_ulna

	# Transform the coordinates to the robot's base frame of reference
	humerus_angle_radians = base_rotation_angle * DEGREES_TO_RADIANS
	elbow_angle_radians = elbow_rotation_angle * DEGREES_TO_RADIANS

	# Position of the elbow joint
	elbow = Point(length_humerus * math.cos(humerus_angle_radians),
				  length_humerus * math.sin(humerus_angle_radians))

	# Position of the wrist joint (end of ulna)
	wrist = Point(elbow.x + length_ulna * math.cos(humerus_angle_radians + elbow_angle_radians),
				  elbow.y + length_ulna * math.sin(humerus_angle_radians + elbow_angle_radians))

	# Adjust the coordinates for the camera's position on the ulna
	camera_mount = Point(elbow.x + camera_position_on_ulna * math.cos(humerus_angle_radians + elbow_angle_radians),
						 elbow.y + camera_position_on_ulna * math.sin(humerus_angle_radians + elbow_angle_radians))

	# Calculate the object position relative to the camera
	object_x_relative = camera_x * math.cos(humerus_angle_radians + elbow_angle_radians) - camera_y * math.sin(humerus_angle_radians + elbow_angle_radians)
	object_y_relative = camera_x * math.sin(humerus_angle_radians + elbow_angle_radians) + camera_y * math.cos(humerus_angle_radians + elbow_angle_radians)

	# Absolute position of the object
	obj = Point(camera_mount.x + object_x_relative,
				camera_mount.y + object_y_relative)

	print(f"{obj.x} {obj.y}")  # Debug log
	return obj

# Calculate the distance between the base and the target coordinates
def calculate_distance_to_target(x, y):
	distance_from_base_to_target = math.sqrt(x**2 + y**2)  # Pythagoras' theorem
	return distance_from_base_to_target

# Calculate the needed rotation of the gripper to grab the object while remaining perpendicular to it
def calculate_gripper_angle(vx, vy):
	# Perpendicular direction vector
	px = -vy
	py = vx

	# Calculate the angle with respect to the x-axis
	angle_radians = math.atan2(py, px)
	angle_degrees = angle_radians * (180.0 / math.pi)

	# Normalize angle to be within the range of [-180, 180]
	if angle_degrees > 180:
		angle_degrees -= 360
	elif angle_degrees < -180:
		angle_degrees += 360

	# Account for the dead zone of the servos (<-150 and >150)
	if angle_degrees > 150:
		angle_degrees -= 180  # Flip 180 degrees
	elif angle_degrees < -150:
		angle_degrees += 180  # Flip 180 degrees

	# Normalize angle again to be within the range of [-150, 150]
	if angle_degrees > 150:
		angle_degrees -= 360
	elif angle_degrees < -150:
		angle_degrees += 360

	return angle_degrees

# Calculate the angles of the robot's elbow and base
def calculate_arm_angles(x, y, distance_to_target):  # x and y of the center of mass of the object, along with the distance
	arm_angles = np.zeros(2)
	# Use trigonometry to calculate the angles
	arm_angles[0] = 180 - (math.acos((length_ulna**2 + length_humerus**2 - distance_to_target**2) / (2 * length_humerus * length_ulna))) * (180 / math.pi)  # Elbow
	arm_angles[1] = (math.acos((distance_to_target**2 + length_humerus**2 - length_ulna**2) / (2 * length_humerus * distance_to_target)) + math.atan(abs(y) / abs(x))) * (180 / math.pi)  # Base angle
	return arm_angles

# Run all the previous calculations
def calculator(x, y, vx, vy):
	results = np.zeros(3)
	print(f"external c++ calculator has run with parameters {x} {y} {vx} {vy}")  # Debug log

	pointC = calculate_real_life_coordinates(x, y)  # The point where gripper is going to be heading
	distance_to_target = calculate_distance_to_target(pointC.x, pointC.y)  # Calculate distance from base to target coordinates
	# if distance_to_target > length_humerus + length_ulna or distance_to_target < length_humerus - length_ulna:
	#	 print("\nout of reach\n")  # Cannot reach the point, return previous, assume object didn't move
	#	 return results  # Results of previous iteration
	arm_angles = calculate_arm_angles(pointC.x, pointC.y, distance_to_target)  # Calculate required angles for the elbow and base servos
	results[0] = calculate_gripper_angle(vx, vy)  # Calculate angle for the gripper to be perpendicular to the scissors
	results[1] = arm_angles[0]  # Store the arm angle variables
	results[2] = arm_angles[1]
	return results
