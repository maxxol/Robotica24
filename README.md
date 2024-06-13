# Robotica24
code for the project "robotica" 2023-2024 for NHL-Stenden

HOW TO USE:
1. open cmd and go to the folder you wish to contain the project folder 'cd [child folder]'
2. run 'git clone https://github.com/maxxol/Robotica24.git'
3. run 'cd Robotica24'
4. push/pull/commit from this directory using your favourite terminal application.



*main*:  
g++ -std=c++11 roboticaSourceCode/mainController.cpp roboticaSourceCode/calculator.cpp roboticaSourceCode/checkBluetooth.cpp -o mainController
./mainController


*scissors*: 
g++ -std=c++11 hardcoded_scripts/scissors/scissorsController.cpp roboticaSourceCode/calculator.cpp -o scissorsController
./scissorsController


*kilogram*: 
python3 /home/rob8/Robotica24/hardcoded_scripts/kilo.py