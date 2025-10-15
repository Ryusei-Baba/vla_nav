#!/usr/bin/env python3
# Gemini を使用した Vision-Language-Action Models (VLA) ナビゲーション ROS 2 ノード
import os
import google.generativeai as genai
from PIL import Image
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image as RosImage
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge


class VlaNavNode(Node):
    def __init__(self):
        super().__init__('vla_nav_node')

        # パラメータの宣言と取得
        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('api_key', 'YOUR_API_KEY')
        self.declare_parameter('model_name', 'gemini-2.5-flash-lite')
        self.declare_parameter('inference_interval', 4.0)  # 推論間隔（秒）
        self.declare_parameter('prompt', 'Navigate the robot safely.')
        self.declare_parameter('linear_vel', 0.2)
        self.declare_parameter('angular_vel', 1.0)

        self.camera_topic = self.get_parameter('camera_topic').get_parameter_value().string_value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value
        api_key = self.get_parameter('api_key').get_parameter_value().string_value
        model_name = self.get_parameter('model_name').get_parameter_value().string_value
        self.inference_interval = self.get_parameter('inference_interval').get_parameter_value().double_value
        self.prompt = self.get_parameter('prompt').get_parameter_value().string_value
        self.linear_vel = self.get_parameter('linear_vel').get_parameter_value().double_value
        self.angular_vel = self.get_parameter('angular_vel').get_parameter_value().double_value

        # Gemini API設定
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        # CvBridgeの初期化
        self.bridge = CvBridge()

        # 最新画像を保存
        self.latest_image = None
        self.last_inference_time = 0.0

        # カメラ画像のサブスクライバ
        self.subscription = self.create_subscription(
            RosImage, 
            self.camera_topic, 
            self.image_callback, 
            10
        )

        # コマンド速度のパブリッシャ
        self.publisher_ = self.create_publisher(Twist, self.cmd_vel_topic, 10)

        # タイマーで定期的に推論実行
        self.timer = self.create_timer(self.inference_interval, self.inference_callback)

        self.get_logger().info('VLA Navigation Node has been started.')

    def image_callback(self, msg):
        """画像を受信して保存"""
        try:
            # ROS画像をOpenCV形式に変換
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
            self.latest_image = cv_image
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {str(e)}')

    def inference_callback(self):
        """定期的に推論を実行"""
        if self.latest_image is None:
            self.get_logger().warn('No image received yet.')
            return

        try:
            # OpenCV画像をPIL画像に変換
            pil_image = Image.fromarray(self.latest_image)

            # プロンプト作成
            prompt = self.prompt

            # Gemini APIで推論
            response = self.model.generate_content([prompt, pil_image])
            command = response.text.strip().lower()

            self.get_logger().info(f'Received command: {command}')

            # コマンドを解析してTwistメッセージを作成
            twist = Twist()
            
            if 'forward' in command:
                twist.linear.x = self.linear_vel
                twist.angular.z = 0.0
            elif 'left' in command:
                twist.linear.x = 0.0
                twist.angular.z = self.angular_vel
            elif 'right' in command:
                twist.linear.x = 0.0
                twist.angular.z = -self.angular_vel
            elif 'stop' in command:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            else:
                self.get_logger().warn(f'Unknown command: {command}, stopping.')
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            # コマンド速度をパブリッシュ
            self.publisher_.publish(twist)

        except Exception as e:
            self.get_logger().error(f'Inference failed: {str(e)}')
            # エラー時は停止
            twist = Twist()
            self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    vla_nav_node = VlaNavNode()
    
    try:
        rclpy.spin(vla_nav_node)
    except KeyboardInterrupt:
        pass
    finally:
        vla_nav_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()