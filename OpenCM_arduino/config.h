#include <DynamixelSDK.h>

#define ADDR_TORQUE_ENABLE    64
#define ADDR_CURRENT          102
#define ADDR_ACCELERATION     108
#define ADDR_VELOCITY         112
#define ADDR_GOAL_POSITION    116
#define ADDR_PRESENT_POSITION 132
#define ADDR_MOVING           122

#define PROTOCOL_VERSION      2.0

#define TOOL_ID               16
#define BAUDRATE              1000000
#define DEVICENAME            "3"

#define TORQUE_ENABLE         1
#define TORQUE_DISABLE        0

#define JOINT_PROFILE_ACC     5
#define JOINT_PROFILE_VEL     50

#define GRIPPER_CURRENT       100
#define GRIPPER_PROFILE_ACC   10
#define GRIPPER_PROFILE_VEL   200
#define GRIPPER_OPEN          1
#define GRIPPER_CLOSE         0

#define START_BUTTON          16
#define STOP_BUTTON           17

const int JOINT_ID[5] = {11, 12, 13, 14, 15};

int32_t HOME[5] = {2048, 1548, 2248, 2748, 2048};
int32_t EXIT[5] = {2048, 2100, 2298, 2748, 2048};
int32_t DEMO_1[5] = {2048, 2548, 2048, 1448, 2048};
int32_t DEMO_2[5] = {2048, 2348, 2048, 1448, 2048};

boolean torque_state = true;
boolean gripper_state = true;

dynamixel::PortHandler *portHandler;
dynamixel::PacketHandler *packetHandler;

void Init(){
  pinMode(START_BUTTON, INPUT);
  pinMode(STOP_BUTTON, INPUT);

  portHandler = dynamixel::PortHandler::getPortHandler(DEVICENAME);
  packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

  portHandler->openPort();
  portHandler->setBaudRate(BAUDRATE);
}

void Torque (boolean onoff) {
  if (onoff == true) {
    for (int i = 0; i < 5; i++) {
      packetHandler->write1ByteTxRx(portHandler, JOINT_ID[i], ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
      packetHandler->write4ByteTxRx(portHandler, JOINT_ID[i], ADDR_ACCELERATION, JOINT_PROFILE_ACC);
      packetHandler->write4ByteTxRx(portHandler, JOINT_ID[i], ADDR_VELOCITY, JOINT_PROFILE_VEL);
    }
    packetHandler->write1ByteTxRx(portHandler, TOOL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE);
    packetHandler->write2ByteTxRx(portHandler, TOOL_ID, ADDR_CURRENT, GRIPPER_CURRENT);
    packetHandler->write4ByteTxRx(portHandler, TOOL_ID, ADDR_ACCELERATION, GRIPPER_PROFILE_ACC);
    packetHandler->write4ByteTxRx(portHandler, TOOL_ID, ADDR_VELOCITY, GRIPPER_PROFILE_VEL);
  }
  else {
    for (int i = 0; i < 5; i++) {
      packetHandler->write1ByteTxRx(portHandler, JOINT_ID[i], ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
    }
    packetHandler->write1ByteTxRx(portHandler, TOOL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE);
  }
}

void Joint (int32_t *motion) {
  for (int i = 0; i < 5; i++)
    packetHandler->write4ByteTxRx(portHandler, JOINT_ID[i], ADDR_GOAL_POSITION, motion[i]);
}

void Set (int ID, int32_t GOAL) {
  packetHandler->write4ByteTxRx(portHandler, ID, ADDR_GOAL_POSITION, GOAL);
}

void Gripper (boolean onoff) {
  if (onoff == true)
    packetHandler->write4ByteTxRx(portHandler, TOOL_ID, ADDR_GOAL_POSITION, 1248);
  else
    packetHandler->write4ByteTxRx(portHandler, TOOL_ID, ADDR_GOAL_POSITION, 2648);
}

void Moving() {
  uint8_t cnt = 0;
  delay(300);
  while (1) {
    int moving = 0;
    for (int i = 0; i < 5; i++) {
      packetHandler->read1ByteTxRx(portHandler, JOINT_ID[i], ADDR_MOVING, &cnt);
      moving += cnt;
    }
    if (moving == 0)
      break;
  }
}
