# How to use

Parameters: nav_msgs/Path topic | automate start and goal points (1/0) | start point x | start point y | goal point x | goal point y

Example: python calculate_path_distance.py /move_base/NavfnROS/plan 1 1.0 0 100 37.42

If you run the script with automate start and goal points == 0, you can run it with only two parameters.

Example: python calculate_path_distance.py /move_base/NavfnROS/plan 0

# Robot not following the path

You will notice that the robot does not follow the generated path. This is done on purpose, because the aim of this script is to calculate the distance of the path. If you need the robot to follow the path comment out the pub_stop.publish(GoalID()) line.
