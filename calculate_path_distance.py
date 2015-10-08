#!/usr/bin/env python

import math
import roslib, rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
import sys
import os
      
subscriber = None


def calculate_path_distance():
    global subscriber
    if not len(sys.argv) >= 4:
        print "Parameters: nav_msgs/Path topic | automate start and goal points (1/0) | follow path (1/0) | start point position x | start point position y | start point orientation z |  start point orientation w | goal point position x | goal point y | goal point orientation z | goal point orientation w"
        print "-------------------------------------------------------------------------------------"
        print "Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 1 0 1.0 -0.65 2.0 -1.307 100 37.42 0 0"
        print "-------------------------------------------------------------------------------------"
        print "If you run the script with automate start and goal points == 0, you can run it with only three parameters."
        print "---------------------------------------------------------------------"
        print "Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 0 0"
        print "---------------------------------------------------------------------"
    else:
        if str(sys.argv[2]) == '1':
            if not len(sys.argv) == 12:
                print "Parameters: nav_msgs/Path topic | automate start and goal points (1/0) | follow path (1/0) | start point position x | start point position y | start point orientation z |  start point orientation w | goal point position x | goal point y | goal point orientation z | goal point orientation w"
                print "-------------------------------------------------------------------------------------"
                print "Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 1 0 1.0 -0.65 2.0 -1.307 100 37.42 0 0"
                print "-------------------------------------------------------------------------------------"
                print "If you run the script with automate start and goal points == 0, you can run it with only three parameters."
                print "---------------------------------------------------------------------"
                print "Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 0 0"
                print "---------------------------------------------------------------------"
                sys.exit(0)
        topic = str(sys.argv[1])
        rospy.init_node('calculate_path_distance', anonymous=True)
        pub_goal = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
        pub_start = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
        subscriber = rospy.Subscriber(topic, Path, printPath)

        if str(sys.argv[2]) == '1':
            start_point = PoseWithCovarianceStamped()
            #start point position x
            start_point.pose.pose.position.x = float(sys.argv[4])
            #start point position y     
            start_point.pose.pose.position.y = float(sys.argv[5])
            start_point.header.stamp = rospy.Time.now()
            start_point.pose.pose.orientation.z = float(sys.argv[6])
            start_point.pose.pose.orientation.w = float(sys.argv[7])
            start_point.header.frame_id = 'map'
            rospy.sleep(1)
            pub_start.publish(start_point)
            print "Start Point:"
            print start_point
            print "--------------------"
            goal_point = PoseStamped()
            #goal point position x
            goal_point.pose.position.x = float(sys.argv[8])    
            #goal point Y        
            goal_point.pose.position.y = float(sys.argv[9])           
            goal_point.header.stamp = rospy.Time.now()
            goal_point.pose.orientation.z = float(sys.argv[10])
            goal_point.pose.orientation.w = float(sys.argv[11])
            goal_point.header.frame_id = 'map'
            rospy.sleep(2)
            pub_goal.publish(goal_point)
            print "Goal Point:"
            print goal_point
            print "--------------------"

        print "Listening to "+topic
        rospy.spin()

def printPath(path):
    global subscriber
    first_time = True
    prev_x = 0.0
    prev_y = 0.0
    total_distance = 0.0
    if len(path.poses) > 0:
	if str(sys.argv[3]) == '0':
	        pub_stop = rospy.Publisher('move_base/cancel', GoalID, queue_size=10)
        	rospy.sleep(1)
	        pub_stop.publish(GoalID())
        for current_point in path.poses:
            x = current_point.pose.position.x
            y = current_point.pose.position.y
            if not first_time:
                total_distance += math.hypot(prev_x - x, prev_y - y) 
            else:
                first_time = False
            prev_x = x
            prev_y = y
        subscriber.unregister()
        print "Total Distance = "+str(total_distance)+" meters"
        print "Press Ctrl+C to exit."


if __name__ == '__main__':
    calculate_path_distance()
