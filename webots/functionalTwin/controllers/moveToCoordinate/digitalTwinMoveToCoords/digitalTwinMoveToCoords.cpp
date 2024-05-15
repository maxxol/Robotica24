//creates the robot
#include <webots/Robot.hpp>
//motor controls
#include <webots/Motor.hpp>
//sensor readings
#include <webots/PositionSensor.hpp> 
//console logs
#include <iostream> 
//strings because for some reason they are not a regular data type in c++ who made this language I hope they stub their toe
#include <string>

#include <cmath>

#include <thread>
#include <chrono>

#include <cstdlib> // for rand() and srand()
#include <ctime>   // for time()
//needed for robot classes
using namespace webots;


//making an instance of the robot class
Robot *robot = new Robot();

// Get handles to the motors
Motor *arm1Motor = robot->getMotor("arm1motor");
Motor *arm2Motor = robot->getMotor("arm2motor");
Motor *rightFinger = robot->getMotor("rightGripperFinger");
Motor *leftFinger = robot->getMotor("leftGripperFinger");
Motor *gripperHeight = robot->getMotor("gripperHeightMotor");

// getting handles to the sensors
PositionSensor *fingerPositionSensor = robot->getPositionSensor("rightGripperFinger_sensor");
PositionSensor *gripperHeightSensor = robot->getPositionSensor("gripperHeightSensor");
PositionSensor *arm1MotorPositionSensor = robot->getPositionSensor("arm1Sensor");
PositionSensor *arm2MotorPositionSensor = robot->getPositionSensor("arm2Sensor");

double armBone1Length = 2.54; //the humerus of the robot arm (distance between joints) 2.54 for webots 
double armBone2Length = 1.15; //the radius/ulna of the robot arm (distance between joints) 1.22 for webots

double arm1MotorAngle;
double arm2MotorAngle;
double requiredArm1MotorAngle;
double requiredArm2MotorAngle;
bool arm1HasReachedPosition = false;
bool arm2HasReachedPosition = false;
int arm1Wraps = 0;
int arm2Wraps = 0;
	
bool linksOfRechtsOm(double robot, double target) {
    // Calculate the difference between the two radians
    double difference = target - robot;

    // Normalize the difference to be within [-pi, pi]
    difference = fmod(difference + M_PI, 2 * M_PI) - M_PI;

    //std::cout << "robot: " << robot << " target: "<< target << std::endl;
    //std::cout << "Angle between robot and target: " << difference << " radians" << std::endl;

    if (difference < 0 && difference > -M_PI) {
        return true; // Clockwise rotation
    } else {
        return false; // Counterclockwise rotation
    }
}

void MoveArmToCoordinates(double coordinateX, double coordinateY, double speed) {
    double distanceFromBaseToTarget = sqrt(pow(coordinateX, 2) + pow(coordinateY, 2));

    // Check if the target is reachable for the gripper
    if (distanceFromBaseToTarget > armBone1Length + armBone2Length || distanceFromBaseToTarget < abs(armBone1Length - armBone2Length)) {
        std::cout << "Target is outside robot range" << std::endl;
        return;
    }
    // else {
        //std::cout << "Target is inside robot range" << std::endl;
    // }

    // Calculate required angles
    requiredArm2MotorAngle = fmod((acos((pow(armBone1Length, 2) + pow(armBone2Length, 2) - pow(distanceFromBaseToTarget, 2)) / (2 * armBone1Length * armBone2Length)) + M_PI), (2 * M_PI));
    requiredArm1MotorAngle = fmod((atan2(coordinateY, coordinateX) - atan2((armBone2Length * sin(requiredArm2MotorAngle)), (armBone1Length + armBone2Length * cos(requiredArm2MotorAngle)))), (2 * M_PI));

    // Ensure required angles are within [0, 2*pi)
    if (requiredArm2MotorAngle < 0) {
        requiredArm2MotorAngle += (2 * M_PI);
    }
    if (requiredArm1MotorAngle < 0) {
        requiredArm1MotorAngle += (2 * M_PI);
    }

    // std::cout << "Required arm 2 angle: " << requiredArm2MotorAngle/M_PI << " pi radians" << std::endl;
    // std::cout << "Required arm 1 angle: " << requiredArm1MotorAngle/M_PI << " pi radians" << std::endl;
    // std::cout << "Required arm 2 angle: " << requiredArm2MotorAngle*(180/M_PI) << std::endl;
    // std::cout << "Required arm 1 angle: " << requiredArm1MotorAngle*(180/M_PI) << std::endl;

    // Move the arms towards the required angles
    while (true) {
        arm1MotorAngle = arm1MotorPositionSensor->getValue()+arm1Wraps*2*M_PI;
        arm2MotorAngle = arm2MotorPositionSensor->getValue()+arm2Wraps*2*M_PI;
        
        if (arm1MotorAngle < 0) {
        arm1Wraps++;
        }
        if (arm1MotorAngle > 2*M_PI) {
        arm1Wraps--;
        }
        if (arm2MotorAngle < 0) {
        arm2Wraps++;
        }
        if (arm2MotorAngle > 2*M_PI) {
        arm2Wraps--;
        }
        
        // std::cout << "req " << requiredArm1MotorAngle  << std::endl;
        // std::cout << "cur " << arm1MotorAngle << std::endl;
        //std::cout << requiredArm1MotorAngle - arm1MotorAngle << std::endl;
        // Check if arm 1 has reached its target angle
        if (!arm1HasReachedPosition) {
            if (linksOfRechtsOm(arm1MotorAngle,requiredArm1MotorAngle)) {
                arm1Motor->setVelocity(-0.1 * speed); // Counterclockwise
            }
            else {
                arm1Motor->setVelocity(0.1 * speed); // Clockwise
            }

            if (arm1MotorAngle < requiredArm1MotorAngle+0.1 && arm1MotorAngle > requiredArm1MotorAngle-0.02) {
                arm1Motor->setVelocity(0);
                arm1HasReachedPosition = true;
                //std::cout << "Arm 1 reached target angle" << std::endl;
            }
        }

        // Check if arm 2 has reached its target angle
        if (!arm2HasReachedPosition) {
            if (linksOfRechtsOm(arm2MotorAngle,requiredArm2MotorAngle)) {
                arm2Motor->setVelocity(-0.2 * speed); // Counterclockwise
            }
            else {
                arm2Motor->setVelocity(0.2 * speed); // Clockwise
            }

            if(arm2MotorAngle < requiredArm2MotorAngle+0.01 && arm2MotorAngle > requiredArm2MotorAngle-0.02) {
                arm2Motor->setVelocity(0);
                arm2HasReachedPosition = true;
                //std::cout << "Arm 2 reached target angle" << std::endl;
            }
        }

        // Check if both arms have reached their target angles
        if (arm1HasReachedPosition && arm2HasReachedPosition) {
            arm1HasReachedPosition = false;
            arm2HasReachedPosition = false;
            //std::cout << "Both arms reached target angles\n" << std::endl;
            std::cout << "GOT IT\n "<< std::endl;
            break;
        }

        robot->step(1); // Add a small delay to prevent the loop from running too quickly
    }
}


