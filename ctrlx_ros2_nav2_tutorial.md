# Canva Slide Design & PDF Export Guide: Deploying ROS 2 & Nav2 on ctrlX CORE Using Snap

This document is organized page-by-page (slide-by-slide) in English so you can easily copy-paste the content into **Canva**, design clean visual slides, and export them as a professional PDF guide.

---

## 🖥️ SLIDE 1: Title & Cover Slide
* **Canva Layout Suggestion**: 
  * Modern, industrial tech design using the ctrlX OS theme colors (Dark Grey background with Rexroth Red or Bright Orange accents).
  * Prominent, bold title aligned to the left or center. Use clean sans-serif typography (e.g., Montserrat, Inter).
* **Display Text**:
  * **Main Title**: DEPLOYING ROS 2 & NAV2 ON CTRLX CORE USING SNAP
  * **Subtitle**: A Step-by-Step Guide to Package, Install, and Run Autonomous Navigation (AMR) on ctrlX OS
  * **Footer**: Technical Tutorial & Practical Reference Guide
* **Image Description**:
  * 📸 `[IMAGE 1.1]`: Grid or collage of logos: Bosch Rexroth, ctrlX World, ROS 2, and Nav2. Feature a high-quality product photo of a physical ctrlX CORE controller next to a mobile robot (e.g., TurtleBot3).
* **Design Tips**: Ensure at least 40% of the slide is negative space (uncluttered) to give the main robot graphic visual weight.

---

## 🖥️ SLIDE 2: System Architecture & Data Flow
* **Canva Layout Suggestion**: 
  * Two-column layout: Text explanation on the left, visual flow diagram/schematic on the right.
* **Display Text**:
  * **System Overview**: Real-time communication between the Simulation Laptop (Gazebo/RViz) and the ctrlX CORE hardware target via CycloneDDS Unicast routing.
  * **Architecture Components**:
    * **Laptop (Host Simulator)**: Runs Gazebo virtual world physics and RViz2 graphical visualization.
    * **ctrlX CORE (Target)**: Runs the snapped application containing the background services: SLAM Toolbox, Nav2 Stack, AMCL, and the Web Dashboard server.
    * **User Web Browser**: Controls and monitors the robot remotely via the HTTP-based Web UI.
* **Image Description**:
  * 📸 `[IMAGE 2.1]`: Draw a block diagram showing:
    ```
    [Laptop: Gazebo / RViz2] <--- CycloneDDS (Unicast) ---> [ctrlX CORE: SLAM, Nav2, AMCL, Web Server]
                                                                        ^
                                                                        | HTTP API
                                                                        v
                                                             [Browser: Web UI Dashboard]
    ```
* **Design Tips**: Color-code the boxes (e.g., Blue for Laptop, Red/Grey for ctrlX CORE, and Orange for Web Browser) to make the data flow easy to follow.

---

## 🖥️ SLIDE 3: Prerequisites
* **Canva Layout Suggestion**: 
  * Side-by-side infographic cards representing the two main devices (Laptop and ctrlX CORE).
* **Display Text**:
  * **1. Laptop (Host Machine)**:
    * Operating System: **Ubuntu 22.04 LTS (Jammy Jellyfish)**.
    * ROS 2 Humble Desktop and TurtleBot3 simulation packages installed:
      ```bash
      sudo apt install -y ros-humble-desktop ros-humble-turtlebot3-gazebo ros-humble-navigation2 ros-humble-nav2-bringup
      ```
  * **2. ctrlX CORE / ctrlX OS (Target Device)**:
    * Connected to the same Local Area Network (LAN) as the laptop (Default IP: `192.168.1.1`).
    * SSH terminal access enabled (Default user: `rexroot`).
* **Image Description**:
  * 📸 `[IMAGE 3.1]`: Icons of Ubuntu 22.04, ROS 2 Humble, and ctrlX OS. Graphic illustration showing an Ethernet cable bridging the laptop to the ctrlX CORE controller.
