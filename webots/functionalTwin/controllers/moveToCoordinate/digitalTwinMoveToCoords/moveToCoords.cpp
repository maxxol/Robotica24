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

//needed for robot classes
using namespace webots;

//code that gets executed starts here
int main() {
  //making an instance of the robot class
  Robot *robot = new Robot();
  
  // Get handles to the motors
  Motor *arm1motor = robot->getMotor("arm1motor");
  Motor *arm2motor = robot->getMotor("arm2motor");
  Motor *rightFinger = robot->getMotor("rightGripperFinger");
  Motor *leftFinger = robot->getMotor("leftGripperFinger");
  Motor *gripperHeight = robot->getMotor("gripperHeightMotor");
  
  // getting handles to the sensors
  PositionSensor *fingerPositionSensor = robot->getPositionSensor("rightGripperFinger_sensor");
  PositionSensor *gripperHeightSensor = robot->getPositionSensor("gripperHeightSensor");
  // enable sensors
  fingerPositionSensor->enable(64);
  gripperHeightSensor->enable(64);
  

  double speed = 1; // it go fast or it go slow
  double maxGripperAngle = -0.065; //the higher this is, the more the fingers rotate inwards.
  std::string gripperState = "gripping"; //initial gripper state
  
  //setting up motors for function
  arm1motor->setPosition(INFINITY);
  arm2motor->setPosition(INFINITY);
  rightFinger->setPosition(INFINITY);
  leftFinger->setPosition(INFINITY);
  gripperHeight->setPosition(INFINITY);
  
  
  //setting initial speeds
  arm1motor->setVelocity(0);
  arm2motor->setVelocity(0);
  rightFinger->setVelocity(0);
  leftFinger->setVelocity(0);
  gripperHeight->setVelocity(-0.1*speed);
  
  
  // Main control loop
  while (robot->step(64) != -1) {// This loop will continue running until the simulation is stopped
  
    //allow the sensors to sense stuff because they are sensitive
    double fingerPosition = fingerPositionSensor->getValue();
    double gripperHeightPosition = gripperHeightSensor->getValue();
    //std::cout << gripperHeightPosition << std::endl; //console log for debug
    std::cout << fingerPosition << std::endl; //console log for debug
    
    if(gripperHeightPosition <= -0.17){
    rightFinger->setVelocity(0.2*speed);
    leftFinger->setVelocity(0.2*speed);
    gripperHeight->setVelocity(0);
    //std::cout << "in this loop" << std::endl; //console log for debug
    }
    
    
    //if the gripper has closed
    if(fingerPosition > maxGripperAngle && gripperState == "gripping"){
      //stop moving the gripper fingers
      std::cout << "set to 0" << std::endl; //console log for debug
      maxGripperAngle = -0.9; //change gripper angle to maximum external rotation for later
      gripperState = "holding"; //the gripper is currently presumably holding something
      gripperHeight->setVelocity(0.1*speed); //move the gripper-arm upwards
      
      //std::cout << gripperHeightPosition << std::endl; //console log for debug
    }
    if(gripperHeightPosition>=0){ //true if gripper is in position 0(base position tends to be slightly above or below)
      
      arm1motor->setVelocity(-0.1*speed);
      arm2motor->setVelocity(-0.1*speed);
      
      //std::cout << "in this loop" << std::endl; //console log for debug
      }
      
    // if(Position < maxGripperAngle && gripperState == "releasing"){
      // rightFinger->setVelocity(speed);
      // leftFinger->setVelocity(speed);
      // maxGripperAngle = 0.15;
      // gripperState = "gripping";
    // }
  }
  
  delete robot;
  return 0;
}