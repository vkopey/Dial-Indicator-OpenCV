#include <Stepper.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup()
{
	// set the speed at 60 rpm:
	myStepper.setSpeed(60);
	// initialize the serial port:
	Serial.begin(9600);
}

void loop() 
{
while (Serial.available() > 0) {
 int x = Serial.parseInt();
 if (Serial.read() == '\n') {
      //Serial.print(x); 
      myStepper.step(x);
      delay(100);
      }
      }
}
