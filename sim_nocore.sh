#!/usr/bin/bash
# ==============================================================================
# Script khởi chạy mô phỏng Gazebo và RViz2 hoàn toàn cục bộ trên Laptop
# Không cần kết nối mạng dây, không cần ctrlX CORE
# ==============================================================================

# Thiết lập các biến môi trường cần thiết
export TURTLEBOT3_MODEL=waffle
export QT_QPA_PLATFORM=xcb
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models
export ROS_DOMAIN_ID=0

# Xóa cấu hình CycloneDDS unicast trỏ tới ctrlX CORE
# ROS 2 sẽ tự động dùng DDS mặc định (SHM / Localhost) để các node tự kết nối
unset CYCLONEDDS_URI
unset RMW_IMPLEMENTATION

# Thư mục chứa script này
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Source môi trường ROS 2 Humble trên máy host
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
else
    echo "LỖI: Không tìm thấy ROS 2 Humble tại /opt/ros/humble/setup.bash"
    exit 1
fi

echo "========================================================="
echo "   Khởi chạy Giả lập Cục bộ (Chế độ Không cần ctrlX CORE)"
echo "   DDS: Mặc định (Localhost / SHM / Tự do giao tiếp)"
echo "   Domain ID: ${ROS_DOMAIN_ID}"
echo "========================================================="

# 1. Chạy Gazebo giả lập trong nền (background)
echo "----> Đang khởi chạy mô phỏng Gazebo (TurtleBot3 World)..."
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py > /tmp/gazebo_sim.log 2>&1 &
GAZEBO_PID=$!

# Đợi một chút để Gazebo và robot spawn hoàn tất
echo "----> Đang đợi Gazebo và Robot xuất hiện (5s)..."
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
