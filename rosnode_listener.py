import rospy
from geometry_msgs.msg import PoseStamped
import time
import pandas as pd
from zmqRemoteApi import RemoteAPIClient
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="Experiment logs file name")
args = vars(ap.parse_args())
log_file = args["name"]


client = RemoteAPIClient()
sim = client.getObject('sim')

# Getting object handles 
targetID = sim.getObjectHandle('TargetPSMR')
gripper1 =  sim.getObjectHandle("J3_dx_TOOL2")
gripper2 =  sim.getObjectHandle("J3_sx_TOOL2")
toolPitch =  sim.getObjectHandle("/RCM_PSM2/J2_TOOL2")
toolRoll =  sim.getObjectHandle("J1_TOOL2")
peg = sim.getObjectHandle("Peg")

print("Target ID = ", targetID)

# Scaling factors for mapping between hardware and simulation
scale = 1 # mapping geomagic stylus to simulated PSM
yaw_sensitivity = 1 # Geomagic yaw to PSM tooltip yaw
roll_sensitivity = 1.3 # Geomagic Roll to PSM tip roll

class callback():

    def __init__(self):
        self.init_pos = False
        self.init_orient = False
        self.posy, self.posx, self.posz = 0,0,0 # Current PSM tooltip position

        # Old tooltip position
        self.posx_old, self.posy_old, self.posz_old = self.posx, self.posy, self.posz
        # old values of tool yaw, pitch and roll
        self.oa, self.ob, self.oc = 0,0,0
        # Tool Yaw and Roll will only change when sensor_on = True
        self.sensor_on = False 

        # CSV file to log simultion data
        self.df = pd.DataFrame(columns = ['Timestamp', 'PSM_xyz', 'PSM_roll_pitch', 'Gripper_angle_radians', 'Puzzle_position_xyz'])
        self.row = {'Timestamp': 0, 'PSM_xyz': (0,0,0), 'PSM_roll_pitch': (0,0), 'Gripper_angle_radians':(0,0), 'Puzzle_position_xyz':0}

        # Reading initial position of the Left PSM
        self.pos =  sim.getObjectPosition(targetID, -1)
        self.posg1, self.posg2 =  sim.getJointPosition(gripper1),  sim.getJointPosition(gripper2)
        self.tool_roll, self.tool_pitch =  sim.getJointPosition(toolRoll), sim.getJointPosition(toolPitch)

        # Logging initial position
        self.row['Timestamp'] = time.time()
        self.row['PSM_xyz'] = (self.pos[0],self.pos[1],self.pos[2])
        self.row['PSM_roll_pitch'] = (self.tool_roll, self.tool_pitch)
        self.row['Gripper_angle_radians'] = (self.posg1, self.posg2)
        self.row['Puzzle_position_xyz'] = sim.getObjectPosition(peg, -1)
        self.df = self.df.append(self.row, ignore_index=True)
        self.df.to_csv(log_file)

    def move_bot(self, data):

        '''
        Pressing both buttons together on stylus will set 
        data.pose.orientation.w value to 3 and flip sensor_on bool value.
        Pressing the upper button only will set the value to 2 and
        open the PSM gripper and the bottom will set the value to 1 and 
        close the gripper. 
        '''
        log_flag = 0

        grip = -1
        if data.pose.orientation.w == 3:
            self.sensor_on = not self.sensor_on
        elif int(data.pose.orientation.w) == 2: #Close the gripper
            grip = 0
        elif int(data.pose.orientation.w) == 1: #Open the gripper
            grip = 0.7

        # data.pose.position gives stylus xyz coordinates
        stylus_pos = data.pose.position
        self.posx, self.posy, self.posz = stylus_pos.x, stylus_pos.y, stylus_pos.z

        # Moving the PSM tolltip proportional to the change in stylus position
        if self.init_pos and not self.sensor_on:

            movex = self.posx - self.posx_old
            movey = self.posy - self.posy_old
            movez = self.posz - self.posz_old
            print(movex, movey,movez)

            if(movex or movey or movez):
                log_flag = 1
                self.pos[0] += movey*scale
                self.pos[1] -= movex*scale
                self.pos[2] += movez*scale

                sim.setObjectPosition(targetID,-1,self.pos)

            # Moving the PSM gripper according to the button presses
            if grip == 0.7 or grip == 0: 
                self.posg1 , self.posg2 = grip, grip
                sim.setJointPosition(gripper1, self.posg1) #gripper1
                sim.setJointPosition(gripper2, self.posg2) #gripper2

        else:
            log_flag = 1
            self.init_pos = 1
        
        self.posx_old, self.posy_old, self.posz_old = self.posx, self.posy, self.posz

        # Setting tooltip Roll and Yaw

        # data.pose.orientation gives stylus pitch, yaw and roll
        orient = data.pose.orientation
        na, nb, nc = orient.x, orient.y, orient.z

        if self.init_orient and self.sensor_on:
            log_flag = 1

            pos_roll = (nc-self.oc)
            pos_yaw = (nb-self.ob)
            
            self.tool_pitch += pos_yaw*yaw_sensitivity
            self.tool_roll += pos_roll*roll_sensitivity
            # print(self.tool_pitch, self.tool_roll)

            sim.setJointPosition(toolPitch, self.tool_pitch) 
            sim.setJointPosition(toolRoll, self.tool_roll)

        else:
            self.init_orient = 1
        
        self.oa,self.ob,self.oc = na,nb,nc

        if log_flag:
            # Logging data
            self.row['Timestamp'] = time.time()
            self.row['PSM_xyz'] = (self.pos[0], self.pos[1], self.pos[2])
            self.row['PSM_roll_pitch'] = (self.tool_roll, self.tool_pitch)
            self.row['Gripper_angle_radians'] = (self.posg1, self.posg2)
            self.row['Puzzle_position_xyz'] = sim.getObjectPosition(peg, -1)
            self.df = self.df.append(self.row, ignore_index=True)
            self.df.to_csv(log_file)


cb = callback()
rospy.init_node('position_listen', anonymous=True)
# Subscribing to phantom/pose which gives xyz position. yaw, pitch, roll
# and button press event.
rospy.Subscriber("/phantom/pose", PoseStamped, cb.move_bot)
rospy.spin()