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

    int x = 0;
    int y = 0;


    while(true) {
        std::string pythonFilepath = "python3 /home/rob8/Robotica24/roboticaSourceCode/python/"; // general filepath for the python scripts
        std::string commandRotateServos = pythonFilepath + "rotateServos.py"; // servo command script
        
        Point pointC;
        pointC.x = 0;
        pointC.y = 0; // coords within a circle around 0,0 with a radius of 70. close to 0,0 is unreachable 
        double distanceToTarget = calculateDistanceToTarget(pointC.x,pointC.y); //calculate distance from base to target coordinates

        double* armAngles = calculateArmAngles(pointC.x,pointC.y,distanceToTarget); // calculate required angles for the elbow and base servos
        //results[0] = calculateGripperAngle(vx,vy);	//calculate angle for the gripper to be perpendicular to the scissors
        results[1] = armAngles[0]; //store the arm angle variables
        results[2] = armAngles[1];



        double* calcResults = calculator(computerVisionResults[2], computerVisionResults[3], computerVisionResults[4], computerVisionResults[5]); // give the calculator the values from computer vision

        commandRotateServos = commandRotateServos + " " + std::to_string(calcResults[0]) + " " + std::to_string(calcResults[1]) + " " + std::to_string(calcResults[2]); // append the parameter arguments to the servo python script call
        system(commandRotateServos.c_str()); // call the servo python script



        checkBluetooth();
        std::cout << "main c++ program done-----------------------------------------------------" << std::endl;
    }
    return 0;
}
