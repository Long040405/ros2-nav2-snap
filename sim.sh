#!/usr/bin/bash
# Thiết lập các biến môi trường cần thiết
export TURTLEBOT3_MODEL=waffle
export QT_QPA_PLATFORM=xcb

# Thư mục chứa script này
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Sử dụng CycloneDDS với cấu hình unicast để giao tiếp đáng tin cậy với ctrlX CORE
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="${SCRIPT_DIR}/cyclonedds_unicast.xml"

# Source môi trường ROS 2 Humble trên máy host
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
else
    echo "LỖI: Không tìm thấy ROS 2 Humble tại /opt/ros/humble/setup.bash"
    exit 1
fi

# Kiểm tra CycloneDDS đã cài chưa
if ! ros2 pkg list 2>/dev/null | grep -q "rmw_cyclonedds_cpp"; then
    echo "----> Đang cài đặt CycloneDDS..."
    sudo apt install -y ros-humble-rmw-cyclonedds-cpp
fi

# 1. Chạy Gazebo giả lập trong nền (background)
echo "----> Đang khởi chạy mô phỏng Gazebo (TurtleBot3 World)..."
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py > /dev/null 2>&1 &
GAZEBO_PID=$!

# Đợi một chút để Gazebo khởi động
sleep 5

# 2. Chạy RViz2 với cấu hình 3D của Nav2 và Sim Time
echo "----> Đang khởi chạy RViz2 (chế độ 3D)..."
echo "Bấm Ctrl+C trong Terminal này để tắt cả Gazebo và RViz cùng lúc."

# Tự động dọn dẹp Gazebo khi tắt RViz
cleanup() {
    echo "----> Đang dọn dẹp các tiến trình giả lập..."
    kill $GAZEBO_PID 2>/dev/null || true
    pkill -f gzserver || true
    pkill -f gzclient || true
    pkill -f robot_state_publisher || true
}
trap cleanup EXIT SIGINT SIGTERM

# Dùng file cấu hình 3D riêng nếu tồn tại, ngược lại dùng mặc định của Nav2
RVIZ_CONFIG="${SCRIPT_DIR}/nav2_3d_view.rviz"
if [ ! -f "${RVIZ_CONFIG}" ]; then
    RVIZ_CONFIG="/opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz"
fi

rviz2 -d "${RVIZ_CONFIG}" --ros-args -p use_sim_time:=true

