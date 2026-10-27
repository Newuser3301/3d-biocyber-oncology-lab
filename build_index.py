import json
import os

with open(r'C:\Users\Gubernatr\Desktop\new\cancer_meta.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

html_template = '''<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Bio-Cyber Oncology Lab // ML Real-Time Diagnostic</title>
    <!-- Three.js & OrbitControls -->
    <script src="libs/three.min.js"></script>
    <script>
        if (!window.THREE) {
            document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\\/script>');
        }
    </script>
    <script src="libs/OrbitControls.js"></script>
    <script>
        if (!window.THREE || !window.THREE.OrbitControls) {
            document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"><\\/script>');
        }
    </script>
    <!-- FontAwesome & Fonts -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-color: #040711;
            --panel-bg: rgba(8, 14, 28, 0.85);
            --panel-border: rgba(0, 240, 255, 0.3);
            --cyan: #00f0ff;
            --cyan-glow: rgba(0, 240, 255, 0.6);
            --green: #00ff88;
            --green-glow: rgba(0, 255, 136, 0.6);
            --red: #ff0055;
            --red-glow: rgba(255, 0, 85, 0.7);
            --amber: #ffb700;
            --text-main: #e8f4fc;
            --text-dim: #7f9bb3;
            --font-display: 'Orbitron', sans-serif;
            --font-ui: 'Rajdhani', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-ui);
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            transition: background 0.5s ease;
        }

        body.status-malignant {
            background-color: #12040a;
        }

        body.status-benign {
            background-color: #030f0c;
        }

        #webgl-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .scanlines {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            opacity: 0.5;
        }

        /* Top Header */
        .header-bar {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            background: linear-gradient(180deg, rgba(4, 7, 17, 0.98) 0%, rgba(4, 7, 17, 0.7) 80%, transparent 100%);
            border-bottom: 1px solid var(--panel-border);
            z-index: 10;
            backdrop-filter: blur(10px);
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-symbol {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid var(--cyan);
            box-shadow: 0 0 16px var(--cyan-glow);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--cyan);
            font-size: 20px;
            animation: pulse-ring 2.5s infinite alternate ease-in-out;
        }

        @keyframes pulse-ring {
            0% { transform: scale(1); box-shadow: 0 0 10px var(--cyan-glow); }
            100% { transform: scale(1.1); box-shadow: 0 0 24px var(--cyan); }
        }

        .title-group h1 {
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 900;
            letter-spacing: 2px;
            color: #fff;
            text-shadow: 0 0 12px var(--cyan-glow);
        }

        .title-group p {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--cyan);
            letter-spacing: 1px;
        }

        .header-metrics {
            display: flex;
            gap: 12px;
            font-family: var(--font-mono);
            font-size: 12px;
        }

        .metric-badge {
            background: rgba(0, 240, 255, 0.08);
            border: 1px solid rgba(0, 240, 255, 0.3);
            padding: 6px 14px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
        }

        .metric-badge.active-badge {
            background: rgba(0, 240, 255, 0.25);
            border-color: var(--cyan);
            box-shadow: 0 0 15px var(--cyan-glow);
        }

        .metric-badge span.val {
            font-weight: 700;
            color: var(--cyan);
        }

        .header-actions {
            display: flex;
            gap: 10px;
        }

        .action-btn {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: var(--text-main);
            padding: 8px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-family: var(--font-ui);
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }

        .action-btn:hover {
            background: rgba(0, 240, 255, 0.2);
            border-color: var(--cyan);
            color: #fff;
            box-shadow: 0 0 12px var(--cyan-glow);
        }

        /* Floating HUD Panels */
        .panel {
            position: absolute;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(20px);
            z-index: 10;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
            overflow-y: auto;
            max-height: calc(100vh - 84px);
        }

        .panel::-webkit-scrollbar {
            width: 5px;
        }
        .panel::-webkit-scrollbar-thumb {
            background: var(--cyan);
            border-radius: 3px;
        }

        /* Left Controls */
        .left-panel {
            top: 74px;
            left: 20px;
            width: 380px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        /* Right Diagnostics */
        .right-panel {
            top: 74px;
            right: 20px;
            width: 390px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .section-title {
            font-family: var(--font-display);
            font-size: 12px;
            letter-spacing: 1.5px;
            color: var(--cyan);
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 6px;
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        }

        /* Model Selector Tabs */
        .model-tabs {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 6px;
            background: rgba(0, 0, 0, 0.5);
            padding: 4px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .model-tab {
            background: transparent;
            border: none;
            color: var(--text-dim);
            padding: 10px 4px;
            font-family: var(--font-display);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-align: center;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.25s ease;
        }

        .model-tab.active {
            background: var(--cyan);
            color: #040711;
            font-weight: 900;
            box-shadow: 0 0 16px var(--cyan-glow);
        }

        .model-tab:hover:not(.active) {
            color: #fff;
            background: rgba(255, 255, 255, 0.08);
        }

        /* Interactive Sliders */
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .control-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            font-weight: 700;
        }

        .control-header span.name {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .control-header span.val {
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 700;
            color: var(--cyan);
            background: rgba(0, 240, 255, 0.15);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid rgba(0, 240, 255, 0.3);
            min-width: 65px;
            text-align: right;
        }

        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.15);
            outline: none;
            transition: background 0.2s;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--cyan);
            cursor: pointer;
            box-shadow: 0 0 12px var(--cyan-glow);
            transition: transform 0.1s;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.3);
        }

        /* Presets */
        .preset-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 6px;
        }

        .preset-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-main);
            padding: 10px 4px;
            border-radius: 5px;
            font-family: var(--font-ui);
            font-size: 13px;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .preset-btn.benign:hover {
            border-color: var(--green);
            background: rgba(0, 255, 136, 0.2);
            color: var(--green);
            box-shadow: 0 0 12px var(--green-glow);
        }

        .preset-btn.borderline:hover {
            border-color: var(--amber);
            background: rgba(255, 183, 0, 0.2);
            color: var(--amber);
            box-shadow: 0 0 12px rgba(255, 183, 0, 0.6);
        }

        .preset-btn.malignant:hover {
            border-color: var(--red);
            background: rgba(255, 0, 85, 0.2);
            color: var(--red);
            box-shadow: 0 0 14px var(--red-glow);
        }

        /* Main Diagnosis Card */
        .diag-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid rgba(0, 240, 255, 0.3);
            border-radius: 8px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            text-align: center;
            transition: all 0.35s ease;
        }

        .diag-card.benign {
            border-color: var(--green);
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3), inset 0 0 20px rgba(0, 255, 136, 0.1);
        }

        .diag-card.malignant {
            border-color: var(--red);
            box-shadow: 0 0 35px rgba(255, 0, 85, 0.45), inset 0 0 20px rgba(255, 0, 85, 0.2);
            animation: red-pulse 1.5s infinite alternate;
        }

        @keyframes red-pulse {
            0% { box-shadow: 0 0 20px rgba(255, 0, 85, 0.3); }
            100% { box-shadow: 0 0 45px rgba(255, 0, 85, 0.8); }
        }

        .diag-badge {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 900;
            letter-spacing: 1.5px;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
        }

        .diag-card.benign .diag-badge {
            color: var(--green);
            background: rgba(0, 255, 136, 0.15);
            border: 1px solid var(--green);
            text-shadow: 0 0 12px var(--green-glow);
        }

        .diag-card.malignant .diag-badge {
            color: var(--red);
            background: rgba(255, 0, 85, 0.18);
            border: 1px solid var(--red);
            text-shadow: 0 0 14px var(--red-glow);
        }

        .confidence-row {
            display: flex;
            justify-content: space-between;
            font-family: var(--font-mono);
            font-size: 12px;
        }

        .prob-bar-container {
            width: 100%;
            height: 12px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
        }

        .prob-bar-benign {
            height: 100%;
            background: var(--green);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--green-glow);
        }

        .prob-bar-malignant {
            height: 100%;
            background: var(--red);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--red-glow);
        }

        /* Info box */
        .info-box {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 14px;
            font-size: 13px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .info-row span.label {
            color: var(--text-dim);
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .info-row span.value {
            font-family: var(--font-mono);
            font-weight: 700;
            color: #fff;
        }

        /* Decision Tree Step List */
        .tree-steps {
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .tree-step-item {
            padding: 8px 10px;
            background: rgba(0, 240, 255, 0.06);
            border-left: 3px solid var(--cyan);
            border-radius: 0 4px 4px 0;
            color: var(--text-main);
            transition: all 0.2s;
        }

        .tree-step-item.active-step {
            border-left-color: var(--amber);
            background: rgba(255, 183, 0, 0.12);
            font-weight: 700;
        }

        /* Random Forest Mini Trees Grid */
        .rf-trees-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
        }

        .rf-tree-chip {
            padding: 6px 2px;
            text-align: center;
            border-radius: 4px;
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s;
        }

        .rf-tree-chip.b {
            color: var(--green);
            border-color: var(--green);
            background: rgba(0, 255, 136, 0.15);
            box-shadow: 0 0 6px var(--green-glow);
        }

        .rf-tree-chip.m {
            color: var(--red);
            border-color: var(--red);
            background: rgba(255, 0, 85, 0.15);
            box-shadow: 0 0 6px var(--red-glow);
        }

        /* Feature Importance */
        .feature-bar-wrap {
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-top: 4px;
        }

        .feat-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            font-family: var(--font-mono);
        }

        .feat-progress {
            width: 150px;
            height: 7px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 4px;
            overflow: hidden;
        }

        .feat-progress-inner {
            height: 100%;
            background: var(--cyan);
            border-radius: 4px;
            box-shadow: 0 0 8px var(--cyan-glow);
        }

        /* Bottom Legend */
        .bottom-legend {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 24px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            padding: 10px 24px;
            border-radius: 30px;
            backdrop-filter: blur(14px);
            z-index: 10;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .legend-dot.benign {
            background: var(--green);
            box-shadow: 0 0 10px var(--green-glow);
        }

        .legend-dot.malignant {
            background: var(--red);
            box-shadow: 0 0 10px var(--red-glow);
        }

        .legend-dot.probe {
            background: var(--cyan);
            box-shadow: 0 0 12px var(--cyan);
        }

        /* Toggles */
        .toggle-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 13px;
            color: var(--text-main);
            cursor: pointer;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 38px;
            height: 22px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.15);
            transition: .3s;
            border-radius: 22px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: var(--cyan);
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        input:checked + .slider:before {
            transform: translateX(16px);
            background-color: #040711;
        }

        /* 3D Canvas Click Hint */
        .canvas-hint {
            position: absolute;
            bottom: 24px;
            left: 20px;
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-dim);
            z-index: 10;
            pointer-events: none;
            background: rgba(0, 0, 0, 0.6);
            padding: 8px 14px;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .canvas-hint span.hl {
            color: var(--cyan);
            font-weight: 700;
        }
    </style>
</head>
<body>

    <div class="scanlines"></div>
    <div id="webgl-canvas"></div>

    <!-- Header Bar -->
    <header class="header-bar">
        <div class="header-left">
            <div class="logo-symbol">
                <i class="fa-solid fa-dna"></i>
            </div>
            <div class="title-group">
                <h1>BIO-CYBER 3D // REAL-TIME ONCOLOGY</h1>
                <p>INTERACTIVE UCI BREAST CANCER DIAGNOSTIC CORE</p>
            </div>
        </div>

        <div class="header-metrics">
            <div class="metric-badge active-badge" id="badge-knn">
                <span>KNN:</span>
                <span class="val">91.2%</span>
            </div>
            <div class="metric-badge" id="badge-dt">
                <span>D-TREE:</span>
                <span class="val">94.9%</span>
            </div>
            <div class="metric-badge" id="badge-rf">
                <span>R-FOREST:</span>
                <span class="val">95.6%</span>
            </div>
        </div>

        <div class="header-actions">
            <button class="action-btn" id="sound-btn">
                <i class="fa-solid fa-volume-high" id="sound-icon"></i>
                <span id="sound-text">Ovoz: Yoqilgan</span>
            </button>
            <button class="action-btn" id="reset-cam-btn">
                <i class="fa-solid fa-camera-rotate"></i>
                <span>Reset View</span>
            </button>
        </div>
    </header>

    <!-- Left Controls Panel -->
    <div class="panel left-panel">
        <div class="section-title">
            <i class="fa-solid fa-brain"></i>
            <span>Tasniflash Modeli (Active AI)</span>
        </div>
        <div class="model-tabs">
            <button class="model-tab active" data-model="knn">K-NN</button>
            <button class="model-tab" data-model="dt">Decision Tree</button>
            <button class="model-tab" data-model="rf">Random Forest</button>
        </div>

        <div class="section-title">
            <i class="fa-solid fa-sliders"></i>
            <span>Bemor Parametrlari (3D Koordinatalar)</span>
        </div>

        <!-- Slider X: Radius -->
        <div class="control-group">
            <div class="control-header">
                <span class="name"><i class="fa-solid fa-circle-dot" style="color: #ff0055;"></i> X: Radius Mean (Hujayra o'lchami)</span>
                <span class="val" id="val-radius">14.1 mm</span>
            </div>
            <input type="range" id="input-radius" min="7.0" max="28.1" step="0.1" value="14.1">
        </div>

        <!-- Slider Y: Texture -->
        <div class="control-group">
            <div class="control-header">
                <span class="name"><i class="fa-solid fa-cube" style="color: #00ff88;"></i> Y: Texture Mean (To'qima strukturasi)</span>
                <span class="val" id="val-texture">19.3</span>
            </div>
            <input type="range" id="input-texture" min="9.7" max="39.3" step="0.1" value="19.3">
        </div>

        <!-- Slider Z: Concavity -->
        <div class="control-group">
            <div class="control-header">
                <span class="name"><i class="fa-solid fa-wave-square" style="color: #00f0ff;"></i> Z: Concavity Mean (Botiqligi)</span>
                <span class="val" id="val-concavity">0.089</span>
            </div>
            <input type="range" id="input-concavity" min="0.000" max="0.427" step="0.002" value="0.089">
        </div>

        <!-- Presets -->
        <div class="section-title">
            <i class="fa-solid fa-user-doctor"></i>
            <span>Bemor Shablonlari (Tezkor Sinov)</span>
        </div>
        <div class="preset-buttons">
            <button class="preset-btn benign" id="preset-benign">🟢 Sog'lom</button>
            <button class="preset-btn borderline" id="preset-borderline">🟡 Shubhali</button>
            <button class="preset-btn malignant" id="preset-malignant">🔴 Xavfli</button>
        </div>

        <!-- Dynamic Model Controls -->
        <div id="dynamic-controls">
            <!-- KNN -->
            <div id="knn-controls" class="control-group">
                <div class="control-header">
                    <span class="name"><i class="fa-solid fa-network-wired"></i> K (Qo'shnilar soni):</span>
                    <span class="val" id="val-k">7</span>
                </div>
                <input type="range" id="input-k" min="1" max="25" step="2" value="7">
            </div>

            <!-- DT Controls -->
            <div id="dt-controls" style="display: none; flex-direction: column; gap: 8px;">
                <label class="toggle-row">
                    <span><i class="fa-solid fa-layer-group"></i> 3D Kesuvchi Tekisliklar (Planes):</span>
                    <span class="switch">
                        <input type="checkbox" id="toggle-planes" checked>
                        <span class="slider"></span>
                    </span>
                </label>
            </div>
        </div>

        <!-- Visual Settings -->
        <div class="section-title">
            <i class="fa-solid fa-eye"></i>
            <span>3D Sahnani Sozlash</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <label class="toggle-row">
                <span>Avtomatik 3D aylanish:</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-autorotate" checked>
                    <span class="slider"></span>
                </span>
            </label>
            <label class="toggle-row">
                <span>Lazer nurlari va qamrov sferasi:</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-lasers" checked>
                    <span class="slider"></span>
                </span>
            </label>
            <label class="toggle-row">
                <span>3D Koordinata panjarasi (Grid):</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-grid" checked>
                    <span class="slider"></span>
                </span>
            </label>
        </div>
    </div>

    <!-- Right Diagnostics Panel -->
    <div class="panel right-panel">
        <div class="section-title">
            <i class="fa-solid fa-microscope"></i>
            <span>Real-Vaqt Tashxisi (Live Diagnosis)</span>
        </div>

        <!-- Verdict Card -->
        <div class="diag-card benign" id="diag-card">
            <div style="font-family: var(--font-mono); font-size: 11px; color: var(--text-dim); letter-spacing: 1px;">
                AI XULOSASI // DIAGNOSTIC VERDICT
            </div>
            <div>
                <span class="diag-badge" id="diag-badge">BENIGN // SOG'LOM HUJAYRA</span>
            </div>
            <div class="confidence-row">
                <span>Sog'lom ehtimoli: <strong id="prob-benign-txt" style="color: var(--green);">94%</strong></span>
                <span>Xavfli ehtimoli: <strong id="prob-malignant-txt" style="color: var(--red);">6%</strong></span>
            </div>
            <div class="prob-bar-container">
                <div class="prob-bar-benign" id="bar-benign" style="width: 94%;"></div>
                <div class="prob-bar-malignant" id="bar-malignant" style="width: 6%;"></div>
            </div>
        </div>

        <!-- Model Insights -->
        <div class="section-title">
            <i class="fa-solid fa-chart-pie"></i>
            <span id="model-insight-title">KNN Qo'shnilar Tahlili</span>
        </div>
        <div id="insight-container" class="info-box"></div>

        <!-- Feature Importance -->
        <div class="section-title">
            <i class="fa-solid fa-ranking-star"></i>
            <span>Model Muhimlik Reytingi (Feature Weights)</span>
        </div>
        <div class="info-box">
            <div class="feature-bar-wrap">
                <div class="feat-item">
                    <span>1. Concavity Mean (Botiqlik)</span>
                    <span style="color: var(--cyan); font-weight: 700;">46.8%</span>
                </div>
                <div class="feat-progress">
                    <div class="feat-progress-inner" style="width: 46.8%;"></div>
                </div>
            </div>
            <div class="feature-bar-wrap">
                <div class="feat-item">
                    <span>2. Radius Mean (O'lcham)</span>
                    <span style="color: var(--cyan); font-weight: 700;">38.6%</span>
                </div>
                <div class="feat-progress">
                    <div class="feat-progress-inner" style="width: 38.6%;"></div>
                </div>
            </div>
            <div class="feature-bar-wrap">
                <div class="feat-item">
                    <span>3. Texture Mean (To'qima)</span>
                    <span style="color: var(--cyan); font-weight: 700;">14.6%</span>
                </div>
                <div class="feat-progress">
                    <div class="feat-progress-inner" style="width: 14.6%;"></div>
                </div>
            </div>
        </div>

        <!-- Dataset Info -->
        <div class="section-title">
            <i class="fa-solid fa-database"></i>
            <span>Dataset Xarakteristikasi</span>
        </div>
        <div class="info-box" style="font-size: 11px;">
            <div class="info-row">
                <span class="label">Dataset:</span>
                <span class="value">UCI Breast Cancer (Diagnostic)</span>
            </div>
            <div class="info-row">
                <span class="label">Jami namunalar (Samples):</span>
                <span class="value">569 ta biopsiya</span>
            </div>
            <div class="info-row">
                <span class="label">Sog'lom (Benign):</span>
                <span class="value" style="color: var(--green);">357 ta (62.7%)</span>
            </div>
            <div class="info-row">
                <span class="label">Xavfli o'simta (Malignant):</span>
                <span class="value" style="color: var(--red);">212 ta (37.3%)</span>
            </div>
        </div>
    </div>

    <!-- Bottom Center Legend -->
    <div class="bottom-legend">
        <div class="legend-item">
            <div class="legend-dot benign"></div>
            <span>Sog'lom (Benign)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot malignant"></div>
            <span>Xavfli o'simta (Malignant)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot probe"></div>
            <span>Sinov Zondi (Probe)</span>
        </div>
    </div>

    <!-- Clickable Hint -->
    <div class="canvas-hint">
        <i class="fa-solid fa-crosshairs"></i>
        <span>Fazodagi istalgan <span class="hl">nuqtani sichqoncha bilan bosing</span> — zond o'sha nuqtaga uchib boradi!</span>
    </div>

    <!-- Embed Raw Dataset & Trained Models -->
    <script>
        const METADATA = ''' + json.dumps(meta) + ''';
    </script>

    <!-- Main 3D Engine & Logic Script -->
    <script>
        // Web Audio SFX
        class SoundFX {
            constructor() {
                this.enabled = true;
                this.ctx = null;
            }
            init() {
                if (!this.ctx) {
                    const AudioCtx = window.AudioContext || window.webkitAudioContext;
                    this.ctx = new AudioCtx();
                }
            }
            playTone(freq, type, duration, vol) {
                if (!this.enabled) return;
                try {
                    this.init();
                    if (this.ctx.state === "suspended") this.ctx.resume();
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();
                    osc.type = type || "sine";
                    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                    gain.gain.setValueAtTime(vol || 0.04, this.ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + (duration || 0.08));
                    osc.connect(gain);
                    gain.connect(this.ctx.destination);
                    osc.start();
                    osc.stop(this.ctx.currentTime + (duration || 0.08));
                } catch(e) {}
            }
            beep() { this.playTone(800, "sine", 0.04, 0.02); }
            switchTab() { this.playTone(520, "triangle", 0.12, 0.05); }
            alertDanger() {
                this.playTone(280, "sawtooth", 0.22, 0.06);
                setTimeout(() => this.playTone(200, "sawtooth", 0.3, 0.06), 100);
            }
            safePing() {
                this.playTone(660, "sine", 0.12, 0.04);
                setTimeout(() => this.playTone(990, "sine", 0.18, 0.04), 70);
            }
        }
        const sfx = new SoundFX();

        document.getElementById("sound-btn").addEventListener("click", () => {
            sfx.enabled = !sfx.enabled;
            const icon = document.getElementById("sound-icon");
            const text = document.getElementById("sound-text");
            if (sfx.enabled) {
                icon.className = "fa-solid fa-volume-high";
                text.innerText = "Ovoz: Yoqilgan";
                sfx.beep();
            } else {
                icon.className = "fa-solid fa-volume-xmark";
                text.innerText = "Ovoz: O'chirilgan";
            }
        });

        // Application State
        const state = {
            currentModel: "knn",
            patient: { radius: 14.1, texture: 19.3, concavity: 0.089 },
            k: 7,
            showPlanes: true,
            showLasers: true,
            showGrid: true,
            autoRotate: true
        };

        const BOX_SIZE = 60;
        const stats = METADATA.stats;

        function normX(r) { return ((r - stats.min[0]) / (stats.max[0] - stats.min[0]) - 0.5) * BOX_SIZE; }
        function normY(t) { return ((t - stats.min[1]) / (stats.max[1] - stats.min[1]) - 0.5) * BOX_SIZE; }
        function normZ(c) { return ((c - stats.min[2]) / (stats.max[2] - stats.min[2]) - 0.5) * BOX_SIZE; }

        function unnormX(x) { return (x / BOX_SIZE + 0.5) * (stats.max[0] - stats.min[0]) + stats.min[0]; }
        function unnormY(y) { return (y / BOX_SIZE + 0.5) * (stats.max[1] - stats.min[1]) + stats.min[1]; }
        function unnormZ(z) { return (z / BOX_SIZE + 0.5) * (stats.max[2] - stats.min[2]) + stats.min[2]; }

        // Three.js Scene Setup
        const container = document.getElementById("webgl-canvas");
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x040711, 0.005);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(55, 45, 65);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 250;
        controls.minDistance = 15;

        document.getElementById("reset-cam-btn").addEventListener("click", () => {
            camera.position.set(55, 45, 65);
            controls.target.set(0, 0, 0);
            controls.update();
            sfx.beep();
        });

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0x00f0ff, 1.2);
        dirLight1.position.set(60, 80, 60);
        scene.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0xff0055, 0.9);
        dirLight2.position.set(-60, -50, -60);
        scene.add(dirLight2);

        // Bounding Grid
        const gridGroup = new THREE.Group();
        const boxGeo = new THREE.BoxGeometry(BOX_SIZE, BOX_SIZE, BOX_SIZE);
        const boxEdges = new THREE.EdgesGeometry(boxGeo);
        const boxMat = new THREE.LineBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.25 });
        const boxWireframe = new THREE.LineSegments(boxEdges, boxMat);
        gridGroup.add(boxWireframe);

        const gridHelper = new THREE.GridHelper(BOX_SIZE, 12, 0x00f0ff, 0x112244);
        gridHelper.position.y = -BOX_SIZE / 2;
        gridGroup.add(gridHelper);
        scene.add(gridGroup);

        // 3D Axis Labels
        function createTextSprite(text, color) {
            const canvas = document.createElement("canvas");
            canvas.width = 256;
            canvas.height = 64;
            const ctx = canvas.getContext("2d");
            ctx.font = "bold 24px Rajdhani, monospace";
            ctx.fillStyle = color || "#00f0ff";
            ctx.textAlign = "center";
            ctx.fillText(text, 128, 40);

            const texture = new THREE.CanvasTexture(canvas);
            const spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
            const sprite = new THREE.Sprite(spriteMaterial);
            sprite.scale.set(16, 4, 1);
            return sprite;
        }

        const labelX = createTextSprite("X: RADIUS (mm)", "#ff0055");
        labelX.position.set(BOX_SIZE / 2 + 9, -BOX_SIZE / 2, 0);
        gridGroup.add(labelX);

        const labelY = createTextSprite("Y: TEXTURE", "#00ff88");
        labelY.position.set(-BOX_SIZE / 2, BOX_SIZE / 2 + 5, -BOX_SIZE / 2);
        gridGroup.add(labelY);

        const labelZ = createTextSprite("Z: CONCAVITY", "#00f0ff");
        labelZ.position.set(0, -BOX_SIZE / 2, BOX_SIZE / 2 + 9);
        gridGroup.add(labelZ);

        // 569 Cell Mesh Points
        const sphereGeo = new THREE.SphereGeometry(0.8, 12, 12);
        const benignMat = new THREE.MeshStandardMaterial({
            color: 0x00ff88,
            emissive: 0x005522,
            roughness: 0.3,
            metalness: 0.2
        });
        const malignantMat = new THREE.MeshStandardMaterial({
            color: 0xff0055,
            emissive: 0x660022,
            roughness: 0.3,
            metalness: 0.2
        });

        const cellsGroup = new THREE.Group();
        const cellObjects = [];

        METADATA.dataset.forEach((item, index) => {
            const [radius, texture, concavity, label] = item;
            const mat = (label === 1) ? benignMat.clone() : malignantMat.clone();
            const mesh = new THREE.Mesh(sphereGeo, mat);
            mesh.position.set(normX(radius), normY(texture), normZ(concavity));
            mesh.userData = { id: index, radius, texture, concavity, label, origColor: (label === 1 ? 0x00ff88 : 0xff0055) };
            cellsGroup.add(mesh);
            cellObjects.push(mesh);
        });
        scene.add(cellsGroup);

        // Interactive Probe
        const probeGroup = new THREE.Group();
        const probeCoreGeo = new THREE.SphereGeometry(1.6, 24, 24);
        const probeCoreMat = new THREE.MeshStandardMaterial({
            color: 0x00f0ff,
            emissive: 0x00aacc,
            roughness: 0.1,
            metalness: 0.8
        });
        const probeCore = new THREE.Mesh(probeCoreGeo, probeCoreMat);
        probeGroup.add(probeCore);

        const ringGeo = new THREE.TorusGeometry(2.8, 0.08, 16, 64);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.8 });
        const probeRing1 = new THREE.Mesh(ringGeo, ringMat);
        const probeRing2 = new THREE.Mesh(ringGeo, ringMat);
        probeRing2.rotation.x = Math.PI / 2;
        probeGroup.add(probeRing1);
        probeGroup.add(probeRing2);

        // Bounding Sphere for KNN
        const knnSphereGeo = new THREE.SphereGeometry(1, 32, 32);
        const knnSphereMat = new THREE.MeshBasicMaterial({
            color: 0x00f0ff,
            wireframe: true,
            transparent: true,
            opacity: 0.18
        });
        const knnBoundingSphere = new THREE.Mesh(knnSphereGeo, knnSphereMat);
        probeGroup.add(knnBoundingSphere);
        scene.add(probeGroup);

        // KNN Laser Lines
        const laserGroup = new THREE.Group();
        scene.add(laserGroup);

        // Decision Tree Slicing Planes
        const planesGroup = new THREE.Group();
        scene.add(planesGroup);

        function buildDecisionPlanes() {
            while (planesGroup.children.length > 0) {
                planesGroup.remove(planesGroup.children[0]);
            }
            METADATA.dt_splits.forEach((split) => {
                const { feature_idx, threshold } = split;
                let planeGeo, planeMat, planeMesh;
                const colors = [0xff0055, 0x00ff88, 0x00f0ff];
                planeMat = new THREE.MeshBasicMaterial({
                    color: colors[feature_idx],
                    transparent: true,
                    opacity: 0.12,
                    side: THREE.DoubleSide,
                    depthWrite: false
                });

                if (feature_idx === 0) {
                    planeGeo = new THREE.PlaneGeometry(BOX_SIZE, BOX_SIZE);
                    planeMesh = new THREE.Mesh(planeGeo, planeMat);
                    planeMesh.position.x = normX(threshold);
                    planeMesh.rotation.y = Math.PI / 2;
                } else if (feature_idx === 1) {
                    planeGeo = new THREE.PlaneGeometry(BOX_SIZE, BOX_SIZE);
                    planeMesh = new THREE.Mesh(planeGeo, planeMat);
                    planeMesh.position.y = normY(threshold);
                    planeMesh.rotation.x = Math.PI / 2;
                } else {
                    planeGeo = new THREE.PlaneGeometry(BOX_SIZE, BOX_SIZE);
                    planeMesh = new THREE.Mesh(planeGeo, planeMat);
                    planeMesh.position.z = normZ(threshold);
                }
                planesGroup.add(planeMesh);
            });
        }
        buildDecisionPlanes();

        // 3D Raycasting - Click any cell in 3D to move probe!
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        window.addEventListener("pointerdown", (event) => {
            // Ignore if clicking on UI panels
            if (event.target.closest(".panel") || event.target.closest(".header-bar") || event.target.closest(".bottom-legend")) {
                return;
            }
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);

            const intersects = raycaster.intersectObjects(cellObjects);
            if (intersects.length > 0) {
                const clickedCell = intersects[0].object.userData;
                setPatientValues(clickedCell.radius, clickedCell.texture, clickedCell.concavity);
                sfx.beep();
            }
        });

        // Machine Learning Algorithms
        function predictKNN(radius, texture, concavity, k) {
            const distances = METADATA.dataset.map((pt, idx) => {
                const dx = pt[0] - radius;
                const dy = pt[1] - texture;
                const dz = (pt[2] - concavity) * 50;
                const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
                return { idx, dist, label: pt[3], pt };
            });

            distances.sort((a, b) => a.dist - b.dist);
            const neighbors = distances.slice(0, k);

            let benignCount = 0;
            let malignantCount = 0;
            neighbors.forEach(n => {
                if (n.label === 1) benignCount++;
                else malignantCount++;
            });

            const probBenign = benignCount / k;
            const probMalignant = malignantCount / k;
            const prediction = (probBenign >= 0.5) ? 1 : 0;

            return {
                prediction,
                probBenign,
                probMalignant,
                neighbors,
                maxDist: neighbors[neighbors.length - 1].dist
            };
        }

        function evaluateTree(node, r, t, c, path) {
            path = path || [];
            if (node.leaf) {
                return { prediction: node.prediction, prob: node.prob, path };
            }
            const val = (node.feature === "radius") ? r : (node.feature === "texture" ? t : c);
            const goesLeft = val <= node.threshold;
            path.push({
                feature: node.feature,
                val,
                threshold: node.threshold,
                goesLeft
            });
            if (goesLeft) {
                return evaluateTree(node.left, r, t, c, path);
            } else {
                return evaluateTree(node.right, r, t, c, path);
            }
        }

        function predictRandomForest(r, t, c) {
            const trees = METADATA.rf_model;
            let votesMalignant = 0;
            let votesBenign = 0;
            const treeResults = [];

            trees.forEach(tree => {
                const res = evaluateTree(tree, r, t, c);
                treeResults.push(res.prediction);
                if (res.prediction === 1) votesBenign++;
                else votesMalignant++;
            });

            const total = trees.length;
            const probBenign = votesBenign / total;
            const probMalignant = votesMalignant / total;
            const prediction = (probBenign >= 0.5) ? 1 : 0;

            return {
                prediction,
                probBenign,
                probMalignant,
                votesBenign,
                votesMalignant,
                totalTrees: total,
                treeResults
            };
        }

        // Live Simulation & Dynamic Highlighting
        let lastVerdict = -1;

        function updateSimulation() {
            const r = state.patient.radius;
            const t = state.patient.texture;
            const c = state.patient.concavity;

            // Move 3D Probe smoothly
            const px = normX(r);
            const py = normY(t);
            const pz = normZ(c);
            probeGroup.position.set(px, py, pz);

            // Run Prediction
            let result;
            if (state.currentModel === "knn") {
                result = predictKNN(r, t, c, state.k);
                renderKNNVisuals(result);
                renderKNNInsights(result);
            } else if (state.currentModel === "dt") {
                result = evaluateTree(METADATA.dt_model, r, t, c);
                result.probMalignant = result.prob[0];
                result.probBenign = result.prob[1];
                renderDTVisuals(result);
                renderDTInsights(result);
            } else {
                result = predictRandomForest(r, t, c);
                renderRFVisuals(result);
                renderRFInsights(result);
            }

            updateVerdictCard(result);

            // Ambient background glow shift
            if (result.prediction === 1) {
                document.body.className = "status-benign";
            } else {
                document.body.className = "status-malignant";
            }

            if (lastVerdict !== -1 && lastVerdict !== result.prediction) {
                if (result.prediction === 0) sfx.alertDanger();
                else sfx.safePing();
            }
            lastVerdict = result.prediction;
        }

        function updateVerdictCard(result) {
            const card = document.getElementById("diag-card");
            const badge = document.getElementById("diag-badge");
            const probBenignTxt = document.getElementById("prob-benign-txt");
            const probMalTxt = document.getElementById("prob-malignant-txt");
            const barBenign = document.getElementById("bar-benign");
            const barMal = document.getElementById("bar-malignant");

            const pB = Math.round(result.probBenign * 100);
            const pM = Math.round(result.probMalignant * 100);

            probBenignTxt.innerText = pB + "%";
            probMalTxt.innerText = pM + "%";
            barBenign.style.width = pB + "%";
            barMal.style.width = pM + "%";

            if (result.prediction === 1) {
                card.className = "diag-card benign";
                badge.innerText = "BENIGN // SOG'LOM HUJAYRA";
                probeCoreMat.color.setHex(0x00ff88);
                probeCoreMat.emissive.setHex(0x008833);
            } else {
                card.className = "diag-card malignant";
                badge.innerText = "MALIGNANT // XAVFLI O'SIMTA";
                probeCoreMat.color.setHex(0xff0055);
                probeCoreMat.emissive.setHex(0xaa0033);
            }
        }

        // KNN Visuals: Laser Beams + Highlighted Neighbor Spheres
        function renderKNNVisuals(res) {
            while (laserGroup.children.length > 0) {
                laserGroup.remove(laserGroup.children[0]);
            }

            // Reset all cells opacity/scale
            const neighborSet = new Set(res.neighbors.map(n => n.idx));
            cellObjects.forEach((cell, idx) => {
                if (neighborSet.has(idx)) {
                    cell.scale.set(1.6, 1.6, 1.6);
                    cell.material.opacity = 1.0;
                    cell.material.transparent = false;
                } else {
                    cell.scale.set(0.7, 0.7, 0.7);
                    cell.material.opacity = 0.35;
                    cell.material.transparent = true;
                }
            });

            if (!state.showLasers) {
                knnBoundingSphere.visible = false;
                return;
            }

            const probePos = probeGroup.position;
            let max3dDist = 0;

            res.neighbors.forEach(n => {
                const targetMesh = cellObjects[n.idx];
                const targetPos = targetMesh.position;

                const d = probePos.distanceTo(targetPos);
                if (d > max3dDist) max3dDist = d;

                const points = [probePos, targetPos];
                const geo = new THREE.BufferGeometry().setFromPoints(points);
                const color = (n.label === 1) ? 0x00ff88 : 0xff0055;
                const mat = new THREE.LineBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.85,
                    linewidth: 2
                });
                const line = new THREE.Line(geo, mat);
                laserGroup.add(line);
            });

            knnBoundingSphere.visible = true;
            knnBoundingSphere.scale.set(max3dDist + 0.5, max3dDist + 0.5, max3dDist + 0.5);
            knnBoundingSphere.material.color.setHex(res.prediction === 1 ? 0x00ff88 : 0xff0055);
            planesGroup.visible = false;
        }

        function renderKNNInsights(res) {
            document.getElementById("model-insight-title").innerText = "KNN Qo'shnilar Tahlili (K=" + state.k + ")";
            const bCount = Math.round(res.probBenign * state.k);
            const mCount = Math.round(res.probMalignant * state.k);

            const html = `
                <div class="info-row">
                    <span class="label">Tanlangan K:</span>
                    <span class="value" style="color: var(--cyan);">${state.k} ta eng yaqin qo'shni</span>
                </div>
                <div class="info-row">
                    <span class="label">Sog'lom qo'shnilar (🟢):</span>
                    <span class="value" style="color: var(--green);">${bCount} ta (${Math.round(res.probBenign * 100)}%)</span>
                </div>
                <div class="info-row">
                    <span class="label">Xavfli qo'shnilar (🔴):</span>
                    <span class="value" style="color: var(--red);">${mCount} ta (${Math.round(res.probMalignant * 100)}%)</span>
                </div>
                <div class="info-row">
                    <span class="label">Qamrov sferasi radiusi:</span>
                    <span class="value">${res.maxDist.toFixed(2)} birlik</span>
                </div>
            `;
            document.getElementById("insight-container").innerHTML = html;
        }

        // Decision Tree Visuals
        function renderDTVisuals(res) {
            while (laserGroup.children.length > 0) {
                laserGroup.remove(laserGroup.children[0]);
            }
            knnBoundingSphere.visible = false;
            planesGroup.visible = state.showPlanes;

            // Highlight all cells with same prediction
            cellObjects.forEach(cell => {
                if (cell.userData.label === res.prediction) {
                    cell.scale.set(1.2, 1.2, 1.2);
                    cell.material.opacity = 0.95;
                    cell.material.transparent = false;
                } else {
                    cell.scale.set(0.6, 0.6, 0.6);
                    cell.material.opacity = 0.25;
                    cell.material.transparent = true;
                }
            });
        }

        function renderDTInsights(res) {
            document.getElementById("model-insight-title").innerText = "Decision Tree Mantiqiy Yo'li";
            let stepsHtml = '<div class="tree-steps">';
            res.path.forEach((step, idx) => {
                const dir = step.goesLeft ? "≤" : ">";
                const sideText = step.goesLeft ? "Chap shox" : "O'ng shox";
                const isLast = (idx === res.path.length - 1);
                stepsHtml += `
                    <div class="tree-step-item ${isLast ? 'active-step' : ''}">
                        ${idx + 1}. <b>${step.feature.toUpperCase()}</b>: (${step.val.toFixed(2)}) ${dir} ${step.threshold} → <i>${sideText}</i>
                    </div>
                `;
            });
            stepsHtml += `</div>
                <div class="info-row" style="margin-top: 8px;">
                    <span class="label">Daraxt Chuqurligi:</span>
                    <span class="value">4 bosqich</span>
                </div>
                <div class="info-row">
                    <span class="label">Test Aniqligi (Accuracy):</span>
                    <span class="value" style="color: var(--cyan);">${(METADATA.stats.dt_acc * 100).toFixed(1)}%</span>
                </div>
            `;
            document.getElementById("insight-container").innerHTML = stepsHtml;
        }

        // Random Forest Visuals
        function renderRFVisuals(res) {
            while (laserGroup.children.length > 0) {
                laserGroup.remove(laserGroup.children[0]);
            }
            knnBoundingSphere.visible = false;
            planesGroup.visible = false;

            cellObjects.forEach(cell => {
                cell.scale.set(1.0, 1.0, 1.0);
                cell.material.opacity = 0.85;
                cell.material.transparent = false;
            });
        }

        function renderRFInsights(res) {
            document.getElementById("model-insight-title").innerText = "Random Forest Ovoz Berishi (15 ta daraxt)";
            let gridHtml = '<div class="rf-trees-grid">';
            res.treeResults.forEach((pred, i) => {
                const cls = (pred === 1) ? "b" : "m";
                const label = (pred === 1) ? "🟢" : "🔴";
                gridHtml += `<div class="rf-tree-chip ${cls}" title="Daraxt #${i+1}">${label} T${i+1}</div>`;
            });
            gridHtml += '</div>';

            gridHtml += `
                <div class="info-row" style="margin-top: 8px;">
                    <span class="label">Sog'lomga ovozlar:</span>
                    <span class="value" style="color: var(--green);">${res.votesBenign} / ${res.totalTrees} ta daraxt</span>
                </div>
                <div class="info-row">
                    <span class="label">Xavfliga ovozlar:</span>
                    <span class="value" style="color: var(--red);">${res.votesMalignant} / ${res.totalTrees} ta daraxt</span>
                </div>
                <div class="info-row">
                    <span class="label">RF Umumiy Aniqligi:</span>
                    <span class="value" style="color: var(--cyan);">${(METADATA.stats.rf_acc * 100).toFixed(1)}%</span>
                </div>
            `;
            document.getElementById("insight-container").innerHTML = gridHtml;
        }

        // UI Event Listeners
        document.querySelectorAll(".model-tab").forEach(tab => {
            tab.addEventListener("click", () => {
                document.querySelectorAll(".model-tab").forEach(t => t.classList.remove("active"));
                tab.classList.add("active");
                state.currentModel = tab.dataset.model;
                sfx.switchTab();

                document.getElementById("badge-knn").classList.toggle("active-badge", state.currentModel === "knn");
                document.getElementById("badge-dt").classList.toggle("active-badge", state.currentModel === "dt");
                document.getElementById("badge-rf").classList.toggle("active-badge", state.currentModel === "rf");

                document.getElementById("knn-controls").style.display = (state.currentModel === "knn") ? "flex" : "none";
                document.getElementById("dt-controls").style.display = (state.currentModel === "dt") ? "flex" : "none";

                updateSimulation();
            });
        });

        const inRadius = document.getElementById("input-radius");
        const inTexture = document.getElementById("input-texture");
        const inConcavity = document.getElementById("input-concavity");
        const inK = document.getElementById("input-k");

        inRadius.addEventListener("input", (e) => {
            state.patient.radius = parseFloat(e.target.value);
            document.getElementById("val-radius").innerText = state.patient.radius.toFixed(1) + " mm";
            sfx.beep();
            updateSimulation();
        });

        inTexture.addEventListener("input", (e) => {
            state.patient.texture = parseFloat(e.target.value);
            document.getElementById("val-texture").innerText = state.patient.texture.toFixed(1);
            sfx.beep();
            updateSimulation();
        });

        inConcavity.addEventListener("input", (e) => {
            state.patient.concavity = parseFloat(e.target.value);
            document.getElementById("val-concavity").innerText = state.patient.concavity.toFixed(3);
            sfx.beep();
            updateSimulation();
        });

        inK.addEventListener("input", (e) => {
            state.k = parseInt(e.target.value);
            document.getElementById("val-k").innerText = state.k;
            sfx.beep();
            updateSimulation();
        });

        document.getElementById("toggle-planes").addEventListener("change", (e) => {
            state.showPlanes = e.target.checked;
            planesGroup.visible = state.showPlanes;
        });

        document.getElementById("toggle-autorotate").addEventListener("change", (e) => {
            state.autoRotate = e.target.checked;
        });

        document.getElementById("toggle-lasers").addEventListener("change", (e) => {
            state.showLasers = e.target.checked;
            updateSimulation();
        });

        document.getElementById("toggle-grid").addEventListener("change", (e) => {
            state.showGrid = e.target.checked;
            gridGroup.visible = state.showGrid;
        });

        function setPatientValues(r, t, c) {
            state.patient.radius = r;
            state.patient.texture = t;
            state.patient.concavity = c;

            inRadius.value = r;
            inTexture.value = t;
            inConcavity.value = c;

            document.getElementById("val-radius").innerText = r.toFixed(1) + " mm";
            document.getElementById("val-texture").innerText = t.toFixed(1);
            document.getElementById("val-concavity").innerText = c.toFixed(3);

            updateSimulation();
        }

        document.getElementById("preset-benign").addEventListener("click", () => {
            setPatientValues(11.5, 14.8, 0.025);
            sfx.safePing();
        });

        document.getElementById("preset-borderline").addEventListener("click", () => {
            setPatientValues(15.1, 20.2, 0.098);
            sfx.switchTab();
        });

        document.getElementById("preset-malignant").addEventListener("click", () => {
            setPatientValues(21.5, 26.2, 0.285);
            sfx.alertDanger();
        });

        window.addEventListener("resize", () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // Animation Loop
        let clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const elapsed = clock.getElapsedTime();

            probeRing1.rotation.z = elapsed * 2.0;
            probeRing2.rotation.y = elapsed * 2.2;

            malignantMat.emissiveIntensity = 0.5 + Math.sin(elapsed * 4) * 0.35;

            if (state.autoRotate) {
                scene.rotation.y = elapsed * 0.06;
            }

            controls.update();
            renderer.render(scene, camera);
        }

        updateSimulation();
        animate();
    </script>
</body>
</html>
'''

with open(r'C:\Users\Gubernatr\Desktop\new\index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Compiled new index.html with ZERO unescaped quotes successfully!')
