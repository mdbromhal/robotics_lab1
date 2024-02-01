#!/usr/bin/env python3

import rospy

# Read turtlesim/Pose messages
from turtlesim.msg import Pose

# Read Turtlecontrol messages
from robotics_lab1.msg import Turtlecontrol

# Declaring a global variable for the Turtlecontrol messages
turtle_msg = Turtlecontrol()

# Declaring a global variable for the Pose messages
pose_msg = Pose()

import math

ROTATION_SCALE = 180.0/math.pi

def turtlesim_pose_callback(data):
	'''
	Function to retreive position date for the Turtlesim_node subscriber
	'''
	
	global pose_msg
	
	# Convert x and y to cm
	pose_msg.x = data.x
	pose_msg.y = data.y
	pose_msg.theta = data.theta * ROTATION_SCALE


def turtlecontrol_pose_callback(data):
	'''
	Function to retreive positional info from Turtlecontrol messages
	'''

	# Calling global variable
	global turtle_msg
	
	# Convert x and y to cm
	turtle_msg.kp = data.kp
	turtle_msg.xd = data.xd


def proportional_controller(data):
	'''
	This controller generates a control input (velocity of Turtlebot) to minimize error bw the desired output (target position for Turtlebot) and current output (current position of Turtlebot)
	'''
	
	# Equation is vt = Kp(xd - xt)
	vt = turtle_msg.kp * (turtle_msg.xd - pose_msg.x)
	
	return vt
	 
	
if __name__ == '__main__':

	# Initialize the node
	rospy.init_node('control node', anonymous=True)
	
	# Add suscriber to receive position info from turtlesim_node
	pos_sub1 = rospy.Subscriber('/turtle1/pose', Pose, turtlesim_pose_callback)
	
	# Second subscriber, subscribed to Tur
	pos_sub2 = rospy.Subscriber('/turtle1/control_params', Turtlecontrol, turtlecontrol_pose_callback)
	
	# Add publisher with new topic using Shortpos message
	pos_pub = rospy.Publisher('/turtle1/Turtlecontrol', Turtlecontrol, queue_size = 10)
	
	
	# Set frequency for this loop - 10 Hz
	loop_rate = rospy.Rate(10)
	
	while not rospy.is_shutdown():
	
		vt = proportional_controller()
		
		# Publish the message
		pos_pub.publish(vt)
		
		# Wait 0.1s until next loop and repeat
		loop_rate.sleep()
