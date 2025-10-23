import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import random
import uuid
import json
from typing import Dict, List, Any
from collections import defaultdict, deque
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AEGIS CYBER COMMAND • ELITE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS WITH GLASSMORPHISM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        background-attachment: fixed;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(0deg, rgba(0,255,65,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,65,0.03) 3px),
            repeating-linear-gradient(90deg, rgba(0,255,65,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,65,0.03) 3px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header - Enhanced */
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00ff41;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 
            0 0 10px #00ff41,
            0 0 20px #00ff41,
            0 0 30px #00ff41,
            0 0 40px #00ff41,
            0 0 70px #00ff41,
            0 0 80px #00ff41;
        animation: glow-pulse 3s ease-in-out infinite alternate;
        letter-spacing: 8px;
        position: relative;
        z-index: 10;
    }
    
    @keyframes glow-pulse {
        from { 
            text-shadow: 
                0 0 10px #00ff41,
                0 0 20px #00ff41,
                0 0 30px #00ff41;
            transform: scale(1);
        }
        to { 
            text-shadow: 
                0 0 20px #00ff41,
                0 0 30px #00ff41,
                0 0 40px #00ff41,
                0 0 70px #00ff41;
            transform: scale(1.02);
        }
    }
    
    .cyber-subheader {
        text-align: center;
        color: #0ff;
        font-family: 'Orbitron', monospace;
        font-size: 1.4rem;
        letter-spacing: 6px;
        margin-bottom: 2rem;
        text-shadow: 0 0 15px #0ff;
        font-weight: 600;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(26, 31, 58, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 65, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 
            0 8px 32px 0 rgba(0, 255, 65, 0.1),
            inset 0 0 20px rgba(0, 255, 65, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(0, 255, 65, 0.05),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(0, 255, 65, 0.5);
        box-shadow: 
            0 12px 48px 0 rgba(0, 255, 65, 0.2),
            inset 0 0 30px rgba(0, 255, 65, 0.1);
    }
    
    /* Terminal Window - Advanced */
    .terminal-window {
        background: #000;
        border: 2px solid #00ff41;
        border-radius: 12px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff41;
        font-size: 0.95rem;
        height: 450px;
        overflow-y: auto;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.3),
            inset 0 0 30px rgba(0, 255, 65, 0.05);
        position: relative;
    }
    
    .terminal-window::before {
        content: "⬤ ⬤ ⬤";
        position: absolute;
        top: -35px;
        left: 15px;
        color: #ff5f56;
        font-size: 24px;
        letter-spacing: 8px;
    }
    
    .terminal-window::-webkit-scrollbar {
        width: 12px;
    }
    
    .terminal-window::-webkit-scrollbar-track {
        background: #0a0a0a;
        border-radius: 6px;
    }
    
    .terminal-window::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ff41 0%, #00aa2b 100%);
        border-radius: 6px;
    }
    
    .terminal-window::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #44ff66 0%, #00cc33 100%);
    }
    
    /* Log Lines with Animation */
    .log-line {
        margin: 5px 0;
        padding: 5px 10px;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .log-line:hover {
        background: rgba(0, 255, 65, 0.1);
        border-left: 3px solid #00ff41;
        transform: translateX(8px);
        padding-left: 15px;
    }
    
    .log-critical {
        color: #ff0040;
        text-shadow: 0 0 10px #ff0040;
        animation: blink 1.5s infinite;
        font-weight: 600;
    }
    
    .log-high { color: #ff6b00; font-weight: 500; }
    .log-medium { color: #ffeb3b; }
    .log-low { color: #00ff41; }
    .log-info { color: #0ff; }
    
    @keyframes blink {
        0%, 50%, 100% { opacity: 1; }
        25%, 75% { opacity: 0.6; }
    }
    
    /* Metric Cards - Premium */
    .metric-card {
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.9) 0%, rgba(15, 23, 41, 0.9) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(0, 255, 65, 0.3);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(0, 255, 65, 0.15),
            inset 0 0 30px rgba(0, 255, 65, 0.03);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 255, 65, 0.1) 0%, transparent 70%);
        animation: rotate 6s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        border-color: rgba(0, 255, 65, 0.8);
        box-shadow: 
            0 15px 50px rgba(0, 255, 65, 0.3),
            inset 0 0 40px rgba(0, 255, 65, 0.1);
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        margin: 15px 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 20px currentColor;
    }
    
    .metric-label {
        color: #888;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    .metric-trend {
        font-size: 1.2rem;
        margin-top: 10px;
        font-weight: 600;
    }
    
    /* Threat Cards - Enhanced */
    .threat-card {
        background: linear-gradient(135deg, rgba(45, 10, 10, 0.9) 0%, rgba(26, 5, 5, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 0, 64, 0.4);
        border-radius: 15px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 
            0 8px 32px rgba(255, 0, 64, 0.2),
            inset 0 0 20px rgba(255, 0, 64, 0.05);
        transition: all 0.3s ease;
        animation: pulse-red 4s infinite;
        position: relative;
    }
    
    @keyframes pulse-red {
        0%, 100% { 
            box-shadow: 
                0 8px 32px rgba(255, 0, 64, 0.2),
                inset 0 0 20px rgba(255, 0, 64, 0.05);
            border-color: rgba(255, 0, 64, 0.4);
        }
        50% { 
            box-shadow: 
                0 12px 48px rgba(255, 0, 64, 0.4),
                inset 0 0 30px rgba(255, 0, 64, 0.1);
            border-color: rgba(255, 0, 64, 0.8);
        }
    }
    
    .threat-card:hover {
        transform: scale(1.03);
        border-color: rgba(255, 0, 64, 0.8);
    }
    
    /* Success Card */
    .success-card {
        background: linear-gradient(135deg, rgba(10, 42, 10, 0.9) 0%, rgba(5, 26, 5, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 255, 0, 0.4);
        border-radius: 15px;
        padding: 20px;
        margin: 12px 0;
        animation: pulse-green 4s infinite;
    }
    
    @keyframes pulse-green {
        0%, 100% { 
            box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
            border-color: rgba(0, 255, 0, 0.4);
        }
        50% { 
            box-shadow: 0 12px 48px rgba(0, 255, 0, 0.4);
            border-color: rgba(0, 255, 0, 0.8);
        }
    }
    
    /* Status Bar - Enhanced */
    .status-bar {
        background: linear-gradient(90deg, rgba(26, 31, 58, 0.95) 0%, rgba(15, 23, 41, 0.95) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(0, 255, 65, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 255, 65, 0.15);
    }
    
    /* Badges - Advanced */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #ff0040 0%, #cc0033 100%);
        color: #fff;
        box-shadow: 0 4px 15px rgba(255, 0, 64, 0.5);
        animation: badge-pulse 2s infinite;
    }
    
    @keyframes badge-pulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(255, 0, 64, 0.5); }
        50% { box-shadow: 0 6px 25px rgba(255, 0, 64, 0.8); }
    }
    
    .badge-high {
        background: linear-gradient(135deg, #ff6b00 0%, #cc5500 100%);
        color: #fff;
        box-shadow: 0 4px 15px rgba(255, 107, 0, 0.5);
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #ffeb3b 0%, #fbc02d 100%);
        color: #000;
        box-shadow: 0 4px 15px rgba(255, 235, 59, 0.5);
    }
    
    .badge-low {
        background: linear-gradient(135deg, #00ff41 0%, #00aa2b 100%);
        color: #000;
        box-shadow: 0 4px 15px rgba(0, 255, 65, 0.5);
    }
    
    .badge-info {
        background: linear-gradient(135deg, #0ff 0%, #0aa 100%);
        color: #000;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.5);
    }
    
    /* Buttons - Premium */
    .stButton>button {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.2) 0%, rgba(0, 170, 43, 0.2) 100%) !important;
        border: 2px solid #00ff41 !important;
        color: #00ff41 !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 255, 65, 0.2) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.4) 0%, rgba(0, 170, 43, 0.4) 100%) !important;
        border-color: #44ff66 !important;
        color: #fff !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 30px rgba(0, 255, 65, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* Progress Bar - Animated */
    .progress-bar {
        width: 100%;
        height: 12px;
        background: rgba(26, 31, 58, 0.5);
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff41 0%, #00aa2b 50%, #00ff41 100%);
        background-size: 200% 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
        animation: progress-shimmer 2s linear infinite;
    }
    
    @keyframes progress-shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* IP Address Styling */
    .ip-address {
        font-family: 'Courier New', monospace;
        color: #0ff;
        background: rgba(0, 255, 255, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.9em;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .ip-address:hover {
        background: rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    }
    
    /* Network Node Visualization */
    .network-node {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: radial-gradient(circle, #00ff41 0%, #00aa2b 100%);
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
        transition: all 0.3s ease;
        animation: node-pulse 3s infinite;
    }
    
    @keyframes node-pulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
        }
        50% { 
            transform: scale(1.1);
            box-shadow: 0 0 50px rgba(0, 255, 65, 0.9);
        }
    }
    
    .network-node.threat {
        background: radial-gradient(circle, #ff0040 0%, #cc0033 100%);
        box-shadow: 0 0 30px rgba(255, 0, 64, 0.6);
    }
    
    /* Timeline Event */
    .timeline-event {
        position: relative;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #00ff41;
        background: linear-gradient(90deg, rgba(0, 255, 65, 0.1) 0%, transparent 100%);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .timeline-event:hover {
        background: linear-gradient(90deg, rgba(0, 255, 65, 0.2) 0%, transparent 100%);
        transform: translateX(10px);
        border-left-width: 6px;
    }
    
    .timeline-event::before {
        content: "●";
        position: absolute;
        left: -12px;
        top: 20px;
        color: #00ff41;
        font-size: 24px;
        text-shadow: 0 0 15px #00ff41;
    }
    
    /* Data Table Styling */
    .dataframe {
        background: rgba(26, 31, 58, 0.5) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe thead tr th {
        background: rgba(0, 255, 65, 0.2) !important;
        color: #00ff41 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border-bottom: 2px solid #00ff41 !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 255, 65, 0.1) !important;
        transform: scale(1.01);
    }
    
    /* Notification Toast */
    .notification-toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, rgba(26, 31, 58, 0.95) 0%, rgba(15, 23, 41, 0.95) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid #00ff41;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 255, 65, 0.3);
        animation: slideIn 0.5s ease-out;
        z-index: 9999;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Radar Sweep */
    .radar-container {
        position: relative;
        width: 100%;
        max-width: 500px;
        height: 500px;
        margin: 20px auto;
        background: radial-gradient(circle, rgba(0, 17, 0, 0.8) 0%, rgba(0, 0, 0, 0.95) 70%);
        border: 3px solid #00ff41;
        border-radius: 50%;
        box-shadow: 
            0 0 50px rgba(0, 255, 65, 0.3),
            inset 0 0 50px rgba(0, 255, 65, 0.1);
    }
    
    .radar-circle {
        position: absolute;
        border: 1px solid rgba(0, 255, 65, 0.3);
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    
    .radar-sweep {
        position: absolute;
        width: 50%;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(0, 255, 65, 0.8) 50%, #00ff41 100%);
        top: 50%;
        left: 50%;
        transform-origin: 0% 50%;
        animation: radar-spin 4s linear infinite;
        box-shadow: 0 0 20px #00ff41;
    }
    
    @keyframes radar-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Heatmap Cell */
    .heatmap-cell {
        display: inline-block;
        width: 15px;
        height: 15px;
        margin: 2px;
        border-radius: 3px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .heatmap-cell:hover {
        transform: scale(1.8);
        z-index: 10;
        box-shadow: 0 0 15px currentColor;
    }
    
    /* Sidebar Customization */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(26, 31, 58, 0.95) 0%, rgba(15, 23, 41, 0.95) 100%) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 58, 0.5) !important;
        border: 1px solid rgba(0, 255, 65, 0.3) !important;
        border-radius: 10px !important;
        color: #00ff41 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 255, 65, 0.1) !important;
        border-color: rgba(0, 255, 65, 0.6) !important;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(0, 255, 65, 0.2);
        border-top: 4px solid #00ff41;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 14, 39, 0.5);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ff41 0%, #00aa2b 100%);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #44ff66 0%, #00cc33 100%);
    }
    
    /* Selection Color */
    ::selection {
        background: rgba(0, 255, 65, 0.3);
        color: #fff;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background: rgba(0, 0, 0, 0.9);
        color: #00ff41;
        text-align: center;
        border-radius: 8px;
        padding: 8px 12px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #00ff41;
        box-shadow: 0 4px 20px rgba(0, 255, 65, 0.3);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ==================== ADVANCED MITRE ATT&CK ====================
class MITREAttack:
    """Enhanced MITRE ATT&CK Framework with full tactics"""
    
    TACTICS = {
        "TA0001": {"name": "Initial Access", "color": "#ff6b6b"},
        "TA0002": {"name": "Execution", "color": "#ff8c42"},
        "TA0003": {"name": "Persistence", "color": "#ffd93d"},
        "TA0004": {"name": "Privilege Escalation", "color": "#6bcf7f"},
        "TA0005": {"name": "Defense Evasion", "color": "#4d96ff"},
        "TA0006": {"name": "Credential Access", "color": "#9d4edd"},
        "TA0007": {"name": "Discovery", "color": "#ff006e"},
        "TA0008": {"name": "Lateral Movement", "color": "#fb5607"},
        "TA0009": {"name": "Collection", "color": "#ffbe0b"},
        "TA0010": {"name": "Exfiltration", "color": "#8338ec"},
        "TA0011": {"name": "Command and Control", "color": "#3a86ff"},
        "TA0040": {"name": "Impact", "color": "#f72585"}
    }
    
    TECHNIQUES = {
        "T1566.001": {"name": "Spearphishing Attachment", "tactic": "TA0001", "severity": "High"},
        "T1566.002": {"name": "Spearphishing Link", "tactic": "TA0001", "severity": "High"},
        "T1059.001": {"name": "PowerShell", "tactic": "TA0002", "severity": "Medium"},
        "T1059.003": {"name": "Windows Command Shell", "tactic": "TA0002", "severity": "Medium"},
        "T1053.005": {"name": "Scheduled Task", "tactic": "TA0003", "severity": "High"},
        "T1078.001": {"name": "Default Accounts", "tactic": "TA0004", "severity": "Critical"},
        "T1027": {"name": "Obfuscated Files or Information", "tactic": "TA0005", "severity": "High"},
        "T1003.001": {"name": "LSASS Memory", "tactic": "TA0006", "severity": "Critical"},
        "T1083": {"name": "File and Directory Discovery", "tactic": "TA0007", "severity": "Low"},
        "T1021.001": {"name": "Remote Desktop Protocol", "tactic": "TA0008", "severity": "High"},
        "T1005": {"name": "Data from Local System", "tactic": "TA0009", "severity": "Medium"},
        "T1041": {"name": "Exfiltration Over C2 Channel", "tactic": "TA0010", "severity": "Critical"},
        "T1071.001": {"name": "Web Protocols", "tactic": "TA0011", "severity": "High"},
        "T1486": {"name": "Data Encrypted for Impact", "tactic": "TA0040", "severity": "Critical"}
    }
    
    @staticmethod
    def get_random_technique():
        tech_id = random.choice(list(MITREAttack.TECHNIQUES.keys()))
        tech = MITREAttack.TECHNIQUES[tech_id]
        tactic = MITREAttack.TACTICS[tech["tactic"]]
        return {
            "id": tech_id,
            "name": tech["name"],
            "tactic": tactic["name"],
            "tactic_id": tech["tactic"],
            "severity": tech["severity"],
            "color": tactic["color"]
        }
    
    @staticmethod
    def get_kill_chain():
        """Generate cyber kill chain for threat"""
        stages = [
            "Reconnaissance",
            "Weaponization", 
            "Delivery",
            "Exploitation",
            "Installation",
            "Command & Control",
            "Actions on Objectives"
        ]
        current_stage = random.randint(0, len(stages) - 1)
        return {
            "stages": stages,
            "current_stage": current_stage,
            "completed": stages[:current_stage + 1]
        }

# ==================== THREAT INTELLIGENCE DATABASE ====================
class ThreatIntel:
    """Comprehensive Threat Intelligence Database"""
    
    APT_GROUPS = {
        "APT28": {
            "country": "Russia",
            "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "Sednit"],
            "targets": ["Government", "Military", "Security", "Aerospace"],
            "ttps": ["Spear Phishing", "Zero-Day Exploits", "Custom Malware", "Watering Hole"],
            "active_since": "2007",
            "sophistication": "Very High",
            "motivation": "Espionage"
        },
        "APT29": {
            "country": "Russia",
            "aliases": ["Cozy Bear", "The Dukes", "CozyDuke"],
            "targets": ["Government", "Think Tanks", "Healthcare", "Energy"],
            "ttps": ["Stealth Operations", "Advanced Malware", "Long-term Persistence"],
            "active_since": "2008",
            "sophistication": "Very High",
            "motivation": "Intelligence Gathering"
        },
        "APT41": {
            "country": "China",
            "aliases": ["Barium", "Winnti", "Double Dragon"],
            "targets": ["Healthcare", "Telecommunications", "Technology", "Gaming"],
            "ttps": ["Supply Chain Attacks", "Rootkits", "Data Theft", "Ransomware"],
            "active_since": "2012",
            "sophistication": "High",
            "motivation": "Financial Gain & Espionage"
        },
        "Lazarus": {
            "country": "North Korea",
            "aliases": ["Hidden Cobra", "Guardians of Peace", "Zinc"],
            "targets": ["Financial", "Cryptocurrency", "Media", "Defense"],
            "ttps": ["Destructive Attacks", "Financial Fraud", "Ransomware", "Wiper Malware"],
            "active_since": "2009",
            "sophistication": "High",
            "motivation": "Financial Gain & Disruption"
        },
        "Charming Kitten": {
            "country": "Iran",
            "aliases": ["APT35", "Phosphorus", "Newscaster"],
            "targets": ["Government", "Defense", "Media", "Activists"],
            "ttps": ["Credential Harvesting", "Social Engineering", "Surveillance"],
            "active_since": "2014",
            "sophistication": "Medium",
            "motivation": "Espionage & Surveillance"
        }
    }
    
    MALWARE_FAMILIES = {
        "Emotet": {
            "type": "Banking Trojan/Loader",
            "first_seen": "2014",
            "capabilities": ["Credential Theft", "Lateral Movement", "Malware Delivery", "Spam Distribution"],
            "c2_protocol": "HTTP/HTTPS",
            "persistence": ["Registry", "Scheduled Tasks", "Services"],
            "targets": ["Financial", "Healthcare", "Government"],
            "status": "Active"
        },
        "TrickBot": {
            "type": "Banking Trojan/Framework",
            "first_seen": "2016",
            "capabilities": ["Banking Fraud", "Reconnaissance", "Lateral Movement", "Credential Dumping"],
            "c2_protocol": "HTTPS",
            "persistence": ["Services", "Scheduled Tasks", "WMI"],
            "targets": ["Financial", "Healthcare", "Education"],
            "status": "Active"
        },
        "Ryuk": {
            "type": "Ransomware",
            "first_seen": "2018",
            "capabilities": ["File Encryption", "Shadow Copy Deletion", "Network Propagation"],
            "c2_protocol": "N/A (No C2)",
            "persistence": ["One-time execution"],
            "targets": ["Enterprise Networks", "Healthcare", "Government"],
            "status": "Active"
        },
        "Cobalt Strike": {
            "type": "Post-Exploitation Framework",
            "first_seen": "2012",
            "capabilities": ["Remote Access", "Lateral Movement", "Credential Dumping", "Privilege Escalation"],
            "c2_protocol": ["HTTP", "HTTPS", "DNS", "SMB"],
            "persistence": ["Services", "DLL Hijacking", "Registry"],
            "targets": ["All Sectors"],
            "status": "Active (Legitimate & Malicious)"
        },
        "Qakbot": {
            "type": "Banking Trojan/Loader",
            "first_seen": "2007",
            "capabilities": ["Banking Fraud", "Email Collection", "Network Worm", "Lateral Movement"],
            "c2_protocol": "HTTPS",
            "persistence": ["Registry", "Scheduled Tasks"],
            "targets": ["Financial", "Healthcare", "Manufacturing"],
            "status": "Active"
        }
    }
    
    CRITICAL_CVES = [
        {
            "id": "CVE-2021-44228",
            "name": "Log4Shell",
            "cvss": 10.0,
            "description": "Apache Log4j2 Remote Code Execution vulnerability",
            "affected": ["Log4j 2.0-beta9 to 2.15.0"],
            "published": "2021-12-10",
            "exploit_available": True,
            "in_the_wild": True
        },
        {
            "id": "CVE-2021-34527",
            "name": "PrintNightmare",
            "cvss": 8.8,
            "description": "Windows Print Spooler Remote Code Execution",
            "affected": ["Windows Server", "Windows 10/11"],
            "published": "2021-07-02",
            "exploit_available": True,
            "in_the_wild": True
        },
        {
            "id": "CVE-2020-1472",
            "name": "Zerologon",
            "cvss": 10.0,
            "description": "Netlogon Elevation of Privilege Vulnerability",
            "affected": ["Windows Server 2008-2019"],
            "published": "2020-08-17",
            "exploit_available": True,
            "in_the_wild": True
        },
        {
            "id": "CVE-2023-23397",
            "name": "Outlook Elevation of Privilege",
            "cvss": 9.8,
            "description": "Microsoft Outlook Privilege Escalation Vulnerability",
            "affected": ["Microsoft Outlook"],
            "published": "2023-03-14",
            "exploit_available": True,
            "in_the_wild": True
        },
        {
            "id": "CVE-2022-30190",
            "name": "Follina",
            "cvss": 7.8,
            "description": "Microsoft Windows Support Diagnostic Tool (MSDT) RCE",
            "affected": ["Windows 7-11, Windows Server"],
            "published": "2022-05-30",
            "exploit_available": True,
            "in_the_wild": True
        }
    ]

# ==================== ADVANCED CYBER TERMINAL ====================
class AdvancedCyberTerminal:
    """Next-Gen Cyber Security Operations Platform"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8].upper()
        self.start_time = datetime.now()
        self.last_update = datetime.now()
        self.init_security()
        self.init_data()
        
    def init_security(self):
        """Initialize security with MFA simulation"""
        self.operators = {
            "admin": {
                "password": self.hash_pw("cyber2024"),
                "name": "Dr. Alex Morgan",
                "role": "Chief Security Officer",
                "clearance": "COSMIC TOP SECRET",
                "badge_id": "CSO-001",
                "email": "a.morgan@aegis.cyber",
                "department": "Cyber Command",
                "specializations": ["Strategic Defense", "Threat Intelligence", "Incident Command", "Policy Development"],
                "mfa_enabled": True,
                "last_login": None
            },
            "analyst": {
                "password": self.hash_pw("cyber2024"),
                "name": "Jordan Chen",
                "role": "Senior Threat Analyst",
                "clearance": "TOP SECRET",
                "badge_id": "STA-042",
                "email": "j.chen@aegis.cyber",
                "department": "Threat Analysis",
                "specializations": ["Malware Analysis", "Threat Hunting", "Digital Forensics", "Reverse Engineering"],
                "mfa_enabled": True,
                "last_login": None
            },
            "hunter": {
                "password": self.hash_pw("cyber2024"),
                "name": "Taylor Rivera",
                "role": "Threat Hunter",
                "clearance": "SECRET",
                "badge_id": "THN-087",
                "email": "t.rivera@aegis.cyber",
                "department": "Threat Hunting",
                "specializations": ["Behavioral Analysis", "IOC Development", "SIEM Analytics", "Network Forensics"],
                "mfa_enabled": True,
                "last_login": None
            }
        }
    
    def hash_pw(self, password: str) -> str:
        salt = "aegis_elite_2024_v2"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def init_data(self):
        """Initialize comprehensive data structures"""
        # Event streams with deque for performance
        self.event_log = deque(maxlen=2000)
        self.security_events = deque(maxlen=1000)
        self.network_stream = deque(maxlen=1000)
        
        # Threat data
        self.threats = []
        self.incidents = []
        self.alerts = []
        
        # Network & Assets
        self.network_segments = self.generate_network_topology()
        self.endpoints = []
        self.network_traffic = []
        
        # Intelligence
        self.iocs = []  # Indicators of Compromise
        self.threat_feeds = []
        
        # Analytics
        self.threat_history = []
        self.metrics_history = []
        
        # Populate initial data
        self.populate_data()
        
        # Threat correlation engine
        self.threat_correlations = []
        
        # Auto-response playbooks
        self.playbooks = self.init_playbooks()
    
    def init_playbooks(self):
        """Initialize automated response playbooks"""
        return {
            "ransomware": {
                "name": "Ransomware Response",
                "steps": ["Isolate affected systems", "Block C2 IPs", "Snapshot systems", "Notify stakeholders"],
                "auto_execute": ["Block C2 IPs", "Isolate affected systems"]
            },
            "data_breach": {
                "name": "Data Breach Response",
                "steps": ["Identify exfiltration path", "Block outbound traffic", "Preserve evidence", "Legal notification"],
                "auto_execute": ["Block outbound traffic"]
            },
            "apt": {
                "name": "APT Detection Response",
                "steps": ["Deep forensics", "IOC extraction", "Threat hunting", "Patch vulnerable systems"],
                "auto_execute": ["IOC extraction"]
            }
        }
    
    def generate_network_topology(self):
        """Generate realistic network segments"""
        return {
            "DMZ": {
                "subnet": "10.0.1.0/24",
                "devices": ["Web Server (10.0.1.10)", "Mail Server (10.0.1.20)", "DNS Server (10.0.1.30)"],
                "firewall_rules": 145,
                "risk_level": "High",
                "description": "Public-facing services"
            },
            "Corporate": {
                "subnet": "10.0.10.0/24",
                "devices": ["Workstations (50)", "Printers (8)", "VOIP System"],
                "firewall_rules": 89,
                "risk_level": "Medium",
                "description": "Employee workstations"
            },
            "Servers": {
                "subnet": "10.0.20.0/24",
                "devices": ["File Server", "Database Server", "Application Server", "Backup Server"],
                "firewall_rules": 67,
                "risk_level": "Critical",
                "description": "Internal servers"
            },
            "Management": {
                "subnet": "10.0.30.0/24",
                "devices": ["SIEM", "Firewall", "IDS/IPS", "Endpoint Manager"],
                "firewall_rules": 234,
                "risk_level": "Critical",
                "description": "Security infrastructure"
            },
            "Guest": {
                "subnet": "10.0.40.0/24",
                "devices": ["Guest WiFi", "Visitor Devices"],
                "firewall_rules": 23,
                "risk_level": "Low",
                "description": "Guest network (isolated)"
            }
        }
    
    def populate_data(self):
        """Populate with realistic data"""
        # Generate endpoints
        self.generate_endpoints()
        
        # Generate threats
        for _ in range(random.randint(15, 25)):
            self.generate_threat()
        
        # Generate network traffic
        for _ in range(500):
            self.generate_network_event()
        
        # Generate IOCs
        self.generate_iocs()
    
    def generate_endpoints(self):
        """Generate comprehensive endpoint inventory"""
        self.endpoints = []
        
        # Workstations
        for i in range(1, 51):
            endpoint = {
                "id": f"WS-{i:03d}",
                "hostname": f"CORP-WS-{i:03d}",
                "type": "Workstation",
                "os": random.choice(["Windows 11 Pro 22H2", "Windows 10 Enterprise LTSC", "macOS Ventura 13.2"]),
                "ip": f"10.0.10.{i}",
                "mac": f"00:1A:2B:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}",
                "user": f"user{i:03d}",
                "department": random.choice(["Engineering", "Finance", "HR", "Sales", "IT"]),
                "location": random.choice(["Building A", "Building B", "Remote"]),
                "status": random.choice(["Online"] * 8 + ["Offline", "Maintenance"]),
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 120)),
                "risk_score": random.randint(10, 95),
                "av_status": random.choice(["Protected"] * 7 + ["Warning", "Critical"]),
                "av_version": "2024.1.15.3",
                "patches_pending": random.randint(0, 25),
                "last_patch": datetime.now() - timedelta(days=random.randint(0, 30)),
                "encryption": random.choice(["BitLocker", "FileVault", "None"]),
                "firewall": random.choice(["Enabled"] * 9 + ["Disabled"]),
                "open_ports": random.sample([80, 443, 3389, 445, 139, 135], random.randint(1, 3)),
                "running_processes": random.randint(50, 150),
                "cpu_usage": random.randint(10, 80),
                "memory_usage": random.randint(30, 85),
                "disk_usage": random.randint(40, 90)
            }
            self.endpoints.append(endpoint)
        
        # Servers
        server_types = [
            ("File Server", "Windows Server 2022 Datacenter"),
            ("Database Server", "Ubuntu Server 22.04 LTS"),
            ("Web Server", "CentOS 8 Stream"),
            ("Mail Server", "Windows Server 2019 Standard"),
            ("App Server", "Red Hat Enterprise Linux 9"),
            ("Backup Server", "Windows Server 2022 Standard"),
            ("Domain Controller", "Windows Server 2022 Datacenter"),
            ("DHCP Server", "Windows Server 2019 Standard")
        ]
        
        for i, (srv_type, os) in enumerate(server_types, 1):
            endpoint = {
                "id": f"SRV-{i:03d}",
                "hostname": f"CORP-{srv_type.replace(' ', '-').upper()}",
                "type": "Server",
                "os": os,
                "ip": f"10.0.20.{i}",
                "mac": f"00:1A:2B:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}",
                "service": srv_type,
                "status": "Online",
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 15)),
                "risk_score": random.randint(20, 75),
                "av_status": "Protected",
                "av_version": "2024.1.15.3",
                "patches_pending": random.randint(0, 10),
                "last_patch": datetime.now() - timedelta(days=random.randint(0, 14)),
                "encryption": "LUKS" if "Linux" in os else "BitLocker",
                "firewall": "Enabled",
                "open_ports": random.sample([80, 443, 22, 3389, 445, 1433, 3306, 25, 53], random.randint(3, 6)),
                "running_processes": random.randint(80, 200),
                "cpu_usage": random.randint(20, 70),
                "memory_usage": random.randint(40, 80),
                "disk_usage": random.randint(50, 85),
                "uptime_days": random.randint(1, 180)
            }
            self.endpoints.append(endpoint)
    
    def generate_threat(self):
        """Generate advanced threat with MITRE mapping"""
        threat_types = [
            "Advanced Persistent Threat",
            "Ransomware Attack",
            "Phishing Campaign",
            "Data Exfiltration",
            "Malware Infection",
            "Brute Force Attack",
            "SQL Injection",
            "Zero-Day Exploit",
            "Insider Threat",
            "DDoS Attack",
            "Supply Chain Attack",
            "Cryptojacking"
        ]
        
        severities = ["Critical", "High", "Medium", "Low"]
        severity_weights = [15, 30, 40, 15]
        severity = random.choices(severities, weights=severity_weights)[0]
        
        mitre = MITREAttack.get_random_technique()
        kill_chain = MITREAttack.get_kill_chain()
        
        threat = {
            "id": f"THR-{len(self.threats) + 1:06d}",
            "type": random.choice(threat_types),
            "severity": severity,
            "confidence": random.randint(65, 99),
            "timestamp": datetime.now() - timedelta(hours=random.randint(1, 72)),
            "last_activity": datetime.now() - timedelta(minutes=random.randint(1, 180)),
            "source_ip": self.gen_external_ip(),
            "source_port": random.randint(1024, 65535),
            "dest_ip": random.choice([e["ip"] for e in self.endpoints if e["status"] == "Online"]),
            "dest_port": random.choice([80, 443, 22, 3389, 445, 1433]),
            "mitre_technique": mitre,
            "kill_chain": kill_chain,
            "status": random.choice(["Active"] * 4 + ["Investigating", "Contained"]),
            "iocs": self.generate_threat_iocs(),
            "affected_assets": random.randint(1, 15),
            "data_at_risk_gb": random.randint(10, 5000),
            "analyst_assigned": random.choice(list(self.operators.keys())),
            "notes": [],
            "containment_actions": [],
            "ai_risk_score": random.randint(60, 99),
            "predicted_impact": random.choice(["Low", "Medium", "High", "Critical"]),
            "similar_threats": random.randint(0, 5)
        }
        
        self.threats.append(threat)
        self.log_event(f"[THREAT DETECTED] {threat['type']} - {threat['severity']} severity from {threat['source_ip']}", threat['severity'])
        return threat
    
    def generate_threat_iocs(self):
        """Generate Indicators of Compromise"""
        ioc_types = [
            ("IP", lambda: self.gen_external_ip()),
            ("Domain", lambda: f"{random.choice(['malware', 'phish', 'bad', 'exploit', 'c2'])}{random.randint(100, 999)}.{random.choice(['com', 'net', 'org', 'info', 'xyz'])}"),
            ("Hash-MD5", lambda: hashlib.md5(str(random.random()).encode()).hexdigest()),
            ("Hash-SHA256", lambda: hashlib.sha256(str(random.random()).encode()).hexdigest()),
            ("File", lambda: f"{random.choice(['invoice', 'document', 'update', 'report', 'payment'])}.{random.choice(['exe', 'dll', 'scr', 'bat', 'ps1', 'vbs'])}"),
            ("URL", lambda: f"http://{random.choice(['bad', 'malware', 'phish'])}{random.randint(100, 999)}.com/{random.choice(['login', 'update', 'verify'])}")
        ]
        
        num_iocs = random.randint(3, 8)
        iocs = []
        for _ in range(num_iocs):
            ioc_type, generator = random.choice(ioc_types)
            iocs.append({
                "type": ioc_type,
                "value": generator(),
                "confidence": random.randint(70, 99),
                "first_seen": datetime.now() - timedelta(days=random.randint(1, 30)),
                "threat_score": random.randint(50, 100)
            })
        
        return iocs
    
    def generate_iocs(self):
        """Generate IOC database"""
        self.iocs = []
        for _ in range(100):
            ioc = {
                "id": f"IOC-{len(self.iocs) + 1:06d}",
                "type": random.choice(["IP", "Domain", "Hash", "URL", "Email"]),
                "value": f"ioc_value_{random.randint(1000, 9999)}",
                "threat_type": random.choice(["Malware", "Phishing", "C2", "Exploit"]),
                "confidence": random.randint(60, 99),
                "source": random.choice(["OSINT", "Internal", "Partner", "Commercial"]),
                "first_seen": datetime.now() - timedelta(days=random.randint(1, 90)),
                "last_seen": datetime.now() - timedelta(hours=random.randint(1, 48))
            }
            self.iocs.append(ioc)
    
    def generate_network_event(self):
        """Generate network traffic event"""
        protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS", "SSH", "RDP", "SMB", "FTP"]
        
        event = {
            "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 300)),
            "protocol": random.choice(protocols),
            "source_ip": random.choice([self.gen_external_ip(), self.gen_internal_ip()]),
            "dest_ip": self.gen_internal_ip(),
            "source_port": random.randint(1024, 65535),
            "dest_port": random.choice([80, 443, 22, 21, 25, 53, 3389, 445, 3306, 8080]),
            "bytes_sent": random.randint(100, 1000000),
            "bytes_received": random.randint(100, 500000),
            "packets": random.randint(10, 10000),
            "duration": random.randint(1, 300),
            "threat_score": random.randint(0, 100),
            "geo_location": random.choice(["Internal", "USA", "China", "Russia", "Germany", "Brazil", "India"]),
            "action": random.choices(["Allow", "Block", "Alert"], weights=[80, 15, 5])[0],
            "service": random.choice(["Web", "Mail", "File Transfer", "Remote Access", "Database"])
        }
        
        self.network_stream.append(event)
        return event
    
    def gen_external_ip(self):
        """Generate realistic external IP"""
        return f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def gen_internal_ip(self):
        """Generate internal IP"""
        subnet = random.choice([1, 10, 20, 30, 40])
        return f"10.0.{subnet}.{random.randint(1, 254)}"
    
    def log_event(self, message: str, severity: str = "Info"):
        """Log security event"""
        event = {
            "timestamp": datetime.now(),
            "severity": severity,
            "message": message,
            "session": self.session_id
        }
        self.event_log.append(event)
    
    def calculate_security_posture(self):
        """Advanced security posture calculation"""
        score = 100
        
        # Threat impact
        for threat in self.threats:
            if threat["status"] == "Active":
                severity_impact = {
                    "Critical": 20,
                    "High": 12,
                    "Medium": 5,
                    "Low": 2
                }
                score -= severity_impact.get(threat["severity"], 0)
        
        # Endpoint health
        critical_endpoints = len([e for e in self.endpoints if e["risk_score"] > 80])
        score -= critical_endpoints * 3
        
        # Patch compliance
        unpatched = len([e for e in self.endpoints if e["patches_pending"] > 10])
        score -= unpatched * 2
        
        # Normalize
        score = max(0, min(100, score))
        
        # Determine status
        if score >= 90:
            return score, "OPTIMAL", "#00ff41", "🟢"
        elif score >= 75:
            return score, "STRONG", "#7fff00", "🟢"
        elif score >= 60:
            return score, "GOOD", "#ffeb3b", "🟡"
        elif score >= 40:
            return score, "DEGRADED", "#ff6b00", "🟠"
        elif score >= 20:
            return score, "WEAK", "#ff3300", "🔴"
        else:
            return score, "CRITICAL", "#ff0040", "🔴"
    
    def simulate_attack(self):
        """Simulate sophisticated attack"""
        attack_scenarios = [
            {"type": "Ransomware Attack", "severity": "Critical"},
            {"type": "Advanced Persistent Threat", "severity": "Critical"},
            {"type": "Zero-Day Exploit", "severity": "Critical"},
            {"type": "Data Exfiltration", "severity": "High"},
            {"type": "Supply Chain Attack", "severity": "Critical"}
        ]
        
        scenario = random.choice(attack_scenarios)
        threat = self.generate_threat()
        threat.update(scenario)
        threat["status"] = "Active"
        
        # Update last threat in list
        self.threats[-1] = threat
        
        return threat["id"]
    
    def correlate_threats(self):
        """AI-powered threat correlation"""
        correlations = []
        
        # Group threats by source IP
        by_source = defaultdict(list)
        for threat in self.threats:
            by_source[threat["source_ip"]].append(threat)
        
        for source_ip, threats in by_source.items():
            if len(threats) > 1:
                correlations.append({
                    "type": "Multiple threats from same source",
                    "source": source_ip,
                    "threat_count": len(threats),
                    "severity": "High",
                    "threats": [t["id"] for t in threats]
                })
        
        return correlations

# ==================== STREAMLIT APP ====================

def init_session():
    """Initialize session state"""
    if 'terminal' not in st.session_state:
        st.session_state.terminal = AdvancedCyberTerminal()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'mfa_verified' not in st.session_state:
        st.session_state.mfa_verified = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def render_login():
    """Advanced login screen with MFA"""
    st.markdown('<div class="main-header">⚡ AEGIS ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-subheader">ELITE CYBER COMMAND CENTER</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #00ff41; text-align: center; margin: 0; font-family: 'Orbitron', monospace;">
                🔐 SECURE AUTHENTICATION
            </h2>
            <p style="color: #888; text-align: center; margin-top: 10px;">
                Multi-Factor Authentication Required
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            operator_id = st.text_input("👤 OPERATOR ID", placeholder="Enter your operator ID")
            access_code = st.text_input("🔑 ACCESS CODE", type="password", placeholder="Enter your access code")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("⚡ AUTHENTICATE", use_container_width=True)
            with col_b:
                clear = st.form_submit_button("✖ CLEAR", use_container_width=True)
            
            if submit:
                terminal = st.session_state.terminal
                if operator_id in terminal.operators:
                    if terminal.hash_pw(access_code) == terminal.operators[operator_id]["password"]:
                        # MFA simulation
                        mfa_code = random.randint(100000, 999999)
                        st.success(f"✓ Credentials verified! MFA Code: **{mfa_code}** (Auto-verified)")
                        
                        st.session_state.authenticated = True
                        st.session_state.mfa_verified = True
                        st.session_state.user = operator_id
                        terminal.operators[operator_id]["last_login"] = datetime.now()
                        terminal.log_event(f"Operator {terminal.operators[operator_id]['name']} authenticated successfully", "Info")
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("✗ ACCESS DENIED - Invalid credentials")
                        terminal.log_event(f"Failed authentication attempt for {operator_id}", "Warning")
                else:
                    st.error("✗ ACCESS DENIED - Unknown operator")
    
    # Demo credentials with enhanced styling
    st.markdown("---")
    st.markdown("### 🎫 AUTHORIZED OPERATORS")
    
    terminal = st.session_state.terminal
    operators = list(terminal.operators.items())
    
    cols = st.columns(len(operators))
    
    for idx, (op_id, op_data) in enumerate(operators):
        with cols[idx]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">👤</div>
                <h4 style="color: #00ff41; margin: 0;">{op_data['name']}</h4>
                <p style="color: #888; font-size: 0.8rem; margin: 5px 0;">{op_data['role']}</p>
                <p style="color: #0ff; font-size: 0.75rem; margin: 5px 0;">{op_data['badge_id']}</p>
                <hr style="border-color: rgba(0,255,65,0.2); margin: 10px 0;">
                <code style="color: #00ff41; background: rgba(0,255,65,0.1); padding: 5px 10px; border-radius: 5px; display: block; margin: 5px 0;">
                    ID: {op_id}
                </code>
                <code style="color: #0ff; background: rgba(0,255,255,0.1); padding: 5px 10px; border-radius: 5px; display: block; margin: 5px 0;">
                    CODE: cyber2024
                </code>
                <span class="badge badge-info" style="margin-top: 10px;">{op_data['clearance']}</span>
            </div>
            """, unsafe_allow_html=True)

def render_dashboard():
    """Main dashboard router"""
    terminal = st.session_state.terminal
    user_data = terminal.operators[st.session_state.user]
    
    # Enhanced Header
    score, status, color, emoji = terminal.calculate_security_posture()
    
    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 20px;">
        <div style="text-align: center;">
            <h1 style="color: #00ff41; margin: 0; font-family: 'Orbitron', monospace; font-size: 2.5rem; letter-spacing: 5px;">
                ⚡ AEGIS ELITE CYBER COMMAND ⚡
            </h1>
            <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 15px; flex-wrap: wrap;">
                <div style="color: #0ff; font-size: 1.1rem;">
                    <strong>OPERATOR:</strong> {user_data['name']} ({user_data['badge_id']})
                </div>
                <div style="color: #0ff; font-size: 1.1rem;">
                    <strong>ROLE:</strong> {user_data['role']}
                </div>
                <div style="color: #ffeb3b; font-size: 1.1rem;">
                    <strong>CLEARANCE:</strong> {user_data['clearance']}
                </div>
                <div style="color: {color}; font-size: 1.1rem;">
                    <strong>SESSION:</strong> {terminal.session_id}
                </div>
            </div>
            <div style="margin-top: 10px; color: #888; font-size: 0.9rem;">
                {datetime.now().strftime('%A, %B %d, %Y • %H:%M:%S UTC')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚡ QUICK ACTIONS")
        
        if st.button("🔄 REFRESH DATA", use_container_width=True, key="refresh"):
            terminal.populate_data()
            st.rerun()
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True, key="simulate"):
            attack_id = terminal.simulate_attack()
            st.success(f"✓ Attack simulated: {attack_id}")
            time.sleep(0.5)
            st.rerun()
        
        if st.button("🎯 THREAT HUNT", use_container_width=True, key="hunt"):
            st.info("Threat hunt initiated...")
        
        st.markdown("---")
        st.markdown("### 🎯 COMMAND MODULES")
        
        module = st.radio("", [
            "🏠 Command Center",
            "🌐 Network Operations",
            "💻 Endpoint Security",
            "🔍 Threat Intelligence",
            "🚨 Active Incidents",
            "📡 Live Monitoring",
            "🎮 Cyber Warfare",
            "📊 Advanced Analytics",
            "🛡️ Defense Arsenal",
            "🔬 Forensics Lab"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📊 SYSTEM STATUS")
        st.markdown(f"""
        <div class="glass-card">
            <p style="margin: 5px 0;">🟢 <strong>SIEM:</strong> Online</p>
            <p style="margin: 5px 0;">🟢 <strong>Firewall:</strong> Active</p>
            <p style="margin: 5px 0;">🟢 <strong>IDS/IPS:</strong> Monitoring</p>
            <p style="margin: 5px 0;">🟢 <strong>EDR:</strong> Protected</p>
            <p style="margin: 5px 0; color: {color};"><strong>Posture:</strong> {status} {emoji}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 TERMINATE SESSION", use_container_width=True):
            terminal.log_event(f"Operator {user_data['name']} logged out", "Info")
            st.session_state.authenticated = False
            st.session_state.mfa_verified = False
            st.session_state.user = None
            st.rerun()
    
    # Route to modules
    if "Command Center" in module:
        render_command_center(terminal, user_data)
    elif "Network Operations" in module:
        render_network_ops(terminal, user_data)
    elif "Endpoint Security" in module:
        render_endpoint_security(terminal, user_data)
    elif "Threat Intelligence" in module:
        render_threat_intel(terminal, user_data)
    elif "Active Incidents" in module:
        render_active_incidents(terminal, user_data)
    elif "Live Monitoring" in module:
        render_live_monitoring(terminal, user_data)
    elif "Cyber Warfare" in module:
        render_cyber_warfare(terminal, user_data)
    elif "Advanced Analytics" in module:
        render_analytics(terminal, user_data)
    elif "Defense Arsenal" in module:
        render_defense_arsenal(terminal, user_data)
    elif "Forensics Lab" in module:
        render_forensics(terminal, user_data)

# ==================== MODULE RENDERERS ====================

def render_command_center(terminal, user):
    """Elite command center dashboard"""
    
    # Security Posture - Large Display
    score, status, color, emoji = terminal.calculate_security_posture()
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 40px; margin-bottom: 30px;">
        <h1 style="color: {color}; font-size: 4rem; margin: 0; font-family: 'Orbitron', monospace; text-shadow: 0 0 30px {color};">
            {emoji} SECURITY POSTURE: {status}
        </h1>
        <h2 style="color: {color}; font-size: 3rem; margin: 20px 0;">
            {score} / 100
        </h2>
        <div class="progress-bar" style="max-width: 800px; margin: 30px auto; height: 20px;">
            <div class="progress-fill" style="width: {score}%; background: linear-gradient(90deg, {color} 0%, {color} 100%);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics - Enhanced
    col1, col2, col3, col4, col5 = st.columns(5)
    
    critical = len([t for t in terminal.threats if t.get("severity") == "Critical"])
    active = len([t for t in terminal.threats if t.get("status") == "Active"])
    endpoints = len([e for e in terminal.endpoints if e.get("status") == "Online"])
    at_risk = len([e for e in terminal.endpoints if e.get("risk_score", 0) > 70])
    blocked = len([e for e in terminal.network_stream if e.get("action") == "Block"])
    
    metrics = [
        (col1, critical, "CRITICAL THREATS", "#ff0040", "🔴", "+2"),
        (col2, active, "ACTIVE INCIDENTS", "#ff6b00", "⚠️", "-1"),
        (col3, endpoints, "ENDPOINTS ONLINE", "#00ff41", "💻", "0"),
        (col4, at_risk, "AT RISK ASSETS", "#ffeb3b", "⚡", "+3"),
        (col5, blocked, "THREATS BLOCKED", "#0ff", "🛡️", "+15")
    ]
    
    for col, value, label, color, icon, trend in metrics:
        with col:
            trend_color = "#00ff41" if "+" in trend and int(trend) > 0 else "#ff0040" if "-" in trend else "#888"
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-trend" style="color: {trend_color};">{trend}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Content Area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔥 CRITICAL THREAT FEED")
        
        critical_threats = [t for t in terminal.threats if t.get("severity") in ["Critical", "High"] and t.get("status") == "Active"][:8]
        
        if critical_threats:
            for threat in critical_threats:
                severity = threat.get("severity", "Low")
                sev_colors = {
                    "Critical": "#ff0040",
                    "High": "#ff6b00",
                    "Medium": "#ffeb3b",
                    "Low": "#00ff41"
                }
                color = sev_colors.get(severity, "#00ff41")
                
                st.markdown(f"""
                <div class="threat-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="color: #fff; margin: 0; font-size: 1.1rem;">{threat.get('type', 'Unknown')}</h4>
                            <p style="color: #888; margin: 5px 0; font-size: 0.85rem;">{threat.get('id', 'N/A')}</p>
                        </div>
                        <span class="badge badge-{severity.lower()}">{severity}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.9rem;">
                        <span class="ip-address">{threat.get('source_ip', '0.0.0.0')}</span> → 
                        <span class="ip-address">{threat.get('dest_ip', '0.0.0.0')}</span>
                    </div>
                    <div style="margin-top: 10px; color: #aaa; font-size: 0.85rem;">
                        <strong>MITRE:</strong> {threat.get('mitre_technique', {}).get('id', 'N/A')} - {threat.get('mitre_technique', {}).get('name', 'Unknown')}<br>
                        <strong>Confidence:</strong> {threat.get('confidence', 0)}% | 
                        <strong>Assets:</strong> {threat.get('affected_assets', 0)} | 
                        <strong>AI Risk:</strong> {threat.get('ai_risk_score', 0)}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-card">
                <h3 style="color: #00ff41; margin: 0;">✓ NO CRITICAL THREATS DETECTED</h3>
                <p style="color: #888; margin-top: 10px;">All systems operating normally</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📡 LIVE EVENT STREAM")
        
        st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
        
        events = list(terminal.event_log)[-20:]
        for event in reversed(events):
            severity = event.get('severity', 'Info')
            sev_class = f"log-{severity.lower()}"
            ts = event['timestamp'].strftime('%H:%M:%S')
            
            icon_map = {
                "Critical": "🔴",
                "High": "🟠",
                "Warning": "🟡",
                "Medium": "🟡",
                "Info": "🔵",
                "Low": "🟢"
            }
            icon = icon_map.get(severity, "⚪")
            
            st.markdown(f"""
            <div class="log-line {sev_class}">
                {icon} [{ts}] [{severity.upper()}] {event['message']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Threat Radar
    st.markdown("### 🎯 THREAT DETECTION RADAR")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="radar-container">
            <div class="radar-circle" style="width: 400px; height: 400px;"></div>
            <div class="radar-circle" style="width: 300px; height: 300px;"></div>
            <div class="radar-circle" style="width: 200px; height: 200px;"></div>
            <div class="radar-circle" style="width: 100px; height: 100px;"></div>
            <div class="radar-sweep"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Network Activity Heatmap
    st.markdown("### 🔥 24-HOUR ACTIVITY HEATMAP")
    
    hours = list(range(24))
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    heatmap_data = []
    for day in days:
        row = []
        for hour in hours:
            intensity = random.randint(0, 100)
            row.append(intensity)
        heatmap_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=hours,
        y=days,
        colorscale=[
            [0, '#0a0e27'],
            [0.25, '#00ff41'],
            [0.5, '#ffeb3b'],
            [0.75, '#ff6b00'],
            [1, '#ff0040']
        ],
        showscale=True
    ))
    
    fig.update_layout(
        title="Network Activity Intensity",
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#00ff41',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_network_ops(terminal, user):
    """Advanced network operations center"""
    st.markdown("## 🌐 NETWORK OPERATIONS CENTER")
    
    # Network Topology
    st.markdown("### 🗺️ NETWORK TOPOLOGY")
    
    for seg_name, seg_data in terminal.network_segments.items():
        risk_colors = {
            "Critical": "#ff0040",
            "High": "#ff6b00",
            "Medium": "#ffeb3b",
            "Low": "#00ff41"
        }
        color = risk_colors.get(seg_data["risk_level"], "#00ff41")
        
        with st.expander(f"📍 {seg_name} Network - {seg_data['subnet']}", expanded=False):
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4 style="color: #00ff41; margin: 0;">{seg_name} Segment</h4>
                        <p style="color: #888; margin: 5px 0;">{seg_data['description']}</p>
                    </div>
                    <span class="badge badge-{seg_data['risk_level'].lower()}">{seg_data['risk_level']} RISK</span>
                </div>
                <hr style="border-color: rgba(0,255,65,0.2); margin: 15px 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div>
                        <strong style="color: #0ff;">Subnet:</strong><br>
                        <code style="color: #00ff41;">{seg_data['subnet']}</code>
                    </div>
                    <div>
                        <strong style="color: #0ff;">Firewall Rules:</strong><br>
                        <code style="color: #00ff41;">{seg_data['firewall_rules']}</code>
                    </div>
                    <div>
                        <strong style="color: #0ff;">Devices:</strong><br>
                        {'<br>'.join([f"<code style='color: #888;'>{d}</code>" for d in seg_data['devices'][:3]])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔒 Lockdown {seg_name}", key=f"lock_{seg_name}"):
                    st.success(f"✓ {seg_name} segment locked down")
            with col2:
                if st.button(f"🔍 Deep Scan {seg_name}", key=f"scan_{seg_name}"):
                    st.info(f"Scanning {seg_name}...")
            with col3:
                if st.button(f"📊 Analytics {seg_name}", key=f"analytics_{seg_name}"):
                    st.info(f"Generating analytics for {seg_name}...")
    
    # Live Traffic Analysis
    st.markdown("### 📊 LIVE TRAFFIC ANALYSIS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Protocol distribution
        protocols = defaultdict(int)
        for event in list(terminal.network_stream)[:200]:
            protocols[event.get('protocol', 'UNKNOWN')] += 1
        
        if protocols:
            fig = go.Figure(data=[go.Pie(
                labels=list(protocols.keys()),
                values=list(protocols.values()),
                hole=0.4,
                marker=dict(
                    colors=['#00ff41', '#0ff', '#ffeb3b', '#ff6b00', '#ff0040'],
                    line=dict(color='#000', width=2)
                )
            )])
            
            fig.update_layout(
                title="Protocol Distribution",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#00ff41',
                showlegend=True,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Traffic over time
        timestamps = []
        traffic_volume = []
        
        for i in range(60):
            timestamps.append((datetime.now() - timedelta(seconds=60-i)).strftime('%H:%M:%S'))
            traffic_volume.append(random.randint(100, 1000))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=traffic_volume,
            mode='lines',
            name='Traffic Volume',
            line=dict(color='#00ff41', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 65, 0.2)'
        ))
        
        fig.update_layout(
            title="Network Traffic (Last 60 Seconds)",
            xaxis_title="Time",
            yaxis_title="Packets/sec",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#00ff41',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Talkers
    st.markdown("### 🔝 TOP NETWORK TALKERS")
    
    talkers = []
    for _ in range(10):
        talkers.append({
            "IP": terminal.gen_internal_ip(),
            "Packets": random.randint(1000, 100000),
            "Bytes": random.randint(1000000, 10000000),
            "Connections": random.randint(10, 500),
            "Risk": random.choice(["Low", "Medium", "High"])
        })
    
    df = pd.DataFrame(talkers)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_endpoint_security(terminal, user):
    """Advanced endpoint security management"""
    st.markdown("## 💻 ENDPOINT SECURITY MANAGEMENT")
    
    # Overview metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total = len(terminal.endpoints)
    online = len([e for e in terminal.endpoints if e.get("status") == "Online"])
    critical = len([e for e in terminal.endpoints if e.get("risk_score", 0) > 80])
    protected = len([e for e in terminal.endpoints if e.get("av_status") == "Protected"])
    unpatched = len([e for e in terminal.endpoints if e.get("patches_pending", 0) > 10])
    
    metrics = [
        (col1, total, "TOTAL ENDPOINTS", "#0ff"),
        (col2, online, "ONLINE", "#00ff41"),
        (col3, critical, "CRITICAL RISK", "#ff0040"),
        (col4, protected, "PROTECTED", "#00ff41"),
        (col5, unpatched, "NEED PATCHES", "#ffeb3b")
    ]
    
    for col, value, label, color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Filters
    st.markdown("### 🔍 FILTER & SEARCH")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_type = st.selectbox("Type", ["All", "Workstation", "Server"])
    with col2:
        filter_status = st.selectbox("Status", ["All", "Online", "Offline", "Maintenance"])
    with col3:
        filter_risk = st.selectbox("Risk Level", ["All", "Critical", "High", "Medium", "Low"])
    with col4:
        search = st.text_input("Search", placeholder="Search by ID or hostname...")
    
    # Filter endpoints
    filtered = terminal.endpoints.copy()
    
    if filter_type != "All":
        filtered = [e for e in filtered if e.get("type") == filter_type]
    
    if filter_status != "All":
        filtered = [e for e in filtered if e.get("status") == filter_status]
    
    if filter_risk != "All":
        risk_ranges = {"Critical": (80, 100), "High": (60, 80), "Medium": (40, 60), "Low": (0, 40)}
        min_r, max_r = risk_ranges[filter_risk]
        filtered = [e for e in filtered if min_r < e.get("risk_score", 0) <= max_r]
    
    if search:
        filtered = [e for e in filtered if search.lower() in e.get("id", "").lower() or search.lower() in e.get("hostname", "").lower()]
    
    # Display endpoints
    st.markdown(f"### 📋 ENDPOINTS ({len(filtered)} results)")
    
    for endpoint in filtered[:15]:
        risk_score = endpoint.get("risk_score", 0)
        
        if risk_score > 80:
            risk_color = "#ff0040"
            risk_label = "CRITICAL"
        elif risk_score > 60:
            risk_color = "#ff6b00"
            risk_label = "HIGH"
        elif risk_score > 40:
            risk_color = "#ffeb3b"
            risk_label = "MEDIUM"
        else:
            risk_color = "#00ff41"
            risk_label = "LOW"
        
        with st.expander(f"{'🖥️' if endpoint.get('type') == 'Workstation' else '🖧'} {endpoint.get('hostname', 'Unknown')} - Risk: {risk_score}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #00ff41; margin-top: 0;">SYSTEM INFO</h4>
                    <p><strong>ID:</strong> {endpoint.get('id', 'N/A')}</p>
                    <p><strong>Type:</strong> {endpoint.get('type', 'N/A')}</p>
                    <p><strong>OS:</strong> {endpoint.get('os', 'N/A')}</p>
                    <p><strong>IP:</strong> <span class="ip-address">{endpoint.get('ip', '0.0.0.0')}</span></p>
                    <p><strong>MAC:</strong> {endpoint.get('mac', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #0ff; margin-top: 0;">SECURITY STATUS</h4>
                    <p><strong>Risk Score:</strong> <span style="color: {risk_color};">{risk_score}</span></p>
                    <p><strong>AV Status:</strong> {endpoint.get('av_status', 'N/A')}</p>
                    <p><strong>Firewall:</strong> {endpoint.get('firewall', 'N/A')}</p>
                    <p><strong>Encryption:</strong> {endpoint.get('encryption', 'N/A')}</p>
                    <p><strong>Patches Pending:</strong> {endpoint.get('patches_pending', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #ffeb3b; margin-top: 0;">PERFORMANCE</h4>
                    <p><strong>CPU:</strong> {endpoint.get('cpu_usage', 0)}%</p>
                    <p><strong>Memory:</strong> {endpoint.get('memory_usage', 0)}%</p>
                    <p><strong>Disk:</strong> {endpoint.get('disk_usage', 0)}%</p>
                    <p><strong>Processes:</strong> {endpoint.get('running_processes', 0)}</p>
                    <p><strong>Last Seen:</strong> {endpoint.get('last_seen', datetime.now()).strftime('%H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Actions
            st.markdown("#### 🎯 ACTIONS")
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                if st.button("🔄 Scan", key=f"scan_{endpoint.get('id')}"):
                    st.success("Scan initiated")
            with col_b:
                if st.button("🔒 Isolate", key=f"isolate_{endpoint.get('id')}"):
                    st.warning("Endpoint isolated")
            with col_c:
                if st.button("🛡️ Update", key=f"update_{endpoint.get('id')}"):
                    st.info("Updates deploying...")
            with col_d:
                if st.button("📊 Details", key=f"details_{endpoint.get('id')}"):
                    st.info("Loading details...")

def render_threat_intel(terminal, user):
    """Advanced threat intelligence platform"""
    st.markdown("## 🔍 THREAT INTELLIGENCE PLATFORM")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 APT Groups", "🦠 Malware Families", "🕳️ CVE Database", "📡 IOC Feed"])
    
    with tab1:
        st.markdown("### 🌍 ADVANCED PERSISTENT THREAT GROUPS")
        
        for apt_name, apt_data in ThreatIntel.APT_GROUPS.items():
            with st.expander(f"🎯 {apt_name} - {apt_data['country']}", expanded=False):
                st.markdown(f"""
                <div class="threat-card">
                    <h3 style="color: #ff0040; margin-top: 0;">{apt_name}</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 15px;">
                        <div>
                            <h4 style="color: #0ff;">ATTRIBUTION</h4>
                            <p><strong>Country:</strong> {apt_data['country']}</p>
                            <p><strong>Also Known As:</strong><br>{', '.join(apt_data['aliases'])}</p>
                            <p><strong>Active Since:</strong> {apt_data['active_since']}</p>
                        </div>
                        <div>
                            <h4 style="color: #ffeb3b;">OPERATIONS</h4>
                            <p><strong>Sophistication:</strong> <span class="badge badge-critical">{apt_data['sophistication']}</span></p>
                            <p><strong>Motivation:</strong> {apt_data['motivation']}</p>
                            <p><strong>Target Sectors:</strong><br>{', '.join(apt_data['targets'])}</p>
                        </div>
                        <div>
                            <h4 style="color: #00ff41;">TACTICS & TECHNIQUES</h4>
                            {'<br>'.join([f"• {ttp}" for ttp in apt_data['ttps']])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🦠 MALWARE THREAT DATABASE")
        
        for malware_name, malware_data in ThreatIntel.MALWARE_FAMILIES.items():
            status_color = "#00ff41" if "Active" in malware_data['status'] else "#888"
            
            with st.expander(f"🦠 {malware_name} - {malware_data['type']}", expanded=False):
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="color: #ff6b00; margin-top: 0;">{malware_name}</h3>
                    <span class="badge badge-medium">{malware_data['type']}</span>
                    <span class="badge" style="background: {status_color}; color: #000; margin-left: 10px;">{malware_data['status']}</span>
                    
                    <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                        <div>
                            <h4 style="color: #0ff;">CHARACTERISTICS</h4>
                            <p><strong>First Seen:</strong> {malware_data['first_seen']}</p>
                            <p><strong>C2 Protocol:</strong> {', '.join(malware_data['c2_protocol']) if isinstance(malware_data['c2_protocol'], list) else malware_data['c2_protocol']}</p>
                            <p><strong>Persistence:</strong><br>{', '.join(malware_data['persistence'])}</p>
                        </div>
                        <div>
                            <h4 style="color: #ffeb3b;">CAPABILITIES</h4>
                            {'<br>'.join([f"✓ {cap}" for cap in malware_data['capabilities']])}
                        </div>
                        <div>
                            <h4 style="color: #ff6b00;">TARGETING</h4>
                            <p><strong>Primary Targets:</strong><br>{', '.join(malware_data['targets'])}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🕳️ CRITICAL VULNERABILITY INTELLIGENCE")
        
        for cve in ThreatIntel.CRITICAL_CVES:
            cvss = cve['cvss']
            
            if cvss >= 9.0:
                severity_color = "#ff0040"
                severity_label = "CRITICAL"
            elif cvss >= 7.0:
                severity_color = "#ff6b00"
                severity_label = "HIGH"
            else:
                severity_color = "#ffeb3b"
                severity_label = "MEDIUM"
            
            with st.expander(f"🕳️ {cve['id']} - {cve['name']} (CVSS: {cvss})", expanded=False):
                st.markdown(f"""
                <div class="threat-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="color: {severity_color}; margin: 0;">{cve['id']}: {cve['name']}</h3>
                        <span class="badge" style="background: {severity_color}; color: #fff; font-size: 1.2rem;">CVSS {cvss}</span>
                    </div>
                    
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <p style="font-size: 1.1rem; color: #fff; margin: 0;">{cve['description']}</p>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
                        <div>
                            <strong style="color: #0ff;">Severity:</strong><br>
                            <span class="badge" style="background: {severity_color}; color: #fff;">{severity_label}</span>
                        </div>
                        <div>
                            <strong style="color: #0ff;">Published:</strong><br>
                            <code>{cve['published']}</code>
                        </div>
                        <div>
                            <strong style="color: #0ff;">Exploit Available:</strong><br>
                            <span style="color: {'#ff0040' if cve['exploit_available'] else '#00ff41'};">{'YES ⚠️' if cve['exploit_available'] else 'NO ✓'}</span>
                        </div>
                        <div>
                            <strong style="color: #0ff;">In The Wild:</strong><br>
                            <span style="color: {'#ff0040' if cve['in_the_wild'] else '#00ff41'};">{'YES ⚠️' if cve['in_the_wild'] else 'NO ✓'}</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 15px;">
                        <strong style="color: #ffeb3b;">Affected Software:</strong><br>
                        {', '.join(cve['affected'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📡 INDICATORS OF COMPROMISE (IOC) FEED")
        
        # IOC stats
        col1, col2, col3, col4 = st.columns(4)
        
        ioc_by_type = defaultdict(int)
        for ioc in terminal.iocs:
            ioc_by_type[ioc.get('type', 'Unknown')] += 1
        
        total_iocs = len(terminal.iocs)
        high_conf = len([i for i in terminal.iocs if i.get('confidence', 0) > 80])
        
        with col1:
            st.metric("Total IOCs", total_iocs)
        with col2:
            st.metric("High Confidence", high_conf)
        with col3:
            st.metric("IP Addresses", ioc_by_type.get('IP', 0))
        with col4:
            st.metric("Domains", ioc_by_type.get('Domain', 0))
        
        # IOC table
        ioc_df = pd.DataFrame(terminal.iocs[:50])
        st.dataframe(ioc_df, use_container_width=True, hide_index=True)

def render_active_incidents(terminal, user):
    """Active incident management"""
    st.markdown("## 🚨 ACTIVE INCIDENT RESPONSE")
    
    active_incidents = [t for t in terminal.threats if t.get("status") == "Active"]
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 30px;">
        <h1 style="color: #ff0040; font-size: 3rem; margin: 0;">
            🔥 {len(active_incidents)} ACTIVE INCIDENTS
        </h1>
        <p style="color: #888; margin-top: 10px; font-size: 1.2rem;">Requiring immediate attention</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not active_incidents:
        st.markdown("""
        <div class="success-card" style="text-align: center; padding: 40px;">
            <h2 style="color: #00ff41; margin: 0;">✓ ALL CLEAR</h2>
            <p style="color: #888; margin-top: 10px; font-size: 1.1rem;">No active incidents detected</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for incident in active_incidents:
        severity = incident.get("severity", "Low")
        sev_colors = {"Critical": "#ff0040", "High": "#ff6b00", "Medium": "#ffeb3b", "Low": "#00ff41"}
        color = sev_colors.get(severity, "#00ff41")
        
        with st.expander(f"🚨 {incident.get('id')} - {incident.get('type')} [{severity}]", expanded=True):
            # Incident header
            st.markdown(f"""
            <div class="threat-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="color: #fff; margin: 0;">{incident.get('type', 'Unknown Threat')}</h2>
                    <span class="badge badge-{severity.lower()}" style="font-size: 1.2rem;">{severity}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Incident details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #0ff;">THREAT DETAILS</h4>
                    <p><strong>Incident ID:</strong> {incident.get('id')}</p>
                    <p><strong>First Detected:</strong><br>{incident.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Last Activity:</strong><br>{incident.get('last_activity', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Source:</strong> <span class="ip-address">{incident.get('source_ip')}</span></p>
                    <p><strong>Target:</strong> <span class="ip-address">{incident.get('dest_ip')}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                mitre = incident.get('mitre_technique', {})
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #ffeb3b;">ATTACK ANALYSIS</h4>
                    <p><strong>MITRE ATT&CK:</strong><br>{mitre.get('id', 'N/A')} - {mitre.get('name', 'Unknown')}</p>
                    <p><strong>Tactic:</strong><br>{mitre.get('tactic', 'Unknown')}</p>
                    <p><strong>Confidence Score:</strong> {incident.get('confidence', 0)}%</p>
                    <p><strong>AI Risk Score:</strong> {incident.get('ai_risk_score', 0)}%</p>
                    <p><strong>Affected Assets:</strong> {incident.get('affected_assets', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                kill_chain = incident.get('kill_chain', {})
                current_stage = kill_chain.get('current_stage', 0)
                stages = kill_chain.get('stages', [])
                
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #ff6b00;">CYBER KILL CHAIN</h4>
                    <p><strong>Current Stage:</strong><br>{stages[current_stage] if stages else 'Unknown'}</p>
                    <p><strong>Progress:</strong></p>
                """, unsafe_allow_html=True)
                
                for idx, stage in enumerate(stages):
                    if idx <= current_stage:
                        st.markdown(f"✓ <span style='color: #00ff41;'>{stage}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"○ <span style='color: #888;'>{stage}</span>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # IOCs
            st.markdown("#### 📡 INDICATORS OF COMPROMISE")
            
            iocs = incident.get('iocs', [])
            if iocs:
                ioc_cols = st.columns(min(len(iocs), 3))
                for idx, ioc in enumerate(iocs[:3]):
                    with ioc_cols[idx]:
                        st.markdown(f"""
                        <div class="glass-card">
                            <strong style="color: #0ff;">{ioc.get('type', 'Unknown')}</strong><br>
                            <code style="color: #ffeb3b; word-break: break-all;">{ioc.get('value', 'N/A')}</code><br>
                            <small>Confidence: {ioc.get('confidence', 0)}%</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Response Actions
            st.markdown("#### 🎯 RESPONSE ACTIONS")
            
            col_a, col_b, col_c, col_d, col_e = st.columns(5)
            
            with col_a:
                if st.button("🛑 CONTAIN", key=f"contain_{incident.get('id')}", use_container_width=True):
                    incident['status'] = "Contained"
                    terminal.log_event(f"Incident {incident.get('id')} contained", "Warning")
                    st.success("✓ Threat contained!")
                    time.sleep(0.5)
                    st.rerun()
            
            with col_b:
                if st.button("🚫 BLOCK IP", key=f"block_{incident.get('id')}", use_container_width=True):
                    st.success(f"✓ IP {incident.get('source_ip')} blocked")
            
            with col_c:
                if st.button("🔍 INVESTIGATE", key=f"investigate_{incident.get('id')}", use_container_width=True):
                    st.info("Deep investigation initiated...")
            
            with col_d:
                if st.button("📋 PLAYBOOK", key=f"playbook_{incident.get('id')}", use_container_width=True):
                    st.info("Executing response playbook...")
            
            with col_e:
                if st.button("📊 REPORT", key=f"report_{incident.get('id')}", use_container_width=True):
                    st.info("Generating incident report...")

def render_live_monitoring(terminal, user):
    """Live monitoring dashboard"""
    st.markdown("## 📡 LIVE THREAT MONITORING")
    
    # Auto-refresh indicator
    st.markdown("""
    <div class="glass-card" 
