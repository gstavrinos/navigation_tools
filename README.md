# How to use

Parameters: nav_msgs/Path topic | automate start and goal points (1/0) | follow path (1/0) | start point position x | start point position y | start point orientation z |  start point orientation w | goal point position x | goal point y | goal point orientation z | goal point orientation w

Example: Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 1 0 1.0 -0.65 2.0 -1.307 100 37.42 0 0

If you run the script with automate start and goal points == 0, you can run it with only three parameters.

Example: python calculate_path_distance.py /move_base/GlobalPlanner/plan 0 0

# Find the start and goal point values easily

To get the start point values, run on a new terminal:

rostopic echo /initialpose

Using rviz set your robot's start point. All the needed values will be then printed on the previous terminal.

To get the goal point values, run on a new terminal:

rostopic echo move_base_simple/goal

Using rviz set your robot's goal point. All the needed values will be then printed on the previous terminal.