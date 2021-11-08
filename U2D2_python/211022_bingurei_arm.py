#/usr/bin/env python

import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
    def clear():
        os.system('cls')
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *

# Control table
ADDR_TORQUE_ENABLE = 64
ADDR_CURRENT = 102
ADDR_ACCELERATION = 108
ADDR_VELOCITY = 112
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_MOVING = 122

# Protocol
PROTOCOL_VERSION = 2.0

# Setting
JOINT_ID = [11, 12, 13, 14, 15]
TOOL_ID = 16
BAUDRATE = 1000000
DEVICENAME = 'COM9'

JOINT_PROFILE_ACC = 5
JOINT_PROFILE_VEL = 50

GRIPPER_CURRENT = 100
GRIPPER_PROFILE_ACC = 10
GRIPPER_PROFILE_VEL = 200

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
GRIPPER_OPEN = 1
GRIPPER_CLOSE = 0

# Action Page
HOME = [2048, 1548, 2248, 2748, 2048]
EXIT = [2048, 2100, 2298, 2748, 2048]

CHECK_1 = [1848, 1548, 2248, 2748, 1848]
CHECK_2 = [2248, 1548, 2248, 2748, 2248]
CHECK_3 = [2048, 1348, 2348, 2848, 2048]
CHECK_4 = [2048, 1748, 2148, 2648, 2048]

DEMO_1 = [2048, 2548, 2048, 1448, 2048]
DEMO_2 = [2048, 2348, 2048, 1448, 2048]

torque_state = True
gripper_state = True

def Joint(Motion):
    for DXL_ID in range (0, 5):
        packetHandler.write4ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_GOAL_POSITION, Motion[DXL_ID])    
    Moving()

def Torque(onoff):
    if onoff:
        for DXL_ID in range (0, 5):
            packetHandler.write1ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
            packetHandler.write4ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_ACCELERATION, JOINT_PROFILE_ACC)
            packetHandler.write4ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_VELOCITY, JOINT_PROFILE_VEL)

        packetHandler.write1ByteTxRx(portHandler, TOOL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        packetHandler.write2ByteTxRx(portHandler, TOOL_ID, ADDR_CURRENT, GRIPPER_CURRENT)
        packetHandler.write4ByteTxRx(portHandler, TOOL_ID, ADDR_ACCELERATION, GRIPPER_PROFILE_ACC)
        packetHandler.write4ByteTxRx(portHandler, TOOL_ID, ADDR_VELOCITY, GRIPPER_PROFILE_VEL)
    else:
        for DXL_ID in range (0, 5):
            packetHandler.write1ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        packetHandler.write1ByteTxRx(portHandler, TOOL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

def Gripper(onoff):
    if onoff:
        packetHandler.write4ByteTxRx(portHandler, TOOL_ID, ADDR_GOAL_POSITION, 1248)
    else:
        packetHandler.write4ByteTxRx(portHandler, TOOL_ID, ADDR_GOAL_POSITION, 2648)

def Moving():
    time.sleep(0.3)
    while 1:
        moving = 0
        for DXL_ID in range (0, 5):
           cnt , result, err = packetHandler.read1ByteTxRx(portHandler, JOINT_ID[DXL_ID], ADDR_MOVING)
           moving = moving + cnt
        if moving == 0:
            break

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
# Open port
portHandler.openPort()
# Set port baudrate
portHandler.setBaudRate(BAUDRATE)  
# Torque on
Torque(TORQUE_ENABLE)
Gripper(GRIPPER_OPEN)
Joint(HOME)

while 1:
    print("\nh : Home Pose \nc : Joint Check\nd : Demo\nt : Toqrue ON/OFF\ng : Gripper OPEN/CLOSE\nq : Exit\n")
    value = input()
    if value == 'q':
        clear()
        Gripper(GRIPPER_OPEN)
        Joint(EXIT)
        Torque(TORQUE_DISABLE)
        portHandler.closePort()
        break
    
    elif value == 'c':
        clear()
        print("Joint Check")
        Joint(CHECK_1)
        Joint(CHECK_3)
        Joint(CHECK_2)
        Joint(CHECK_4)
        Joint(HOME)
        Joint(EXIT)

    elif value == 'h':
        clear()
        print("Going to [ HOME ] pose...\r")
        Joint(HOME)
        
    elif value == 'd':
        clear()
        print("Going to [ DEMO ] pose...\r")
        Joint(HOME)
        packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 1448)
        time.sleep(0.3) 
        Joint(DEMO_1)
        Gripper(GRIPPER_CLOSE)
        time.sleep(2) 
        packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 1048)
        time.sleep(0.5) 
        Joint(HOME)
        Joint(CHECK_1)
        Joint(CHECK_2)
        Joint(CHECK_1)
        Joint(CHECK_2)
        packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 1048)
        time.sleep(0.3) 
        Joint(DEMO_2)
        packetHandler.write4ByteTxRx(portHandler, 12, ADDR_GOAL_POSITION, 2500)
        time.sleep(0.3) 
        Gripper(GRIPPER_OPEN)
        time.sleep(2) 
        packetHandler.write4ByteTxRx(portHandler, 14, ADDR_GOAL_POSITION, 1048)
        time.sleep(0.5) 
        Joint(HOME)
        Joint(EXIT)

    elif value == 't':
        clear()
        if torque_state:
            print("Torque [ OFF ]")
            Torque(TORQUE_DISABLE)
            torque_state = False
        else:
            print("Torque [ ON ]")
            Torque(TORQUE_ENABLE)
            torque_state = True

    elif value == 'g':
        clear()
        if gripper_state:
            print("Gripper [ CLOSE ]")
            Gripper(GRIPPER_CLOSE)
            gripper_state = False
        else:
            print("Gripper [ OPEN ]")
            Gripper(GRIPPER_OPEN)
            gripper_state = True