* **Design Tips**: Use a dark-colored background panel with monospace fonts for code lines to simulate terminal commands.

---

## 🖥️ SLIDE 4: Step 1 - Clone Repository
* **Canva Layout Suggestion**: 
  * Simple, clear step-by-step column layout. Highlight the Git clone URL using a distinct contrasting color.
* **Display Text**:
  * **Objective**: Clone the official project repository onto your simulation laptop to retrieve build configs, simulation scripts, and custom snap parameters.
  * **Execution (on Laptop Terminal)**:
    1. Clone the repository to your local directory:
       ```bash
       git clone https://github.com/YOUR_USERNAME/ros2-nav2-snap.git
       ```
    2. Navigate into the cloned folder:
       ```bash
       cd ros2-nav2-snap
       ```
* **Image Description**:
  * 📸 `[IMAGE 4.1]`: Screenshot of a Linux terminal showing the successful completion of the `git clone` command and list of workspace directories.
* **Design Tips**: Highlight the text `YOUR_USERNAME` with an alert/accent color (like yellow or orange) to prompt the user to replace it with their username.

---

## 🖥️ SLIDE 5: Step 2 - Pack the Application (Snap Build)
* **Canva Layout Suggestion**: 
  * Linear process flow or vertical timeline layout. Keep text to a minimum, focusing on the code block and built package output.
* **Display Text**:
  * **Objective**: Build and compile the ROS 2 workspace into a deployable `.snap` bundle package.
  * **Execution (on Laptop Terminal)**:
    1. Make sure you are in the workspace folder:
       ```bash
       cd ~/Desktop/ros2-nav2-snap
       ```
    2. Enable experimental extension features for ROS 2 Humble and pack:
       ```bash
       export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
       snapcraft pack --destructive-mode --target-arch=amd64
       ```
    3. Output Artifact: `ros2-nav2_1.1.20_amd64.snap`
* **Image Description**:
  * 📸 `[IMAGE 5.1]`: Screenshot of the terminal output displaying the final stages of the `snapcraft pack` build ending with "Snapped ros2-nav2_1.1.20_amd64.snap".
* **Design Tips**: Place a prominent "SUCCESS" green badge next to the output filename.

---

## 🖥️ SLIDE 6: Step 3 - Transfer & Install on ctrlX CORE
* **Canva Layout Suggestion**: 
  * Vertical 3-step sequence diagram (1. Copy -> 2. Install -> 3. Connect Network Slots).
* **Display Text**:
  * **Deployment Steps**:
    1. **Copy Snap file to CORE**:
       ```bash
       scp ros2-nav2_1.1.20_amd64.snap rexroot@192.168.1.1:/home/rexroot/
       ```
    2. **Install Snap on target** (Use `--dangerous` flag for locally-built unsigned packages):
       ```bash
       ssh -t rexroot@192.168.1.1 "sudo snap install --dangerous /home/rexroot/ros2-nav2_1.1.20_amd64.snap"
       ```
    3. **Authorize network ports & DDS**:
       ```bash
       ssh -t rexroot@192.168.1.1 "sudo snap connect ros2-nav2:network; sudo snap connect ros2-nav2:network-bind"
       ```
* **Image Description**:
  * 📸 `[IMAGE 6.1]`: Split terminal screenshot: Upper half showing the file transfer percentage (`scp`), lower half showing SSH command installing the snap on ctrlX OS.
* **Design Tips**: Label SSH commands clearly with a "Run on Target CORE" tag to avoid confusion with Laptop terminal commands.

---

## 🖥️ SLIDE 7: Step 4 - Run Simulation on Laptop
* **Canva Layout Suggestion**: 
  * Large, eye-catching screenshot of the running simulation environment with detailed step indicators on the side panel.
