# How to use

Run the script using:

python calculate_path_distance.py [Global Planner nav_msgs/Path topic] 0

Then set a goal point (using rviz) and the script will calculate the distance of the path.

For example for navfn the above command will be:

python calculate_path_distance.py /move_base/NavfnROS/plan 0

For automated start and goal points, run the script with the 1 flag (instead of 0).

# Start and goal point automation

To automate the start and goal points so that you can compare different global paths, you can edit the script in the lines start point X, start point Y, goal point X, goal point Y.

# Robot not following the path

You will notice that the robot does not follow the generated path. This is done on purpose, because the aim of this script is to calculate the distance of the path. If you need the robot to follow the path comment out the pub_stop.publish(GoalID()) line.
