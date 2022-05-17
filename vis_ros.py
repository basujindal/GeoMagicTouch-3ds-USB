#!/usr/bin/env python2
# import rospy
# from std_msgs.msg import String
# from geometry_msgs.msg import PoseStamped
# import math
# import time
# import numpy as np
# from scipy.spatial.transform import Rotation
# import matplotlib.pyplot as plt

# li = []
# def move_bot(data):
#     pos = data.pose.position

    # df = pd.DataFrame(columns = ['Timestamp', 'Input_L', 'PSM_L', 'Gripper_L', 'Puzzle_position'])
    # df.to_csv("Experiment1.csv")
    # row = {'Timestamp': 0, 'Input_L': 0, 'PSM_L': (0,0,0), 'Gripper_L':(0,0), 'Puzzle_position':0}

    # # Getting object handles 
    # targetID = sim.getObjectHandle('TargetPSMR')
    # gripper1 =  sim.getObjectHandle("J3_dx_TOOL2")
    # gripper2 =  sim.getObjectHandle("J3_sx_TOOL2")
    # toolPitch =  sim.getObjectHandle("/RCM_PSM2/J2_TOOL2")
    # toolRoll =  sim.getObjectHandle("J1_TOOL2")

    # # Reading initial position
    # pos =  sim.getObjectPosition(targetID, -1)
    # posg1, posg2 =  sim.getJointPosition(gripper1),  sim.getJointPosition(gripper2)
    # tool_roll, tool_pitch =  sim.getJointPosition(toolRoll), sim.getJointPosition(toolPitch)
    # print("TargetID & Position = ", targetID, pos, gripper1, gripper2)


    # # Logging initial position
    # row['PSM_L'] = (pos, tool_roll, tool_pitch)
    # row['Gripper_L'] = (posg1, posg2)
    # row['Timestamp'] = time.time()
    # df = df.append(row, ignore_index=True)
    # df.to_csv("Experiment1.csv")

    # init_joy = 100.0
    # url =  '10.42.0.1'
    # js_ik = json.loads( urllib.request.urlopen('http://' +  url + ':8000/dvrk/apijoy/').read().decode('utf-8'))
    # dely, delx, delz = float(js_ik['x']), float(js_ik['y']), float(js_ik['z'])

    # oldflag = 1
    # scale = 0.0005
    # scale_gripper = 0.05
    # movex, movey, movez = 0,0,0
    # correction_factor = 0.5
    # yaw_sensitivity = 1
    # roll_sensitivity = 0.5
    

    # for i in range(MAX_INT):
    #     flag = 0

    #     delx_old = delx
    #     dely_old = dely
    #     delz_old = delz

    #     js_ik = json.loads( urllib.request.urlopen('http://' + url + ':8000/dvrk/apijoy/').read().decode('utf-8'))
    #     dely, delx,delz, open_grip, close_grip,sensor_on, scale = float(js_ik['x']), float(js_ik['y']), float(js_ik['z']),js_ik['o'],js_ik['c'],js_ik['s'],float(js_ik['sensitivity'])  
    #     row['Input_L'] = js_ik

    #     if not sensor_on:
    #     # if 1:

    #         movex = -(delx - delx_old)
    #         movey = (dely - dely_old)
    #         movez = -(delz - delz_old)
            

    #         scale /= 16667
    #         if (movez or movex or movey):
    #             flag = 1

    #             if delx != init_joy:
    #                 pos[0] -= movex*scale

    #             if dely != init_joy:
    #                 pos[1] += movey*scale

    #             if delz != init_joy:
    #                 pos[2] += movez*scale

    #             print(movez or movex or movey)

    #              sim.setObjectPosition(targetID,-1,pos)

    #         if open_grip or close_grip:
    #             flag = 1
    #             posg1 += (open_grip-close_grip)*scale_gripper
    #             posg2 += (open_grip-close_grip)*scale_gripper

    #              sim.setJointPosition(gripper1, posg1) #gripper1
    #              sim.setJointPosition(gripper2, posg2) #gripper2


    #         if(flag):
    #             row['PSM_L'] = (pos, tool_roll, tool_pitch)
    #             row['Gripper_L'] = (posg1, posg2)
    #             row['Timestamp'] = time.time()
    #             df = df.append(row, ignore_index=True)
    #             df.to_csv("Experiment1.csv")
    #             flag = 0


    #     if sensor_on:
    #     # if 0:

    #         a = urllib.request.urlopen('http://10.42.0.10:8080/sensors.json')
    #         a = json.loads(a.read().decode('utf-8'))["rot_vector"]['data']

    #         i = len(a) -1
    #         quat = [a[i][1][3]] + a[i][1][:3]
    #         rot = Rotation.from_quat(quat)
    #         euler = rot.as_euler('xyz', degrees=True) #(mobile-yaw, mobile-pitch,mobile-roll )
    #         na,nb,nc = math.radians(euler[0]),math.radians(euler[1]),math.radians(euler[2])

    #         if oldflag:
    #             oa,ob,oc = na,nb,nc

    #         pos_roll = (na-oa)
    #         pos_yaw = (nc-oc)
    #         pos_pitch = (nb-ob)
            

    #     # sensor values jump from -pi to pi, so this ensures that there is no sudden change  

    #         if abs(pos_roll) > correction_factor:
    #             pos_roll = 0 
    #         if abs(pos_yaw) > correction_factor:
    #             pos_yaw = 0 
            
    #         tool_pitch += pos_yaw*yaw_sensitivity
    #         tool_roll += pos_roll*roll_sensitivity
    #         print(tool_pitch,  tool_roll)
    #         sim.setJointPosition(toolPitch, tool_pitch) #base-yaw (-pi, pi)   
    #         sim.setJointPosition(toolRoll, tool_roll)  #tool-roll (-pi, pi)

    #         row['PSM_L'] = (pos, tool_roll, tool_pitch)
    #         row['Timestamp'] = time.time()
    #         df = df.append(row, ignore_index=True)
    #         df.to_csv("Experiment1.csv")
        
    #         oa,ob,oc = na,nb,nc
    #         oldflag = 0


