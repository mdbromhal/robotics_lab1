#!/usr/bin/env python3

import rospy

# Read turtlesim/Pose messages
from turtlesim.msg import Pose

# Read Turtlecontrol messages
from robotics_lab1.msg import Turtlecontrol

# Declaring a global variable
pos_msg = Turtlecontrol()

import math

ROTATION_SCALE = 180.0/math.pi

def turtlesim_pose_callback(data):
	'''
	Function to retreive position date for the Turtlesim_node subscriber
	'''

	# Convert angular position to degrees
	rot_in_degree = data.theta * ROTATION_SCALE
	
	# Convert x and y to cm
	x_in_cm = data.x * 100
	y_in_cm = data.y * 100


def turtlecontrol_pose_callback(data):
	'''
	Function to retreive positional info from Turtlecontrol messages
	'''

	# Calling global variable
	global pos_msg
	
	# Convert angular position to degrees
	pos_msg.theta = data.theta * ROTATION_SCALE
	
	# Convert x and y to cm
	pos_msg.x = data.x * 100
	pos_msg.y = data.y * 100
# WHICH ONE TO USE?

def proportional_controller(data):
	'''
	This controller generates a control input (velocity of Turtlebot) to minimize error bw the desired output (target position for Turtlebot) and current output (current position of Turtlebot)
	'''
	# Equation is vt = Kp(xd - xt)
	
	# DON'T ENTIRELY UNDERSTAND WHY WE USE DATA
	pos_msg.kp = data.kp
	pos_msg.xd = data.xd
	
	vt = pos_msg.kp * (pos_msg.xd - pos_msg.x) # IS THIS RIGHT?

if __name__ == '__main__':

	# Initialize the node
	rospy.init_node('control node', anonymous=True)
	
	# Add suscriber to receive position info from turtlesim_node
	pos_sub1 = rospy.Subscriber('/turtle1/pose', Pose, turtlesim_pose_callback)
	
	pos_sub2 = rospy.Subscriber('/turtle1/control_params', Turtlecontrol, proportional_controller)
	# DOES THIS CREATE A NEW TOPIC AUTOMATICALLY?
	# HOW TO WORK WITH PROPORTIONAL CONTROLLER?
	
	# Add publisher with new topic using Shortpos message
	pos_pub = rospy.Publisher('/turtle1/Turtlecontrol', Turtlecontrol, queue_size = 10)
	
	# Set frequency for this loop - 10 Hz
	loop_rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		
		# Publish the message
		pos_pub.publish(pos_msg)
		
		# Wait 0.1s until next loop and repeat
		loop_rate.sleep()
