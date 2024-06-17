#include <iostream>
#include "roboticaFunctions.h"
#define _USE_MATH_DEFINES

#include <math.h>
#include <cmath>


/*
				ROBOT ASCII FOR VARIABLE EXPLANATION

			   base		   elbow	  camera    |  
				O--------------O-----------[]---O gripperbase
				|   humerus		 ulna		   |
				|							  /\  gripper
				|
				|
			  __|__

			O = joint
			-,| = solid
			[] = special component
*/

//constants
const double DEGREES_TO_RADIANS = M_PI / 180.0; //multiplication factor to turn degree values into radian values

//variables 
double base_rotation_angle = 90; // Angle between base and humerus in degrees
double elbow_rotation_angle = 0; // Angle between humerus and ulna in degrees
double length_humerus = 40.5; // Length of the humerus in units (cm)
double length_ulna = 32.0; // Length of the ulna in units (cm)
double camera_position_on_ulna = 30.0; // Distance from elbow joint to camera on ulna in units
double camera_height_from_ground = 49.0; // Height of the camera from the ground in units

//camera specifications
const double camera_fov = 61.0; // Diagonal FOV in degrees
const int camera_width = 640; // Camera resolution width in pixels
const int camera_height = 480; // Camera resolution height in pixels


//calculate the real-life coordinates of the object
Point calculateRealLifeCoordinates(int screen_x, int screen_y) {
	// Convert screen coordinates to normalized coordinates (-1 to 1)
	// The normalised x uses the y coordiantes and vice versa. if you dont do this the read coordinates are flipped 90 degrees for some reason
	double normalized_y = (2.0 * screen_x / camera_width) - 1.0;
	double normalized_x = 1.0 - (2.0 * screen_y / camera_height);

	//calculate the camera's horizontal and vertical FOV in radians
	double diagonal_fov_radians = camera_fov * DEGREES_TO_RADIANS;
	double aspect_ratio = static_cast<double>(camera_width) / camera_height;
	double horizontal_fov_radians = 2 * atan(tan(diagonal_fov_radians / 2) / sqrt(1 + aspect_ratio * aspect_ratio));
	double vertical_fov_radians = 2 * atan(tan(diagonal_fov_radians / 2) / sqrt(1 + (1 / aspect_ratio) * (1 / aspect_ratio)));

	//calculate the real-life coordinates in the camera's frame of reference
	double camera_x = 2 * normalized_x * tan(horizontal_fov_radians / 2) * camera_position_on_ulna;
	double camera_y = 2 * normalized_y * tan(vertical_fov_radians / 2) * camera_position_on_ulna;

	//transform the coordinates to the robot's base frame of reference
	double humerus_angle_radians = base_rotation_angle * DEGREES_TO_RADIANS;
	double elbow_angle_radians = elbow_rotation_angle * DEGREES_TO_RADIANS;

	//position of the elbow joint
	Point elbow;
	elbow.x = length_humerus * cos(humerus_angle_radians);
	elbow.y = length_humerus * sin(humerus_angle_radians);

	//position of the wrist joint (end of ulna)
	Point wrist;
	wrist.x = elbow.x + length_ulna * cos(humerus_angle_radians + elbow_angle_radians);
	wrist.y = elbow.y + length_ulna * sin(humerus_angle_radians + elbow_angle_radians);

	//adjust the coordinates for the camera's position on the ulna
	Point camera_mount;
	camera_mount.x = elbow.x + camera_position_on_ulna * cos(humerus_angle_radians + elbow_angle_radians);
	camera_mount.y = elbow.y + camera_position_on_ulna * sin(humerus_angle_radians + elbow_angle_radians);

	//calculate the object position relative to the camera
	double object_x_relative = camera_x * cos(humerus_angle_radians + elbow_angle_radians) - camera_y * sin(humerus_angle_radians + elbow_angle_radians);
	double object_y_relative = camera_x * sin(humerus_angle_radians + elbow_angle_radians) + camera_y * cos(humerus_angle_radians + elbow_angle_radians);

	//absolute position of the object
	Point object;
	object.x = camera_mount.x + object_x_relative;
	object.y = camera_mount.y + object_y_relative;

	std::cout << object.x << " " << object.y << std::endl; //debug log
	return object;
}

//calculate the distance between the base and the target coordinates
double calculateDistanceToTarget(int x,int y){
	double distanceFromBaseToTarget = sqrt(pow(x, 2) + pow(y, 2)); //pythagoras' theorem
	return distanceFromBaseToTarget;
}

//calculate the needed rotation of the gripper to grab the object while remaining perpendicular to it
#include <cmath>

double calculateGripperAngle(double vx, double vy) {
    // Perpendicular direction vector
    double px = -vy;
    double py = vx;

    // Calculate the angle with respect to the x-axis
    double angleRadians = std::atan2(py, px);
    double angleDegrees = angleRadians * (180.0 / M_PI);

    // Normalize angle to be within the range of [-180, 180]
    if (angleDegrees > 180) {
        angleDegrees -= 360;
    } else if (angleDegrees < -180) {
        angleDegrees += 360;
    }

    // Account for the dead zone of the servos (<-150 and >150)
    if (angleDegrees > 150) {
        angleDegrees -= 180; // Flip 180 degrees
    } else if (angleDegrees < -150) {
        angleDegrees += 180; // Flip 180 degrees
    }

    // Normalize angle again to be within the range of [-150, 150]
    if (angleDegrees > 150) {
        angleDegrees -= 360;
    } else if (angleDegrees < -150) {
        angleDegrees += 360;
    }

    return angleDegrees;
}


//calculate the angles of the robot's elbow and base
double* calculateArmAngles(double x,double y,double distanceToTarget){ //x and y of the center of mass of the object, along with the distance.
	double* armAngles = new double[2]; //create a pointer towards an array with two decimal numbers
	//use trigonometry to calculate the angles: see https://www.geogebra.org/calculator/bf4wfqr5 for elaboration
	armAngles[0] = fmod((acos((pow(length_humerus, 2) + pow(length_ulna, 2) - pow(distanceToTarget, 2)) / (2 * length_humerus * length_ulna)) + M_PI), (2 * M_PI))*(180/M_PI);//elbow
	armAngles[1] = fmod((atan2(y, x) - atan2((length_ulna * sin(armAngles[0])), (length_humerus + length_ulna * cos(armAngles[0])))), (2 * M_PI))*(180/M_PI);//base angle, mult by gear ratio
	return armAngles; 
}

//run all the previous calculation
double* calculator(double x, double y, double vx, double vy) {
	double* results = new double[3];
	std::cout << "external c++ calculator has run with parameters " << x << " " << y << " " << vx << " " << vy << " \n"; //debug log

	Point pointC = calculateRealLifeCoordinates(x,y); //the point where gripper is going to be heading
	double distanceToTarget = calculateDistanceToTarget(pointC.x,pointC.y); //calculate distance from base to target coordinates
	// if(distanceToTarget > length_humerus + length_ulna || distanceToTarget < length_humerus - length_ulna){
	// 	std::cout << "\nout of reach\n" << std::endl; //cannot reach the point, return previous, assume object didnt move.
	// 	return results; //results of previous iteration
	// }
	double* armAngles = calculateArmAngles(pointC.x,pointC.y,distanceToTarget); // calculate required angles for the elbow and base servos
	results[0] = calculateGripperAngle(vx,vy);	//calculate angle for the gripper to be perpendicular to the scissors
	results[1] = armAngles[0]; //store the arm angle variables
	results[2] = armAngles[1];
	return results;
}
