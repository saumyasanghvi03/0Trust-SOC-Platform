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
from typing import Dict, List, Any
import warnings
import math

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CYBER TERMINAL v2.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Cyber Terminal CSS (keeping ALL original CSS)
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #00ff00;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px #00ff00;
        background: linear-gradient(90deg, #00ff00, #ffff00, #00ff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
        to { text-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
    }
    .cyber-terminal {
        background-color: #0a0a0a;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    .dashboard-panel {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
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
    .defense-panel {
        background: linear-gradient(135deg, #0a2a0a 0%, #051a05 100%);
        border: 1px solid #00ff00;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse-green 3s infinite;
    }
    @keyframes pulse-green {
        0% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
        50% { border-color: #44ff44; box-shadow: 0 0 20px rgba(0, 255, 0, 0.6); }
        100% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    }
    .metric-glowing {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #00ff00;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        animation: metric-glow 4s infinite;
    }
    @keyframes metric-glow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 0, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 0, 0.3); }
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        color: #00ff00;
        border-bottom: 1px solid #333;
        padding: 0.3rem 0;
        transition: all 0.3s ease;
    }
    .log-entry:hover {
        background-color: #1a1a1a;
        transform: translateX(5px);
    }
    .cyber-button {
        background: linear-gradient(135deg, #00ff00 0%, #008800 100%);
        border: none;
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
    }
    .cyber-button:hover {
        background: linear-gradient(135deg, #44ff44 0%, #00aa00 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 0, 0.4);
    }
    .cyber-button-red {
        background: linear-gradient(135deg, #ff0000 0%, #880000 100%);
        color: white;
    }
    .cyber-button-red:hover {
        background: linear-gradient(135deg, #ff4444 0%, #aa0000 100%);
        box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
    }
    .terminal-output {
        background-color: #000000;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        height: 400px;
        overflow-y: auto;
        margin: 10px 0;
    }
    .radar-sweep {
        position: relative;
        width: 100%;
        height: 300px;
        background: radial-gradient(circle, #001100 0%, #000000 70%);
        border: 2px solid #00ff00;
        border-radius: 50%;
        overflow: hidden;
    }
    .sweep-line {
        position: absolute;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00ff00 50%, transparent 100%);
        top: 50%;
        transform-origin: center;
        animation: sweep 4s linear infinite;
    }
    @keyframes sweep {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .threat-dot {
        position: absolute;
        width: 12px;
        height: 12px;
        background-color: #ff0000;
        border-radius: 50%;
        animation: threat-pulse 2s infinite;
    }
    @keyframes threat-pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCyberTerminal:
    def __init__(self):
        self.last_update = datetime.now()
        self.live_data_running = False
        self.initialize_cyber_terminal()
        
    def initialize_cyber_terminal(self):
        """Initialize advanced cyber terminal data"""
        # Enhanced threat intelligence
        self.threat_intel_db = {
            "advanced_persistent_threats": [
                {"name": "APT29", "country": "Russia", "targets": ["Government", "Healthcare"], "tactics": ["Spear Phishing", "Custom Malware"]},
                {"name": "APT1", "country": "China", "targets": ["Defense", "Technology"], "tactics": ["Watering Hole", "Zero-Day"]},
                {"name": "Lazarus", "country": "North Korea", "targets": ["Finance", "Cryptocurrency"], "tactics": ["Supply Chain", "Ransomware"]}
            ],
            "malware_families": [
                {"name": "Emotet", "type": "Trojan", "primary_function": "Banking", "propagation": "Email"},
                {"name": "TrickBot", "type": "Banking Trojan", "primary_function": "Credential Theft", "propagation": "Email"},
                {"name": "Ryuk", "type": "Ransomware", "primary_function": "Data Encryption", "propagation": "Network"}
            ],
            "vulnerabilities": [
                {"cve": "CVE-2021-44228", "name": "Log4Shell", "severity": "Critical", "affected_software": ["Log4j"]},
                {"cve": "CVE-2021-34527", "name": "PrintNightmare", "severity": "Critical", "affected_software": ["Windows"]},
                {"cve": "CVE-2020-1472", "name": "Zerologon", "severity": "Critical", "affected_software": ["Windows Server"]}
            ]
        }
        
        # SOC team with enhanced roles
        self.cyber_team = {
            "cyber_commander": {
                "user_id": "cyber_commander",
                "password": self.hash_password("cyber123"),
                "first_name": "Alex",
                "last_name": "Thorne",
                "role": "commander",
                "clearance": "TOP SECRET",
                "specializations": ["Strategic Defense", "Threat Intelligence", "Incident Command"]
            },
            "threat_hunter": {
                "user_id": "threat_hunter",
                "password": self.hash_password("cyber123"),
                "first_name": "Jordan",
                "last_name": "Reyes",
                "role": "threat_hunter",
                "clearance": "SECRET",
                "specializations": ["Malware Analysis", "Digital Forensics", "Threat Hunting"]
            },
            "defense_analyst": {
                "user_id": "defense_analyst",
                "password": self.hash_password("cyber123"),
                "first_name": "Casey",
                "last_name": "Zhang",
                "role": "defense_analyst",
                "clearance": "SECRET",
                "specializations": ["Network Defense", "SIEM Management", "Vulnerability Management"]
            }
        }
        
        # Initialize all data structures
        self.security_incidents = []
        self.live_threats = []
        self.network_activity = []
        self.endpoint_telemetry = []
        self.firewall_logs = []
        self.ids_alerts = []
        self.honeypot_data = []
        self.threat_feeds = []
        self.defense_actions = []
        self.cyber_kill_chains = []
        
        # Generate initial data
        self.generate_live_threats()
        self.generate_network_activity()
        self.generate_endpoint_telemetry()
        self.generate_ids_alerts()
        self.generate_honeypot_data()
        
        # Start live data simulation
        self.start_live_data_simulation()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = "cyber_terminal_salt_2024"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate cyber team member"""
        if username in self.cyber_team:
            user = self.cyber_team[username]
            if self.verify_password(password, user["password"]):
                return True
        return False
    
    def start_live_data_simulation(self):
        """Start live data simulation in background"""
        if not self.live_data_running:
            self.live_data_running = True
    
    def generate_live_threats(self):
        """Generate live threat intelligence"""
        threat_types = ["APT Campaign", "Malware Distribution", "Phishing Campaign", "DDoS Attack", "Data Exfiltration"]
        
        for i in range(10):
            threat = {
                "threat_id": f"THREAT-{i+1:06d}",
                "type": random.choice(threat_types),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "confidence": random.randint(60, 98),
                "first_detected": datetime.now() - timedelta(hours=random.randint(1, 72)),
                "last_activity": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "source_country": random.choice(["Russia", "China", "North Korea", "Iran", "Unknown"]),
                "target_sector": random.choice(["Finance", "Healthcare", "Government", "Energy", "Technology"]),
                "indicators": [f"Indicator-{j}" for j in range(random.randint(2, 5))],
                "status": random.choice(["Active", "Monitoring", "Contained"]),
                "assigned_to": random.choice(list(self.cyber_team.keys()))
            }
            self.live_threats.append(threat)
    
    def generate_network_activity(self):
        """Generate realistic network activity"""
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "SMB"]
        services = ["Web Server", "Database", "File Share", "DNS Server", "Mail Server", "VPN"]
        
        for i in range(500):
            activity = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 300)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "source_port": random.randint(1024, 65535),
                "dest_port": random.choice([80, 443, 22, 53, 25, 3389]),
                "protocol": random.choice(protocols),
                "service": random.choice(services),
                "bytes_sent": random.randint(100, 1000000),
                "bytes_received": random.randint(100, 500000),
                "packet_count": random.randint(10, 1000),
                "threat_score": random.randint(0, 100),
                "geo_location": random.choice(["Internal", "USA", "China", "Russia", "Germany", "Brazil"]),
                "flagged": random.random() < 0.15
            }
            self.network_activity.append(activity)
    
    def generate_endpoint_telemetry(self):
        """Generate endpoint security telemetry"""
        endpoints = [f"WS-{i:03d}" for i in range(1, 51)] + [f"SRV-{i:03d}" for i in range(1, 21)]
        processes = ["explorer.exe", "chrome.exe", "winlogon.exe", "svchost.exe", "powershell.exe", "cmd.exe"]
        
        for endpoint in endpoints:
            telemetry = {
                "endpoint_id": endpoint,
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "os_version": random.choice(["Windows 10", "Windows 11", "Windows Server 2019", "Windows Server 2022"]),
                "antivirus_status": random.choice(["Enabled", "Disabled", "Outdated"]),
                "threats_detected": random.randint(0, 3),
                "suspicious_processes": random.sample(processes, random.randint(0, 2)),
                "network_connections": random.randint(5, 50),
                "risk_score": random.randint(0, 100),
                "patch_level": random.choice(["Current", "1-2 weeks behind", "1 month behind", "Critical updates missing"]),
                "encryption_status": random.choice(["Enabled", "Disabled", "Partial"]),
                "last_scan": datetime.now() - timedelta(days=random.randint(0, 7))
            }
            self.endpoint_telemetry.append(telemetry)
    
    def generate_ids_alerts(self):
        """Generate IDS/IPS alerts"""
        attack_types = ["Port Scan", "Brute Force", "SQL Injection", "XSS", "DDoS", "Malware Download", "Data Theft"]
        
        for i in range(100):
            alert = {
                "alert_id": f"IDS-{i+1:06d}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 240)),
                "attack_type": random.choice(attack_types),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "signature": f"SIG-{random.randint(1000, 9999)}",
                "action_taken": random.choice(["Allowed", "Blocked", "Alerted"]),
                "confidence": random.randint(70, 99),
                "protocol": random.choice(["TCP", "UDP", "HTTP"]),
                "payload_info": f"Malicious payload detected: {random.choice(['Exploit kit', 'Ransomware', 'Trojan', 'Backdoor'])}"
            }
            self.ids_alerts.append(alert)
    
    def generate_honeypot_data(self):
        """Generate honeypot interaction data"""
        for i in range(25):
            interaction = {
                "honeypot_id": f"HONEY-{i+1:03d}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 48)),
                "attacker_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "attacker_country": random.choice(["China", "Russia", "USA", "Brazil", "Vietnam", "Iran"]),
                "attack_type": random.choice(["SSH Brute Force", "Web Exploit", "Database Attack", "Service Scan"]),
                "credentials_tried": random.randint(1, 50),
                "malware_dropped": random.random() < 0.3,
                "data_captured": random.randint(0, 5000),
                "threat_level": random.choice(["Low", "Medium", "High"])
            }
            self.honeypot_data.append(interaction)
    
    def simulate_live_attack(self, attack_type: str):
        """Simulate a live cyber attack"""
        attack_id = f"LIVE-ATTACK-{datetime.now().strftime('%H%M%S')}"
        
        attack = {
            "attack_id": attack_id,
            "type": attack_type,
            "start_time": datetime.now(),
            "source_ip": f"{random.randint(100, 200)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "target": random.choice(["Web Server", "Database", "File Server", "User Workstation"]),
            "intensity": random.choice(["Low", "Medium", "High"]),
            "techniques": random.sample(["Port Scanning", "Credential Stuffing", "Lateral Movement", "Data Exfiltration"], 2),
            "status": "Active"
        }
        
        # Add to live threats
        self.live_threats.append({
            "threat_id": attack_id,
            "type": attack_type,
            "severity": "Critical",
            "confidence": 95,
            "first_detected": datetime.now(),
            "last_activity": datetime.now(),
            "source_country": random.choice(["China", "Russia", "North Korea"]),
            "target_sector": "Internal",
            "indicators": [f"Live-{i}" for i in range(3)],
            "status": "Active",
            "assigned_to": "cyber_commander"
        })
        
        self.last_update = datetime.now()
        return attack_id
    
    def deploy_countermeasures(self, attack_id: str, measures: List[str]):
        """Deploy countermeasures against an attack"""
        for threat in self.live_threats:
            if threat["threat_id"] == attack_id:
                threat["status"] = "Contained"
                threat["last_activity"] = datetime.now()
                
                defense_action = {
                    "action_id": f"DEF-{len(self.defense_actions) + 1:06d}",
                    "timestamp": datetime.now(),
                    "attack_id": attack_id,
                    "measures_deployed": measures,
                    "analyst": st.session_state.user["user_id"],
                    "effectiveness": random.randint(80, 100),
                    "status": "Completed"
                }
                self.defense_actions.append(defense_action)
                self.last_update = datetime.now()
                return True
        return False
    
    def calculate_cyber_posture(self):
        """Calculate overall cyber security posture"""
        critical_threats = len([t for t in self.live_threats if t["severity"] == "Critical"])
        high_threats = len([t for t in self.live_threats if t["severity"] == "High"])
        active_incidents = len([t for t in self.live_threats if t["status"] == "Active"])
        
        base_score = 100
        score = base_score - (critical_threats * 10) - (high_threats * 5) - (active_incidents * 3)
        score = max(0, min(100, score))
        
        if score >= 80:
            return "STRONG", "#00ff00", score
        elif score >= 60:
            return "MODERATE", "#ffff00", score
        elif score >= 40:
            return "WEAK", "#ff6600", score
        else:
            return "CRITICAL", "#ff0000", score
    
    def get_threat_radar_data(self):
        """Generate data for threat radar visualization"""
        threats = []
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0.2, 0.9)
            severity = random.choice(["Low", "Medium", "High", "Critical"])
            threats.append({
                "angle": angle,
                "distance": distance,
                "severity": severity
            })
        return threats

def cyber_login():
    """Display cyber terminal login"""
    st.markdown('<div class="main-header">🛡️ CYBER TERMINAL v2.0</div>', unsafe_allow_html=True)
    st.markdown("### ADVANCED THREAT OPERATIONS PLATFORM", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='dashboard-panel'>
            <h4 style='color: #00ff00;'>SYSTEM STATUS: OPERATIONAL</h4>
            <p style='color: #00ff00;'>🟢 Threat Intelligence: ONLINE</p>
            <p style='color: #00ff00;'>🟢 Network Defense: ACTIVE</p>
            <p style='color: #00ff00;'>🟢 Endpoint Protection: ENABLED</p>
            <p style='color: #00ff00;'>🟢 Incident Response: READY</p>
            <p style='color: #ffff00;'>Last System Scan: 2 minutes ago</p>
            <p style='color: #ffff00;'>Active Threats: 12</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("cyber_login"):
            st.markdown("**TERMINAL ACCESS**", unsafe_allow_html=True)
            username = st.text_input("OPERATOR ID")
            password = st.text_input("ACCESS CODE", type="password")
            login_button = st.form_submit_button("🚀 INITIATE CYBER TERMINAL")
            
            if login_button:
                if username and password:
                    terminal = st.session_state.cyber_terminal
                    if terminal.authenticate_user(username, password):
                        st.session_state.user = terminal.cyber_team[username]
                        st.session_state.logged_in = True
                        st.success("✓ ACCESS GRANTED - WELCOME TO CYBER TERMINAL")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("✗ ACCESS DENIED - INVALID CREDENTIALS")
                else:
                    st.warning("⚠ ENTER CREDENTIALS FOR TERMINAL ACCESS")
    
    st.markdown("---")
    st.markdown("**AUTHORIZED PERSONNEL**", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**CYBER COMMANDER**", unsafe_allow_html=True)
        st.markdown("ID: `cyber_commander`", unsafe_allow_html=True)
        st.markdown("CODE: `cyber123`", unsafe_allow_html=True)
        st.markdown("CLEARANCE: TOP SECRET", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**THREAT HUNTER**", unsafe_allow_html=True)
        st.markdown("ID: `threat_hunter`", unsafe_allow_html=True)
        st.markdown("CODE: `cyber123`", unsafe_allow_html=True)
        st.markdown("CLEARANCE: SECRET", unsafe_allow_html=True)
    
    with col3:
        st.markdown("**DEFENSE ANALYST**", unsafe_allow_html=True)
        st.markdown("ID: `defense_analyst`", unsafe_allow_html=True)
        st.markdown("CODE: `cyber123`", unsafe_allow_html=True)
        st.markdown("CLEARANCE: SECRET", unsafe_allow_html=True)

def cyber_dashboard():
    """Display main cyber terminal dashboard"""
    terminal = st.session_state.cyber_terminal
    user = st.session_state.user
    
    # Terminal Header
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); padding: 15px; border-bottom: 3px solid #00ff00; margin-bottom: 20px;'>
        <h2 style='color: #00ff00; margin: 0; text-align: center;'>
            🛡️ CYBER TERMINAL ACTIVE | OPERATOR: {user['first_name']} {user['last_name']} 
            | ROLE: {user['role'].upper()} | CLEARANCE: {user['clearance']}
        </h2>
        <p style='color: #00ff00; text-align: center; margin: 5px 0;'>LAST UPDATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Sidebar
    with st.sidebar:
        st.markdown("**QUICK ACTIONS**", unsafe_allow_html=True)
        
        if st.button("🔄 FORCE SYSTEM REFRESH", use_container_width=True):
            terminal.generate_network_activity()
            terminal.last_update = datetime.now()
            st.rerun()
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True, key="sim_attack"):
            attack_type = random.choice(["DDoS", "Ransomware", "Data Breach", "APT Intrusion"])
            attack_id = terminal.simulate_live_attack(attack_type)
            st.success(f"✓ Live attack simulated: {attack_id}")
            time.sleep(0.5)
            st.rerun()
        
        st.markdown("---")
        st.markdown("**TERMINAL MODULES**", unsafe_allow_html=True)
        
        module = st.radio("SELECT MODULE", [
            "📊 DASHBOARD", 
            "🌐 NETWORK DEFENSE", 
            "💻 ENDPOINT SECURITY", 
            "🕵️ THREAT HUNTING", 
            "🔍 DIGITAL FORENSICS", 
            "📡 THREAT INTELLIGENCE",
            "🚨 INCIDENT RESPONSE", 
            "📈 ANALYTICS & REPORTING"
        ], key="module_selector")
        
        if st.button("🚪 TERMINATE SESSION", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Route to selected module
    if "DASHBOARD" in module:
        show_cyber_dashboard(terminal)
    elif "NETWORK DEFENSE" in module:
        show_network_defense(terminal)
    elif "ENDPOINT SECURITY" in module:
        show_endpoint_security(terminal)
    elif "THREAT HUNTING" in module:
        show_threat_hunting(terminal)
    elif "DIGITAL FORENSICS" in module:
        show_digital_forensics(terminal)
    elif "THREAT INTELLIGENCE" in module:
        show_threat_intelligence(terminal)
    elif "INCIDENT RESPONSE" in module:
        show_incident_response(terminal)
    elif "ANALYTICS" in module:
        show_analytics_reporting(terminal)

def show_cyber_dashboard(terminal):
    """Display cyber security dashboard"""
    
    # Cyber Posture Indicator
    posture, posture_color, posture_score = terminal.calculate_cyber_posture()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); padding: 20px; border: 3px solid {posture_color}; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h1 style='color: {posture_color}; margin: 0;'>CYBER POSTURE: {posture}</h1>
        <h2 style='color: {posture_color}; margin: 0;'>SCORE: {posture_score}/100</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_threats = len([t for t in terminal.live_threats if t["severity"] == "Critical"])
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ff0000;'>{critical_threats}</h1>
            <p>CRITICAL THREATS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_incidents = len([t for t in terminal.live_threats if t["status"] == "Active"])
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ff6600;'>{active_incidents}</h1>
            <p>ACTIVE INCIDENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        network_alerts = len(terminal.ids_alerts)
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ffff00;'>{network_alerts}</h1>
            <p>NETWORK ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        endpoints_at_risk = len([e for e in terminal.endpoint_telemetry if e["risk_score"] > 70])
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #00ff00;'>{endpoints_at_risk}</h1>
            <p>ENDPOINTS AT RISK</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat Feed and Network Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 LIVE THREAT FEED")
        
        recent_threats = sorted(terminal.live_threats, key=lambda x: x["last_activity"], reverse=True)[:8]
        
        for threat in recent_threats:
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }[threat["severity"]]
            
            st.markdown(f"""
            <div class='log-entry'>
                <span style='color: {severity_color};'>[{threat['last_activity'].strftime('%H:%M:%S')}]</span>
                {threat['type']} | Source: {threat['source_country']} | Confidence: {threat['confidence']}%
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌐 LIVE NETWORK ACTIVITY")
        
        recent_activity = sorted(terminal.network_activity, key=lambda x: x["timestamp"], reverse=True)[:15]
        
        for activity in recent_activity:
            flag_icon = "🚩" if activity["flagged"] else "  "
            threat_color = "#ff0000" if activity["threat_score"] > 80 else "#ffff00" if activity["threat_score"] > 60 else "#00ff00"
            
            st.markdown(f"""
            <div class='log-entry'>
                <span style='color: #00ff00;'>[{activity['timestamp'].strftime('%H:%M:%S')}]</span>
                {flag_icon} {activity['source_ip']}:{activity['source_port']} → {activity['dest_ip']}:{activity['dest_port']}
                <span style='color: #ffff00;'>{activity['protocol']}</span>
                <span style='color: {threat_color};'>Threat: {activity['threat_score']}%</span>
            </div>
            """, unsafe_allow_html=True)

def show_network_defense(terminal):
    """Display network defense module"""
    st.markdown("## 🌐 NETWORK DEFENSE OPERATIONS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛡️ FIREWALL STATUS")
        
        firewall_rules = [
            {"rule": "SSH Access", "status": "Blocked", "hits": 1245},
            {"rule": "Web Traffic", "status": "Allowed", "hits": 89432},
            {"rule": "Database Access", "status": "Restricted", "hits": 234},
            {"rule": "File Sharing", "status": "Blocked", "hits": 567},
            {"rule": "Remote Desktop", "status": "Restricted", "hits": 89}
        ]
        
        for rule in firewall_rules:
            status_color = "#00ff00" if rule["status"] == "Allowed" else "#ffff00" if rule["status"] == "Restricted" else "#ff0000"
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid {status_color};'>
                <strong>{rule['rule']}</strong> | Status: <span style='color: {status_color};'>{rule['status']}</span> | Hits: {rule['hits']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 NETWORK TRAFFIC ANALYSIS")
        
        protocols = {}
        for activity in terminal.network_activity[:100]:
            protocol = activity["protocol"]
            protocols[protocol] = protocols.get(protocol, 0) + 1
        
        if protocols:
            fig = px.pie(values=list(protocols.values()), names=list(protocols.keys()), 
                        title="Protocol Distribution")
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # IDS/IPS Alerts
    st.markdown("### 🚨 INTRUSION DETECTION SYSTEM")
    
    high_severity_alerts = [a for a in terminal.ids_alerts if a["severity"] in ["High", "Critical"]][:10]
    
    for alert in high_severity_alerts:
        severity_color = "#ff0000" if alert["severity"] == "Critical" else "#ff6600"
        
        st.markdown(f"""
        <div class='threat-panel'>
            <strong>{alert['attack_type']}</strong> | 
            Source: {alert['source_ip']} → Dest: {alert['dest_ip']} | 
            Severity: <span style='color: {severity_color};'>{alert['severity']}</span> | 
            Action: {alert['action_taken']} | 
            Confidence: {alert['confidence']}%
        </div>
        """, unsafe_allow_html=True)
    
    # Network Defense Actions
    st.markdown("### 🎯 ACTIVE DEFENSE MEASURES")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔒 BLOCK MALICIOUS IPs", use_container_width=True, key="block_ips"):
            st.success("✓ Malicious IPs blocked across all network segments")
    
    with col2:
        if st.button("🛡️ ENABLE DDoS PROTECTION", use_container_width=True, key="ddos_protect"):
            st.success("✓ DDoS protection enabled - monitoring network traffic")
    
    with col3:
        if st.button("📡 SCAN FOR VULNERABILITIES", use_container_width=True, key="vuln_scan"):
            st.success("✓ Network vulnerability scan initiated")

def show_endpoint_security(terminal):
    """Display endpoint security module"""
    st.markdown("## 💻 ENDPOINT SECURITY MANAGEMENT")
    
    # Endpoint Risk Dashboard
    st.markdown("### 📈 ENDPOINT RISK ASSESSMENT")
    
    high_risk_endpoints = [e for e in terminal.endpoint_telemetry if e["risk_score"] > 70]
    medium_risk_endpoints = [e for e in terminal.endpoint_telemetry if 40 <= e["risk_score"] <= 70]
    low_risk_endpoints = [e for e in terminal.endpoint_telemetry if e["risk_score"] < 40]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Endpoints", len(terminal.endpoint_telemetry))
    with col2:
        st.metric("High Risk", len(high_risk_endpoints))
    with col3:
        st.metric("Medium Risk", len(medium_risk_endpoints))
    with col4:
        st.metric("Low Risk", len(low_risk_endpoints))
    
    # Endpoint Details
    st.markdown("### 🔍 HIGH RISK ENDPOINTS")
    
    for endpoint in high_risk_endpoints[:5]:
        risk_color = "#ff0000" if endpoint["risk_score"] > 80 else "#ff6600"
        
        with st.expander(f"🚨 {endpoint['endpoint_id']} - Risk Score: {endpoint['risk_score']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**OS:** {endpoint['os_version']}")
                st.write(f"**AV Status:** {endpoint['antivirus_status']}")
                st.write(f"**Threats Detected:** {endpoint['threats_detected']}")
            
            with col2:
                st.write(f"**Patch Level:** {endpoint['patch_level']}")
                st.write(f"**Encryption:** {endpoint['encryption_status']}")
                st.write(f"**Last Scan:** {endpoint['last_scan'].strftime('%Y-%m-%d')}")
            
            if endpoint["suspicious_processes"]:
                st.write(f"**Suspicious Processes:** {', '.join(endpoint['suspicious_processes'])}")
            
            # Actions
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🔄 QUARANTINE", key=f"quarantine_{endpoint['endpoint_id']}"):
                    st.success(f"✓ {endpoint['endpoint_id']} quarantined")
            with col_b:
                if st.button("🔍 DEEP SCAN", key=f"scan_{endpoint['endpoint_id']}"):
                    st.info(f"Deep scan initiated on {endpoint['endpoint_id']}")
            with col_c:
                if st.button("🛡️ UPDATE", key=f"update_{endpoint['endpoint_id']}"):
                    st.success(f"✓ Security updates deployed to {endpoint['endpoint_id']}")

def show_threat_hunting(terminal):
    """Display threat hunting module"""
    st.markdown("## 🕵️ ADVANCED THREAT HUNTING")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 HUNTING QUERIES")
        
        hunting_queries = [
            "Processes with network connections to known malicious IPs",
            "Suspicious PowerShell execution patterns",
            "Unusual scheduled task creations",
            "Registry modifications by unknown processes",
            "Lateral movement attempts using WMI"
        ]
        
        for idx, query in enumerate(hunting_queries):
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid #ffff00;'>
                🔍 {query}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Execute Hunt #{idx+1}", key=f"hunt_{idx}"):
                st.success(f"✓ Hunt executed: {random.randint(0, 5)} suspicious activities found")
    
    with col2:
        st.markdown("### 📊 HUNTING RESULTS")
        
        hunting_results = [
            {"type": "Suspicious Process", "endpoint": "WS-023", "confidence": 85},
            {"type": "Network Anomaly", "endpoint": "SRV-005", "confidence": 92},
            {"type": "Fileless Attack", "endpoint": "WS-042", "confidence": 78},
            {"type": "Credential Theft", "endpoint": "WS-015", "confidence": 88}
        ]
        
        for result in hunting_results:
            confidence_color = "#00ff00" if result["confidence"] > 90 else "#ffff00" if result["confidence"] > 75 else "#ff6600"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border: 1px solid {confidence_color};'>
                <strong>{result['type']}</strong><br>
                Endpoint: {result['endpoint']} | 
                Confidence: <span style='color: {confidence_color};'>{result['confidence']}%</span>
            </div>
            """, unsafe_allow_html=True)

def show_digital_forensics(terminal):
    """Display digital forensics module"""
    st.markdown("## 🔍 DIGITAL FORENSICS LAB")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧩 FORENSIC ARTIFACTS")
        
        artifacts = [
            {"type": "Memory Dump", "size": "4.2 GB", "analysis": "Completed", "findings": 3},
            {"type": "Disk Image", "size": "128 GB", "analysis": "In Progress", "findings": 12},
            {"type": "Network Capture", "size": "2.1 GB", "analysis": "Completed", "findings": 8},
            {"type": "Log Files", "size": "856 MB", "analysis": "Pending", "findings": 0}
        ]
        
        for artifact in artifacts:
            status_color = "#00ff00" if artifact["analysis"] == "Completed" else "#ffff00" if artifact["analysis"] == "In Progress" else "#ff6600"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid {status_color};'>
                <strong>{artifact['type']}</strong><br>
                Size: {artifact['size']} | 
                Status: <span style='color: {status_color};'>{artifact['analysis']}</span> | 
                Findings: {artifact['findings']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔬 MALWARE ANALYSIS")
        
        malware_samples = [
            {"name": "Trojan.Emotet", "risk": "High", "analysis": "Behavioral analysis completed"},
            {"name": "Ransomware.Ryuk", "risk": "Critical", "analysis": "Reverse engineering in progress"},
            {"name": "Backdoor.DarkComet", "risk": "High", "analysis": "Network analysis completed"}
        ]
        
        for malware in malware_samples:
            risk_color = "#ff0000" if malware["risk"] == "Critical" else "#ff6600"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border: 1px solid {risk_color};'>
                <strong>{malware['name']}</strong><br>
                Risk: <span style='color: {risk_color};'>{malware['risk']}</span><br>
                {malware['analysis']}
            </div>
            """, unsafe_allow_html=True)

def show_threat_intelligence(terminal):
    """Display threat intelligence module"""
    st.markdown("## 📡 THREAT INTELLIGENCE PLATFORM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 ADVANCED PERSISTENT THREATS")
        
        for apt in terminal.threat_intel_db["advanced_persistent_threats"]:
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid #ff0000;'>
                <strong>{apt['name']}</strong> | Country: {apt['country']}<br>
                Targets: {', '.join(apt['targets'])}<br>
                Tactics: {', '.join(apt['tactics'])}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🦠 MALWARE FAMILIES")
        
        for malware in terminal.threat_intel_db["malware_families"]:
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid #ff6600;'>
                <strong>{malware['name']}</strong> | Type: {malware['type']}<br>
                Function: {malware['primary_function']}<br>
                Propagation: {malware['propagation']}
            </div>
            """, unsafe_allow_html=True)
    
    # Vulnerabilities
    st.markdown("### 🕳️ CRITICAL VULNERABILITIES")
    
    for vuln in terminal.threat_intel_db["vulnerabilities"]:
        st.markdown(f"""
        <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid #ff0000;'>
            <strong>{vuln['cve']} - {vuln['name']}</strong><br>
            Severity: <span style='color: #ff0000;'>{vuln['severity']}</span><br>
            Affected: {', '.join(vuln['affected_software'])}
        </div>
        """, unsafe_allow_html=True)

def show_incident_response(terminal):
    """Display incident response module"""
    st.markdown("## 🚨 INCIDENT RESPONSE COMMAND")
    
    active_incidents = [t for t in terminal.live_threats if t["status"] == "Active"]
    
    st.markdown(f"### 🔥 ACTIVE INCIDENTS: {len(active_incidents)}")
    
    if not active_incidents:
        st.success("✓ No active incidents requiring attention")
        return
    
    for incident in active_incidents:
        severity_color = {
            "Critical": "#ff0000", 
            "High": "#ff6600", 
            "Medium": "#ffff00", 
            "Low": "#00ff00"
        }[incident["severity"]]
        
        with st.expander(f"🚨 {incident['threat_id']} - {incident['type']} - Severity: {incident['severity']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**First Detected:** {incident['first_detected'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Source Country:** {incident['source_country']}")
                st.write(f"**Target Sector:** {incident['target_sector']}")
                st.write(f"**Confidence:** {incident['confidence']}%")
            
            with col2:
                st.write(f"**Assigned To:** {incident['assigned_to']}")
                st.write(f"**Status:** {incident['status']}")
                st.write("**Indicators:**")
                for indicator in incident["indicators"]:
                    st.write(f"  - {indicator}")
            
            # Response Actions
            st.markdown("#### 🛡️ RESPONSE ACTIONS")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🛑 CONTAIN THREAT", key=f"contain_{incident['threat_id']}"):
                    measures = ["Network Isolation", "Endpoint Quarantine", "Firewall Rules Update"]
                    if terminal.deploy_countermeasures(incident["threat_id"], measures):
                        st.success("✓ Threat contained successfully!")
                        time.sleep(0.5)
                        st.rerun()
            
            with col_b:
                if st.button("🔍 INVESTIGATE", key=f"investigate_{incident['threat_id']}"):
                    st.info("✓ Deep investigation initiated...")
            
            with col_c:
                if st.button("📋 ESCALATE", key=f"escalate_{incident['threat_id']}"):
                    st.warning("✓ Incident escalated to Cyber Commander")

def show_analytics_reporting(terminal):
    """Display analytics and reporting module"""
    st.markdown("## 📈 CYBER SECURITY ANALYTICS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 THREAT TRENDS")
        
        dates = [(datetime.now() - timedelta(days=x)).strftime('%m-%d') for x in range(30, 0, -1)]
        threats_per_day = [random.randint(5, 25) for _ in range(30)]
        
        fig = px.line(x=dates, y=threats_per_day, title="Daily Threat Detection (Last 30 Days)")
        fig.update_layout(
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#1a1a1a',
            font_color='#00ff00',
            xaxis_title="Date",
            yaxis_title="Threats Detected"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 ATTACK VECTOR ANALYSIS")
        
        attack_vectors = {}
        for threat in terminal.live_threats:
            attack_vectors[threat['type']] = attack_vectors.get(threat['type'], 0) + 1
        
        if attack_vectors:
            fig = px.pie(values=list(attack_vectors.values()), names=list(attack_vectors.keys()),
                        title="Attack Type Distribution")
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Security Reports
    st.markdown("### 📄 SECURITY REPORTS")
    
    reports = [
        {"name": "Daily Security Briefing", "period": "Last 24 hours", "status": "Generated"},
        {"name": "Weekly Threat Assessment", "period": "Last 7 days", "status": "Pending"},
        {"name": "Monthly Compliance Report", "period": "Last 30 days", "status": "Generated"},
        {"name": "Quarterly Security Review", "period": "Last 90 days", "status": "In Progress"}
    ]
    
    for idx, report in enumerate(reports):
        status_color = "#00ff00" if report["status"] == "Generated" else "#ffff00" if report["status"] == "In Progress" else "#ff6600"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid {status_color};'>
                <strong>{report['name']}</strong><br>
                Period: {report['period']} | 
                Status: <span style='color: {status_color};'>{report['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("📥 Download", key=f"download_report_{idx}"):
                st.success("✓ Report downloaded")

def main():
    # Initialize cyber terminal in session state
    if 'cyber_terminal' not in st.session_state:
        st.session_state.cyber_terminal = AdvancedCyberTerminal()
    
    # Initialize login state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        cyber_login()
    else:
        cyber_dashboard()

if __name__ == "__main__":
    main()
