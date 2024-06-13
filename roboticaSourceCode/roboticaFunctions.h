// roboticaFunctions.h
double* calculator(double x, double y, double vx, double vy);

double calculateDistanceToTarget(int x,int y);
double* calculateArmAngles(double x,double y,double distanceToTarget);

void checkBluetooth();
struct Point {
	double x;
	double y;
};