# def move_bot(data):
#     orient = data.pose.orientation
#     rot = Rotation.from_quat([orient.x, orient.y, orient.z, orient.w])
#     euler = rot.as_euler('xyz', degrees=True) #(mobile-yaw, mobile-pitch,mobile-roll )
#     # print(math.radians(euler[0]),math.radians(euler[1]),math.radians(euler[2]))
#     li.append(math.radians(euler[0]))
#     plt.plot(li[-10:])
#     plt.show(block=True)
    # time.sleep(0.01)
    # pclear()
   
# def listener():

#     rospy.init_node('position_listen', anonymous=True)
#     # rospy.init_node('pose_listen', anonymous=True)
#     rospy.Subscriber("/phantom/pose", PoseStamped, move_bot)
#     rospy.spin()


# if __name__ == '__main__':
    
#     listener()


# from matplotlib.animation import FuncAnimation


# class Visualiser:
#     def __init__(self):
#         self.fig, self.ax = plt.subplots()
#         self.ln, = plt.plot([], [], 'ro')
#         self.x_data, self.y_data = [] , []

#     def plot_init(self):
#         self.ax.set_xlim(0, 10000)
#         self.ax.set_ylim(-1, 1)
#         return self.ln
    
#     def getYaw(self, pose):
#         orient = pose.orientation
#         rot = Rotation.from_quat([orient.x, orient.y, orient.z, orient.w])
#         euler = rot.as_euler('xyz', degrees=True) #(mobile-yaw, mobile-pitch,mobile-roll )
#         # print(math.radians(euler[0]),math.radians(euler[1]),math.radians(euler[2]))
#         return math.radians(euler[1])


#     def odom_callback(self, msg):
#         yaw_angle = self.getYaw(msg.pose)
#         self.y_data.append(yaw_angle)
#         x_index = len(self.x_data)
#         self.x_data.append(x_index+1)
    
#     def update_plot(self, frame):
#         self.ln.set_data(self.x_data, self.y_data)
#         return self.ln


# rospy.init_node('position_listen', anonymous=True)
# # rospy.init_node('pose_listen', anonymous=True)

# vis = Visualiser()
# rospy.Subscriber("/phantom/pose", PoseStamped, vis.odom_callback)

# ani = FuncAnimation(vis.fig, vis.update_plot, init_func=vis.plot_init)
# plt.show(block=True) 