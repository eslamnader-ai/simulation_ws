import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    desc_share = get_package_share_directory('auv_description')
    sf_share = get_package_share_directory('stonefish_ros2')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(sf_share, 'launch', 'stonefish_simulator.launch.py')),
            launch_arguments={
                'simulation_data': os.path.join(desc_share, 'data'),
                'scenario_desc': os.path.join(desc_share, 'auv_scenario', 'auv_scenario.xml'),
                'simulation_rate': '300.0',
                'window_res_x': '1200',
                'window_res_y': '800',
                'rendering_quality': 'medium',
            }.items()
        )
    ])

    