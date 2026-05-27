#!/usr/bin/env python3
import os
import json
import socket
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

# HTML Dashboard with professional premium dark glassmorphism styling
HTML_CONTENT = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ctrlX OS - ROS 2 Navigation Control</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #07090c;
            --card-bg: rgba(18, 22, 33, 0.65);
            --border-color: rgba(255, 255, 255, 0.06);
            --border-hover: rgba(255, 255, 255, 0.15);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            
            --accent-yellow: #f59e0b;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-red: #ef4444;
            
            --glow-yellow: rgba(245, 158, 11, 0.15);
            --glow-green: rgba(16, 185, 129, 0.15);
            --glow-blue: rgba(59, 130, 246, 0.15);
            --glow-purple: rgba(139, 92, 246, 0.15);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 60%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.05) 0%, transparent 60%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-x: hidden;
        }

        .container {
            width: 100%;
            max-width: 1300px;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 28px;
            padding: 35px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 25px;
        }

        header h1 {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 40%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }

        header p {
            color: var(--text-secondary);
            font-size: 1rem;
            letter-spacing: 0.5px;
        }

        /* Status Area */
        .status-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }

        .status-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .status-info {
            display: flex;
            flex-direction: column;
        }

        .status-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--text-secondary);
            margin-bottom: 4px;
            font-weight: 500;
        }

        .status-value {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.2px;
        }

        .status-dot-container {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 14px;
            height: 14px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: var(--text-secondary);
            transition: all 0.4s ease;
        }

        /* Status Colors */
        .status-active .status-dot {
            background-color: var(--accent-green);
            box-shadow: 0 0 12px 3px rgba(16, 185, 129, 0.5);
        }

        .status-active {
            border-color: rgba(16, 185, 129, 0.2);
            background: rgba(16, 185, 129, 0.02);
        }

        .status-inactive .status-dot {
            background-color: var(--accent-red);
            box-shadow: 0 0 12px 3px rgba(239, 68, 68, 0.5);
        }

        .status-inactive {
            border-color: rgba(239, 68, 68, 0.15);
            background: rgba(239, 68, 68, 0.01);
        }

        /* Controls Grid */
        .control-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .control-card {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid var(--border-color);
            border-radius: 22px;
            padding: 26px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .control-card:hover {
            transform: translateY(-4px);
            border-color: var(--border-hover);
            box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.6);
        }

        .control-card.slam-card { border-top: 4px solid var(--accent-yellow); }
        .control-card.save-card { border-top: 4px solid var(--accent-blue); }
        .control-card.load-card { border-top: 4px solid var(--accent-purple); }
        .control-card.nav-card { border-top: 4px solid var(--accent-green); }

        .control-card.slam-card:hover { box-shadow: 0 12px 30px -10px var(--glow-yellow); }
        .control-card.save-card:hover { box-shadow: 0 12px 30px -10px var(--glow-blue); }
        .control-card.load-card:hover { box-shadow: 0 12px 30px -10px var(--glow-purple); }
        .control-card.nav-card:hover { box-shadow: 0 12px 30px -10px var(--glow-green); }

        .card-header {
            margin-bottom: 12px;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-title .icon {
            font-size: 1.4rem;
        }

        .control-card p {
            font-size: 0.88rem;
            color: var(--text-secondary);
            margin-bottom: 22px;
            line-height: 1.5;
            flex-grow: 1;
        }

        /* Inputs & Selects */
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }

        input[type="text"], select {
            font-family: inherit;
            width: 100%;
            padding: 12px 16px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 0.9rem;
            transition: all 0.3s ease;
            outline: none;
        }

        input[type="text"]:focus, select:focus {
            border-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.05);
        }

        .select-row {
            display: flex;
            gap: 8px;
            align-items: center;
            width: 100%;
        }

        .select-row select {
            flex-grow: 1;
        }

        /* Buttons */
        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .btn-row {
            display: flex;
            gap: 10px;
        }

        .btn-row button {
            flex: 1;
        }

        button {
            font-family: inherit;
            font-weight: 600;
            font-size: 0.92rem;
            padding: 12px 20px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            color: #000000;
        }

        button:active {
            transform: scale(0.98);
        }

        .btn-yellow { background-color: var(--accent-yellow); }
        .btn-yellow:hover { box-shadow: 0 4px 15px var(--glow-yellow); opacity: 0.9; }

        .btn-blue { background-color: var(--accent-blue); color: #ffffff; }
        .btn-blue:hover { box-shadow: 0 4px 15px var(--glow-blue); opacity: 0.9; }

        .btn-purple { background-color: var(--accent-purple); color: #ffffff; }
        .btn-purple:hover { box-shadow: 0 4px 15px var(--glow-purple); opacity: 0.9; }

        .btn-green { background-color: var(--accent-green); }
        .btn-green:hover { box-shadow: 0 4px 15px var(--glow-green); opacity: 0.9; }

        .btn-outline {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .btn-outline:hover {
            background-color: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .btn-icon {
            padding: 12px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .btn-icon:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .refresh-spinner {
            display: inline-block;
            transition: transform 0.4s ease;
        }

        .btn-icon:active .refresh-spinner {
            transform: rotate(360deg);
        }

        /* Log console */
        .console-container {
            background: #030406;
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 22px;
            margin-top: 10px;
        }

        .console-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .console-title {
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .console-output {
            height: 140px;
            overflow-y: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.85rem;
            color: #10b981;
            line-height: 1.6;
            white-space: pre-wrap;
            scrollbar-width: thin;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }

        @media (max-width: 768px) {
            .status-container { grid-template-columns: 1fr; }
            .control-grid { grid-template-columns: 1fr; }
            .container { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ROS 2 Nav2 Control Panel</h1>
            <p>ctrlX CORE Navigation & Map Management Dashboard</p>
        </header>

        <!-- Status Bar -->
        <div class="status-container">
            <div class="status-card" id="card-slam">
                <div class="status-info">
                    <span class="status-label">SLAM (Mapping)</span>
                    <span class="status-value" id="status-val-slam">Checking...</span>
                </div>
                <div class="status-dot-container">
                    <div class="status-dot"></div>
                </div>
            </div>
            <div class="status-card" id="card-localization">
                <div class="status-info">
                    <span class="status-label">Localization</span>
                    <span class="status-value" id="status-val-localization">Checking...</span>
                </div>
                <div class="status-dot-container">
                    <div class="status-dot"></div>
                </div>
            </div>
            <div class="status-card" id="card-navigation">
                <div class="status-info">
                    <span class="status-label">Navigation (Nav2)</span>
                    <span class="status-value" id="status-val-navigation">Checking...</span>
                </div>
                <div class="status-dot-container">
                    <div class="status-dot"></div>
                </div>
            </div>
        </div>

        <!-- Controls Grid -->
        <div class="control-grid">
            <!-- SLAM Card -->
            <div class="control-card slam-card">
                <div class="card-header">
                    <h2 class="card-title"><span class="icon">🧭</span> SLAM (Quét Bản Đồ)</h2>
                </div>
                <p>Khởi động chế độ quét bản đồ LiDAR. Robot được điều khiển thủ công bằng Teleop trên máy tính laptop.</p>
                <div class="btn-group">
                    <button class="btn-yellow" onclick="callAPI('slam', 'start')">Bật SLAM</button>
                    <button class="btn-outline" onclick="callAPI('slam', 'stop')">Dừng SLAM</button>
                </div>
            </div>

            <!-- Save Map Card -->
            <div class="control-card save-card">
                <div class="card-header">
                    <h2 class="card-title"><span class="icon">💾</span> Lưu Bản Đồ</h2>
                </div>
                <p>Lưu bản đồ hiện tại đang quét từ SLAM với tên tùy chỉnh vào bộ nhớ hệ thống.</p>
                <div class="input-group">
                    <input type="text" id="map-name-input" placeholder="Nhập tên bản đồ (ví dụ: office_map)..." value="new_map">
                    <button class="btn-blue" onclick="saveMap()">Lưu Bản Đồ</button>
                </div>
            </div>

            <!-- Load Map Card -->
            <div class="control-card load-card">
                <div class="card-header">
                    <h2 class="card-title"><span class="icon">📂</span> Tải Bản Đồ</h2>
                </div>
                <p>Chọn một bản đồ từ danh sách đã lưu để thiết lập làm bản đồ hoạt động hiện tại.</p>
                <div class="input-group">
                    <div class="select-row">
                        <select id="map-select">
                            <option value="">Đang tải danh sách...</option>
                        </select>
                        <button class="btn-icon" onclick="loadMapList()" title="Làm mới danh sách">
                            <span class="refresh-spinner">↻</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Navigation Card -->
            <div class="control-card nav-card">
                <div class="card-header">
                    <h2 class="card-title"><span class="icon">⚡</span> Dẫn Đường (Nav2)</h2>
                </div>
                <p>Khởi động bộ tự động dẫn đường và định vị trên bản đồ đã chọn. Có thể điều khiển trực tiếp trên Bản đồ tương tác bên dưới.</p>
                <div class="btn-group">
                    <button class="btn-green" onclick="callAPI('nav2', 'start')">Bật Navigation</button>
                    <div class="btn-row">
                        <button class="btn-outline" onclick="callAPI('nav2', 'restart')">Khởi động lại</button>
                        <button class="btn-outline" onclick="callAPI('nav2', 'stop')">Dừng</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Map Visualizer Card -->
        <div class="map-container-card" id="map-card" style="display:none; margin-bottom: 30px; background: rgba(255, 255, 255, 0.015); border: 1px solid var(--border-color); border-radius: 22px; padding: 26px;">
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px;">
                <h2 class="card-title"><span class="icon">🗺️</span> Bản Đồ Tương Tác (Interactive Map)</h2>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-outline" id="btn-mode-pose" onclick="setInteractionMode('pose')" style="padding: 6px 12px; font-size: 0.8rem;">📍 Đặt Vị Trí Robot</button>
                    <button class="btn-green" id="btn-mode-goal" onclick="setInteractionMode('goal')" style="padding: 6px 12px; font-size: 0.8rem;">🎯 Chỉ Định Đích Đến</button>
                </div>
            </div>
            <div style="display: flex; justify-content: center; background: #030406; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); position: relative; min-height: 200px; align-items: center; padding: 20px;">
                <canvas id="map-canvas" style="cursor: crosshair; width: 100%; max-width: 900px; height: auto; display: block; image-rendering: pixelated;"></canvas>
                <div id="canvas-overlay-text" style="position: absolute; bottom: 10px; right: 15px; font-family: monospace; font-size: 0.8rem; color: var(--text-secondary); background: rgba(0,0,0,0.75); padding: 4px 8px; border-radius: 6px; border: 1px solid var(--border-color);">
                    X: 0.00m, Y: 0.00m
                </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 10px;">
                * Hướng dẫn: Chọn chế độ ở trên, sau đó **Click giữ và kéo chuột** trên bản đồ để vẽ mũi tên chỉ vị trí và góc hướng (Yaw) cho Robot hoặc Đích đến.
            </p>
            
            <!-- Waypoint Manager Section -->
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid var(--border-color);">
                <h3 style="font-size: 1.05rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; font-weight: 700; color: var(--text-primary);">
                    <span>📍</span> Danh Sách Điểm Đã Lưu (Saved Waypoints)
                </h3>
                
                <!-- Saved Waypoints List -->
                <div id="waypoints-list" style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px; min-height: 40px; align-items: center;">
                    <span style="font-size: 0.85rem; color: var(--text-secondary);">Chưa có điểm nào được lưu. Hãy chọn một điểm trên bản đồ để lưu.</span>
                </div>

                <!-- Save Waypoint Form -->
                <div id="save-waypoint-form" style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap; background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid var(--border-color);">
                    <span style="font-size: 0.85rem; color: var(--text-secondary);">Tọa độ chọn:</span>
                    <input type="text" id="wp-coord-display" readonly placeholder="Chưa chọn điểm..." style="padding: 6px 12px; font-size: 0.85rem; border-radius: 8px; border: 1px solid var(--border-color); background: rgba(0,0,0,0.3); color: var(--text-secondary); width: 220px; text-align: center;">
                    
                    <input type="text" id="wp-name-input" placeholder="Tên điểm (vd: Phòng khách)..." style="padding: 6px 12px; font-size: 0.85rem; border-radius: 8px; border: 1px solid var(--border-color); background: rgba(0,0,0,0.2); color: white; flex-grow: 1; min-width: 150px;">
                    
                    <button class="btn-blue" onclick="addWaypoint()" style="padding: 6px 12px; font-size: 0.85rem; white-space: nowrap;">💾 Lưu Điểm</button>
                </div>
            </div>
        </div>

        <!-- Console Log -->
        <div class="console-container">
            <div class="console-header">
                <span class="console-title">💬 Nhật ký hệ thống (System Log)</span>
                <span id="log-time">Live Connection</span>
            </div>
            <div class="console-output" id="console-output">Khởi động bảng điều khiển thành công. Chờ lệnh từ người dùng...</div>
        </div>
    </div>

    <script>
        let mapInfo = null;
        let mapImage = new Image();
        let robotPose = null; // { x, y, yaw } in pixels
        let interactionMode = 'goal'; // 'goal' or 'pose'
        let isDrawing = false;
        let startX = 0;
        let startY = 0;
        let currentX = 0;
        let currentY = 0;
        let isRenderLoopStarted = false;
        let lastSelectedPose = null;

        function log(message) {
            const consoleBox = document.getElementById('console-output');
            const time = new Date().toLocaleTimeString();
            consoleBox.innerHTML += `\n[${time}] ${message}`;
            consoleBox.scrollTop = consoleBox.scrollHeight;
        }

        function setInteractionMode(mode) {
            interactionMode = mode;
            const btnPose = document.getElementById('btn-mode-pose');
            const btnGoal = document.getElementById('btn-mode-goal');
            if (mode === 'pose') {
                btnPose.className = 'btn-yellow';
                btnGoal.className = 'btn-outline';
                log("Chuyển chế độ: Thiết lập Vị Trí Robot (Initial Pose)");
            } else {
                btnPose.className = 'btn-outline';
                btnGoal.className = 'btn-green';
                log("Chuyển chế độ: Gửi Điểm Đích Đến (Nav2 Goal)");
            }
        }

        async function initMap() {
            try {
                const res = await fetch('api/map/info');
                const data = await res.json();
                if (data.success) {
                    mapInfo = data;
                    document.getElementById('map-card').style.display = 'block';
                    mapImage.src = 'api/map/image?name=' + data.name + '&t=' + new Date().getTime();
                    mapImage.onload = () => {
                        drawMap();
                        if (!isRenderLoopStarted) {
                            isRenderLoopStarted = true;
                            renderLoop();
                        }
                    };
                } else {
                    document.getElementById('map-card').style.display = 'none';
                }
            } catch (err) {
                console.error("Lỗi lấy thông tin bản đồ:", err);
            }
        }

        async function fetchRobotPose() {
            if (!mapInfo) return;
            try {
                const res = await fetch('api/navigation/pose');
                const data = await res.json();
                if (data.valid) {
                    const canvas = document.getElementById('map-canvas');
                    if (canvas) {
                        const pixelX = (data.x - mapInfo.origin_x) / mapInfo.resolution;
                        const pixelY = canvas.height - ((data.y - mapInfo.origin_y) / mapInfo.resolution);
                        robotPose = { x: pixelX, y: pixelY, yaw: data.yaw };
                    }
                } else {
                    robotPose = null;
                }
            } catch (err) {
                console.error("Lỗi lấy tọa độ bot:", err);
            }
        }

        setInterval(fetchRobotPose, 200);

        function drawMap() {
            const canvas = document.getElementById('map-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            canvas.width = mapImage.width;
            canvas.height = mapImage.height;
            ctx.drawImage(mapImage, 0, 0);

            // Draw robot pose if valid
            if (robotPose) {
                ctx.save();
                ctx.translate(robotPose.x, robotPose.y);
                
                // Pulsing ring
                const pulseRadius = 9 + 3.5 * Math.sin(Date.now() / 150);
                ctx.beginPath();
                ctx.arc(0, 0, pulseRadius, 0, 2 * Math.PI);
                ctx.fillStyle = 'rgba(59, 130, 246, 0.35)';
                ctx.fill();

                // Outer border
                ctx.beginPath();
                ctx.arc(0, 0, 8.5, 0, 2 * Math.PI);
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                // Inner robot body (blue)
                ctx.beginPath();
                ctx.arc(0, 0, 6.5, 0, 2 * Math.PI);
                ctx.fillStyle = '#3b82f6';
                ctx.fill();

                // Direction pointer arrow
                ctx.rotate(-robotPose.yaw);
                ctx.beginPath();
                ctx.moveTo(5.5, 0);
                ctx.lineTo(-3.5, -3.5);
                ctx.lineTo(-3.5, 3.5);
                ctx.closePath();
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                ctx.restore();
            }
        }

        function renderLoop() {
            if (mapInfo && mapImage.complete && !isDrawing) {
                drawMap();
            }
            requestAnimationFrame(renderLoop);
        }

        async function updateStatus() {
            try {
                const response = await fetch('api/status');
                const data = await response.json();
                
                const services = ['slam', 'localization', 'navigation'];
                services.forEach(srv => {
                    const card = document.getElementById(`card-${srv}`);
                    const valueEl = document.getElementById(`status-val-${srv}`);
                    const status = data[srv];
                    
                    valueEl.innerText = status.toUpperCase();
                    
                    if (status === 'active') {
                        card.className = 'status-card status-active';
                    } else if (status === 'inactive') {
                        card.className = 'status-card status-inactive';
                    } else {
                        card.className = 'status-card';
                    }
                });
            } catch (error) {
                console.error("Error fetching status:", error);
            }
        }

        async function callAPI(service, action) {
            log(`Gửi lệnh: ${action.toUpperCase()} tới dịch vụ ${service.toUpperCase()}...`);
            try {
                const response = await fetch('api/service', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service, action })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Thành công: ${result.message}`);
                    if (service === 'nav2' && action === 'start') {
                        setTimeout(initMap, 2000);
                    }
                } else {
                    log(`Lỗi: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi kết nối mạng: ${err.message}`);
            }
            setTimeout(updateStatus, 1500);
        }

        async function loadMapList() {
            try {
                const response = await fetch('api/maps');
                const maps = await response.json();
                const select = document.getElementById('map-select');
                select.innerHTML = '';
                
                if (maps.length === 0) {
                    select.innerHTML = '<option value="">Không có bản đồ nào</option>';
                    log("Không tìm thấy bản đồ nào trong thư mục lưu trữ.");
                    return;
                }
                
                maps.forEach(map => {
                    const opt = document.createElement('option');
                    opt.value = map;
                    opt.innerText = map;
                    select.appendChild(opt);
                });
                log(`Đã cập nhật danh sách bản đồ (${maps.length} bản đồ được tìm thấy)`);
            } catch (err) {
                log(`Lỗi tải danh sách bản đồ: ${err.message}`);
            }
        }

        async function saveMap() {
            const nameInput = document.getElementById('map-name-input');
            const name = nameInput.value.trim();
            if (!name) {
                log("Lỗi: Tên bản đồ không được để trống!");
                return;
            }
            log(`Đang yêu cầu lưu bản đồ với tên: '${name}'...`);
            try {
                const response = await fetch('api/map/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Thành công: ${result.message}`);
                    loadMapList();
                } else {
                    log(`Lỗi: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi kết nối mạng: ${err.message}`);
            }
        }

        async function loadMap() {
            const select = document.getElementById('map-select');
            const name = select.value;
            if (!name) {
                log("Lỗi: Vui lòng chọn một bản đồ để nạp!");
                return;
            }
            log(`Đang nạp bản đồ: '${name}' vào hệ thống...`);
            try {
                const response = await fetch('api/map/load', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Thành công: ${result.message}`);
                    setTimeout(initMap, 2000);
                } else {
                    log(`Lỗi: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi kết nối mạng: ${err.message}`);
            }
            setTimeout(updateStatus, 1500);
        }

        // Register Canvas Events
        window.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('map-canvas');
            if (!canvas) return;
            
            canvas.addEventListener('mousemove', (e) => {
                if (!mapInfo || !mapImage.complete) return;
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const pixelX = (e.clientX - rect.left) * scaleX;
                const pixelY = (e.clientY - rect.top) * scaleY;
                
                const rosX = mapInfo.origin_x + pixelX * mapInfo.resolution;
                const rosY = mapInfo.origin_y + (canvas.height - pixelY) * mapInfo.resolution;
                
                document.getElementById('canvas-overlay-text').innerText = `X: ${rosX.toFixed(2)}m, Y: ${rosY.toFixed(2)}m`;
                
                if (isDrawing) {
                    currentX = pixelX;
                    currentY = pixelY;
                    redrawCanvasWithArrow();
                }
            });
            
            canvas.addEventListener('mousedown', (e) => {
                if (!mapInfo || !mapImage.complete) return;
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                startX = (e.clientX - rect.left) * scaleX;
                startY = (e.clientY - rect.top) * scaleY;
                currentX = startX;
                currentY = startY;
                isDrawing = true;
            });
            
            canvas.addEventListener('mouseup', (e) => {
                if (!isDrawing) return;
                isDrawing = false;
                
                const rosX = mapInfo.origin_x + startX * mapInfo.resolution;
                const rosY = mapInfo.origin_y + (canvas.height - startY) * mapInfo.resolution;
                
                const dx = currentX - startX;
                const dy = startY - currentY; // Invert Y axis for ROS
                let yaw = Math.atan2(dy, dx);
                
                lastSelectedPose = { x: rosX, y: rosY, yaw: yaw };
                document.getElementById('wp-coord-display').value = `X: ${rosX.toFixed(2)}, Y: ${rosY.toFixed(2)}, Yaw: ${yaw.toFixed(2)}`;
                
                sendPose(rosX, rosY, yaw);
            });
        });

        function redrawCanvasWithArrow() {
            const canvas = document.getElementById('map-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(mapImage, 0, 0);

            // Draw robot pose if valid
            if (robotPose) {
                ctx.save();
                ctx.translate(robotPose.x, robotPose.y);
                
                // Pulsing ring
                const pulseRadius = 9 + 3.5 * Math.sin(Date.now() / 150);
                ctx.beginPath();
                ctx.arc(0, 0, pulseRadius, 0, 2 * Math.PI);
                ctx.fillStyle = 'rgba(59, 130, 246, 0.35)';
                ctx.fill();

                // Outer border
                ctx.beginPath();
                ctx.arc(0, 0, 8.5, 0, 2 * Math.PI);
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                // Inner robot body (blue)
                ctx.beginPath();
                ctx.arc(0, 0, 6.5, 0, 2 * Math.PI);
                ctx.fillStyle = '#3b82f6';
                ctx.fill();

                // Direction pointer arrow
                ctx.rotate(-robotPose.yaw);
                ctx.beginPath();
                ctx.moveTo(5.5, 0);
                ctx.lineTo(-3.5, -3.5);
                ctx.lineTo(-3.5, 3.5);
                ctx.closePath();
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                ctx.restore();
            }
            
            ctx.beginPath();
            ctx.arc(startX, startY, 6, 0, 2 * Math.PI);
            ctx.fillStyle = interactionMode === 'pose' ? '#f59e0b' : '#10b981';
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(currentX, currentY);
            ctx.strokeStyle = interactionMode === 'pose' ? '#f59e0b' : '#10b981';
            ctx.lineWidth = 4;
            ctx.stroke();
            
            const angle = Math.atan2(currentY - startY, currentX - startX);
            ctx.beginPath();
            ctx.moveTo(currentX, currentY);
            ctx.lineTo(currentX - 16 * Math.cos(angle - Math.PI / 6), currentY - 16 * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(currentX - 16 * Math.cos(angle + Math.PI / 6), currentY - 16 * Math.sin(angle + Math.PI / 6));
            ctx.closePath();
            ctx.fillStyle = interactionMode === 'pose' ? '#f59e0b' : '#10b981';
            ctx.fill();
        }

        async function sendPose(x, y, yaw) {
            const endpoint = interactionMode === 'pose' ? 'api/navigation/initialpose' : 'api/navigation/goal';
            log(`Đang gửi vị trí (${interactionMode.toUpperCase()}): x=${x.toFixed(2)}, y=${y.toFixed(2)}, yaw=${yaw.toFixed(2)} rad`);
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ x, y, yaw })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Gửi thành công: ${result.message}`);
                } else {
                    log(`Gửi thất bại: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi mạng: ${err.message}`);
            }
            setTimeout(drawMap, 1500);
        }

        async function addWaypoint() {
            if (!lastSelectedPose) {
                log("Lỗi: Vui lòng click và kéo chuột trên bản đồ để chọn một điểm trước khi lưu.");
                return;
            }
            const name = document.getElementById('wp-name-input').value.trim();
            if (!name) {
                log("Lỗi: Vui lòng nhập tên cho điểm cần lưu.");
                return;
            }
            
            try {
                const response = await fetch('api/waypoints', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: name,
                        x: lastSelectedPose.x,
                        y: lastSelectedPose.y,
                        yaw: lastSelectedPose.yaw
                    })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Đã lưu điểm: ${name}`);
                    document.getElementById('wp-name-input').value = '';
                    document.getElementById('wp-coord-display').value = '';
                    lastSelectedPose = null;
                    loadWaypoints();
                } else {
                    log(`Lỗi lưu điểm: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi kết nối mạng: ${err.message}`);
            }
        }

        async function loadWaypoints() {
            try {
                const response = await fetch('api/waypoints');
                const waypoints = await response.json();
                const listDiv = document.getElementById('waypoints-list');
                listDiv.innerHTML = '';
                
                if (waypoints.length === 0) {
                    listDiv.innerHTML = '<span style="font-size: 0.85rem; color: var(--text-secondary);">Chưa có điểm nào được lưu. Hãy chọn một điểm trên bản đồ để lưu.</span>';
                    return;
                }
                
                waypoints.forEach(wp => {
                    const btnGroup = document.createElement('div');
                    btnGroup.style.display = 'inline-flex';
                    btnGroup.style.alignItems = 'center';
                    btnGroup.style.background = 'rgba(59, 130, 246, 0.1)';
                    btnGroup.style.border = '1px solid rgba(59, 130, 246, 0.3)';
                    btnGroup.style.borderRadius = '8px';
                    btnGroup.style.overflow = 'hidden';
                    btnGroup.style.margin = '2px';
                    
                    const btnGo = document.createElement('button');
                    btnGo.innerText = wp.name;
                    btnGo.className = 'btn-green';
                    btnGo.style.padding = '5px 12px';
                    btnGo.style.fontSize = '0.8rem';
                    btnGo.style.borderRadius = '0';
                    btnGo.style.border = 'none';
                    btnGo.onclick = () => {
                        log(`Đi tới điểm đã lưu: ${wp.name} (x=${wp.x.toFixed(2)}, y=${wp.y.toFixed(2)})`);
                        sendPoseDirectly(wp.x, wp.y, wp.yaw);
                    };
                    
                    const btnDel = document.createElement('button');
                    btnDel.innerHTML = '&times;';
                    btnDel.style.background = 'rgba(239, 68, 68, 0.2)';
                    btnDel.style.color = '#ef4444';
                    btnDel.style.border = 'none';
                    btnDel.style.borderLeft = '1px solid rgba(59, 130, 246, 0.3)';
                    btnDel.style.padding = '5px 8px';
                    btnDel.style.cursor = 'pointer';
                    btnDel.style.fontSize = '0.9rem';
                    btnDel.style.lineHeight = '1';
                    btnDel.onclick = async () => {
                        if (confirm(`Bạn có chắc chắn muốn xóa điểm "${wp.name}"?`)) {
                            await deleteWaypoint(wp.name);
                        }
                    };
                    
                    btnGroup.appendChild(btnGo);
                    btnGroup.appendChild(btnDel);
                    listDiv.appendChild(btnGroup);
                });
            } catch (err) {
                console.error("Lỗi lấy danh sách điểm lưu:", err);
            }
        }

        async function deleteWaypoint(name) {
            try {
                const response = await fetch('api/waypoints/delete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Đã xóa điểm: ${name}`);
                    loadWaypoints();
                } else {
                    log(`Lỗi xóa điểm: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi kết nối mạng: ${err.message}`);
            }
        }

        async function sendPoseDirectly(x, y, yaw) {
            log(`Đang gửi lệnh di chuyển tới: x=${x.toFixed(2)}, y=${y.toFixed(2)}, yaw=${yaw.toFixed(2)} rad`);
            try {
                const response = await fetch('api/navigation/goal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ x, y, yaw })
                });
                const result = await response.json();
                if (result.success) {
                    log(`Gửi lệnh thành công: ${result.message}`);
                } else {
                    log(`Gửi lệnh thất bại: ${result.message}`);
                }
            } catch (err) {
                log(`Lỗi mạng: ${err.message}`);
            }
        }

        // Khởi động
        updateStatus();
        loadMapList();
        loadWaypoints();
        initMap();
        setInterval(updateStatus, 3000);
    </script>
</body>
</html>
"""
import threading

latest_pose = {"x": 0.0, "y": 0.0, "yaw": 0.0, "valid": False}

def pose_listener_subprocess_fallback():
    global latest_pose
    import time
    cmd = ["ros2", "topic", "echo", "/amcl_pose", "geometry_msgs/msg/PoseWithCovarianceStamped"]
    while True:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
            x_val, y_val, z_rot, w_rot = None, None, None, None
            for line in proc.stdout:
                line = line.strip()
                if line.startswith("x:"):
                    try:
                        val = float(line.split()[1])
                        if x_val is None:
                            x_val = val
                    except Exception:
                        pass
                elif line.startswith("y:"):
                    try:
                        val = float(line.split()[1])
                        if y_val is None:
                            y_val = val
                    except Exception:
                        pass
                elif line.startswith("z:"):
                    try:
                        val = float(line.split()[1])
                        z_rot = val
                    except Exception:
                        pass
                elif line.startswith("w:"):
                    try:
                        val = float(line.split()[1])
                        w_rot = val
                    except Exception:
                        pass
                elif line.startswith("---"):
                    if x_val is not None and y_val is not None and z_rot is not None and w_rot is not None:
                        import math
                        yaw = 2.0 * math.atan2(z_rot, w_rot)
                        latest_pose = {"x": x_val, "y": y_val, "yaw": yaw, "valid": True}
                    x_val, y_val, z_rot, w_rot = None, None, None, None
            proc.wait()
        except Exception as e:
            print(f"Error in fallback pose listener: {e}", file=sys.stderr)
        time.sleep(2)

def pose_listener_thread():
    global latest_pose
    try:
        import rclpy
        from rclpy.node import Node
        from geometry_msgs.msg import PoseWithCovarianceStamped
        
        if not rclpy.ok():
            rclpy.init()
            
        class PoseSubscriber(Node):
            def __init__(self):
                super().__init__('web_server_pose_listener')
                self.subscription = self.create_subscription(
                    PoseWithCovarianceStamped,
                    '/amcl_pose',
                    self.listener_callback,
                    10)
                
            def listener_callback(self, msg):
                global latest_pose
                x = msg.pose.pose.position.x
                y = msg.pose.pose.position.y
                z = msg.pose.pose.orientation.z
                w = msg.pose.pose.orientation.w
                import math
                yaw = 2.0 * math.atan2(z, w)
                latest_pose = {"x": x, "y": y, "yaw": yaw, "valid": True}
                
        node = PoseSubscriber()
        rclpy.spin(node)
    except Exception as e:
        print(f"Error in rclpy pose listener: {e}", file=sys.stderr)
        pose_listener_subprocess_fallback()

def parse_map_yaml(yaml_path):
    info = {}
    if not os.path.exists(yaml_path):
        return None
    try:
        with open(yaml_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    info[key] = val
    except Exception as e:
        print(f"Error parsing yaml {yaml_path}: {e}", file=sys.stderr)
    return info

class UnixHTTPServer(HTTPServer):
    def server_bind(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Ensure cleanup of existing socket file
        if os.path.exists(self.server_address):
            os.remove(self.server_address)
        self.socket.bind(self.server_address)
        self.socket.listen(5)

class DashboardRequestHandler(BaseHTTPRequestHandler):
    def address_string(self):
        return "unix"

    def get_maps_dir(self):
        snap_common = os.environ.get('SNAP_COMMON')
        if snap_common:
            return os.path.join(snap_common, 'maps')
        # Fallback to local workspace maps directory
        local_maps = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'maps'))
        if os.path.exists(local_maps):
            return local_maps
        return '/tmp/maps'

    def get_waypoints_file(self):
        maps_dir = self.get_maps_dir()
        os.makedirs(maps_dir, exist_ok=True)
        return os.path.join(maps_dir, 'waypoints.json')

    def get_saved_maps(self):
        maps_dir = self.get_maps_dir()
        if not os.path.exists(maps_dir):
            return []
        maps = []
        try:
            for f in os.listdir(maps_dir):
                if f.endswith('.yaml') and f != 'current_map.yaml':
                    maps.append(f[:-5]) # Remove '.yaml' extension
        except Exception as e:
            print(f"Error listing maps in {maps_dir}: {e}", file=sys.stderr)
        return sorted(maps)

    def do_GET(self):
        if self.path == '/ros2-nav2' or self.path == '/ros2-nav2/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
            return
            
        elif self.path == '/ros2-nav2/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = self.get_snap_services_status()
            self.wfile.write(json.dumps(status).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/maps':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            maps = self.get_saved_maps()
            self.wfile.write(json.dumps(maps).encode('utf-8'))
            return
            
        elif self.path == '/ros2-nav2/api/navigation/pose':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(latest_pose).encode('utf-8'))
            return
            
        elif self.path == '/ros2-nav2/api/waypoints':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            wps_file = self.get_waypoints_file()
            wps = []
            if os.path.exists(wps_file):
                try:
                    with open(wps_file, 'r') as f:
                        wps = json.load(f)
                except Exception as e:
                    print(f"Error reading waypoints file: {e}", file=sys.stderr)
            self.wfile.write(json.dumps(wps).encode('utf-8'))
            return
            
        elif self.path.startswith('/ros2-nav2/api/map/info'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            map_name = params.get('name', [None])[0]
            
            maps_dir = self.get_maps_dir()
            if map_name and map_name != 'undefined':
                yaml_path = os.path.join(maps_dir, f"{map_name}.yaml")
            else:
                yaml_path = os.path.join(maps_dir, 'current_map.yaml')
                
            map_info = parse_map_yaml(yaml_path)
            if not map_info:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Map info not found"}).encode('utf-8'))
                return
                
            try:
                resolution = float(map_info.get('resolution', 0.05))
                origin_str = map_info.get('origin', '[0.0, 0.0, 0.0]')
                origin_str = origin_str.replace('[', '').replace(']', '')
                origin_parts = [float(x.strip()) for x in origin_str.split(',')]
                
                response_data = {
                    "success": True,
                    "name": map_name or "current_map",
                    "resolution": resolution,
                    "origin_x": origin_parts[0],
                    "origin_y": origin_parts[1],
                    "origin_yaw": origin_parts[2]
                }
            except Exception as e:
                response_data = {"success": False, "message": f"Error parsing map: {str(e)}"}
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        elif self.path.startswith('/ros2-nav2/api/map/image'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            map_name = params.get('name', [None])[0]
            
            maps_dir = self.get_maps_dir()
            if map_name and map_name != 'undefined' and map_name != 'null':
                yaml_path = os.path.join(maps_dir, f"{map_name}.yaml")
            else:
                yaml_path = os.path.join(maps_dir, 'current_map.yaml')
                
            map_info = parse_map_yaml(yaml_path)
            if not map_info or 'image' not in map_info:
                self.send_error(404, "Map image config not found")
                return
                
            image_path = os.path.join(maps_dir, map_info['image'])
            if not os.path.exists(image_path):
                self.send_error(404, f"Map image file {map_info['image']} not found")
                return
                
            self.send_response(200)
            if image_path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            elif image_path.endswith('.pgm'):
                self.send_header('Content-type', 'image/x-portable-graymap')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            
            with open(image_path, 'rb') as f:
                self.wfile.write(f.read())
            return

        elif self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/ros2-nav2/')
            self.end_headers()
            return
            
        self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/ros2-nav2/api/service':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            service = req.get('service')
            action = req.get('action')
            
            success, msg = self.handle_service_action(service, action)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            res = {"success": success, "message": msg}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/waypoints':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            name = req.get('name')
            x = float(req.get('x', 0.0))
            y = float(req.get('y', 0.0))
            yaw = float(req.get('yaw', 0.0))
            
            wps_file = self.get_waypoints_file()
            wps = []
            if os.path.exists(wps_file):
                try:
                    with open(wps_file, 'r') as f:
                        wps = json.load(f)
                except Exception as e:
                    print(f"Error reading waypoints file: {e}", file=sys.stderr)
            
            wps = [wp for wp in wps if wp.get('name') != name]
            wps.append({"name": name, "x": x, "y": y, "yaw": yaw})
            
            success = True
            msg = "Saved successfully"
            try:
                with open(wps_file, 'w') as f:
                    json.dump(wps, f, indent=4)
            except Exception as e:
                success = False
                msg = f"Error saving waypoints file: {str(e)}"
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return
            
        elif self.path == '/ros2-nav2/api/waypoints/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            name = req.get('name')
            
            wps_file = self.get_waypoints_file()
            wps = []
            if os.path.exists(wps_file):
                try:
                    with open(wps_file, 'r') as f:
                        wps = json.load(f)
                except Exception as e:
                    print(f"Error reading waypoints file: {e}", file=sys.stderr)
            
            new_wps = [wp for wp in wps if wp.get('name') != name]
            
            success = True
            msg = "Deleted successfully"
            try:
                with open(wps_file, 'w') as f:
                    json.dump(new_wps, f, indent=4)
            except Exception as e:
                success = False
                msg = f"Error saving waypoints file: {str(e)}"
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/navigation/goal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            x = float(req.get('x', 0.0))
            y = float(req.get('y', 0.0))
            yaw = float(req.get('yaw', 0.0))
            
            import math
            sin_y = math.sin(yaw * 0.5)
            cos_y = math.cos(yaw * 0.5)
            
            pose_msg = f"{{header: {{frame_id: 'map'}}, pose: {{position: {{x: {x}, y: {y}, z: 0.0}}, orientation: {{x: 0.0, y: 0.0, z: {sin_y}, w: {cos_y}}}}}}}"
            
            cmd = ["ros2", "topic", "pub", "--once", "/goal_pose", "geometry_msgs/msg/PoseStamped", pose_msg]
            try:
                res = subprocess.run(cmd, env=os.environ, capture_output=True, text=True, timeout=5)
                if res.returncode == 0:
                    success, msg = True, f"Đích đến x={x:.2f}, y={y:.2f}, yaw={yaw:.2f}"
                else:
                    success, msg = False, f"Lỗi gửi đích: {res.stderr or res.stdout}"
            except Exception as e:
                success, msg = False, f"Lỗi hệ thống: {str(e)}"
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/navigation/initialpose':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            
            x = float(req.get('x', 0.0))
            y = float(req.get('y', 0.0))
            yaw = float(req.get('yaw', 0.0))
            
            import math
            sin_y = math.sin(yaw * 0.5)
            cos_y = math.cos(yaw * 0.5)
            
            pose_msg = f"{{header: {{frame_id: 'map'}}, pose: {{pose: {{position: {{x: {x}, y: {y}, z: 0.0}}, orientation: {{x: 0.0, y: 0.0, z: {sin_y}, w: {cos_y}}}}}, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]}}}}"
            
            cmd = ["ros2", "topic", "pub", "--once", "/initialpose", "geometry_msgs/msg/PoseWithCovarianceStamped", pose_msg]
            try:
                res = subprocess.run(cmd, env=os.environ, capture_output=True, text=True, timeout=5)
                if res.returncode == 0:
                    success, msg = True, f"Vị trí Robot x={x:.2f}, y={y:.2f}, yaw={yaw:.2f}"
                else:
                    success, msg = False, f"Lỗi gửi vị trí ban đầu: {res.stderr or res.stdout}"
            except Exception as e:
                success, msg = False, f"Lỗi hệ thống: {str(e)}"
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/map/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            name = req.get('name', '').strip()
            
            if not name:
                success, msg = False, "Tên bản đồ không được để trống"
            elif not name.replace('_', '').isalnum():
                success, msg = False, "Tên bản đồ chỉ được chứa chữ cái, số và dấu gạch dưới"
            else:
                snap = os.environ.get('SNAP', '')
                script_path = os.path.join(snap, 'usr/bin/save_map.sh') if snap else './snap/local/save_map.sh'
                
                try:
                    if os.path.exists(script_path):
                        try:
                            os.chmod(script_path, 0o755)
                        except OSError:
                            pass # Bỏ qua nếu chạy trong file system Read-only của snap
                    
                    res = subprocess.run([script_path, name], capture_output=True, text=True, env=os.environ, timeout=20)
                    if res.returncode == 0:
                        success, msg = True, f"Đã lưu bản đồ '{name}' thành công!"
                    else:
                        success, msg = False, f"Lỗi chạy script lưu: {res.stderr or res.stdout}"
                except Exception as e:
                    success, msg = False, f"Lỗi thực thi: {str(e)}"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return

        elif self.path == '/ros2-nav2/api/map/load':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            name = req.get('name', '').strip()
            
            maps_dir = self.get_maps_dir()
            map_path = os.path.join(maps_dir, f"{name}.yaml")
            
            if not name:
                success, msg = False, "Tên bản đồ không hợp lệ"
            elif not os.path.exists(map_path):
                success, msg = False, f"Bản đồ '{name}' không tồn tại trong {maps_dir}!"
            else:
                try:
                    # 1. Update map path using snapctl
                    subprocess.run(["snapctl", "set", f"map={map_path}"])
                    
                    # 2. Update current_map.yaml symlink
                    current_map_path = os.path.join(maps_dir, 'current_map.yaml')
                    if os.path.exists(current_map_path) or os.path.islink(current_map_path):
                        os.remove(current_map_path)
                    os.symlink(map_path, current_map_path)
                    
                    # 3. Check and restart active services
                    status = self.get_snap_services_status()
                    restarted = []
                    if status.get('localization') == 'active':
                        subprocess.run(["snapctl", "restart", "ros2-nav2.localization"])
                        restarted.append("Localization")
                    if status.get('navigation') == 'active':
                        subprocess.run(["snapctl", "restart", "ros2-nav2.navigation"])
                        restarted.append("Navigation")
                        
                    if restarted:
                        msg = f"Đã tải bản đồ '{name}' và khởi động lại: {', '.join(restarted)}"
                    else:
                        msg = f"Đã thiết lập bản đồ '{name}' làm mặc định thành công."
                    success = True
                except Exception as e:
                    success, msg = False, f"Lỗi nạp bản đồ: {str(e)}"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success, "message": msg}).encode('utf-8'))
            return
            
        self.send_error(404, "Endpoint not found")

    def get_snap_services_status(self):
        statuses = {"slam": "inactive", "localization": "inactive", "navigation": "inactive"}
        try:
            # Check services status using snapctl
            res = subprocess.run(["snapctl", "services"], capture_output=True, text=True, timeout=2)
            lines = res.stdout.splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    state = parts[2]
                    short_name = name.split(".")[-1]
                    if short_name in statuses:
                        statuses[short_name] = state
        except Exception:
            pass
        return statuses

    def handle_service_action(self, service, action):
        if service == 'slam':
            if action == 'start':
                res = subprocess.run(["snapctl", "start", "ros2-nav2.slam"], capture_output=True, text=True)
                return res.returncode == 0, "Bật SLAM thành công" if res.returncode == 0 else f"Lỗi: {res.stderr}"
            elif action == 'stop':
                res = subprocess.run(["snapctl", "stop", "ros2-nav2.slam"], capture_output=True, text=True)
                return res.returncode == 0, "Dừng SLAM thành công" if res.returncode == 0 else f"Lỗi: {res.stderr}"
                
        elif service == 'nav2':
            if action == 'start':
                res_loc = subprocess.run(["snapctl", "start", "ros2-nav2.localization"], capture_output=True, text=True)
                res_nav = subprocess.run(["snapctl", "start", "ros2-nav2.navigation"], capture_output=True, text=True)
                success = (res_loc.returncode == 0 and res_nav.returncode == 0)
                return success, "Bật dẫn đường Nav2 thành công" if success else f"Lỗi: Loc({res_loc.returncode}), Nav({res_nav.returncode})"
            elif action == 'stop':
                res_nav = subprocess.run(["snapctl", "stop", "ros2-nav2.navigation"], capture_output=True, text=True)
                res_loc = subprocess.run(["snapctl", "stop", "ros2-nav2.localization"], capture_output=True, text=True)
                success = (res_loc.returncode == 0 and res_nav.returncode == 0)
                return success, "Dừng dẫn đường Nav2 thành công" if success else "Lỗi khi dừng các dịch vụ"
            elif action == 'restart':
                res_loc = subprocess.run(["snapctl", "restart", "ros2-nav2.localization"], capture_output=True, text=True)
                res_nav = subprocess.run(["snapctl", "restart", "ros2-nav2.navigation"], capture_output=True, text=True)
                success = (res_loc.returncode == 0 and res_nav.returncode == 0)
                return success, "Khởi động lại Nav2 thành công" if success else "Lỗi khi khởi động lại các dịch vụ"
                
        return False, "Yêu cầu không hợp lệ"

def main():
    # Khởi động thread lắng nghe vị trí Robot
    t = threading.Thread(target=pose_listener_thread, daemon=True)
    t.start()

    snap_data = os.environ.get('SNAP_DATA', '/tmp')
    socket_dir = os.path.join(snap_data, 'package-run', 'ros2-nav2')
    os.makedirs(socket_dir, exist_ok=True)
    socket_path = os.path.join(socket_dir, 'web.sock')
    
    print(f"Khởi động Web Server tại socket: {socket_path}")
    
    server = UnixHTTPServer(socket_path, DashboardRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Đang dừng Web Server...")
    finally:
        if os.path.exists(socket_path):
            os.remove(socket_path)

if __name__ == '__main__':
    main()
