#include "config.h"

void setup() {
  // put your setup code here, to run once:
  Init();
  Torque(TORQUE_ENABLE);
  Gripper(GRIPPER_OPEN);
  Joint(HOME);
  Moving();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(START_BUTTON)) {
    delay(500);
    Joint(HOME);
    Moving();
    Set(14, 1448);
    delay(300);
    Joint(DEMO_1);
    Moving();
    Gripper(GRIPPER_CLOSE);
    delay(200);
    Set(14, 1048);
    delay(500);
    Joint(HOME);
    Moving();
    delay(1000);
    Set(14, 1048);
    delay(300);
    Joint(DEMO_2);
    Moving();
    Set(12, 2500);
    delay(300);
    Gripper(GRIPPER_OPEN);
    delay(200);
    Set(14, 1048);
    delay(500);
    Joint(HOME);
    Moving();
    Joint(EXIT);
    Moving();
  }
  else if (digitalRead(STOP_BUTTON)) {
    delay(500);
    Gripper(GRIPPER_OPEN);
    Joint(EXIT);
    Moving();
    Torque(TORQUE_DISABLE);
    portHandler->closePort();
    return;
  }
}
