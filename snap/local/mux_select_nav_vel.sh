#!/usr/bin/bash

# Check if /mux/select service is active before calling it to avoid blocking
if ros2 service list 2>/dev/null | grep -q "/mux/select"; then
    echo "Mux select service found. Selecting /cmd_vel_nav..."
    ros2 service call /mux/select topic_tools_interfaces/srv/MuxSelect "{topic: /cmd_vel_nav}"
else
    echo "Mux select service not found, skipping selection..."
fi

exec $@
