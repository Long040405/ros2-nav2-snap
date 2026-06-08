# ROS 2 & Nav2 Snap for ctrlX OS (AMR Navigation)

This repository provides an integrated packaging of **ROS 2 Humble** and **Nav2 Stack** as an Ubuntu Snap for deployment on **ctrlX CORE (ctrlX OS)** devices. It enables mapping (SLAM), localization (AMCL), autonomous navigation (Nav2), and incorporates a **Web UI Dashboard** to control and monitor the robot remotely.

---

## Features

- **Snap Packaging**: Completely sandboxed, cross-compiled, and ready to deploy on ctrlX CORE.
- **DDS Networking**: Pre-configured CycloneDDS setup for seamless communication between simulated environments and the physical controller.
- **Web UI Dashboard**: A web-based interface for managing SLAM, loading maps, setting initial poses, and assigning navigation goals.
- **Simulation Friendly**: Fully compatible with Gazebo and RViz2 simulations running on an external Ubuntu host.

---

## Step 1: Network Configuration

Before compiling the snap, you must configure CycloneDDS to match your local network interfaces and IP addresses.

### 1. Check IP Addresses
- **ctrlX CORE IP**: Default is usually `192.168.1.1`.
- **Laptop IP**: Open a terminal on your laptop and check your active IP (e.g., WiFi interface `wlo1` or Ethernet `enp44s0`):
  ```bash
  ip addr
  ```
  *Example Laptop IP: `192.168.2.67` (connected to WiFi `wlo1` on a `/22` subnet).*

### 2. Configure DDS Files in the Repository
Modify the DDS configuration files in this repository before building the snap:

- **`cyclonedds_snap.xml` (ctrlX CORE DDS Config)**:
  Open this file and update the `Peers` section with your **Laptop IP** and **ctrlX CORE IP**:
  ```xml
  <Peers>
    <Peer Address="YOUR_LAPTOP_IP"/>     <!-- Replace with your Laptop IP (e.g. 192.168.2.67) -->
    <Peer Address="192.168.1.1"/>        <!-- ctrlX CORE IP -->
  </Peers>
  ```

- **`cyclonedds_unicast.xml` (Laptop DDS Config)**:
  Open this file, set the correct network interface name (`wlo1` for WiFi, `enp44s0` for Ethernet), and update the peers:
  ```xml
  <General>
    <Interfaces>
      <NetworkInterface name="YOUR_LAPTOP_INTERFACE" multicast="false"/> <!-- e.g., wlo1 -->
    </Interfaces>
  </General>
  <Discovery>
    <Peers>
      <Peer Address="192.168.1.1"/>      <!-- ctrlX CORE IP -->
      <Peer Address="YOUR_LAPTOP_IP"/>   <!-- Laptop IP -->
    </Peers>
  </Discovery>
  ```

### 3. Configure Subnetwork Routing
Since ctrlX CORE uses a `/24` subnet (`192.168.1.1/24`) by default, it will fail to send UDP packets to a laptop in a different subnet (e.g., `192.168.2.x`) without a route.
Choose one of the two solutions below:
- **Solution A (Permanent - Recommended)**: Log in to the ctrlX OS Web UI -> Go to **Settings** -> **Network** -> **Interfaces** -> Select **XF10** -> Change the IPv4 Subnet Mask from `/24` (`255.255.255.0`) to **`/22`** (`255.255.252.0`).
- **Solution B (Temporary)**: Run this command in your laptop terminal to add a temporary route on ctrlX CORE:
  ```bash
  ssh -t rexroot@192.168.1.1 "sudo ip route add YOUR_LAPTOP_IP dev XF10"
  ```

---

## Step 2: Build the Snap (on Ubuntu Host)

Build the snap package using `snapcraft` inside the repository workspace on your laptop:
```bash
snapcraft clean
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
export DESTDIR=/tmp/dummy
snapcraft pack --destructive-mode --target-arch=amd64
```
This generates the installation package, e.g., `ros2-nav2_1.1.20_amd64.snap`.