* **Display Text**:
  * **Objective**: Start the virtual environment on your laptop to stream sensor frames (LaserScan, Odometry) to the controller.
  * **Execution (on Laptop)**:
    ```bash
    cd ~/Desktop/ros2-nav2-snap
    ./sim.sh
    ```
  * **Automated script tasks**:
    * Exports robot model: `export TURTLEBOT3_MODEL=waffle`
    * Sets up CycloneDDS routing to ctrlX CORE via `cyclonedds_unicast.xml`.
    * Launches Gazebo 3D simulator world and RViz2 workspace.
* **Image Description**:
  * 📸 `[IMAGE 7.1]`: Desktop screen capture showing the Gazebo environment (TurtleBot3 robot in a maze of walls) alongside the RViz2 visualization tool.
* **Design Tips**: Put a stylish mockup frame of a physical laptop or monitor around the simulation screenshot.

---

## 🖥️ SLIDE 8: Step 5 - Web Dashboard: SLAM & Mapping
* **Canva Layout Suggestion**: 
  * Focus on the Web Dashboard interface. Use callouts or lines to point to the "Start SLAM" and "Save Map" buttons.
* **Display Text**:
  * **Access URL**: Open your web browser and go to 👉 **`http://192.168.1.1/ros2-nav2/`**
  * **Mapping Steps (SLAM)**:
    1. **Start SLAM**: Click the **Bật SLAM** button (spawns the `slam-toolbox` service on ctrlX CORE).
    2. **Drive Robot**: Open a new terminal on your Laptop and run teleop controls:
       ```bash
       export TURTLEBOT3_MODEL=waffle
       ros2 run turtlebot3_teleop teleop_keyboard
       ```
    3. **Save Map**: Type a map name (e.g., `my_office_map`), click **Lưu Bản Đồ**, then click **Dừng SLAM**.
* **Image Description**:
  * 📸 `[IMAGE 8.1]`: Screenshot of the Web UI showing the active 2D grid map being updated in real-time, coupled with a small overlay of the terminal window running keyboard teleoperation.
* **Design Tips**: Use red numbered icons (①, ②, ③) corresponding to the UI actions on the layout.

---

## 🖥️ SLIDE 9: Step 5 (Cont.) - Load Map & Activate Navigation
* **Canva Layout Suggestion**: 
  * Visual cards mapping the two key navigation actions: Map loading and Nav2 initialization.
* **Display Text**:
  * **Navigation Configuration on Web UI**:
    1. **Load Saved Map**:
       * Select your saved map name (e.g., `my_office_map`) from the **Tải Bản Đồ** dropdown menu.
       * Click **Nạp Bản Đồ** to load the static 2D grid layout onto the canvas.
    2. **Activate Navigation Stack**:
       * Click **Bật Navigation** to start AMCL localization and the Nav2 planning stack on the ctrlX CORE.
* **Image Description**:
  * 📸 `[IMAGE 9.1]`: Screenshot of the loaded static map in the Web UI window, showing the dropdown menu with the active selection and the toggled navigation button.
* **Design Tips**: Highlight active buttons with a green border or drop-shadow effect to indicate a successful state transition.

---

## 🖥️ SLIDE 10: Step 5 (Cont.) - Initial Pose & Goals
* **Canva Layout Suggestion**: 
  * Split layout: "Estimate Initial Pose" on the left, "Send Navigation Goal" on the right.
* **Display Text**:
  * **1. Initial Pose Estimation (AMCL)**:
    * Click **📍 Đặt Vị Trí Robot** (button turns yellow).
    * Click and hold on the map at the robot's real position, drag to draw an arrow matching the robot's direction, then release.
    * *Result*: A glowing blue circle represents the localized robot on the map.
  * **2. Send Navigation Goal (Nav2)**:
    * Click **🎯 Chỉ Định Đích Đến** (button turns green).
    * Click, drag, and release to set the target coordinates and desired heading. The robot will plan a path and drive.
