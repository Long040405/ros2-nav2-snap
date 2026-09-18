#!/usr/bin/bash
if [ -f "$SNAP/usr/bin/ros2_env.sh" ]; then
    source "$SNAP/usr/bin/ros2_env.sh"
elif [ -f "/opt/ros/humble/setup.bash" ]; then
    source "/opt/ros/humble/setup.bash"
fi
exec python3 $SNAP/usr/bin/web_server.py