---

## Step 3: Deploy and Connect (on ctrlX CORE)

### 1. Copy the Snap to the controller
```bash
scp ros2-nav2_1.1.20_amd64.snap rexroot@192.168.1.1:/home/rexroot/
```

### 2. Install the Snap (Run inside ctrlX CORE shell)
SSH into the ctrlX CORE and install the snap:
```bash
ssh -t rexroot@192.168.1.1 "sudo snap install --dangerous /home/rexroot/ros2-nav2_1.1.20_amd64.snap"
```

### 3. Grant Network & System Web UI Connections
Because local/dangerous snaps do not auto-connect slots, you must run the connection commands manually:
```bash
# Connect basic system plugs
ssh -t rexroot@192.168.1.1 "sudo snap connect ros2-nav2:network; sudo snap connect ros2-nav2:network-bind"

# Connect Web UI Sidebar integration
ssh -t rexroot@192.168.1.1 "sudo snap connect rexroth-deviceadmin:package-assets ros2-nav2:package-assets"
ssh -t rexroot@192.168.1.1 "sudo snap connect rexroth-deviceadmin:package-run ros2-nav2:package-run"

# Restart the web server daemon to apply connections
ssh -t rexroot@192.168.1.1 "sudo snap restart ros2-nav2.web-server"
```

---

## Step 4: Initialize Config Parameters (on ctrlX CORE)

The snap applications (SLAM, Localization, Navigation) will fail to start if their configuration files are not set.

SSH into the ctrlX CORE and run:
```bash
# 1. Reset configuration templates to the local directory
ssh -t rexroot@192.168.1.1 "sudo ros2-nav2.reset-config-templates"

# 2. Configure parameters for all services
ssh -t rexroot@192.168.1.1 "sudo snap set ros2-nav2 simulation=\"True\""
ssh -t rexroot@192.168.1.1 "sudo snap set ros2-nav2 slam-config=\"/var/snap/ros2-nav2/common/configuration_templates/slam_params_template.yaml\""
ssh -t rexroot@192.168.1.1 "sudo snap set ros2-nav2 localization-config=\"/var/snap/ros2-nav2/common/configuration_templates/localization_params_template.yaml\""
ssh -t rexroot@192.168.1.1 "sudo snap set ros2-nav2 navigation-config=\"/var/snap/ros2-nav2/common/configuration_templates/nav2_params_template.yaml\""
```

---

## Step 5: Run Simulation & Teleoperation (on Laptop Host)

### 1. Run Simulation Environment (Gazebo & RViz2)
Ensure your laptop has ROS 2 Humble and TurtleBot3 packages installed:
```bash
sudo apt update
sudo apt install -y ros-humble-desktop ros-humble-turtlebot3-gazebo ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-teleop-twist-keyboard
```
Launch the simulation script:
```bash
./sim.sh
```

### 2. Run Keyboard Teleoperation
Open a **new terminal window** on your laptop, navigate to the repository directory, and run:
```bash
# Source the ROS 2 environment
source /opt/ros/humble/setup.bash

# Set model and DDS settings to match the simulation
export TURTLEBOT3_MODEL=waffle
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="./cyclonedds_unicast.xml"

# Run the teleoperation node
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Use the `u`, `i`, `o`, `j`, `k`, `l`, `m`, `,`, `.` keys on your keyboard to navigate the robot and scan the environment.

---

## Step 6: Access the Web UI Dashboard

Open your browser and navigate to the ctrlX CORE web dashboard:
**`http://192.168.1.1/ros2-nav2/`** (Or click **ROS 2 Navigation** in the sidebar of the ctrlX CORE Web UI).

From here, you can:
- **Build Maps**: Turn on **SLAM**, drive the robot with `teleop_twist_keyboard` in the terminal, and save your map.
- **Navigate**: Turn on **Navigation**, set the **Initial Pose** using the interactive map, and send **Nav2 Goals** or save **Waypoints**.
