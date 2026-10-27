import json
import os

with open(r'C:\Users\Gubernatr\Desktop\new\cancer_meta.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

# Build the complete, state-of-the-art 3D application
html_code = """<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Bio-Cyber Oncology Lab // Dynamic AI Hyperparameter Lab</title>
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
    <!-- FontAwesome & Google Fonts -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --bg-color: #030611;
            --panel-bg: rgba(6, 12, 26, 0.88);
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
            transition: background 0.4s ease;
        }

        body.status-malignant { background-color: #14040b; }
        body.status-benign { background-color: #02120d; }

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
            background: linear-gradient(180deg, rgba(3, 6, 17, 0.98) 0%, rgba(3, 6, 17, 0.75) 80%, transparent 100%);
            border-bottom: 1px solid var(--panel-border);
            z-index: 10;
            backdrop-filter: blur(12px);
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
            font-size: 17px;
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
            box-shadow: 0 0 16px var(--cyan-glow);
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

        .panel::-webkit-scrollbar { width: 5px; }
        .panel::-webkit-scrollbar-thumb { background: var(--cyan); border-radius: 3px; }

        .left-panel {
            top: 74px;
            left: 20px;
            width: 390px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .right-panel {
            top: 74px;
            right: 20px;
            width: 390px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .section-title {
            font-family: var(--font-display);
            font-size: 11px;
            letter-spacing: 1.5px;
            color: var(--cyan);
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 5px;
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
            color: #030611;
            font-weight: 900;
            box-shadow: 0 0 16px var(--cyan-glow);
        }

        /* Retrain Parameters Box */
        .param-box {
            background: rgba(0, 240, 255, 0.04);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 6px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .param-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 700;
        }

        .param-header span.name {
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-main);
        }

        .param-header span.val {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--cyan);
            background: rgba(0, 240, 255, 0.12);
            padding: 2px 7px;
            border-radius: 3px;
            border: 1px solid rgba(0, 240, 255, 0.3);
        }

        .seed-row {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .seed-input {
            width: 80px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(0, 240, 255, 0.3);
            color: var(--cyan);
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 4px;
            text-align: center;
        }

        .btn-seed {
            flex: 1;
            background: rgba(0, 240, 255, 0.15);
            border: 1px solid var(--cyan);
            color: #fff;
            padding: 6px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-family: var(--font-ui);
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .btn-seed:hover {
            background: var(--cyan);
            color: #000;
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        /* Sliders */
        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 7px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.15);
            outline: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--cyan);
            cursor: pointer;
            box-shadow: 0 0 10px var(--cyan-glow);
            transition: transform 0.1s;
        }

        input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.3); }

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
            padding: 8px 4px;
            border-radius: 4px;
            font-family: var(--font-ui);
            font-size: 12px;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .preset-btn.benign:hover {
            border-color: var(--green);
            background: rgba(0, 255, 136, 0.2);
            color: var(--green);
            box-shadow: 0 0 10px var(--green-glow);
        }

        .preset-btn.borderline:hover {
            border-color: var(--amber);
            background: rgba(255, 183, 0, 0.2);
            color: var(--amber);
            box-shadow: 0 0 10px rgba(255, 183, 0, 0.6);
        }

        .preset-btn.malignant:hover {
            border-color: var(--red);
            background: rgba(255, 0, 85, 0.2);
            color: var(--red);
            box-shadow: 0 0 12px var(--red-glow);
        }

        /* Diagnosis Card */
        .diag-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid rgba(0, 240, 255, 0.3);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            text-align: center;
            transition: all 0.35s ease;
        }

        .diag-card.benign {
            border-color: var(--green);
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.3), inset 0 0 15px rgba(0, 255, 136, 0.1);
        }

        .diag-card.malignant {
            border-color: var(--red);
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.45), inset 0 0 15px rgba(255, 0, 85, 0.2);
            animation: red-pulse 1.5s infinite alternate;
        }

        @keyframes red-pulse {
            0% { box-shadow: 0 0 15px rgba(255, 0, 85, 0.3); }
            100% { box-shadow: 0 0 35px rgba(255, 0, 85, 0.8); }
        }

        .diag-badge {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 900;
            letter-spacing: 1.5px;
            padding: 7px 12px;
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
            height: 10px;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 5px;
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

        .info-box {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 12px;
            font-size: 13px;
            display: flex;
            flex-direction: column;
            gap: 7px;
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

        .tree-steps {
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .tree-step-item {
            padding: 6px 8px;
            background: rgba(0, 240, 255, 0.06);
            border-left: 3px solid var(--cyan);
            border-radius: 0 4px 4px 0;
            color: var(--text-main);
        }

        .tree-step-item.active-step {
            border-left-color: var(--amber);
            background: rgba(255, 183, 0, 0.15);
            font-weight: 700;
        }

        .rf-trees-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 5px;
            max-height: 120px;
            overflow-y: auto;
        }

        .rf-tree-chip {
            padding: 5px 2px;
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
        }

        .rf-tree-chip.m {
            color: var(--red);
            border-color: var(--red);
            background: rgba(255, 0, 85, 0.15);
        }

        /* View Mode Switcher */
        .view-mode-tabs {
            position: absolute;
            top: 74px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            padding: 6px 12px;
            border-radius: 30px;
            backdrop-filter: blur(14px);
            z-index: 10;
        }

        .view-btn {
            background: transparent;
            border: none;
            color: var(--text-dim);
            padding: 6px 14px;
            border-radius: 20px;
            font-family: var(--font-ui);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .view-btn.active {
            background: var(--cyan);
            color: #030611;
            box-shadow: 0 0 12px var(--cyan-glow);
        }

        /* Retrain notification pill */
        .retrain-pill {
            position: absolute;
            top: 124px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 240, 255, 0.25);
            border: 1px solid var(--cyan);
            color: #fff;
            padding: 6px 18px;
            border-radius: 20px;
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 20px var(--cyan-glow);
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            z-index: 20;
        }

        .retrain-pill.show { opacity: 1; }

        /* Bottom Legend */
        .bottom-legend {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            padding: 8px 22px;
            border-radius: 30px;
            backdrop-filter: blur(14px);
            z-index: 10;
            font-size: 12px;
            font-weight: 700;
        }

        .legend-item { display: flex; align-items: center; gap: 8px; }
        .legend-dot { width: 12px; height: 12px; border-radius: 50%; }
        .legend-dot.benign { background: var(--green); box-shadow: 0 0 10px var(--green-glow); }
        .legend-dot.malignant { background: var(--red); box-shadow: 0 0 10px var(--red-glow); }
        .legend-dot.probe { background: var(--cyan); box-shadow: 0 0 10px var(--cyan); }
        .legend-dot.test-sample { border: 2px solid #fff; background: transparent; }

        /* Toggles */
        .toggle-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-main);
            cursor: pointer;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 36px;
            height: 20px;
        }

        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: rgba(255, 255, 255, 0.15); transition: .3s; border-radius: 20px;
        }
        .slider:before {
            position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px;
            background-color: white; transition: .3s; border-radius: 50%;
        }
        input:checked + .slider { background-color: var(--cyan); box-shadow: 0 0 10px var(--cyan-glow); }
        input:checked + .slider:before { transform: translateX(16px); background-color: #030611; }

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
        .canvas-hint span.hl { color: var(--cyan); font-weight: 700; }
    </style>
</head>
<body>

    <div class="scanlines"></div>
    <div id="webgl-canvas"></div>

    <!-- Retrain Notification Pill -->
    <div class="retrain-pill" id="retrain-pill">
        <i class="fa-solid fa-arrows-rotate fa-spin"></i>
        <span>AI MODELLARI QAYTA O'QITILDI! (RETRAINED)</span>
    </div>

    <!-- 3D Scene Mode Switcher -->
    <div class="view-mode-tabs">
        <button class="view-btn active" data-view="data"><i class="fa-solid fa-cubes"></i> 3D Data Fazosi</button>
        <button class="view-btn" data-view="tree"><i class="fa-solid fa-sitemap"></i> 3D Hologram Daraxt</button>
        <button class="view-btn" data-view="forest"><i class="fa-solid fa-satellite"></i> 3D RF Konstellatsiya</button>
        <button class="view-btn" data-view="split"><i class="fa-solid fa-columns"></i> Ikkisi Birgalikda</button>
    </div>

    <!-- Top Header Bar -->
    <header class="header-bar">
        <div class="header-left">
            <div class="logo-symbol">
                <i class="fa-solid fa-dna"></i>
            </div>
            <div class="title-group">
                <h1>BIO-CYBER 3D // AI HYPERPARAMETER LAB</h1>
                <p>DYNAMIC RETRAINING & MULTI-MODEL 3D INFERENCE</p>
            </div>
        </div>

        <div class="header-metrics">
            <div class="metric-badge active-badge" id="badge-knn">
                <span>KNN:</span>
                <span class="val" id="metric-knn-acc">91.2%</span>
            </div>
            <div class="metric-badge" id="badge-dt">
                <span>D-TREE:</span>
                <span class="val" id="metric-dt-acc">94.9%</span>
            </div>
            <div class="metric-badge" id="badge-rf">
                <span>R-FOREST:</span>
                <span class="val" id="metric-rf-acc">95.6%</span>
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
        <!-- AI Model Tabs -->
        <div class="section-title">
            <i class="fa-solid fa-brain"></i>
            <span>Tasniflash Modeli (Active AI)</span>
        </div>
        <div class="model-tabs">
            <button class="model-tab active" data-model="knn">K-NN</button>
            <button class="model-tab" data-model="dt">Decision Tree</button>
            <button class="model-tab" data-model="rf">Random Forest</button>
        </div>

        <!-- Hyperparameters & Retraining Section -->
        <div class="section-title">
            <i class="fa-solid fa-gears"></i>
            <span>Modelni Qayta O'qitish (Hyperparameters)</span>
        </div>
        <div class="param-box">
            <!-- Train/Test Split -->
            <div>
                <div class="param-header">
                    <span class="name"><i class="fa-solid fa-chart-pie"></i> train_test_split (Test ulushi):</span>
                    <span class="val" id="val-test-size">20% (Test: 114)</span>
                </div>
                <input type="range" id="input-test-size" min="0.10" max="0.50" step="0.05" value="0.20">
            </div>

            <!-- Random State (Seed) -->
            <div>
                <div class="param-header">
                    <span class="name"><i class="fa-solid fa-dice"></i> random_state (Urug' / Seed):</span>
                    <span class="val" id="val-seed">42</span>
                </div>
                <div class="seed-row" style="margin-top: 5px;">
                    <input type="number" id="input-seed" class="seed-input" value="42" min="0" max="9999">
                    <button class="btn-seed" id="btn-random-seed"><i class="fa-solid fa-shuffle"></i> 🎲 Tasodifiy Seed</button>
                </div>
            </div>

            <!-- Max Depth for Trees -->
            <div>
                <div class="param-header">
                    <span class="name"><i class="fa-solid fa-sitemap"></i> max_depth (Daraxt chuqurligi):</span>
                    <span class="val" id="val-max-depth">4 bosqich</span>
                </div>
                <input type="range" id="input-max-depth" min="1" max="7" step="1" value="4">
            </div>

            <!-- N Estimators for RF -->
            <div id="param-nest-wrap">
                <div class="param-header">
                    <span class="name"><i class="fa-solid fa-tree"></i> n_estimators (RF daraxtlar soni):</span>
                    <span class="val" id="val-nest">15 ta daraxt</span>
                </div>
                <input type="range" id="input-nest" min="5" max="25" step="1" value="15">
            </div>
        </div>

        <!-- Patient Coordinates Sliders -->
        <div class="section-title">
            <i class="fa-solid fa-sliders"></i>
            <span>Bemor Ko'rsatkichlari (3D O'qlar)</span>
        </div>

        <div>
            <div class="param-header">
                <span class="name"><i class="fa-solid fa-circle-dot" style="color: #ff0055;"></i> X: Radius Mean (O'lcham)</span>
                <span class="val" id="val-radius">14.1 mm</span>
            </div>
            <input type="range" id="input-radius" min="7.0" max="28.1" step="0.1" value="14.1">
        </div>

        <div>
            <div class="param-header">
                <span class="name"><i class="fa-solid fa-cube" style="color: #00ff88;"></i> Y: Texture Mean (To'qima)</span>
                <span class="val" id="val-texture">19.3</span>
            </div>
            <input type="range" id="input-texture" min="9.7" max="39.3" step="0.1" value="19.3">
        </div>

        <div>
            <div class="param-header">
                <span class="name"><i class="fa-solid fa-wave-square" style="color: #00f0ff;"></i> Z: Concavity Mean (Botiqlik)</span>
                <span class="val" id="val-concavity">0.089</span>
            </div>
            <input type="range" id="input-concavity" min="0.000" max="0.427" step="0.002" value="0.089">
        </div>

        <!-- Presets -->
        <div class="section-title">
            <i class="fa-solid fa-user-doctor"></i>
            <span>Bemor Shablonlari</span>
        </div>
        <div class="preset-buttons">
            <button class="preset-btn benign" id="preset-benign">🟢 Sog'lom</button>
            <button class="preset-btn borderline" id="preset-borderline">🟡 Shubhali</button>
            <button class="preset-btn malignant" id="preset-malignant">🔴 Xavfli</button>
        </div>

        <!-- Visual Toggles -->
        <div class="section-title">
            <i class="fa-solid fa-eye"></i>
            <span>3D Ko'rinish Sozlamalari</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 7px;">
            <label class="toggle-row">
                <span>Avtomatik 3D aylanish:</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-autorotate" checked>
                    <span class="slider"></span>
                </span>
            </label>
            <label class="toggle-row">
                <span>Lazer nurlari & Aloqalar:</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-lasers" checked>
                    <span class="slider"></span>
                </span>
            </label>
            <label class="toggle-row">
                <span>3D Kesuvchi Tekisliklar (DT Planes):</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-planes" checked>
                    <span class="slider"></span>
                </span>
            </label>
            <label class="toggle-row">
                <span>Test nuqtalarini ajratib ko'rsatish:</span>
                <span class="switch">
                    <input type="checkbox" id="toggle-test-highlight" checked>
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

        <!-- Main Verdict Card -->
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

        <!-- Active Model Specific Diagnostic -->
        <div class="section-title">
            <i class="fa-solid fa-chart-pie"></i>
            <span id="model-insight-title">Model Tahlili</span>
        </div>
        <div id="insight-container" class="info-box"></div>

        <!-- Feature Importances -->
        <div class="section-title">
            <i class="fa-solid fa-ranking-star"></i>
            <span>Xususiyatlar Muhimlik Reytingi</span>
        </div>
        <div class="info-box">
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: var(--font-mono);">
                    <span>1. Concavity Mean (Botiqlik)</span>
                    <span id="txt-imp-c" style="color: var(--cyan); font-weight: 700;">46.8%</span>
                </div>
                <div style="height: 6px; background: rgba(255,255,255,0.12); border-radius: 3px; overflow: hidden;">
                    <div id="bar-imp-c" style="width: 46.8%; height: 100%; background: var(--cyan);"></div>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: var(--font-mono);">
                    <span>2. Radius Mean (O'lcham)</span>
                    <span id="txt-imp-r" style="color: var(--cyan); font-weight: 700;">38.6%</span>
                </div>
                <div style="height: 6px; background: rgba(255,255,255,0.12); border-radius: 3px; overflow: hidden;">
                    <div id="bar-imp-r" style="width: 38.6%; height: 100%; background: var(--cyan);"></div>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: var(--font-mono);">
                    <span>3. Texture Mean (To'qima)</span>
                    <span id="txt-imp-t" style="color: var(--cyan); font-weight: 700;">14.6%</span>
                </div>
                <div style="height: 6px; background: rgba(255,255,255,0.12); border-radius: 3px; overflow: hidden;">
                    <div id="bar-imp-t" style="width: 14.6%; height: 100%; background: var(--cyan);"></div>
                </div>
            </div>
        </div>

        <!-- Train/Test Split Info -->
        <div class="section-title">
            <i class="fa-solid fa-database"></i>
            <span>O'qitish va Test Taqsimoti</span>
        </div>
        <div class="info-box" style="font-size: 11px;">
            <div class="info-row">
                <span class="label">O'qitish to'plami (Train):</span>
                <span class="value" id="info-train-samples" style="color: var(--cyan);">455 ta (80%)</span>
            </div>
            <div class="info-row">
                <span class="label">Sinov to'plami (Test):</span>
                <span class="value" id="info-test-samples" style="color: var(--amber);">114 ta (20%)</span>
            </div>
            <div class="info-row">
                <span class="label">Aktiv Tasodifiy Urug' (Seed):</span>
                <span class="value" id="info-active-seed">42</span>
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
            <span>Xavfli (Malignant)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot probe"></div>
            <span>Sinov Zondi (Probe)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot test-sample"></div>
            <span>Test To'plami</span>
        </div>
    </div>

    <!-- Mouse Controls Hint -->
    <div class="canvas-hint">
        <i class="fa-solid fa-crosshairs"></i>
        <span>3D fazodagi nuqtani <span class="hl">sichqoncha bilan bosing</span> — zond o'sha yerga uchib boradi!</span>
    </div>

    <!-- Initial Metadata -->
    <script>
        let METADATA = """ + json.dumps(meta) + """;
    </script>

    <!-- Main Logic & 3D Interactive Script -->
    <script>
        // Web Audio Synthesizer
        class SoundFX {
            constructor() { this.enabled = true; this.ctx = null; }
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
            beep() { this.playTone(850, "sine", 0.04, 0.02); }
            switchTab() { this.playTone(520, "triangle", 0.12, 0.05); }
            retrainSweep() {
                this.playTone(400, "sawtooth", 0.1, 0.05);
                setTimeout(() => this.playTone(600, "sine", 0.1, 0.05), 60);
                setTimeout(() => this.playTone(900, "sine", 0.15, 0.06), 120);
            }
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
            viewMode: "data", // 'data' | 'tree' | 'forest' | 'split'
            patient: { radius: 14.1, texture: 19.3, concavity: 0.089 },
            hyperparams: {
                test_size: 0.20,
                random_state: 42,
                max_depth: 4,
                n_estimators: 15,
                k: 7
            },
            showPlanes: true,
            showLasers: true,
            showTestHighlight: true,
            autoRotate: true,
            testIndicesSet: new Set()
        };

        const BOX_SIZE = 55;
        const stats = METADATA.stats;

        function normX(r) { return ((r - stats.min[0]) / (stats.max[0] - stats.min[0]) - 0.5) * BOX_SIZE; }
        function normY(t) { return ((t - stats.min[1]) / (stats.max[1] - stats.min[1]) - 0.5) * BOX_SIZE; }
        function normZ(c) { return ((c - stats.min[2]) / (stats.max[2] - stats.min[2]) - 0.5) * BOX_SIZE; }

        // Three.js Scene Setup
        const container = document.getElementById("webgl-canvas");
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x030611, 0.004);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1500);
        camera.position.set(50, 40, 65);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 350;
        controls.minDistance = 15;

        document.getElementById("reset-cam-btn").addEventListener("click", () => {
            resetCamera();
            sfx.beep();
        });

        function resetCamera() {
            if (state.viewMode === "data") {
                camera.position.set(50, 40, 65);
                controls.target.set(0, 0, 0);
            } else if (state.viewMode === "tree") {
                camera.position.set(0, 15, 80);
                controls.target.set(0, 10, 0);
            } else if (state.viewMode === "forest") {
                camera.position.set(0, 45, 65);
                controls.target.set(0, 0, 0);
            } else { // split
                camera.position.set(30, 40, 100);
                controls.target.set(0, 0, 0);
            }
            controls.update();
        }

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0x00f0ff, 1.2);
        dirLight1.position.set(60, 80, 60);
        scene.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0xff0055, 0.9);
        dirLight2.position.set(-60, -50, -60);
        scene.add(dirLight2);

        // 3D Groups
        const dataGroup = new THREE.Group();
        scene.add(dataGroup);

        const treeGroup = new THREE.Group();
        treeGroup.position.set(0, 0, 0);
        scene.add(treeGroup);

        const forestGroup = new THREE.Group();
        scene.add(forestGroup);

        // 1. Data Bounding Box & Grid
        const boxGeo = new THREE.BoxGeometry(BOX_SIZE, BOX_SIZE, BOX_SIZE);
        const boxEdges = new THREE.EdgesGeometry(boxGeo);
        const boxMat = new THREE.LineBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.22 });
        const boxWireframe = new THREE.LineSegments(boxEdges, boxMat);
        dataGroup.add(boxWireframe);

        const gridHelper = new THREE.GridHelper(BOX_SIZE, 10, 0x00f0ff, 0x112244);
        gridHelper.position.y = -BOX_SIZE / 2;
        dataGroup.add(gridHelper);

        // Axis Sprites
        function createTextSprite(text, color) {
            const canvas = document.createElement("canvas");
            canvas.width = 256; canvas.height = 64;
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
        labelX.position.set(BOX_SIZE / 2 + 8, -BOX_SIZE / 2, 0);
        dataGroup.add(labelX);

        const labelY = createTextSprite("Y: TEXTURE", "#00ff88");
        labelY.position.set(-BOX_SIZE / 2, BOX_SIZE / 2 + 5, -BOX_SIZE / 2);
        dataGroup.add(labelY);

        const labelZ = createTextSprite("Z: CONCAVITY", "#00f0ff");
        labelZ.position.set(0, -BOX_SIZE / 2, BOX_SIZE / 2 + 8);
        dataGroup.add(labelZ);

        // 569 Cell Spheres
        const sphereGeo = new THREE.SphereGeometry(0.8, 12, 12);
        const benignMat = new THREE.MeshStandardMaterial({ color: 0x00ff88, emissive: 0x005522, roughness: 0.3 });
        const malignantMat = new THREE.MeshStandardMaterial({ color: 0xff0055, emissive: 0x660022, roughness: 0.3 });

        const cellObjects = [];
        METADATA.dataset.forEach((item, index) => {
            const [radius, texture, concavity, label] = item;
            const mat = (label === 1) ? benignMat.clone() : malignantMat.clone();
            const mesh = new THREE.Mesh(sphereGeo, mat);
            mesh.position.set(normX(radius), normY(texture), normZ(concavity));
            mesh.userData = { id: index, radius, texture, concavity, label };
            dataGroup.add(mesh);
            cellObjects.push(mesh);
        });

        // Test Point Ring Markers
        const testRingGeo = new THREE.RingGeometry(1.0, 1.2, 16);
        const testRingMat = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide, transparent: true, opacity: 0.8 });
        const testRingMeshes = [];

        // Patient Probe in Data Box
        const probeGroup = new THREE.Group();
        const probeCoreGeo = new THREE.SphereGeometry(1.6, 24, 24);
        const probeCoreMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x00aacc, roughness: 0.1 });
        const probeCore = new THREE.Mesh(probeCoreGeo, probeCoreMat);
        probeGroup.add(probeCore);

        const ringGeo = new THREE.TorusGeometry(2.8, 0.08, 16, 64);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.8 });
        const probeRing1 = new THREE.Mesh(ringGeo, ringMat);
        const probeRing2 = new THREE.Mesh(ringGeo, ringMat);
        probeRing2.rotation.x = Math.PI / 2;
        probeGroup.add(probeRing1);
        probeGroup.add(probeRing2);

        const knnSphereGeo = new THREE.SphereGeometry(1, 32, 32);
        const knnSphereMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.18 });
        const knnBoundingSphere = new THREE.Mesh(knnSphereGeo, knnSphereMat);
        probeGroup.add(knnBoundingSphere);
        dataGroup.add(probeGroup);

        const laserGroup = new THREE.Group();
        dataGroup.add(laserGroup);

        const planesGroup = new THREE.Group();
        dataGroup.add(planesGroup);

        // 2. Dedicated 3D Decision Tree Components
        const dtGraphGroup = new THREE.Group();
        treeGroup.add(dtGraphGroup);

        // 3. Dedicated 3D Random Forest Constellation Components
        const rfConstellationGroup = new THREE.Group();
        forestGroup.add(rfConstellationGroup);

        // Central Aggregator Orb for Random Forest
        const aggOrbGeo = new THREE.SphereGeometry(3.5, 32, 32);
        const aggOrbMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x006688, roughness: 0.2, metalness: 0.8 });
        const aggOrbMesh = new THREE.Mesh(aggOrbGeo, aggOrbMat);
        aggOrbMesh.position.set(0, 0, 0);
        forestGroup.add(aggOrbMesh);

        const aggRingGeo = new THREE.RingGeometry(4.5, 5.0, 32);
        const aggRingMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.7 });
        const aggRingMesh = new THREE.Mesh(aggRingGeo, aggRingMat);
        aggRingMesh.rotation.x = Math.PI / 2;
        forestGroup.add(aggRingMesh);

        // RF Beams Group
        const rfBeamsGroup = new THREE.Group();
        forestGroup.add(rfBeamsGroup);

        // Raycasting for clicking 3D points
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        window.addEventListener("pointerdown", (event) => {
            if (event.target.closest(".panel") || event.target.closest(".header-bar") || event.target.closest(".bottom-legend") || event.target.closest(".view-mode-tabs")) {
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

        // 3D Slicing Planes Builder
        function updateSlicingPlanes(splits) {
            while (planesGroup.children.length > 0) {
                planesGroup.remove(planesGroup.children[0]);
            }
            if (!splits) return;
            splits.forEach(split => {
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
            planesGroup.visible = state.showPlanes;
        }

        // 3D Holographic Decision Tree Builder
        let activeTreeNodesMap = new Map();
        let activeTreeLinks = [];

        function build3DDecisionTree(nodes, links) {
            while (dtGraphGroup.children.length > 0) {
                dtGraphGroup.remove(dtGraphGroup.children[0]);
            }
            activeTreeNodesMap.clear();
            activeTreeLinks = [];

            if (!nodes || nodes.length === 0) return;

            // Render Links
            links.forEach(l => {
                const p1 = new THREE.Vector3(l.source_pos[0], l.source_pos[1], l.source_pos[2]);
                const p2 = new THREE.Vector3(l.target_pos[0], l.target_pos[1], l.target_pos[2]);
                const geo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
                const mat = new THREE.LineBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.35, linewidth: 2 });
                const line = new THREE.Line(geo, mat);
                dtGraphGroup.add(line);
                activeTreeLinks.push({ source: l.source, target: l.target, line, mat });
            });

            // Render Nodes
            const nodeGeo = new THREE.SphereGeometry(1.5, 16, 16);
            nodes.forEach(n => {
                const isLeaf = n.is_leaf;
                let color = 0x00f0ff;
                if (isLeaf) {
                    color = (n.prediction === 1) ? 0x00ff88 : 0xff0055;
                }
                const mat = new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: isLeaf ? (n.prediction === 1 ? 0x004411 : 0x550011) : 0x003344,
                    roughness: 0.2
                });
                const mesh = new THREE.Mesh(nodeGeo, mat);
                mesh.position.set(n.x, n.y, n.z);
                mesh.userData = n;
                dtGraphGroup.add(mesh);
                activeTreeNodesMap.set(n.id, { mesh, mat, data: n });

                // Node Text Badge
                let text = isLeaf ? (n.prediction === 1 ? "🟢 Benign" : "🔴 Malignant") : (n.feature.toUpperCase() + " ≤ " + n.threshold);
                const sprite = createTextSprite(text, isLeaf ? (n.prediction === 1 ? "#00ff88" : "#ff0055") : "#00f0ff");
                sprite.position.set(n.x, n.y + 2.8, n.z);
                sprite.scale.set(12, 3, 1);
                dtGraphGroup.add(sprite);
            });
        }

        // Highlight Active Path in 3D Decision Tree
        function highlight3DTreePath(pathIds) {
            const pathSet = new Set(pathIds || []);
            activeTreeNodesMap.forEach((val, id) => {
                if (pathSet.has(id)) {
                    val.mesh.scale.set(1.5, 1.5, 1.5);
                    val.mat.emissiveIntensity = 2.0;
                } else {
                    val.mesh.scale.set(0.85, 0.85, 0.85);
                    val.mat.emissiveIntensity = 0.3;
                }
            });

            activeTreeLinks.forEach(l => {
                if (pathSet.has(l.source) && pathSet.has(l.target)) {
                    l.mat.color.setHex(0xffb700); // Amber active laser path
                    l.mat.opacity = 1.0;
                    l.line.scale.set(1.2, 1.2, 1.2);
                } else {
                    l.mat.color.setHex(0x00f0ff);
                    l.mat.opacity = 0.2;
                    l.line.scale.set(1, 1, 1);
                }
            });
        }

        // 3D Random Forest Constellation Builder
        let rfCrystalMeshes = [];
        function build3DRandomForest(constellation) {
            while (rfConstellationGroup.children.length > 0) {
                rfConstellationGroup.remove(rfConstellationGroup.children[0]);
            }
            rfCrystalMeshes = [];
            if (!constellation) return;

            const crystalGeo = new THREE.OctahedronGeometry(2.0, 0);
            const crystalMat = new THREE.MeshStandardMaterial({
                color: 0x00f0ff,
                emissive: 0x004455,
                roughness: 0.1,
                metalness: 0.8
            });

            const orbitRingGeo = new THREE.TorusGeometry(30, 0.08, 16, 100);
            const orbitRingMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.3 });
            const orbitRing = new THREE.Mesh(orbitRingGeo, orbitRingMat);
            orbitRing.rotation.x = Math.PI / 2;
            rfConstellationGroup.add(orbitRing);

            constellation.forEach(item => {
                const mesh = new THREE.Mesh(crystalGeo, crystalMat.clone());
                mesh.position.set(item.pos[0], item.pos[1], item.pos[2]);
                mesh.userData = item;
                rfConstellationGroup.add(mesh);
                rfCrystalMeshes.push(mesh);

                const label = createTextSprite("Tree #" + (item.tree_id + 1), "#00f0ff");
                label.position.set(item.pos[0], item.pos[1] + 3.2, item.pos[2]);
                label.scale.set(10, 2.5, 1);
                rfConstellationGroup.add(label);
            });
        }

        // Render RF Beams towards Aggregator Core
        function updateRFBeams(votes) {
            while (rfBeamsGroup.children.length > 0) {
                rfBeamsGroup.remove(rfBeamsGroup.children[0]);
            }
            if (!votes || rfCrystalMeshes.length === 0) return;

            const aggPos = new THREE.Vector3(0, 0, 0);
            votes.forEach(v => {
                const crystal = rfCrystalMeshes[v.tree_id];
                if (!crystal) return;

                const isBenign = (v.vote === 1);
                const color = isBenign ? 0x00ff88 : 0xff0055;

                crystal.material.color.setHex(color);
                crystal.material.emissive.setHex(isBenign ? 0x006622 : 0x660022);

                if (state.showLasers) {
                    const points = [crystal.position, aggPos];
                    const geo = new THREE.BufferGeometry().setFromPoints(points);
                    const mat = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.8, linewidth: 2 });
                    const beam = new THREE.Line(geo, mat);
                    rfBeamsGroup.add(beam);
                }
            });

            // Update Aggregator Orb Color
            const benignVotes = votes.filter(v => v.vote === 1).length;
            const majorityBenign = benignVotes >= (votes.length / 2);
            aggOrbMat.color.setHex(majorityBenign ? 0x00ff88 : 0xff0055);
            aggOrbMat.emissive.setHex(majorityBenign ? 0x008833 : 0xaa0033);
        }

        // Scene Mode Layout Adjustments
        function applyViewMode(mode) {
            state.viewMode = mode;
            document.querySelectorAll(".view-btn").forEach(btn => {
                btn.classList.toggle("active", btn.dataset.view === mode);
            });

            if (mode === "data") {
                dataGroup.visible = true;
                dataGroup.position.set(0, 0, 0);
                treeGroup.visible = false;
                forestGroup.visible = false;
            } else if (mode === "tree") {
                dataGroup.visible = false;
                treeGroup.visible = true;
                treeGroup.position.set(0, -10, 0);
                forestGroup.visible = false;
            } else if (mode === "forest") {
                dataGroup.visible = false;
                treeGroup.visible = false;
                forestGroup.visible = true;
                forestGroup.position.set(0, 0, 0);
            } else { // split
                dataGroup.visible = true;
                dataGroup.position.set(-45, 0, 0);
                treeGroup.visible = true;
                treeGroup.position.set(45, -10, 0);
                forestGroup.visible = false;
            }
            resetCamera();
        }

        document.querySelectorAll(".view-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                applyViewMode(btn.dataset.view);
                sfx.switchTab();
            });
        });

        // Highlight Test Samples in Data Cloud
        function updateTestSetHighlighting(testIndices) {
            state.testIndicesSet = new Set(testIndices || []);
            cellObjects.forEach((cell, idx) => {
                if (state.testIndicesSet.has(idx)) {
                    if (state.showTestHighlight) {
                        cell.material.wireframe = true;
                        cell.scale.set(1.1, 1.1, 1.1);
                    } else {
                        cell.material.wireframe = false;
                        cell.scale.set(1.0, 1.0, 1.0);
                    }
                } else {
                    cell.material.wireframe = false;
                    cell.scale.set(1.0, 1.0, 1.0);
                }
            });
        }

        // Live Retrain API Call
        let retrainTimeout = null;
        function triggerRetrain(showPill = true) {
            if (retrainTimeout) clearTimeout(retrainTimeout);
            retrainTimeout = setTimeout(async () => {
                try {
                    const res = await fetch("/api/retrain", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(state.hyperparams)
                    });
                    const data = await res.json();
                    if (data.success) {
                        const meta = data.meta;
                        // Update HUD Accuracy Badges
                        document.getElementById("metric-dt-acc").innerText = meta.dt_acc + "%";
                        document.getElementById("metric-knn-acc").innerText = meta.knn_acc + "%";
                        document.getElementById("metric-rf-acc").innerText = meta.rf_acc + "%";

                        document.getElementById("info-train-samples").innerText = meta.train_samples + " ta (" + (100 - state.hyperparams.test_size*100).toFixed(0) + "%)";
                        document.getElementById("info-test-samples").innerText = meta.test_samples + " ta (" + (state.hyperparams.test_size*100).toFixed(0) + "%)";
                        document.getElementById("info-active-seed").innerText = state.hyperparams.random_state;

                        // Feature Importances
                        document.getElementById("bar-imp-c").style.width = meta.rf_importances[2] + "%";
                        document.getElementById("txt-imp-c").innerText = meta.rf_importances[2] + "%";
                        document.getElementById("bar-imp-r").style.width = meta.rf_importances[0] + "%";
                        document.getElementById("txt-imp-r").innerText = meta.rf_importances[0] + "%";
                        document.getElementById("bar-imp-t").style.width = meta.rf_importances[1] + "%";
                        document.getElementById("txt-imp-t").innerText = meta.rf_importances[1] + "%";

                        // Update 3D components
                        updateSlicingPlanes(meta.dt_splits);
                        build3DDecisionTree(meta.dt_nodes, meta.dt_links);
                        build3DRandomForest(meta.rf_constellation);
                        updateTestSetHighlighting(meta.test_indices);

                        // Trigger Prediction
                        runPrediction();

                        if (showPill) {
                            const pill = document.getElementById("retrain-pill");
                            pill.classList.add("show");
                            sfx.retrainSweep();
                            setTimeout(() => pill.classList.remove("show"), 2000);
                        }
                    }
                } catch(e) {
                    console.error("Retrain error:", e);
                }
            }, 150);
        }

        // Live Prediction API Call
        let predictTimeout = null;
        function runPrediction() {
            if (predictTimeout) clearTimeout(predictTimeout);
            predictTimeout = setTimeout(async () => {
                const r = state.patient.radius;
                const t = state.patient.texture;
                const c = state.patient.concavity;

                // Move 3D Probe in Data Box
                probeGroup.position.set(normX(r), normY(t), normZ(c));

                try {
                    const res = await fetch("/api/predict", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ radius: r, texture: t, concavity: c, model: state.currentModel, k: state.hyperparams.k })
                    });
                    const data = await res.json();

                    // Update UI according to active model
                    let activeResult;
                    if (state.currentModel === "dt") {
                        activeResult = data.dt;
                        highlight3DTreePath(data.dt.active_path_ids);
                        renderDTInsights(data.dt);
                    } else if (state.currentModel === "rf") {
                        activeResult = data.rf;
                        updateRFBeams(data.rf.votes);
                        renderRFInsights(data.rf);
                    } else { // knn
                        activeResult = data.knn;
                        renderKNNVisuals(r, t, c, state.hyperparams.k);
                        renderKNNInsights(data.knn);
                    }

                    updateVerdictCard(activeResult);
                } catch(e) {
                    console.error("Predict error:", e);
                }
            }, 50);
        }

        function updateVerdictCard(result) {
            const card = document.getElementById("diag-card");
            const badge = document.getElementById("diag-badge");
            const pB = Math.round(result.prob_benign * 100);
            const pM = Math.round(result.prob_malignant * 100);

            document.getElementById("prob-benign-txt").innerText = pB + "%";
            document.getElementById("prob-malignant-txt").innerText = pM + "%";
            document.getElementById("bar-benign").style.width = pB + "%";
            document.getElementById("bar-malignant").style.width = pM + "%";

            if (result.prediction === 1) {
                card.className = "diag-card benign";
                badge.innerText = "BENIGN // SOG'LOM HUJAYRA";
                document.body.className = "status-benign";
                probeCoreMat.color.setHex(0x00ff88);
            } else {
                card.className = "diag-card malignant";
                badge.innerText = "MALIGNANT // XAVFLI O'SIMTA";
                document.body.className = "status-malignant";
                probeCoreMat.color.setHex(0xff0055);
            }
        }

        function renderKNNVisuals(radius, texture, concavity, k) {
            while (laserGroup.children.length > 0) {
                laserGroup.remove(laserGroup.children[0]);
            }

            const distances = METADATA.dataset.map((pt, idx) => {
                const dx = pt[0] - radius;
                const dy = pt[1] - texture;
                const dz = (pt[2] - concavity) * 50;
                return { idx, dist: Math.sqrt(dx*dx + dy*dy + dz*dz), label: pt[3] };
            });
            distances.sort((a, b) => a.dist - b.dist);
            const neighbors = distances.slice(0, k);

            const probePos = probeGroup.position;
            let max3dDist = 0;

            neighbors.forEach(n => {
                const targetMesh = cellObjects[n.idx];
                const d = probePos.distanceTo(targetMesh.position);
                if (d > max3dDist) max3dDist = d;

                if (state.showLasers) {
                    const geo = new THREE.BufferGeometry().setFromPoints([probePos, targetMesh.position]);
                    const mat = new THREE.LineBasicMaterial({
                        color: (n.label === 1 ? 0x00ff88 : 0xff0055),
                        transparent: true, opacity: 0.8, linewidth: 2
                    });
                    laserGroup.add(new THREE.Line(geo, mat));
                }
            });

            knnBoundingSphere.scale.set(max3dDist + 0.5, max3dDist + 0.5, max3dDist + 0.5);
            knnBoundingSphere.visible = state.showLasers;
        }

        function renderKNNInsights(knn) {
            document.getElementById("model-insight-title").innerText = "KNN Qo'shnilar Tahlili (K=" + state.hyperparams.k + ")";
            document.getElementById("insight-container").innerHTML = `
                <div class="info-row">
                    <span class="label">Tanlangan K:</span>
                    <span class="value" style="color: var(--cyan);">${state.hyperparams.k} ta eng yaqin biopsiya</span>
                </div>
                <div class="info-row">
                    <span class="label">Sog'lomlik ehtimoli:</span>
                    <span class="value" style="color: var(--green);">${(knn.prob_benign * 100).toFixed(1)}%</span>
                </div>
                <div class="info-row">
                    <span class="label">Xavflilik ehtimoli:</span>
                    <span class="value" style="color: var(--red);">${(knn.prob_malignant * 100).toFixed(1)}%</span>
                </div>
            `;
        }

        function renderDTInsights(dt) {
            document.getElementById("model-insight-title").innerText = "Decision Tree Mantiqiy Qoidalari";
            let html = '<div class="tree-steps">';
            dt.steps.forEach((s, idx) => {
                const dir = s.goes_left ? "≤" : ">";
                const sideText = s.goes_left ? "Chap shox" : "O'ng shox";
                const isLast = (idx === dt.steps.length - 1);
                html += `
                    <div class="tree-step-item ${isLast ? 'active-step' : ''}">
                        ${idx + 1}. <b>${s.feature.toUpperCase()}</b>: (${s.value}) ${dir} ${s.threshold} → <i>${sideText}</i>
                    </div>
                `;
            });
            html += `</div>
                <div class="info-row" style="margin-top: 6px;">
                    <span class="label">Aktiv shoxlar soni:</span>
                    <span class="value" style="color: var(--cyan);">${dt.active_path_ids.length} ta tugun</span>
                </div>
            `;
            document.getElementById("insight-container").innerHTML = html;
        }

        function renderRFInsights(rf) {
            document.getElementById("model-insight-title").innerText = "Random Forest Ovoz Berishi (" + rf.votes.length + " ta daraxt)";
            let html = '<div class="rf-trees-grid">';
            rf.votes.forEach((v, idx) => {
                const cls = (v.vote === 1) ? "b" : "m";
                const label = (v.vote === 1) ? "🟢" : "🔴";
                html += `<div class="rf-tree-chip ${cls}" title="Tree #${idx+1}">${label} T${idx+1}</div>`;
            });
            html += '</div>';
            html += `
                <div class="info-row" style="margin-top: 6px;">
                    <span class="label">Sog'lomga ovozlar:</span>
                    <span class="value" style="color: var(--green);">${rf.votes_benign} ta</span>
                </div>
                <div class="info-row">
                    <span class="label">Xavfliga ovozlar:</span>
                    <span class="value" style="color: var(--red);">${rf.votes_malignant} ta</span>
                </div>
            `;
            document.getElementById("insight-container").innerHTML = html;
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

                // Auto switch view mode to showcase model
                if (state.currentModel === "dt" && state.viewMode === "data") {
                    applyViewMode("tree");
                } else if (state.currentModel === "rf" && state.viewMode === "data") {
                    applyViewMode("forest");
                }

                runPrediction();
            });
        });

        // Sliders & Inputs
        const inTestSize = document.getElementById("input-test-size");
        const inSeed = document.getElementById("input-seed");
        const inMaxDepth = document.getElementById("input-max-depth");
        const inNest = document.getElementById("input-nest");

        inTestSize.addEventListener("input", (e) => {
            const val = parseFloat(e.target.value);
            state.hyperparams.test_size = val;
            document.getElementById("val-test-size").innerText = Math.round(val * 100) + "% (Test: " + Math.round(569 * val) + ")";
            triggerRetrain(true);
        });

        inSeed.addEventListener("change", (e) => {
            state.hyperparams.random_state = parseInt(e.target.value) || 0;
            document.getElementById("val-seed").innerText = state.hyperparams.random_state;
            triggerRetrain(true);
        });

        document.getElementById("btn-random-seed").addEventListener("click", () => {
            const newSeed = Math.floor(Math.random() * 1000);
            state.hyperparams.random_state = newSeed;
            inSeed.value = newSeed;
            document.getElementById("val-seed").innerText = newSeed;
            triggerRetrain(true);
        });

        inMaxDepth.addEventListener("input", (e) => {
            const val = parseInt(e.target.value);
            state.hyperparams.max_depth = val;
            document.getElementById("val-max-depth").innerText = val + " bosqich";
            triggerRetrain(true);
        });

        inNest.addEventListener("input", (e) => {
            const val = parseInt(e.target.value);
            state.hyperparams.n_estimators = val;
            document.getElementById("val-nest").innerText = val + " ta daraxt";
            triggerRetrain(true);
        });

        // Coordinates Sliders
        const inRadius = document.getElementById("input-radius");
        const inTexture = document.getElementById("input-texture");
        const inConcavity = document.getElementById("input-concavity");

        inRadius.addEventListener("input", (e) => {
            state.patient.radius = parseFloat(e.target.value);
            document.getElementById("val-radius").innerText = state.patient.radius.toFixed(1) + " mm";
            sfx.beep();
            runPrediction();
        });

        inTexture.addEventListener("input", (e) => {
            state.patient.texture = parseFloat(e.target.value);
            document.getElementById("val-texture").innerText = state.patient.texture.toFixed(1);
            sfx.beep();
            runPrediction();
        });

        inConcavity.addEventListener("input", (e) => {
            state.patient.concavity = parseFloat(e.target.value);
            document.getElementById("val-concavity").innerText = state.patient.concavity.toFixed(3);
            sfx.beep();
            runPrediction();
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

            runPrediction();
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

        document.getElementById("toggle-planes").addEventListener("change", (e) => {
            state.showPlanes = e.target.checked;
            planesGroup.visible = state.showPlanes;
        });

        document.getElementById("toggle-autorotate").addEventListener("change", (e) => {
            state.autoRotate = e.target.checked;
        });

        document.getElementById("toggle-lasers").addEventListener("change", (e) => {
            state.showLasers = e.target.checked;
            runPrediction();
        });

        document.getElementById("toggle-test-highlight").addEventListener("change", (e) => {
            state.showTestHighlight = e.target.checked;
            updateTestSetHighlighting(Array.from(state.testIndicesSet));
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

            aggRingMesh.rotation.z = elapsed * 1.5;
            aggOrbMesh.rotation.y = elapsed * 0.8;

            rfCrystalMeshes.forEach((mesh, idx) => {
                mesh.rotation.y = elapsed * 2 + idx;
                mesh.rotation.x = elapsed * 1.5;
            });

            if (state.autoRotate) {
                if (state.viewMode === "data") dataGroup.rotation.y = elapsed * 0.05;
                else if (state.viewMode === "forest") forestGroup.rotation.y = elapsed * 0.08;
                else if (state.viewMode === "tree") treeGroup.rotation.y = Math.sin(elapsed * 0.2) * 0.15;
            }

            controls.update();
            renderer.render(scene, camera);
        }

        // Initialize First Retrain & Start Loop
        triggerRetrain(false);
        animate();
    </script>
</body>
</html>
"""

with open(r'C:\Users\Gubernatr\Desktop\new\index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("index.html compiled successfully!")
