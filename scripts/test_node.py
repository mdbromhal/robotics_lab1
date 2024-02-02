#!/usr/bin/env python3

import rospy

# Read turtlesim/Pose messages
from turtlesim.msg import Pose

# Import geometry_msgs/Twist for control commands
from geometry_msgs.msg import Twist

# Import Turtlecontrol messages for kp and xd commands
from robotics_lab1.msg import Turtlecontrol


# Declaring a global variable for the Pose messages
pose_msg = Pose()

# Declaring a global variable for Turtlecontrol messages
turtlecontrol_msg = Turtlecontrol()



def pose_callback(data):
	'''
	Function to retreive position data for the Turtlesim_node subscriber (pose_sub)
	'''
	global pose_msg
	
	pose_msg = data

def turtlecontrol_callback(data):
	'''
	Function to retreive data from Turtlecontrol subscriber (turtlecontrol_sub)
	'''
	global turtlecontrol_msg
	
	turtlecontrol_msg = data


	
if __name__ == '__main__':

	# Initialize the node
	rospy.init_node('test_node', anonymous=True)
	
	
	# Add suscriber to receive position info from turtlesim_node
	pose_sub = rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
	
	# Subscriber for kp and xd components used in proportional controller
	turtlecontrol_sub = rospy.Subscriber('turtle1/control_params', Turtlecontrol, turtlecontrol_callback)
	
	
	# Add publisher with new topic using Shortpos message
	cmd_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	
	
	# Set frequency for this loop - 10 Hz
	loop_rate = rospy.Rate(10)
	
	# Declare variable of type Twist for sending control commands
	vel_cmd = Twist()
	
	# Declare variable of type Turtlecontrol for sending control commands
	#prop_cont = Turtlecontrol()
	
	
	
	while not rospy.is_shutdown():
	
		# Calculate vt = kp * (xd - xt)
		vel_cmd.linear.x = turtlecontrol_msg.kp * (turtlecontrol_msg.xd - pose_msg.x)
		
		# Publish the message
		cmd_pub.publish(vel_cmd)
		
		# Wait 0.1s until next loop and repeat
		loop_rate.sleep()

