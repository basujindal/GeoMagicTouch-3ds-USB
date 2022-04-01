
# Introduction


This repository has been forked from the following three repositories:
1. Francisco Suárez Ruiz, [http://fsuarez6.github.io](http://fsuarez6.github.io) for the Sensable PHANToM haptic device (https://github.com/fsuarez6/phantom_omni)

2. Bharat Mathur [https://github.com/bharatm11](https://github.com/bharatm11/Geomagic_Touch_ROS_Drivers)

3. By Johns Hopkins University [https://github.com/jhu-cisst-external](https://github.com/jhu-cisst-external/3ds-touch-openhaptics)

ROS packages developed by the [Group of Robots and Intelligent Machines](http://www.romin.upm.es/) from the [Universidad Politécnica de Madrid](http://www.upm.es/internacional). This group is part of the [Centre for Automation and Robotics](http://www.car.upm-csic.es/) (CAR UPM-CSIC). 


--- 

The goal of this repository is to facilitate the installation of:
1. GeoMagic/3DS Touch hapic device drivers (USB or Ethernet based)
2. OpenHaptics SDK (education version) 
3. ROS Drivers to communcate with the device on Ubuntu 18.04.

This was successfuly tested on Ubuntu 18.04 LTS 64 bits and ROS Melodic. (It didn't work for us on Ubuntu 20.04). 


# Install OpenHaptics SDK and GeoMagic/3DS Touch hapic device drivers

These scripts are provided to automate the installation process described in https://support.3dsystems.com/s/article/OpenHaptics-for-Linux-Developer-Edition-v34. The original instructions are at: https://s3.amazonaws.com/dl.3dsystems.com/binaries/Sensable/Linux/Installation+Instructions.pdf.

The 4 scripts provided will perform most of the steps required to download/install OR un-install the files required for the Touch drivers as well as the OpenHaptics SDK. The two install scripts should be executed without `sudo` though sudo privileges are required (you might be prompted for a password). This is so temporary files are not created with root id/gid.

The two uninstall scripts need to be executed with `sudo`.

# Notes

The install is a bit different from the process described in the 3DS instructions:
* Environment variables are set in `/etc/profile.d` instead of `/etc/environment`


# Install 3D Systems Geomagic Touch ROS Driver

1. Install Dependencies

```
sudo apt-get install --no-install-recommends freeglut3-dev g++ libdrm-dev libexpat1-dev libglw1-mesa libglw1-mesa-dev libmotif-dev libncurses5-dev libraw1394-dev libx11-dev libxdamage-dev libxext-dev libxt-dev libxxf86vm-dev tcsh unzip x11proto-dri2-dev x11proto-gl-dev x11proto-print-dev
```

2. Device setup

The haptic device always creates a COM Port as /dev/ttyACM0 and requires admin priviliges
```
sudo chmod 777 /dev/ttyACM0
```

Run `/usr/bin/Touch_Setup` and ensure that the device serial number is displayed 

3. Device Diagnostics

Run `/usr/bin/Touch_Diagnostic`. This can be used to calibrate the device, read encoders, apply test forces etc. 

4. Build the ROS Package

Run `catkin_make` inside this repo

5. Finally, launch ROS Node

```
source devel/setup.bash
roslaunch omni_common omni_state.launch 
```


Data from the haptic device can be read from the following rostopics:

  /phantom/button
  
  /phantom/force_feedback
  
  /phantom/joint_states
  
  /phantom/pose
  
  /phantom/state 


