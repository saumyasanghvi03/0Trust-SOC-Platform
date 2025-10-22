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
import asyncio
import queue
from typing import Dict, List, Any
import warnings
from cryptography.fernet import Fernet
import ipaddress
import re
import math
import uuid
from streamlit_autorefresh import st_autorefresh

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CYBER TERMINAL v2.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Cyber Terminal CSS with real-time animations
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
    .live-data-stream {
        background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.1), transparent);
        background-size: 200% 100%;
        animation: stream-flow 3s linear infinite;
    }
    @keyframes stream-flow {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .blinking-cursor {
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

class LiveDataStream:
    """Real-time data streaming engine"""
    def __init__(self):
        self.data_queue = queue.Queue()
        self.running = False
        self.thread = None
        
    def start_streaming(self):
        """Start the live data streaming thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._data_generator, daemon=True)
            self.thread.start()
    
    def stop_streaming(self):
        """Stop the live data streaming"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _data_generator(self):
        """Generate live data events"""
        event_types = [
            "network_activity", "threat_detected", "ids_alert", 
            "endpoint_event", "firewall_event", "honeypot_interaction"
        ]
        
        while self.running:
            # Generate random events
            event_type = random.choice(event_types)
            event_data = self._generate_event(event_type)
            self.data_queue.put(event_data)
            
            # Random interval between events (0.1 to 2 seconds)
            time.sleep(random.uniform(0.1, 2))
    
    def _generate_event(self, event_type):
        """Generate specific event types"""
        base_event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "type": event_type
        }
        
        if event_type == "network_activity":
            base_event.update({
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
                "bytes": random.randint(100, 10000),
                "threat_score": random.randint(0, 100)
            })
        elif event_type == "threat_detected":
            base_event.update({
                "threat_type": random.choice(["Malware", "Phishing", "DDoS", "Data Exfiltration"]),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "source": random.choice(["External", "Internal"]),
                "confidence": random.randint(70, 99)
            })
        elif event_type == "ids_alert":
            base_event.update({
                "alert_type": random.choice(["Port Scan", "Brute Force", "SQL Injection", "XSS"]),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "action": random.choice(["Blocked", "Allowed", "Quarantined"])
            })
        
        return base_event
    
    def get_events(self, max_events=10):
        """Get recent events from the queue"""
        events = []
        while not self.data_queue.empty() and len(events) < max_events:
            try:
                events.append(self.data_queue.get_nowait())
            except queue.Empty:
                break
        return events

class AdvancedCyberTerminal:
    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.last_update = datetime.now()
        self.live_data_running = False
        self.data_stream = LiveDataStream()
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
        self.live_events = []
        
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
            self.data_stream.start_streaming()
    
    def update_live_data(self):
        """Update all live data streams"""
        # Get new events from data stream
        new_events = self.data_stream.get_events(20)
        self.live_events.extend(new_events)
        
        # Keep only last 1000 events
        if len(self.live_events) > 1000:
            self.live_events = self.live_events[-1000:]
        
        # Process events and update respective data structures
        for event in new_events:
            self._process_live_event(event)
        
        # Update timestamps and refresh data
        self._refresh_network_activity()
        self._refresh_threats()
        self._refresh_endpoints()
        self._refresh_alerts()
        
        self.last_update = datetime.now()
    
    def _process_live_event(self, event):
        """Process incoming live events"""
        if event["type"] == "network_activity":
            self.network_activity.append({
                "timestamp": event["timestamp"],
                "source_ip": event["source_ip"],
                "dest_ip": event["dest_ip"],
                "protocol": event["protocol"],
                "bytes_sent": event["bytes"],
                "threat_score": event["threat_score"],
                "flagged": event["threat_score"] > 70
            })
            
        elif event["type"] == "threat_detected":
            self.live_threats.append({
                "threat_id": f"THREAT-{len(self.live_threats)+1:06d}",
                "type": event["threat_type"],
                "severity": event["severity"],
                "confidence": event["confidence"],
                "first_detected": event["timestamp"],
                "last_activity": event["timestamp"],
                "source_country": random.choice(["Russia", "China", "North Korea", "Iran", "Unknown"]),
                "target_sector": random.choice(["Finance", "Healthcare", "Government", "Energy", "Technology"]),
                "indicators": [f"IOC-{random.randint(1000, 9999)}" for _ in range(random.randint(2, 5))],
                "status": "Active",
                "assigned_to": random.choice(list(self.cyber_team.keys()))
            })
            
        elif event["type"] == "ids_alert":
            self.ids_alerts.append({
                "alert_id": f"IDS-{len(self.ids_alerts)+1:06d}",
                "timestamp": event["timestamp"],
                "attack_type": event["alert_type"],
                "source_ip": event["source_ip"],
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "severity": event["severity"],
                "signature": f"SIG-{random.randint(1000, 9999)}",
                "action_taken": event["action"],
                "confidence": random.randint(70, 99),
                "protocol": random.choice(["TCP", "UDP", "HTTP"]),
                "payload_info": f"Malicious payload detected"
            })
    
    def _refresh_network_activity(self):
        """Refresh network activity with new data"""
        # Add some random new network activity
        if random.random() < 0.3:  # 30% chance to add new activity
            new_activity = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 10)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "source_port": random.randint(1024, 65535),
                "dest_port": random.choice([80, 443, 22, 53, 25, 3389]),
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH"]),
                "service": random.choice(["Web Server", "Database", "File Share", "DNS Server", "Mail Server"]),
                "bytes_sent": random.randint(100, 1000000),
                "bytes_received": random.randint(100, 500000),
                "packet_count": random.randint(10, 1000),
                "threat_score": random.randint(0, 100),
                "geo_location": random.choice(["Internal", "USA", "China", "Russia", "Germany", "Brazil"]),
                "flagged": random.random() < 0.15
            }
            self.network_activity.append(new_activity)
            
        # Keep only recent activity (last 500 entries)
        if len(self.network_activity) > 500:
            self.network_activity = self.network_activity[-500:]
    
    def _refresh_threats(self):
        """Refresh threat data"""
        # Update threat statuses and add new threats
        for threat in self.live_threats:
            if threat["status"] == "Active" and random.random() < 0.1:
                threat["last_activity"] = datetime.now()
                threat["confidence"] = min(99, threat["confidence"] + random.randint(-5, 5))
    
    def _refresh_endpoints(self):
        """Refresh endpoint telemetry"""
        for endpoint in self.endpoint_telemetry:
            if random.random() < 0.2:  # 20% chance to update endpoint
                endpoint["last_seen"] = datetime.now()
                endpoint["risk_score"] = max(0, min(100, endpoint["risk_score"] + random.randint(-10, 10)))
                endpoint["network_connections"] = max(0, endpoint["network_connections"] + random.randint(-5, 5))
    
    def _refresh_alerts(self):
        """Refresh IDS alerts"""
        # Keep only recent alerts
        if len(self.ids_alerts) > 200:
            self.ids_alerts = self.ids_alerts[-200:]
    
    def generate_live_threats(self):
        """Generate live threat intelligence"""
        threat_types = ["APT Campaign", "Malware Distribution", "Phishing Campaign", "DDoS Attack", "Data Exfiltration"]
        
        for i in range(8):
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
        
        for i in range(200):
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
        endpoints = [f"WS-{i:03d}" for i in range(1, 31)] + [f"SRV-{i:03d}" for i in range(1, 11)]
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
        
        for i in range(50):
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
        for i in range(15):
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
        
        # Create intensive attack simulation
        for _ in range(5):
            self.data_stream.data_queue.put({
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "type": "threat_detected",
                "threat_type": attack_type,
                "severity": "Critical",
                "source": "External",
                "confidence": 95
            })
        
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
        
        self.last_update = datetime.now()
        return attack_id
    
    def deploy_countermeasures(self, attack_id: str, measures: List[str]):
        """Deploy countermeasures against an attack"""
        for threat in self.live_threats:
            if threat["threat_id"] == attack_id:
                threat["status"] = "Contained"
                threat["last_activity"] = datetime.now()
                
                # Log defense action
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
        critical_threats = len([t for t in self.live_threats if t["severity"] == "Critical" and t["status"] == "Active"])
        high_threats = len([t for t in self.live_threats if t["severity"] == "High" and t["status"] == "Active"])
        active_incidents = len([t for t in self.live_threats if t["status"] == "Active"])
        
        # Calculate posture score (0-100)
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
        """Generate dynamic data for threat radar visualization"""
        threats = []
        for _ in range(random.randint(5, 12)):
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
    
    # Terminal-style interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='dashboard-panel'>
            <h4 style='color: #00ff00;'>SYSTEM STATUS: OPERATIONAL</h4>
            <p style='color: #00ff00;'>🟢 Threat Intelligence: ONLINE</p>
            <p style='color: #00ff00;'>🟢 Network Defense: ACTIVE</p>
            <p style='color: #00ff00;'>🟢 Endpoint Protection: ENABLED</p>
            <p style='color: #00ff00;'>🟢 Incident Response: READY</p>
            <p style='color: #ffff00;'>Live Data Stream: ACTIVE</p>
            <p style='color: #ffff00;'>Real-time Monitoring: ENABLED</p>
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
                        st.session_state.last_refresh = terminal.last_update
                        st.success("ACCESS GRANTED - WELCOME TO CYBER TERMINAL")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED - INVALID CREDENTIALS")
                else:
                    st.warning("ENTER CREDENTIALS FOR TERMINAL ACCESS")
    
    # Demo credentials
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
    
    # Auto-refresh every 3 seconds for real-time updates
    st_autorefresh(interval=3000, key="cyber_dashboard_refresh")
    
    # Update live data
    terminal.update_live_data()
    
    # Terminal Header with live timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); padding: 15px; border-bottom: 3px solid #00ff00; margin-bottom: 20px;'>
        <h2 style='color: #00ff00; margin: 0; text-align: center;'>
            🛡️ CYBER TERMINAL ACTIVE | OPERATOR: {user['first_name']} {user['last_name']} 
            | ROLE: {user['role'].upper()} | CLEARANCE: {user['clearance']}
        </h2>
        <p style='color: #00ff00; text-align: center; margin: 5px 0;'>
            LIVE UPDATE: {current_time} | DATA STREAM: <span class='blinking-cursor'>ACTIVE</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Sidebar
    with st.sidebar:
        st.markdown("**QUICK ACTIONS**", unsafe_allow_html=True)
        
        if st.button("🔄 FORCE SYSTEM REFRESH", use_container_width=True):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        attack_type = st.selectbox("Select Attack Type", ["DDoS", "Ransomware", "Data Breach", "APT Intrusion", "Phishing Campaign"])
        if st.button("🚨 SIMULATE LIVE ATTACK", use_container_width=True):
            attack_id = terminal.simulate_live_attack(attack_type)
            st.success(f"Live attack simulated: {attack_id}")
        
        if st.button("🛡️ DEPLOY COUNTERMEASURES", use_container_width=True):
            st.session_state.show_defense = True
        
        st.markdown("---")
        st.markdown("**TERMINAL MODULES**", unsafe_allow_html=True)
        
        module = st.radio("SELECT MODULE", [
            "📊 LIVE DASHBOARD", "🌐 NETWORK DEFENSE", "💻 ENDPOINT SECURITY", 
            "🕵️ THREAT HUNTING", "🔍 DIGITAL FORENSICS", "📡 THREAT INTELLIGENCE",
            "🚨 INCIDENT RESPONSE", "📈 ANALYTICS & REPORTING"
        ])
        
        st.markdown("---")
        st.markdown("**LIVE DATA STREAM**", unsafe_allow_html=True)
        
        # Show recent live events
        recent_events = terminal.live_events[-5:] if terminal.live_events else []
        for event in reversed(recent_events):
            event_color = "#ff0000" if event.get("severity") in ["High", "Critical"] else "#ffff00"
            st.markdown(f"""
            <div style='font-size: 0.8em; color: {event_color}; margin: 2px 0;'>
                [{event['timestamp'].strftime('%H:%M:%S')}] {event['type']}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚪 TERMINATE SESSION", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Route to selected module
    if "LIVE DASHBOARD" in module:
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
    """Display real-time cyber security dashboard"""
    
    # Cyber Posture Indicator
    posture, posture_color, posture_score = terminal.calculate_cyber_posture()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); padding: 20px; border: 3px solid {posture_color}; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h1 style='color: {posture_color}; margin: 0;'>CYBER POSTURE: {posture}</h1>
        <h2 style='color: {posture_color}; margin: 0;'>SCORE: {posture_score}/100</h2>
        <p style='color: #00ff00; margin: 5px 0;'>Last Updated: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics with live updates
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_threats = len([t for t in terminal.live_threats if t["severity"] == "Critical" and t["status"] == "Active"])
        st.markdown(f"""
        <div class='metric-glowing live-data-stream'>
            <h1 style='color: #ff0000;'>{critical_threats}</h1>
            <p>CRITICAL THREATS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_incidents = len([t for t in terminal.live_threats if t["status"] == "Active"])
        st.markdown(f"""
        <div class='metric-glowing live-data-stream'>
            <h1 style='color: #ff6600;'>{active_incidents}</h1>
            <p>ACTIVE INCIDENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        high_severity_alerts = len([a for a in terminal.ids_alerts if a["severity"] in ["High", "Critical"]])
        st.markdown(f"""
        <div class='metric-glowing live-data-stream'>
            <h1 style='color: #ffff00;'>{high_severity_alerts}</h1>
            <p>HIGH SEVERITY ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        endpoints_at_risk = len([e for e in terminal.endpoint_telemetry if e["risk_score"] > 70])
        st.markdown(f"""
        <div class='metric-glowing live-data-stream'>
            <h1 style='color: #00ff00;'>{endpoints_at_risk}</h1>
            <p>ENDPOINTS AT RISK</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat Radar and Live Monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 LIVE THREAT RADAR")
        
        # Create radar container
        radar_html = """
        <div class='radar-sweep'>
            <div class='sweep-line'></div>
        """
        
        # Add dynamic threat dots
        threats = terminal.get_threat_radar_data()
        for threat in threats:
            angle = threat["angle"]
            distance = threat["distance"]
            severity = threat["severity"]
            
            # Convert polar to Cartesian coordinates
            x = 50 + (distance * 40 * math.cos(angle))
            y = 50 + (distance * 40 * math.sin(angle))
            
            color = {"Critical": "#ff0000", "High": "#ff6600", "Medium": "#ffff00", "Low": "#00ff00"}[severity]
            
            radar_html += f"""
            <div class='threat-dot' style='left: {x}%; top: {y}%; background-color: {color};'></div>
            """
        
        radar_html += "</div>"
        st.markdown(radar_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📡 REAL-TIME THREAT FEED")
        
        # Real-time threat updates with streaming effect
        recent_threats = sorted(terminal.live_threats, key=lambda x: x["last_activity"], reverse=True)[:8]
        
        threat_feed_container = st.container()
        with threat_feed_container:
            for threat in recent_threats:
                severity_color = {
                    "Critical": "#ff0000",
                    "High": "#ff6600", 
                    "Medium": "#ffff00",
                    "Low": "#00ff00"
                }[threat["severity"]]
                
                time_diff = (datetime.now() - threat["last_activity"]).total_seconds()
                is_new = time_diff < 30  # Highlight threats from last 30 seconds
                new_indicator = " 🆕" if is_new else ""
                
                st.markdown(f"""
                <div class='log-entry live-data-stream'>
                    <span style='color: {severity_color};'>[{threat['last_activity'].strftime('%H:%M:%S')}]</span>
                    {threat['type']} | Source: {threat['source_country']} | Confidence: {threat['confidence']}%{new_indicator}
                </div>
                """, unsafe_allow_html=True)
    
    # Real-time Network Activity Stream
    st.markdown("### 🌐 LIVE NETWORK ACTIVITY STREAM")
    
    # Create a streaming log of network activity
    recent_activity = sorted(terminal.network_activity, key=lambda x: x["timestamp"], reverse=True)[:20]
    
    log_container = st.container()
    with log_container:
        for activity in recent_activity:
            flag_icon = "🚩" if activity["flagged"] else "  "
            threat_color = "#ff0000" if activity["threat_score"] > 80 else "#ffff00" if activity["threat_score"] > 60 else "#00ff00"
            
            # Highlight very recent activity
            time_diff = (datetime.now() - activity["timestamp"]).total_seconds()
            stream_class = "live-data-stream" if time_diff < 10 else ""
            
            st.markdown(f"""
            <div class='log-entry {stream_class}'>
                <span style='color: #00ff00;'>[{activity['timestamp'].strftime('%H:%M:%S')}]</span>
                {flag_icon} {activity['source_ip']}:{activity.get('source_port', 'N/A')} → {activity['dest_ip']}:{activity.get('dest_port', 'N/A')}
                <span style='color: #ffff00;'>{activity['protocol']}</span>
                <span style='color: {threat_color};'>Threat: {activity['threat_score']}%</span>
            </div>
            """, unsafe_allow_html=True)

def show_network_defense(terminal):
    """Display real-time network defense module"""
    st.markdown("## 🌐 NETWORK DEFENSE OPERATIONS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛡️ LIVE FIREWALL STATUS")
        
        # Dynamic firewall rules and status
        firewall_rules = [
            {"rule": "SSH Access", "status": random.choice(["Blocked", "Allowed", "Restricted"]), "hits": random.randint(1000, 5000)},
            {"rule": "Web Traffic", "status": random.choice(["Blocked", "Allowed", "Restricted"]), "hits": random.randint(50000, 100000)},
            {"rule": "Database Access", "status": random.choice(["Blocked", "Allowed", "Restricted"]), "hits": random.randint(200, 1000)},
            {"rule": "File Sharing", "status": random.choice(["Blocked", "Allowed", "Restricted"]), "hits": random.randint(500, 2000)},
            {"rule": "Remote Desktop", "status": random.choice(["Blocked", "Allowed", "Restricted"]), "hits": random.randint(50, 500)}
        ]
        
        for rule in firewall_rules:
            status_color = "#00ff00" if rule["status"] == "Allowed" else "#ffff00" if rule["status"] == "Restricted" else "#ff0000"
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 4px solid {status_color};'>
                <strong>{rule['rule']}</strong> | Status: <span style='color: {status_color};'>{rule['status']}</span> | Hits: {rule['hits'] + random.randint(-10, 10)}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 REAL-TIME TRAFFIC ANALYSIS")
        
        # Protocol distribution with live updates
        protocols = {}
        recent_activity = terminal.network_activity[-100:]  # Last 100 activities
        for activity in recent_activity:
            protocol = activity["protocol"]
            protocols[protocol] = protocols.get(protocol, 0) + 1
        
        if protocols:
            fig = px.pie(values=list(protocols.values()), names=list(protocols.keys()), 
                        title="Live Protocol Distribution")
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Real-time IDS/IPS Alerts
    st.markdown("### 🚨 LIVE INTRUSION DETECTION")
    
    high_severity_alerts = [a for a in terminal.ids_alerts if a["severity"] in ["High", "Critical"]][:10]
    
    for alert in high_severity_alerts:
        severity_color = "#ff0000" if alert["severity"] == "Critical" else "#ff6600"
        
        # Highlight recent alerts
        time_diff = (datetime.now() - alert["timestamp"]).total_seconds()
        is_recent = time_diff < 60  # Last minute
        
        recent_class = "live-data-stream" if is_recent else ""
        
        st.markdown(f"""
        <div class='threat-panel {recent_class}'>
            <strong>{alert['attack_type']}</strong> | 
            Source: {alert['source_ip']} → Dest: {alert['dest_ip']} | 
            Severity: <span style='color: {severity_color};'>{alert['severity']}</span> | 
            Action: {alert['action_taken']} | 
            Confidence: {alert['confidence']}%
        </div>
        """, unsafe_allow_html=True)
    
    # Live Network Defense Actions
    st.markdown("### 🎯 ACTIVE DEFENSE MEASURES")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔒 BLOCK MALICIOUS IPs", use_container_width=True):
            # Simulate blocking action
            blocked_ips = [alert["source_ip"] for alert in terminal.ids_alerts[-5:]]
            st.success(f"Blocked {len(blocked_ips)} malicious IPs")
    
    with col2:
        if st.button("🛡️ ENABLE DDoS PROTECTION", use_container_width=True):
            st.success("DDoS protection enabled - monitoring network traffic")
    
    with col3:
        if st.button("📡 SCAN FOR VULNERABILITIES", use_container_width=True):
            st.success("Network vulnerability scan initiated")

# ... (Other module functions would follow similar real-time patterns)

def main():
    # Initialize cyber terminal in session state
    if 'cyber_terminal' not in st.session_state:
        st.session_state.cyber_terminal = AdvancedCyberTerminal()
    
    # Initialize login state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.last_refresh = datetime.now()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        cyber_login()
    else:
        cyber_dashboard()

if __name__ == "__main__":
    main()
