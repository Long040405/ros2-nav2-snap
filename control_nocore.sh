#!/usr/bin/bash
# ==============================================================================
# Điều khiển robot bằng bàn phím (Teleop) ở chế độ cục bộ (không cần ctrlX CORE)
# ==============================================================================

export TURTLEBOT3_MODEL=waffle
export ROS_DOMAIN_ID=0

# Xóa cấu hình CycloneDDS unicast
unset CYCLONEDDS_URI
unset RMW_IMPLEMENTATION

# Source môi trường ROS 2 Humble trên máy host
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
else
    echo "LỖI: Không tìm thấy ROS 2 Humble tại /opt/ros/humble/setup.bash"
    exit 1
fi

echo "========================================================="
echo "   Bắt đầu điều khiển robot bằng bàn phím (Teleop Local) "
echo "   Lưu ý: Nhấp chuột chọn Terminal này để điều khiển!    "
echo "========================================================="
ros2 run turtlebot3_teleop teleop_keyboard