* **Image Description**:
  * 📸 `[IMAGE 10.1]`: Close-up of the Web UI map showing the localized robot (glowing blue dot) and a red path planning line leading to the goal.
* **Design Tips**: Use hand cursor symbols on the screen mockups to illustrate the click-and-drag mouse actions.

---

## 🖥️ SLIDE 11: Step 6 - Waypoint Management
* **Canva Layout Suggestion**: 
  * Grid or tabular card design representing the three key functions: Saving, Executing, and Deleting waypoints.
* **Display Text**:
  * **Objective**: Save specific landmarks (e.g., Charging Station, Warehouse, Lobby) to deploy the robot there with a single click.
  * **Features**:
    1. **💾 Save Waypoint**: Click-drag a goal on the map -> Type a name (e.g., `Charger`) in the **Tên điểm** field -> click **Lưu Điểm**.
    2. **🚀 Go to Waypoint**: Click any button in the **Điểm Đã Lưu** list. The robot plans a route and moves immediately.
    3. **❌ Delete Waypoint**: Click the red **x** button on the right of the waypoint name to remove it from memory.
* **Image Description**:
  * 📸 `[IMAGE 11.1]`: Image crop of the Web UI showing the coordinates panel, waypoint name text box, and buttons like `[ Charger 🔋 x ]` or `[ Storage 📦 x ]`.
* **Design Tips**: Use appropriate emojis/icons (🔋, 📦, ❌) to make the waypoint list buttons visually distinct and attractive.

---

## 🖥️ SLIDE 12: Troubleshooting (Part 1)
* **Canva Layout Suggestion**: 
  * Card-based grid structure with a soft light-red or warning-yellow background to denote troubleshooting steps.
* **Display Text**:
  * **Issue 1: Map not displaying on Web UI**
    * *Cause*: Map was not loaded, or the Web Server service on ctrlX CORE crashed.
    * *Solution*: Select the map from the dropdown list and click **Nạp Bản Đồ**. If the issue persists, SSH into the CORE and restart the server:
      ```bash
      sudo snap restart ros2-nav2.web-server
      ```
  * **Issue 2: Robot position indicator (blue dot) does not appear**
    * *Cause*: AMCL service not running or not receiving sensor scan data from the laptop simulator.
    * *Solution*: Make sure Gazebo on your laptop is active and running. Ensure you clicked **Bật Navigation** on the Web UI. Try re-setting the **Initial Pose** on the map.
* **Image Description**:
  * 📸 `[IMAGE 12.1]`: Warning icon. Screenshot of the Web UI depicting an empty map canvas or network timeout indicators.
* **Design Tips**: Use a bold, red font for the "Cause" and a green font for the "Solution" for high readability.

---

## 🖥️ SLIDE 13: Troubleshooting (Part 2)
* **Canva Layout Suggestion**: 
  * Match layout with Slide 12 to maintain visual consistency. Include repository or support info in the footer.
* **Display Text**:
  * **Issue 3: Navigation goal sent, but robot does not move**
    * *Cause*: CycloneDDS communication error (Host and Target are on mismatched subnets or incorrect configuration).
    * *Solution*: Verify both devices are on the exact same LAN subnet. Check the XML peer configuration `cyclonedds_unicast.xml` on the Laptop to verify the Peer IP address matches ctrlX CORE's IP.
  * **Issue 4: Waypoints list is lost after rebooting target**
    * *Cause*: Snap lacks write permission connections for data directories.
    * *Solution*: Waypoints are saved in `$SNAP_COMMON/maps/waypoints.json`. Inspect snap connections and make sure they are active:
      ```bash
      snap connections ros2-nav2
      ```
* **Image Description**:
  * 📸 `[IMAGE 13.1]`: Text snippet of `cyclonedds_unicast.xml` highlighting the peer tag `<Peer Address="192.168.1.1"/>` in yellow.
* **Design Tips**: Place links to the main project GitHub repository or support email in a footer bar at the bottom.
