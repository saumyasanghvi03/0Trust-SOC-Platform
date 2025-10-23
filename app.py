import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import time
import random
import threading
from typing import Dict, List, Any
import warnings
from cryptography.fernet import Fernet
import ipaddress
import re
import math
from collections import deque
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CYBER COMMAND v3.0",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- REALISM ENHANCEMENT: ADVANCED CSS ---
# Added scanlines, flickering, and a more authentic terminal font.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    .main-header {
        font-size: 2.8rem;
        color: #00ff00;
        text-align: center;
        font-family: 'Roboto Mono', monospace;
        text-shadow: 0 0 15px #00ff00;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: 4px;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
        to { text-shadow: 0 0 20px #00ff00, 0 0 35px #00ff00, 0 0 50px #00ff00; }
    }
    .cyber-terminal {
        background-color: #0a0a0a;
        color: #00ff00;
        font-family: 'Roboto Mono', monospace;
    }
    body {
        background-color: #0a0a0a;
    }
    .stApp {
        background: #0a0a0a;
        position: relative;
        overflow: hidden;
    }
    .stApp::after {
        content: " ";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: rgba(18, 16, 16, 0.1);
        opacity: 0;
        z-index: 2;
        pointer-events: none;
        animation: flicker 0.15s infinite;
    }
    @keyframes flicker {
        0% { opacity: 0.1; }
        50% { opacity: 0.2; }
        100% { opacity: 0.1; }
    }
    .dashboard-panel {
        background: #0d0d0d;
        border: 1px solid #00ff00;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
    }
    .threat-panel {
        background: linear-gradient(135deg, #2a0a0a 0%, #1a0505 100%);
        border: 1px solid #ff0000;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse-red 3s infinite;
    }
    @keyframes pulse-red {
        0% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255, 0, 0, 0.3); }
        50% { border-color: #ff4444; box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); }
        100% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255, 0, 0, 0.3); }
    }
    .metric-glowing {
        background: #0d0d0d;
        border: 1px solid #00ff00;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: box-shadow 0.5s ease-in-out;
    }
    .metric-glowing:hover {
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
    }
    .log-entry {
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9em;
        color: #00ff00;
        padding: 0.2rem 0;
    }
    .live-terminal-output {
        background-color: #000;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Roboto Mono', monospace;
        color: #00ff00;
        height: 400px;
        overflow-y: scroll;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-shadow: inset 0 0 15px rgba(0,255,0,0.3);
    }
    /* Hide scrollbar for Chrome, Safari and Opera */
    .live-terminal-output::-webkit-scrollbar {
        display: none;
    }
    /* Hide scrollbar for IE, Edge and Firefox */
    .live-terminal-output {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
</style>
""", unsafe_allow_html=True)


class AdvancedCyberTerminal:
    def __init__(self):
        if 'initialized' in st.session_state:
            return
        st.session_state.initialized = True
        
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.initialize_cyber_terminal()
        
    def initialize_cyber_terminal(self):
        # --- REALISM ENHANCEMENT: DYNAMIC STATE ---
        st.session_state.live_threats = deque(maxlen=50)
        st.session_state.network_activity = deque(maxlen=1000)
        st.session_state.ids_alerts = deque(maxlen=200)
        st.session_state.terminal_log = deque(maxlen=100)
        st.session_state.defense_actions = deque(maxlen=50)
        st.session_state.blocked_ips = set()
        st.session_state.quarantined_endpoints = set()
        st.session_state.last_update = time.time()
        
        self.cyber_team = {
            "commander": {"user_id": "commander", "password": self.hash_password("alpha-one"), "first_name": "Alex", "last_name": "Thorne", "role": "Commander", "clearance": "TOP SECRET"},
            "hunter": {"user_id": "hunter", "password": self.hash_password("bravo-seven"), "first_name": "Jordan", "last_name": "Reyes", "role": "Threat Hunter", "clearance": "SECRET"},
            "analyst": {"user_id": "analyst", "password": self.hash_password("charlie-three"), "first_name": "Casey", "last_name": "Zhang", "role": "Defense Analyst", "clearance": "SECRET"}
        }
        self.generate_initial_data()
        self.log_to_terminal("System Initialized. CYBER COMMAND v3.0 is online.")

    def hash_password(self, password: str) -> str:
        salt = "cyber_terminal_salt_v3"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed

    def authenticate_user(self, username: str, password: str) -> bool:
        if username in self.cyber_team and self.verify_password(password, self.cyber_team[username]["password"]):
            self.log_to_terminal(f"Operator {username.upper()} authenticated. Access granted.")
            return True
        self.log_to_terminal(f"Access Denied. Failed login attempt for operator: {username.upper()}", level="WARN")
        return False

    def log_to_terminal(self, message, level="INFO"):
        """Logs a message to the live terminal display."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_levels = {"INFO": "00ff00", "WARN": "ffff00", "CRITICAL": "ff0000", "ACTION": "00ffff"}
        color = log_levels.get(level, "00ff00")
        log_entry = f"<span style='color:#{color}'>[{timestamp} {level}]</span> {message}"
        st.session_state.terminal_log.append(log_entry)

    def generate_initial_data(self):
        for _ in range(20): self.generate_network_activity_entry()
        for _ in range(5): self.generate_ids_alert_entry()
        self.log_to_terminal("Initial data streams populated.")

    # --- REALISM ENHANCEMENT: CONTINUOUS DATA GENERATION ---
    def update_live_data(self):
        """This is the 'heartbeat' of the app, run on every refresh."""
        now = time.time()
        if now - st.session_state.last_update > 1: # Update every 1 second
            # Generate a burst of new data
            for _ in range(random.randint(1, 5)):
                self.generate_network_activity_entry()
            
            if random.random() < 0.1: # 10% chance per second to generate a new IDS alert
                self.generate_ids_alert_entry()

            st.session_state.last_update = now

    def generate_network_activity_entry(self, flagged=False, attacker_ip=None):
        source_ip = attacker_ip if attacker_ip else f"192.168.1.{random.randint(10, 250)}"
        dest_ip = f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Check if the source IP is on the blocked list
        if source_ip in st.session_state.blocked_ips:
            self.log_to_terminal(f"Blocked connection attempt from {source_ip}", level="ACTION")
            return # Don't add it to the activity log

        activity = {
            "timestamp": datetime.now(), "source_ip": source_ip, "dest_ip": dest_ip,
            "dest_port": random.choice([80, 443, 22, 53, 3389]),
            "protocol": random.choice(["TCP", "UDP", "HTTPS", "DNS"]),
            "bytes_sent": random.randint(100, 10000), "threat_score": random.randint(0, 40),
            "flagged": flagged
        }
        if flagged:
            activity["threat_score"] = random.randint(70, 95)
        st.session_state.network_activity.append(activity)

    def generate_ids_alert_entry(self, attack_type=None, attacker_ip=None):
        alert = {
            "alert_id": f"IDS-{random.randint(10000, 99999)}", "timestamp": datetime.now(),
            "attack_type": attack_type or random.choice(["Port Scan", "SQL Injection Attempt", "XSS Probe"]),
            "source_ip": attacker_ip or f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "severity": random.choice(["Medium", "High"]),
            "action_taken": "Alerted"
        }
        st.session_state.ids_alerts.append(alert)
        self.log_to_terminal(f"IDS Alert: {alert['attack_type']} from {alert['source_ip']}", level="WARN")

    # --- REALISM ENHANCEMENT: DYNAMIC ATTACK SIMULATION ---
    def simulate_live_attack(self, attack_type: str):
        """Simulates a coordinated attack, generating a flurry of related events."""
        attacker_ip = f"{random.randint(100, 200)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        target = random.choice(["Web Server 01", "Database Cluster", "File Server 03"])
        self.log_to_terminal(f"!!! CRITICAL ALERT: Coordinated {attack_type} attack detected from {attacker_ip} targeting {target} !!!", level="CRITICAL")

        attack_id = f"ATTACK-{random.randint(1000, 9999)}"
        new_threat = {
            "threat_id": attack_id, "type": attack_type, "severity": "Critical", "confidence": 98,
            "first_detected": datetime.now(), "last_activity": datetime.now(),
            "source_ip": attacker_ip, "target": target,
            "status": "Active", "assigned_to": "commander"
        }
        st.session_state.live_threats.append(new_threat)
        
        # Generate a burst of malicious activity
        for _ in range(10): self.generate_network_activity_entry(flagged=True, attacker_ip=attacker_ip)
        self.generate_ids_alert_entry(attack_type="Data Exfiltration", attacker_ip=attacker_ip)
        self.generate_ids_alert_entry(attack_type="Lateral Movement", attacker_ip=attacker_ip)

    # --- REALISM ENHANCEMENT: REACTIVE COUNTERMEASURES ---
    def deploy_countermeasures(self, threat_id: str, measures: List[str]):
        """Deploys countermeasures with visible effects."""
        threat_to_contain = None
        for threat in st.session_state.live_threats:
            if threat["threat_id"] == threat_id and threat["status"] == "Active":
                threat_to_contain = threat
                break
        
        if threat_to_contain:
            threat_to_contain["status"] = "Contained"
            threat_to_contain["last_activity"] = datetime.now()
            
            if "Block IP" in measures and "source_ip" in threat_to_contain:
                st.session_state.blocked_ips.add(threat_to_contain["source_ip"])
                self.log_to_terminal(f"Firewall rule deployed. IP {threat_to_contain['source_ip']} blocked.", level="ACTION")

            if "Isolate Endpoint" in measures and "target" in threat_to_contain:
                st.session_state.quarantined_endpoints.add(threat_to_contain["target"])
                self.log_to_terminal(f"Network isolation protocol activated for endpoint: {threat_to_contain['target']}.", level="ACTION")
            
            st.session_state.defense_actions.append({
                "action_id": f"DEF-{len(st.session_state.defense_actions) + 1:04d}", "timestamp": datetime.now(),
                "threat_id": threat_id, "measures_deployed": measures, "analyst": st.session_state.user["user_id"],
                "status": "Completed"
            })
            self.log_to_terminal(f"Countermeasures deployed for {threat_id}. Threat contained.", level="INFO")
            return True
        else:
            self.log_to_terminal(f"Failed to deploy countermeasures for {threat_id}. Threat not active or not found.", level="WARN")
            return False

    def calculate_cyber_posture(self):
        critical_threats = len([t for t in st.session_state.live_threats if t["severity"] == "Critical" and t["status"] == "Active"])
        active_incidents = len([t for t in st.session_state.live_threats if t["status"] == "Active"])
        
        score = 100 - (critical_threats * 25) - (active_incidents * 5)
        score = max(0, min(100, score))
        
        if score >= 80: return "NOMINAL", "#00ff00", score
        elif score >= 60: return "ELEVATED", "#ffff00", score
        elif score >= 40: return "HIGH", "#ff6600", score
        else: return "CRITICAL", "#ff0000", score


def display_live_terminal(height=400):
    """Renders the scrolling terminal output."""
    st.markdown("### 实时终端日志 (Live Terminal Log)")
    log_content = "\n".join(st.session_state.terminal_log)
    
    # NEW: Using st.empty to create a dynamic element
    terminal_container = st.empty()
    terminal_container.markdown(f"""
        <div id="terminal-log" class="live-terminal-output" style="height: {height}px;">
            {'<br>'.join(st.session_state.terminal_log)}
        </div>
        <script>
            var term = document.getElementById("terminal-log");
            term.scrollTop = term.scrollHeight;
        </script>
    """, unsafe_allow_html=True)

def cyber_login():
    st.markdown('<div class="main-header">🛡️ CYBER COMMAND v3.0</div>', unsafe_allow_html=True)
    st.markdown("### THREAT OPERATIONS PLATFORM", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        display_live_terminal(height=250)

    with col2:
        with st.form("cyber_login"):
            st.markdown("**OPERATOR AUTHENTICATION**", unsafe_allow_html=True)
            username = st.text_input("OPERATOR ID", key="login_user").lower()
            password = st.text_input("ACCESS CODE", type="password", key="login_pass")
            login_button = st.form_submit_button(">> INITIATE CONNECTION")
            
            if login_button:
                terminal = st.session_state.cyber_terminal
                if terminal.authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.user = terminal.cyber_team[username]
                    st.success("ACCESS GRANTED. Initializing dashboard...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("ACCESS DENIED. Invalid credentials.")
    
    st.markdown("---")
    st.markdown("**DEMO CREDENTIALS**")
    st.code("ID: commander | Code: alpha-one\nID: hunter    | Code: bravo-seven\nID: analyst   | Code: charlie-three")


def cyber_dashboard():
    terminal = st.session_state.cyber_terminal
    user = st.session_state.user
    
    # --- REALISM ENHANCEMENT: THE "LIVENESS" ENGINE ---
    # This runs the heartbeat on every interaction/rerun
    terminal.update_live_data()

    # Terminal Header
    st.markdown(f"""
    <div style='padding: 10px; border-bottom: 3px solid #00ff00; margin-bottom: 20px; text-align:center;'>
        <h2 style='color: #00ff00; margin: 0; font-family: "Roboto Mono", monospace;'>
            OPERATOR: {user['first_name']} {user['last_name']} | ROLE: {user['role'].upper()}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Sidebar
    with st.sidebar:
        st.markdown(f"**Welcome, {user['role']} {user['last_name']}**")
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True):
            attack_type = random.choice(["Ransomware", "Data Breach", "APT Intrusion"])
            terminal.simulate_live_attack(attack_type)
            st.rerun()

        st.markdown("---")
        
        # --- REALISM ENHANCEMENT: DYNAMIC INCIDENT RESPONSE ---
        st.markdown("**ACTIVE INCIDENTS**")
        active_threats = [t for t in st.session_state.live_threats if t["status"] == "Active"]
        if not active_threats:
            st.info("No active critical incidents.")
        else:
            for threat in active_threats:
                if st.button(f"RESPOND TO {threat['threat_id']}", key=threat['threat_id'], use_container_width=True):
                    measures_to_deploy = ["Block IP", "Isolate Endpoint"]
                    if terminal.deploy_countermeasures(threat['threat_id'], measures_to_deploy):
                        st.sidebar.success(f"{threat['threat_id']} Contained.")
                        time.sleep(1)
                        st.rerun()
        
        st.markdown("---")
        if st.button("🚪 LOGOUT", use_container_width=True):
            terminal.log_to_terminal(f"Operator {user['user_id'].upper()} logged out.", level="INFO")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # Main Dashboard
    posture, posture_color, posture_score = terminal.calculate_cyber_posture()
    st.markdown(f"""
    <div style='padding: 20px; border: 3px solid {posture_color}; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h1 style='color: {posture_color}; margin: 0;'>DEFENSE POSTURE: {posture}</h1>
        <h2 style='color: {posture_color}; margin: 0;'>INTEGRITY: {posture_score}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])

    with col1:
        display_live_terminal()

    with col2:
        st.markdown("### 🚨 HIGH-SEVERITY ALERTS")
        high_alerts = [a for a in st.session_state.ids_alerts if a['severity'] == 'High']
        recent_high_alerts = sorted(high_alerts, key=lambda x: x['timestamp'], reverse=True)[:5]
        if not recent_high_alerts:
            st.markdown("<p style='color:#00ff00;'>System clear. No high-severity alerts.</p>", unsafe_allow_html=True)
        for alert in recent_high_alerts:
            st.markdown(f"""
            <div class='threat-panel' style='padding:10px; margin: 5px 0;'>
                <strong>{alert['attack_type']}</strong><br>
                Source: {alert['source_ip']}<br>
                <span style='font-size:0.8em; color:#ccc;'>{alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
            """, unsafe_allow_html=True)

    # Auto-refresh mechanism
    time.sleep(1.5) # The "tick" rate of the dashboard
    st.rerun()


def main():
    if 'cyber_terminal' not in st.session_state:
        st.session_state.cyber_terminal = AdvancedCyberTerminal()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
    
    if not st.session_state.logged_in:
        cyber_login()
    else:
        cyber_dashboard()

if __name__ == "__main__":
    main()
