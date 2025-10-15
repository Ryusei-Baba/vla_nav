# vla_nav

Google Gemini を使用した Vision-Language-Action (VLA) ナビゲーションパッケージ

## インストール

```bash
# Python依存パッケージのインストール
pip3 install google-generativeai pillow opencv-python

# パッケージのビルド
cd ~/orne_ws
colcon build --symlink-install --packages-select vla_nav
source install/setup.bash
```

## 設定

`config/config.yaml` を編集してパラメータを設定します：

```yaml
vla_nav_node:
  ros__parameters:
    camera_topic: /image_raw          # カメラ画像トピック
    cmd_vel_topic: /cmd_vel            # 速度指令トピック
    api_key: YOUR_API_KEY_HERE         # Google Gemini APIキー
    model_name: gemini-2.5-flash-lite  # 使用するGeminiモデル名
    inference_interval: 4.0            # 推論間隔（秒）
    linear_vel: 0.6                    # 並進速度 (m/s)
    angular_vel: 1.0                   # 角速度 (rad/s)
```

**重要**: `YOUR_API_KEY_HERE` を実際のGoogle Gemini APIキーに置き換えてください。

## 使用方法

VLAナビゲーションノードを起動：

```bash
ros2 launch vla_nav vla_nav.launch.py
```

または、ノードを直接実行：

```bash
ros2 run vla_nav vla_nav_node
```
