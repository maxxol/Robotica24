import math
import numpy as np
from getServoPositions import getPosition
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


length_humerus = 40.5  # Length of the humerus in units (cm)
length_ulna = 32.0  # Length of the ulna in units (cm)
camera_position_on_ulna = 20.0  # Distance from elbow joint to camera on ulna in units
camera_height_from_ground = 43.0  # Height of the camera from the ground in units

# Camera specifications
camera_fov = 61.0  # Diagonal FOV in degrees
camera_width = 640  # Camera resolution width in pixels
camera_height = 480  # Camera resolution height in pixels

id_base = 2
id_elbow = 18
class Point:
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y


def calculate_camera_coords():
	base_rotation_angle = getPosition(id_base) / 3.33 * (math.pi/180) # Angle between base and humerus in degrees
	elbow_rotation_angle = getPosition(id_elbow) / 2 * (math.pi/180) # Angle between humerus and ulna in degrees
	
	elbow_coords = Point(length_humerus*math.cos(base_rotation_angle),length_humerus*math.sin(base_rotation_angle))

	elbow_theta = base_rotation_angle + elbow_rotation_angle
	camera_coords = Point(elbow_coords.x + (camera_position_on_ulna*math.cos(elbow_theta)),elbow_coords.y + (camera_position_on_ulna*math.sin(elbow_theta)))
	return [camera_coords,elbow_theta]


# Calculate the real-life coordinates of the object
def calculate_real_life_coordinates(screen_x, screen_y):
	data = calculate_camera_coords()
	camera_coords = data[0]
	elbow_theta = data[1]
	#print(f"camera: {camera_coords.x} {camera_coords.y}")

	conversion_rate = 38/640 #pixels per cm
	
	distance_camera_centroid = math.sqrt((-screen_x+320)**2+(screen_y-240)**2) * conversion_rate
	#print(f"distance: {distance_camera_centroid}")
	#print(distance_camera_centroid)
	theta_centroid = math.atan2((screen_x-320),(-screen_y+240))

	theta_centroid_real_life = theta_centroid-elbow_theta
	print(theta_centroid_real_life)
	
	targetx = camera_coords.x + (distance_camera_centroid*math.cos(theta_centroid_real_life))
	targety = camera_coords.y + (distance_camera_centroid*math.sin(theta_centroid_real_life))


	target_coords = Point(targetx,targety)
	return target_coords


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
	#print(f"external c++ calculator has run with parameters {x} {y} {vx} {vy}")  # Debug log

	pointC = calculate_real_life_coordinates(x, y)  # The point where gripper is going to be heading
	#pointC = calculate_real_life_coordinates(320, 240)  # The point where gripper is going to be heading
	print(f"relative coords {x} {y}")
	print(f"absolute coords {round(pointC.x,1)} {round(pointC.y,1)}\n")
	distance_to_target = calculate_distance_to_target(pointC.x, pointC.y)  # Calculate distance from base to target coordinates
	# if distance_to_target > length_humerus + length_ulna or distance_to_target < length_humerus - length_ulna:
	#	 print("\nout of reach\n")  # Cannot reach the point, return previous, assume object didn't move
	#	 return results  # Results of previous iteration
	arm_angles = calculate_arm_angles(pointC.x, pointC.y, distance_to_target)  # Calculate required angles for the elbow and base servos
	results[0] = calculate_gripper_angle(vx, vy)  # Calculate angle for the gripper to be perpendicular to the scissors
	results[1] = arm_angles[0]  # Store the arm angle variables
	results[2] = arm_angles[1]
	return results
