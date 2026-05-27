# ROS 2 & Nav2 Snap for ctrlX OS (AMR Navigation)

This repository provides an integrated packaging of **ROS 2 Humble** and **Nav2 Stack** as an Ubuntu Snap for deployment on **ctrlX CORE (ctrlX OS)** devices. It enables mapping (SLAM), localization (AMCL), autonomous navigation (Nav2), and incorporates a **Web UI Dashboard** to control and monitor the robot remotely.

---

## Features

- **Snap Packaging**: Completely sandboxed, cross-compiled, and ready to deploy on ctrlX CORE.
- **DDS Networking**: Pre-configured CycloneDDS setup for seamless communication between simulated environments and the physical controller.
- **Web UI Dashboard**: A web-based interface for managing SLAM, loading maps, setting initial poses, and assigning navigation goals.
- **Simulation Friendly**: Fully compatible with Gazebo and RViz2 simulations running on an external Ubuntu host.

---

## Quick Start Guide

### 1. Clone the Repository
Clone this repository to your local development machine:
```bash
git clone https://github.com/Long040405/ros2-nav2-snap.git
cd ros2-nav2-snap
```

### 2. Build the Snap (on Ubuntu Host)
Build the snap package using `snapcraft` inside the repository workspace:
```bash
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
snapcraft pack --destructive-mode --target-arch=amd64
```
This generates the installation package, e.g., `ros2-nav2_1.1.20_amd64.snap`.

### 3. Deploy to ctrlX CORE
Copy and install the built snap on your ctrlX CORE target:
```bash
# Copy to the controller
scp ros2-nav2_1.1.20_amd64.snap rexroot@192.168.1.1:/home/rexroot/

# Install the snap
ssh -t rexroot@192.168.1.1 "sudo snap install --dangerous /home/rexroot/ros2-nav2_1.1.20_amd64.snap"

# Grant network and DDS permissions
ssh -t rexroot@192.168.1.1 "sudo snap connect ros2-nav2:network; sudo snap connect ros2-nav2:network-bind"
```

### 4. Run Simulation (on Laptop Host)
Ensure your laptop has ROS 2 Humble and TurtleBot3 packages installed:
```bash
sudo apt update
sudo apt install -y ros-humble-desktop ros-humble-turtlebot3-gazebo ros-humble-navigation2 ros-humble-nav2-bringup
```
Run the simulation script which configures CycloneDDS and launches the Gazebo virtual environment:
```bash
./sim.sh
```

### 5. Access the Web UI
Open your browser and navigate to the ctrlX CORE web dashboard:
👉 **`http://192.168.1.1/ros2-nav2/`**

From here, you can:
- **Build Maps**: Turn on **SLAM**, drive the robot with `teleop_keyboard`, and save your map.
- **Navigate**: Turn on **Navigation**, set the **Initial Pose** using the interactive map, and send **Nav2 Goals** or save **Waypoints**.

---

## Detailed Service Configuration
By default, the snap services are managed using snap parameters:
- `simulation`: Set to `True` when running with a simulated robot (e.g. `sudo snap set ros2-nav2 simulation="True"`).
- `slam-config`: Path or URL to mapping parameters.
- `localization-config`: Path or URL to AMCL parameters.
- `navigation-config`: Path or URL to Nav2 routing parameters.

For full configuration templates and instructions, refer to the [ctrlX CORE Tutorial Guide](ctrlx_ros2_nav2_tutorial.md).
