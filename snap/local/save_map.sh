#!/usr/bin/bash


MAP_DIR="${SNAP_COMMON}/maps"
MAP_IMG_EXT="png"
MAP_NAME=${1:-new_map}
MAP_FILE_NO_EXT="${MAP_DIR}/${MAP_NAME}"
MAP_TOPIC="map"
MAP_FREE_THRESH="0.15"
MAP_OCC_THRESH="0.65"
MAP_MODE="trinary"

source $SNAP/usr/bin/url_management.sh
MAP_SAVER_CONFIG_FILE="$(snapctl get map-saver-config)"

# it the config-path is a URL we save it to a default local location
# otherwise, it it's a local path we use that.
if is_url "${MAP_SAVER_CONFIG_FILE}" ; then
    STORAGE_PATH_TO_CONFIG="$SNAP_COMMON/config/map_saver.yaml"
    if get_url "${MAP_SAVER_CONFIG_FILE}" "${STORAGE_PATH_TO_CONFIG}"; then
        CONFIG_FILE=${STORAGE_PATH_TO_CONFIG}
    fi
else
    echo "Config is not a URL, setting local path"
    CONFIG_FILE=${MAP_SAVER_CONFIG_FILE}
fi

# if we have a config file we overwrite the thresholds accordingly
if [ -n "${CONFIG_FILE}" ]; then
    MAP_SAVER_YAML_CONTENT=$(<$(readlink -f "${CONFIG_FILE}"))
    MAP_FREE_THRESH=$(echo "$MAP_SAVER_YAML_CONTENT" | grep -oP 'free_thresh_default:\s*\K[0-9.]+')
    MAP_OCC_THRESH=$(echo "$MAP_SAVER_YAML_CONTENT" | grep -oP 'occupied_thresh_default:\s*\K[0-9.]+')
fi

# Create map directory if it doesn't exist
mkdir -p ${MAP_DIR}

ros2 service call /map_saver/save_map nav2_msgs/srv/SaveMap \
  "{map_topic: ${MAP_TOPIC}, map_url: ${MAP_FILE_NO_EXT}, \
  image_format: ${MAP_IMG_EXT}, map_mode: ${MAP_MODE}, \
  free_thresh: ${MAP_FREE_THRESH}, occupied_thresh: ${MAP_OCC_THRESH}}"
