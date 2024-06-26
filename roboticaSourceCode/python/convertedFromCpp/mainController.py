import numpy as np
import re
import sys
import os

# Adjust the sys.path to include the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(parent_dir)

from calculator import calculator
from checkbluetooth import check_bluetooth
from computerVision import get_computer_vision_results
from rotateArmServos import rotate_arm_servos
from main import main
# Assuming the `main` function and `rotate_servos` function are defined in their respective modules
#from main import get_computer_vision_results


def mainCont():
	
		#print("main Python program running-------------------------------------------------")

		computer_vision_results = np.zeros(4)  # Empty array for computer vision results

		focus_object = None

		while True:
			try:
				# Call the computer vision script function directly and get results
				computer_vision_results = get_computer_vision_results()
				#result = [1,2,3,4,5,6]

				
				#focus_object = main('PyCharm', None)

				# # Give the calculator the values from computer vision
				calc_results = calculator(computer_vision_results[0], computer_vision_results[1], computer_vision_results[2], computer_vision_results[3])
				# print(f"calc results: {calc_results[0]} {calc_results[1]} {calc_results[2]}")
				# # Call the rotate servos function with the calculated parameters
				#rotate_arm_servos(calc_results[0], calc_results[1], calc_results[2])
				#print("sent servos")
				# Check Bluetooth
				# check_bluetooth()

				#print("main Python program done-----------------------------------------------------")
			except Exception as e: print(e)

if __name__ == "__main__":
	mainCont()
