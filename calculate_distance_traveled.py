#!/usr/bin/env python

import math
import roslib, rospy
#from geometry_msgs.msg import PoseWithCovarianceStamped
#from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionGoal
from move_base_msgs.msg import MoveBaseActionFeedback
#from actionlib_msgs.msg import GoalID
#import sys
#import os
      
pose_subscriber = None
goal_subscriber = None
total_distance = 0
prev_x = 0.0
prev_y = 0.0
goal_point = []
first_time = True

def calculate_distance_traveled():
    global pose_subscriber
    
    pose_topic = "/move_base/feedback"
    goal_topic = "/move_base/goal"
    rospy.init_node('calculate_distance_traveled', anonymous=True)
    pose_subscriber = rospy.Subscriber(pose_topic, MoveBaseActionFeedback, addPointToTotalDistance)
    goal_subscriber = rospy.Subscriber(goal_topic, MoveBaseActionGoal, getGoalPoint)

    print "Listening to "+pose_topic
    rospy.spin()

def getGoalPoint(g):
    global goal_point, goal_subscriber
    goal_point = g

def distancePoints(x1,y1,x2,y2):
    return math.hypot(x2 - x1, y2 - y1)

def addPointToTotalDistance(current_point):
    global pose_subscriber, total_distance, prev_x, prev_y, goal_point, first_time
    
    if first_time:
        first_time = False
        prev_x = current_point.feedback.base_position.pose.position.x
        prev_y = current_point.feedback.base_position.pose.position.y
    else:
        x = current_point.feedback.base_position.pose.position.x
        y = current_point.feedback.base_position.pose.position.y

        total_distance += distancePoints(x, y, prev_x, prev_y)

        prev_x = x
        prev_y = y
        print "Current distance traveled= " + str(total_distance) + " meters"
        if goal_point != []:
            if distancePoints(x, y, goal_point.goal.target_pose.pose.position.x, goal_point.goal.target_pose.pose.position.y) <= 0.1:
                pose_subscriber.unregister()
                print "Total Distance = " + str(total_distance) + " meters"
                print "Press Ctrl+C to exit."


if __name__ == '__main__':
    calculate_distance_traveled()
