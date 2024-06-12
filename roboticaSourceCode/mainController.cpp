#include <cstdlib>
#include <iostream>
#include <array>
#include <string>
#include <sstream>
#include <cstdio>
#include <regex>
#include "roboticaFunctions.h"

int main() {
    std::cout << "main c++ program running-------------------------------------------------" << std::endl;

    std::array<double, 5> computerVisionResults; // empty array for computer vision results

    while(true) {
        std::string pythonFilepath = "python3 /home/rob8/Robotica24/roboticaSourceCode/python/"; // general filepath for the python scripts
        std::string commandComputerVision = pythonFilepath + "main.py"; // computer vision script
        std::string commandRotateServos = pythonFilepath + "rotateServos.py"; // servo command script
        FILE* pipe = popen(commandComputerVision.c_str(), "r"); // open a pipe for the computer vision results
        if (!pipe) { // if opening the pipe failed
            std::cerr << "popen failed!" << std::endl;
            return 1;
        }
        
        char buffer[128];
        std::string result = ""; // results of computer vision will be found in console. this string will contain the full results.
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }

        pclose(pipe); // close the pipe

        // Use regular expression to extract the numbers
        std::regex numberRegex(R"(\d+\.\d+|\d+)"); // This regex matches integers and floating point numbers
        std::sregex_iterator iter(result.begin(), result.end(), numberRegex);
        std::sregex_iterator end;

        size_t index = 0;
        while (iter != end && index < 5) {
            computerVisionResults[index] = std::stod((*iter).str());
            ++iter;
            ++index;
        }

        if (index < 5) {
            std::cerr << "Not enough numbers found in the output!" << std::endl;
        }

        double* calcResults = calculator(computerVisionResults[0], computerVisionResults[1], computerVisionResults[2], computerVisionResults[3]); // give the calculator the values from computer vision

        commandRotateServos = commandRotateServos + " " + std::to_string(calcResults[0]) + " " + std::to_string(calcResults[1]) + " " + std::to_string(calcResults[2]); // append the parameter arguments to the servo python script call
        system(commandRotateServos.c_str()); // call the servo python script

        checkBluetooth();

        std::cout << "main c++ program done-----------------------------------------------------" << std::endl;
    }
    return 0;
}
