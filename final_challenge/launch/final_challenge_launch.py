#Imports
from launch import LaunchDescription
from launch_ros.actions import Node

#Launch description function
def generate_launch_description():

    set_point_node = Node(name="set_point",
                          package='final_challenge',
                          executable='set_point',
                          emulate_tty=True,
                          output='screen',
                          #Parameters from yaml file
                          parameters=['config/params.yaml']
                          )
    
    rqt_plot_node =  Node(package='rqt_plot',
                          executable = 'rqt_plot',
                          arguments = ['/motor_output/data', '/motor_input/data', '/set_point/data']
                          )
    
    rqt_graph_node = Node(package='rqt_graph',
                          executable = 'rqt_graph',
                          output='screen')
    
    l_d = LaunchDescription([set_point_node, rqt_plot_node , rqt_graph_node]) 

    return l_d 
