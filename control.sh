#!/usr/bin/bash
# Thiết lập các biến môi trường cần thiết
export TURTLEBOT3_MODEL=waffle
# Sử dụng CycloneDDS với cấu hình unicast để giao tiếp đáng tin cậy với các node khác
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="$(dirname "$(readlink -f "$0")")/cyclonedds_unicast.xml"

# Source môi trường ROS 2 Humble trên máy host
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
else
    echo "LỖI: Không tìm thấy ROS 2 Humble tại /opt/ros/humble/setup.bash"
    exit 1
fi

echo "========================================================="
echo "   Bắt đầu điều khiển robot bằng bàn phím (Teleop)       "
echo "   Lưu ý: Nhấp chuột chọn Terminal này để điều khiển!    "
echo "========================================================="
ros2 run turtlebot3_teleop teleop_keyboard
