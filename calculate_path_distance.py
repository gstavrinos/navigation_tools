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
    if not len(sys.argv) == 3:
        print "Please specify the nav_msgs/Path topic you want to subscribe to and if you want to automate start and goal points (1/0)"
    else:
        topic = str(sys.argv[1])
        rospy.init_node('calculate_path_distance', anonymous=True)
        pub_goal = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
        pub_start = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
        subscriber = rospy.Subscriber(topic, Path, printPath)

        if str(sys.argv[2]) == '1':
            start_point = PoseWithCovarianceStamped()
            #start point X
            start_point.pose.pose.position.x = 621.998 
            #start point Y     
            start_point.pose.pose.position.y = 309.295      
            start_point.header.stamp = rospy.Time.now()
            start_point.pose.pose.orientation.w = 1.0
            start_point.header.frame_id = 'map'
            rospy.sleep(1)
            pub_start.publish(start_point)
            print "Start Point:"
            print start_point
            print "--------------------"
            goal_point = PoseStamped()
            #goal point X
            goal_point.pose.position.x = 684.025    
            #goal point Y        
            goal_point.pose.position.y = 509.816           
            goal_point.header.stamp = rospy.Time.now()
            goal_point.pose.orientation.w = 1.0
            goal_point.header.frame_id = 'map'
            rospy.sleep(2)
            pub_goal.publish(goal_point)
            print "Goal Point:"
            print goal_point
            print "--------------------"
        
        #os.system("rostopic pub /initialpose geometry_msgs/PoseWithCovarianceStamped \'{header: {stanow, frame_id: \"map\"}, pose: {pose: {position: {x: 619.998, y: 309.295, z: 0.0}, orientation: {w: 1.0}}}}\'")
        #os.system("rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \'{header: {stamp: now, frame_id: \"map\"}, pose: {position: {x: 684.025, y: 509.816, z: 0.0}, orientation: {w: 1.0}}}\'")
        #os.system("rostopic pub /move_base/cancel actionlib_msgs/GoalID -- {}")

        print "Listening to "+topic
        rospy.spin()

def printPath(path):
    global subscriber
    first_time = True
    prev_x = 0.0
    prev_y = 0.0
    total_distance = 0.0
    if len(path.poses) > 0:
        pub_stop = rospy.Publisher('move_base/cancel', GoalID, queue_size=10)
        rospy.sleep(1)
        pub_stop.publish(GoalID())
        for current_point in path.poses:
            x = current_point.pose.position.x
            y = current_point.pose.position.y
            if not first_time:
                total_distance += math.hypot(prev_x - x, prev_y - y)           
                #total_distance += math.sqrt( (prev_x - x)**2 + (prev_y - y)**2 )
            else:
                first_time = False
            prev_x = x
            prev_y = y
        subscriber.unregister()
        print "Total Distance = "+str(total_distance)+" meters"
        print "Press Ctrl+C to exit."


if __name__ == '__main__':
    calculate_path_distance()
