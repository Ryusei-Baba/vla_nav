# ノードの起動 launchファイル
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # パッケージのshareディレクトリからconfigファイルのパスを取得
    config_file = os.path.join(
        get_package_share_directory('vla_nav'),
        'config',
        'config.yaml'
    )

    return LaunchDescription([
        Node(
            package='vla_nav',
            executable='vla_nav_node',
            name='vla_nav_node',
            output='screen',
            parameters=[config_file]
        )
    ]) 