//code that gets executed starts here
int main() {
  
  // enable sensors
  fingerPositionSensor->enable(64);
  gripperHeightSensor->enable(64);
  arm1MotorPositionSensor->enable(64);
  arm2MotorPositionSensor->enable(64);
  
    //setting up motors for function
  arm1Motor->setPosition(INFINITY);
  arm2Motor->setPosition(INFINITY);
  rightFinger->setPosition(INFINITY);
  leftFinger->setPosition(INFINITY);
  gripperHeight->setPosition(INFINITY);
  
  
  //setting initial speeds
  arm1Motor->setVelocity(0);
  arm2Motor->setVelocity(0);
  rightFinger->setVelocity(0);
  leftFinger->setVelocity(0);
  gripperHeight->setVelocity(0);

 

  // Seed the random number generator
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    std::cout << "main loop"<< std::endl;
  double speed = 1; // it go fast or it go slow
  double maxGripperAngle = -0.065; //the higher this is, the more the fingers rotate inwards.
  std::string gripperState = "gripping"; //initial gripper state
 
  
  
  // Main control loop
  while (robot->step(64) != -1) {// This loop will continue running until the simulation is stopped
  
    //allow the sensors to sense stuff because they are sensitive
    //double fingerPosition = fingerPositionSensor->getValue();
    //double gripperHeightPosition = gripperHeightSensor->getValue();
    //std::cout << gripperHeightPosition << std::endl; //console log for debug
    //std::cout << fingerPosition << std::endl; //console log for debug
   

   // MoveArmToCoordinates(0.79,-1.56,speed);
   // std::this_thread::sleep_for(std::chrono::seconds(1));
   // MoveArmToCoordinates(0.21,2,speed);
   // std::this_thread::sleep_for(std::chrono::seconds(1));
   // MoveArmToCoordinates(-2.81,1.96,speed);
   // std::this_thread::sleep_for(std::chrono::seconds(1));
   // MoveArmToCoordinates(-2.663066,-2.554247,speed);
   // std::this_thread::sleep_for(std::chrono::seconds(1));
   
   

    // Generate a random number between -300 and 300 (to get 2 decimal places)
    int random_int1 = std::rand() % 601 - 300;
    int random_int2 = std::rand() % 601 - 300;

    // Convert the random integer to a double with 2 decimal places
    double random_double1 = static_cast<double>(random_int1) / 100.0;
    double random_double2 = static_cast<double>(random_int2) / 100.0;
    std::cout << "target: (" << random_double1 << "," << random_double2 << ")" << std::endl;
    MoveArmToCoordinates(random_double1,random_double2,speed);
    
  }
  
  delete robot;
  return 0;
}