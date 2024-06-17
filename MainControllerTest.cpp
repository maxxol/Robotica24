#include <cstdlib>
#include <iostream>
#include <array>
#include <string>
#include <sstream>
#include <cstdio>
#include <regex>
#include "roboticaSourceCode/roboticaFunctions.h"

int main() {
    std::cout << "main c++ program running-------------------------------------------------" << std::endl;

    std::array<double, 6> computerVisionResults; // empty array for computer vision results

    double length_humerus = 40.5; // Length of the humerus in units (cm)
    double length_ulna = 32.0; // Length of the ulna in units (cm)
    int x = 60;
    int y = 0;


    while(true) {
        double* results = new double[3];
        std::string pythonFilepath = "python3 /home/rob8/Robotica24/roboticaSourceCode/python/"; // general filepath for the python scripts
        std::string commandRotateServos = pythonFilepath + "rotateServos.py"; // servo command script
        
        Point pointC;
        pointC.x = x;
        pointC.y = y; // coords within a circle around 0,0 with a radius of 70. close to 0,0 is unreachable 
        double distanceToTarget = calculateDistanceToTarget(pointC.x,pointC.y); //calculate distance from base to target coordinates
        if(distanceToTarget > length_humerus + length_ulna || distanceToTarget < length_humerus - length_ulna){
		std::cout << "\nout of reach\n" << std::endl; //cannot reach the point, return previous, assume object didnt move.
	    }
        double* armAngles = calculateArmAngles(pointC.x,pointC.y,distanceToTarget); // calculate required angles for the elbow and base servos
        //results[0] = calculateGripperAngle(vx,vy);	//calculate angle for the gripper to be perpendicular to the scissors
        results[1] = armAngles[0]; //store the arm angle variables
        results[2] = armAngles[1];
        if (results[1] > 150)
            results[1] -= 360;
        if (results[2] > 150)
            results[2] -= 360;
        std::cout << "angles: "<< results[1] << " "<< results[2] << std::endl;

        commandRotateServos = commandRotateServos + " " + std::to_string(0) + " " + std::to_string(results[1]) + " " + std::to_string(results[2]); // append the parameter arguments to the servo python script call
        system(commandRotateServos.c_str()); // call the servo python script



        checkBluetooth();
        std::cout << "main c++ program done-----------------------------------------------------" << std::endl;
    }
    return 0;
}
