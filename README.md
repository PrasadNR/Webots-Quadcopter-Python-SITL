# Webots-Quadcopter-Python-SITL

_Note: This repository is under heavy development right now (and will likely be available by December 2019)._

## Background

A couple of years ago, I had authored a paper on object tracking Quadcopter. (Link: https://www.academia.edu/40403950/Single_Horizontal_Camera-Based_Object_Tracking_Quadcopter_Using_StaGaus_Algorithm ) I had some difficulties with reproducible results (with physical drone as mentioned in the paper). However, back then, I ended up building a ROS and Gazebo based multi-type multi-vehicle SITL (Software In The Loop) simulator (as detailed in the paper). The setup was extensive and worked only with a specific version of Ubuntu.

Also, few of the repositories have been archived now and I believe Erle Robotics has shut down completely and their github repositories are archived (which means that my ROS Gazebo SITL simulator may/may not be fully reproducible).

## Solution

1. Building a cross-platform compatible (main target OS being Windows, Linux and Mac OS) with pure Python implementation of controllers for multi-type, multi-vehicle SITL simulator. As I could not find anything like this yet for object tracking in Webots, I started out with Mavic 2 Pro Quadcopter and Pioneer 3DX rover.

2. I also wrote pure Python SITL Flight Controller (for waypoint navigation) as I could not find pure general purpose quadcopter controller in Python for SITL. It can also be used in hardware (and it is general purpose code, so, it will work with all hardwares that can run Python interpreter).

<p align="center">
  <img src="docs/doc_image.jpeg" width="80%">
</p>