#include <cstdlib>
#include <iostream>
#include <array>
#include <string>
#include <sstream>
#include <cstdio>
#include "roboticaFunctions.h"

int main() {
    std::cout << "main c++ program running-------------------------------------------------" << std::endl;

    

    // Call the Python CV script and capture the output
    std::array<double, 4> computerVisionResults;

    while(true){
        std::string pythonFilepath = "python3 /home/rob8/Desktop/roboticaSourceCode/python/";
        std::string commandComputerVision = pythonFilepath + "computerVision.py";
        std::string commandRotateServos = pythonFilepath + "rotateServos.py";   
        FILE* pipe = popen(commandComputerVision.c_str(), "r");
        if (!pipe) {
            std::cerr << "popen failed!" << std::endl;
            return 1;
        }
        
        char buffer[128];
        std::string result = "";
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }

        pclose(pipe);

        std::stringstream ss(result);
        for (double& value : computerVisionResults) {
            ss >> value;
        }

        double* calcResults = calculator(computerVisionResults[0], computerVisionResults[1], computerVisionResults[2], computerVisionResults[3]);
        //double* calcResults = calculator(320, 240, computerVisionResults[2], computerVisionResults[3]);
        //std::cout << "RESULTS: " << calcResults[0] << std::endl;

        commandRotateServos = commandRotateServos + " " + std::to_string(calcResults[0]) + " " + std::to_string(calcResults[1]) + " " + std::to_string(calcResults[2]);
        system(commandRotateServos.c_str());

        checkBluetooth();

        std::cout << "main c++ program done-----------------------------------------------------" << std::endl;
       
    }
    return 0;
}
