#include <iostream>
#include "roboticaFunctions.h"
#define _USE_MATH_DEFINES

#include <math.h>
#include <cmath>

// Constants

const double DEGREES_TO_RADIANS = M_PI / 180.0;

// Variables (these can be adjusted as needed)
double base_rotation_angle = 90; // Angle between base and humerus in degrees
double elbow_rotation_angle = 0; // Angle between humerus and ulna in degrees
double length_humerus = 40.0; // Length of the humerus in units (cm)
double length_ulna = 31.0; // Length of the ulna in units (cm)
double camera_position_on_ulna = 30.0; // Distance from elbow joint to camera on ulna in units
double camera_height_from_ground = 49.0; // Height of the camera from the ground in units

// Camera specifications
const double camera_fov = 55.0; // Diagonal FOV in degrees
const int camera_width = 640; // Camera resolution width in pixels
const int camera_height = 480; // Camera resolution height in pixels

// Struct to represent a point in 2D space
struct Point {
    double x;
    double y;
};

// Calculate the real-life coordinates of the object
Point calculateRealLifeCoordinates(int screen_x, int screen_y) {
    // Convert screen coordinates to normalized coordinates (-1 to 1)
    double normalized_x = (2.0 * screen_x / camera_width) - 1.0;
    double normalized_y = 1.0 - (2.0 * screen_y / camera_height);

    // Calculate the camera's horizontal and vertical FOV in radians
    double diagonal_fov_radians = camera_fov * DEGREES_TO_RADIANS;
    double aspect_ratio = static_cast<double>(camera_width) / camera_height;
    double horizontal_fov_radians = 2 * atan(tan(diagonal_fov_radians / 2) / sqrt(1 + aspect_ratio * aspect_ratio));
    double vertical_fov_radians = 2 * atan(tan(diagonal_fov_radians / 2) / sqrt(1 + (1 / aspect_ratio) * (1 / aspect_ratio)));

    // Calculate the real-life coordinates in the camera's frame of reference
    double camera_x = normalized_x * tan(horizontal_fov_radians / 2) * camera_position_on_ulna;
    double camera_y = normalized_y * tan(vertical_fov_radians / 2) * camera_position_on_ulna;

    // Transform the coordinates to the robot's base frame of reference
    double humerus_angle_radians = base_rotation_angle * DEGREES_TO_RADIANS;
    double elbow_angle_radians = elbow_rotation_angle * DEGREES_TO_RADIANS;

    // Position of the elbow joint
    Point elbow;
    elbow.x = length_humerus * cos(humerus_angle_radians);
    elbow.y = length_humerus * sin(humerus_angle_radians);

    // Position of the wrist joint (end of ulna)
    Point wrist;
    wrist.x = elbow.x + length_ulna * cos(humerus_angle_radians + elbow_angle_radians);
    wrist.y = elbow.y + length_ulna * sin(humerus_angle_radians + elbow_angle_radians);

    // Adjust the coordinates for the camera's position on the ulna
    Point camera_mount;
    camera_mount.x = elbow.x + camera_position_on_ulna * cos(humerus_angle_radians + elbow_angle_radians);
    camera_mount.y = elbow.y + camera_position_on_ulna * sin(humerus_angle_radians + elbow_angle_radians);

    // Calculate the object position relative to the camera
    double object_x_relative = camera_x * cos(humerus_angle_radians + elbow_angle_radians) - camera_y * sin(humerus_angle_radians + elbow_angle_radians);
    double object_y_relative = camera_x * sin(humerus_angle_radians + elbow_angle_radians) + camera_y * cos(humerus_angle_radians + elbow_angle_radians);

    // Absolute position of the object
    Point object;
    object.x = camera_mount.x + object_x_relative;
    object.y = camera_mount.y + object_y_relative;

    std::cout << object.x << " " << object.y << std::endl;
    return object;
}

//calculate the distance between the base and the target coordinates
double calculateDistanceToTarget(int x,int y){
	double distanceFromBaseToTarget = sqrt(pow(x, 2) + pow(y, 2)); //pythagoras' theorem
	return distanceFromBaseToTarget;
}

//calculate the needed rotation of the gripper to grab the object while remaining perpendicular to it
double calculateGripperAngle(double vx, double vy) {
    // Perpendicular direction vector
    double px = -vy;
    double py = vx;
    
    // Calculate the angle with respect to the x-axis
    double angleRadians = std::atan2(py, px);
    double angleDegrees = angleRadians * (180.0 / M_PI);

    if (angleDegrees > 150)
        angleDegrees-=180;
    if(angleDegrees < -150)
        angleDegrees+=180;
    std::cout << px << " " << py << " " << angleDegrees << std::endl;
    return angleDegrees;
}

//calculate the angles of the robot's elbow and base(shoulder)
double* calculateArmAngles(double x,double y,double distanceToTarget){ //x and y of the center of mass of the object, along with the distance.
	double* armAngles = new double[2]; //create a pointer towards an array with two decimal numbers
	//use trigonometry to calculate the angles: see https://www.geogebra.org/calculator/bf4wfqr5 for elaboration
    armAngles[0] = fmod((acos((pow(length_humerus, 2) + pow(length_ulna, 2) - pow(distanceToTarget, 2)) / (2 * length_humerus * length_ulna)) + M_PI), (2 * M_PI))*(180/M_PI);
    armAngles[1] = fmod((atan2(y, x) - atan2((length_ulna * sin(armAngles[0])), (length_humerus + length_ulna * cos(armAngles[0])))), (2 * M_PI))*(180/M_PI);
	return armAngles; 
}

//run all the previous calculation
double* calculator(double x, double y, double vx, double vy) {
    double* results = new double[3];
    std::cout << "external c++ calculator has run with parameters " << x << " " << y << " " << vx << " " << vy << " \n";
   
    //Point pointC = calculateTargetCoordinates(x,y);
    Point pointC = calculateRealLifeCoordinates(x,y);
	double distanceToTarget = calculateDistanceToTarget(pointC.x,pointC.y); //calculate distance from base to target coordinates
    if(distanceToTarget > length_humerus + length_ulna || distanceToTarget < length_humerus - length_ulna){
        std::cout << "\nout of reach\n" << std::endl;
        return results; //old results
    }
	double* armAngles = calculateArmAngles(pointC.x,pointC.y,distanceToTarget); // calculate required angles for the elbow and base servos
	results[0] = calculateGripperAngle(vx,vy);	//calculate angle for the gripper to be perpendicular to the scissors
    results[1] = armAngles[0]; //store the arm angle variables
    results[2] = armAngles[1];
    return results;
}
