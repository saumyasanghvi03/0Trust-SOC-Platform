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
    page_title="CYBER TERMINAL v3.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Cyber Terminal CSS with enhanced animations
st.markdown("""
<style>
    .main-header {
        font-size: 3.2rem;
        color: #00ff00;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px #00ff00;
        background: linear-gradient(90deg, #00ff00, #ffff00, #00ff00, #00ffff, #00ff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 100%;
        animation: gradient-shift 3s ease-in-out infinite, glow 2s ease-in-out infinite alternate;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
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
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.15);
        transition: all 0.3s ease;
    }
    .dashboard-panel:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.25);
    }
    .threat-panel {
        background: linear-gradient(135deg, #2a0a0a 0%, #1a0505 100%);
        border: 1px solid #ff0000;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        animation: pulse-red 2s infinite;
        transition: all 0.3s ease;
    }
    .threat-panel:hover {
        transform: scale(1.02);
    }
    @keyframes pulse-red {
        0% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255, 0, 0, 0.3); }
        50% { border-color: #ff4444; box-shadow: 0 0 25px rgba(255, 0, 0, 0.6); }
        100% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255, 0, 0, 0.3); }
    }
    .defense-panel {
        background: linear-gradient(135deg, #0a2a0a 0%, #051a05 100%);
        border: 1px solid #00ff00;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        animation: pulse-green 2s infinite;
        transition: all 0.3s ease;
    }
    .defense-panel:hover {
        transform: scale(1.02);
    }
    @keyframes pulse-green {
        0% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
        50% { border-color: #44ff44; box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
        100% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
    }
    .metric-glowing {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #00ff00;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        animation: metric-glow 3s infinite;
        transition: all 0.3s ease;
    }
    .metric-glowing:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.4);
    }
    @keyframes metric-glow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 0, 0.3); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 0, 0.3); }
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #00ff00;
        border-bottom: 1px solid #333;
        padding: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }
    .log-entry:hover {
        background-color: #1a1a1a;
        transform: translateX(8px);
        border-left: 3px solid #00ff00;
    }
    .terminal-output {
        background-color: #000000;
        border: 2px solid #00ff00;
        border-radius: 8px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        height: 500px;
        overflow-y: auto;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    }
    .cyber-button {
        background: linear-gradient(135deg, #00ff00, #00cc00);
        color: #000;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
    }
    .cyber-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 0, 0.4);
        background: linear-gradient(135deg, #00ff00, #00ff88);
    }
    .cyber-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .cyber-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.2);
        border-color: #00ff00;
    }
    .progress-cyber {
        height: 10px;
        border-radius: 5px;
        background: #333;
        overflow: hidden;
    }
    .progress-cyber-bar {
        height: 100%;
        background: linear-gradient(90deg, #00ff00, #ffff00);
        border-radius: 5px;
        transition: width 0.5s ease;
    }
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .neon-border {
        position: relative;
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 20px;
    }
    .neon-border::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ff00, #ffff00, #00ff00, #00ffff, #00ff00);
        border-radius: 14px;
        z-index: -1;
        animation: border-glow 3s linear infinite;
        background-size: 400% 400%;
    }
    @keyframes border-glow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hologram-effect {
        background: linear-gradient(135deg, 
            rgba(0, 255, 0, 0.1) 0%, 
            rgba(0, 255, 255, 0.1) 25%, 
            rgba(255, 255, 0, 0.1) 50%, 
            rgba(255, 0, 255, 0.1) 75%, 
            rgba(0, 255, 0, 0.1) 100%);
        background-size: 400% 400%;
        animation: hologram 8s ease infinite;
    }
    @keyframes hologram {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCyberTerminal:
    def __init__(self):
        self.last_update = datetime.now()
        self.live_data_running = False
        self.alert_history = []
        self.system_health = {
            "cpu_usage": 45,
            "memory_usage": 62,
            "network_throughput": 1.2,
            "storage_utilization": 78,
            "threat_detection_rate": 94
        }
        self.initialize_cyber_terminal()
        
    def initialize_cyber_terminal(self):
        """Initialize advanced cyber terminal data"""
        # Enhanced threat intelligence with more APT groups
        self.threat_intel_db = {
            "advanced_persistent_threats": [
                {"name": "APT29", "country": "Russia", "targets": ["Government", "Healthcare"], "tactics": ["Spear Phishing", "Custom Malware"], "risk_level": "High"},
                {"name": "APT1", "country": "China", "targets": ["Defense", "Technology"], "tactics": ["Watering Hole", "Zero-Day"], "risk_level": "Critical"},
                {"name": "Lazarus", "country": "North Korea", "targets": ["Finance", "Cryptocurrency"], "tactics": ["Supply Chain", "Ransomware"], "risk_level": "High"},
                {"name": "Equation Group", "country": "USA", "targets": ["Critical Infrastructure"], "tactics": ["Advanced Malware", "Zero-Day"], "risk_level": "Critical"},
                {"name": "Fancy Bear", "country": "Russia", "targets": ["Political", "Military"], "tactics": ["Phishing", "Credential Theft"], "risk_level": "High"}
            ],
            "malware_families": [
                {"name": "Emotet", "type": "Trojan", "primary_function": "Banking", "propagation": "Email", "detection_rate": 85},
                {"name": "TrickBot", "type": "Banking Trojan", "primary_function": "Credential Theft", "propagation": "Email", "detection_rate": 92},
                {"name": "Ryuk", "type": "Ransomware", "primary_function": "Data Encryption", "propagation": "Network", "detection_rate": 78},
                {"name": "WannaCry", "type": "Ransomware", "primary_function": "Data Encryption", "propagation": "Worm", "detection_rate": 95},
                {"name": "Stuxnet", "type": "Worm", "primary_function": "Industrial Sabotage", "propagation": "USB", "detection_rate": 99}
            ],
            "vulnerabilities": [
                {"cve": "CVE-2021-44228", "name": "Log4Shell", "severity": "Critical", "affected_software": ["Log4j"], "patch_status": "Available"},
                {"cve": "CVE-2021-34527", "name": "PrintNightmare", "severity": "Critical", "affected_software": ["Windows"], "patch_status": "Available"},
                {"cve": "CVE-2020-1472", "name": "Zerologon", "severity": "Critical", "affected_software": ["Windows Server"], "patch_status": "Available"},
                {"cve": "CVE-2022-22965", "name": "Spring4Shell", "severity": "High", "affected_software": ["Spring Framework"], "patch_status": "Available"}
            ]
        }
        
        # Enhanced SOC team with more roles
        self.cyber_team = {
            "cyber_commander": {
                "user_id": "cyber_commander",
                "password": self.hash_password("cyber123"),
                "first_name": "Alex",
                "last_name": "Thorne",
                "role": "commander",
                "clearance": "TOP SECRET",
                "specializations": ["Strategic Defense", "Threat Intelligence", "Incident Command"],
                "avatar": "👨‍💼"
            },
            "threat_hunter": {
                "user_id": "threat_hunter",
                "password": self.hash_password("cyber123"),
                "first_name": "Jordan",
                "last_name": "Reyes",
                "role": "threat_hunter",
                "clearance": "SECRET",
                "specializations": ["Malware Analysis", "Digital Forensics", "Threat Hunting"],
                "avatar": "👩‍💻"
            },
            "defense_analyst": {
                "user_id": "defense_analyst",
                "password": self.hash_password("cyber123"),
                "first_name": "Casey",
                "last_name": "Zhang",
                "role": "defense_analyst",
                "clearance": "SECRET",
                "specializations": ["Network Defense", "SIEM Management", "Vulnerability Management"],
                "avatar": "👨‍🔬"
            },
            "forensics_expert": {
                "user_id": "forensics_expert",
                "password": self.hash_password("cyber123"),
                "first_name": "Morgan",
                "last_name": "Kowalski",
                "role": "forensics_expert",
                "clearance": "SECRET",
                "specializations": ["Digital Forensics", "Memory Analysis", "Incident Response"],
                "avatar": "👩‍🔍"
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
        self.iot_devices = []
        self.cloud_assets = []
        
        # Generate initial data
        self.generate_live_threats()
        self.generate_network_activity()
        self.generate_endpoint_telemetry()
        self.generate_ids_alerts()
        self.generate_honeypot_data()
        self.generate_iot_devices()
        self.generate_cloud_assets()
        
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
        threat_types = ["APT Campaign", "Malware Distribution", "Phishing Campaign", "DDoS Attack", "Data Exfiltration", "Insider Threat", "Supply Chain Attack"]
        
        for i in range(15):
            threat = {
                "threat_id": f"THREAT-{i+1:06d}",
                "type": random.choice(threat_types),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "confidence": random.randint(60, 98),
                "first_detected": datetime.now() - timedelta(hours=random.randint(1, 72)),
                "last_activity": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "source_country": random.choice(["Russia", "China", "North Korea", "Iran", "Unknown", "USA", "Brazil"]),
                "target_sector": random.choice(["Finance", "Healthcare", "Government", "Energy", "Technology", "Education"]),
                "indicators": [f"Indicator-{j}" for j in range(random.randint(2, 5))],
                "status": random.choice(["Active", "Monitoring", "Contained", "Eradicated"]),
                "assigned_to": random.choice(list(self.cyber_team.keys())),
                "kill_chain_phase": random.choice(["Reconnaissance", "Weaponization", "Delivery", "Exploitation", "Installation", "C2", "Actions"]),
                "impact_score": random.randint(1, 10)
            }
            self.live_threats.append(threat)
    
    def generate_network_activity(self):
        """Generate realistic network activity"""
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "SMB", "RDP", "ICMP"]
        services = ["Web Server", "Database", "File Share", "DNS Server", "Mail Server", "VPN", "API Gateway", "Load Balancer"]
        
        # Clear existing and generate fresh data
        self.network_activity = []
        
        for i in range(800):
            activity = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 300)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "source_port": random.randint(1024, 65535),
                "dest_port": random.choice([80, 443, 22, 53, 25, 3389, 8080, 8443]),
                "protocol": random.choice(protocols),
                "service": random.choice(services),
                "bytes_sent": random.randint(100, 1000000),
                "bytes_received": random.randint(100, 500000),
                "packet_count": random.randint(10, 1000),
                "threat_score": random.randint(0, 100),
                "geo_location": random.choice(["Internal", "USA", "China", "Russia", "Germany", "Brazil", "India", "Japan"]),
                "flagged": random.random() < 0.15,
                "encrypted": random.random() < 0.7
            }
            self.network_activity.append(activity)
    
    def generate_endpoint_telemetry(self):
        """Generate endpoint security telemetry"""
        endpoints = [f"WS-{i:03d}" for i in range(1, 81)] + [f"SRV-{i:03d}" for i in range(1, 31)] + [f"MOB-{i:03d}" for i in range(1, 21)]
        processes = ["explorer.exe", "chrome.exe", "winlogon.exe", "svchost.exe", "powershell.exe", "cmd.exe", "notepad.exe", "teams.exe"]
        
        self.endpoint_telemetry = []
        
        for endpoint in endpoints:
            telemetry = {
                "endpoint_id": endpoint,
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "os_version": random.choice(["Windows 10", "Windows 11", "Windows Server 2019", "Windows Server 2022", "macOS 13", "Ubuntu 22.04"]),
                "antivirus_status": random.choice(["Enabled", "Disabled", "Outdated"]),
                "threats_detected": random.randint(0, 3),
                "suspicious_processes": random.sample(processes, random.randint(0, 2)),
                "network_connections": random.randint(5, 50),
                "risk_score": random.randint(0, 100),
                "patch_level": random.choice(["Current", "1-2 weeks behind", "1 month behind", "Critical updates missing"]),
                "encryption_status": random.choice(["Enabled", "Disabled", "Partial"]),
                "last_scan": datetime.now() - timedelta(days=random.randint(0, 7)),
                "user_activity": random.choice(["Active", "Idle", "Offline"]),
                "compliance_status": random.choice(["Compliant", "Non-Compliant", "At Risk"])
            }
            self.endpoint_telemetry.append(telemetry)
    
    def generate_ids_alerts(self):
        """Generate IDS/IPS alerts"""
        attack_types = ["Port Scan", "Brute Force", "SQL Injection", "XSS", "DDoS", "Malware Download", "Data Theft", "Zero-Day Exploit", "Credential Stuffing"]
        
        self.ids_alerts = []
        
        for i in range(150):
            alert = {
                "alert_id": f"IDS-{i+1:06d}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 240)),
                "attack_type": random.choice(attack_types),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "signature": f"SIG-{random.randint(1000, 9999)}",
                "action_taken": random.choice(["Allowed", "Blocked", "Alerted", "Quarantined"]),
                "confidence": random.randint(70, 99),
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
                "payload_info": f"Malicious payload detected: {random.choice(['Exploit kit', 'Ransomware', 'Trojan', 'Backdoor', 'Coin Miner'])}",
                "mitre_technique": random.choice(["T1055", "T1068", "T1071", "T1082", "T1105"])
            }
            self.ids_alerts.append(alert)
    
    def generate_honeypot_data(self):
        """Generate honeypot interaction data"""
        self.honeypot_data = []
        
        for i in range(35):
            interaction = {
                "honeypot_id": f"HONEY-{i+1:03d}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 48)),
                "attacker_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "attacker_country": random.choice(["China", "Russia", "USA", "Brazil", "Vietnam", "Iran", "North Korea", "India"]),
                "attack_type": random.choice(["SSH Brute Force", "Web Exploit", "Database Attack", "Service Scan", "IoT Exploit"]),
                "credentials_tried": random.randint(1, 50),
                "malware_dropped": random.random() < 0.3,
                "data_captured": random.randint(0, 5000),
                "threat_level": random.choice(["Low", "Medium", "High", "Critical"]),
                "campaign_id": f"CAMP-{random.randint(1000, 9999)}" if random.random() < 0.4 else None
            }
            self.honeypot_data.append(interaction)
    
    def generate_iot_devices(self):
        """Generate IoT device security data"""
        iot_types = ["Smart Camera", "Thermostat", "Smart Lock", "Industrial Sensor", "Medical Device", "Vehicle System"]
        
        self.iot_devices = []
        
        for i in range(25):
            device = {
                "device_id": f"IOT-{i+1:03d}",
                "type": random.choice(iot_types),
                "ip_address": f"10.1.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "firmware_version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                "last_seen": datetime.now() - timedelta(hours=random.randint(1, 24)),
                "security_status": random.choice(["Secure", "Vulnerable", "Compromised", "Unknown"]),
                "vulnerabilities": random.randint(0, 5),
                "network_traffic": random.randint(10, 1000),
                "risk_score": random.randint(0, 100)
            }
            self.iot_devices.append(device)
    
    def generate_cloud_assets(self):
        """Generate cloud asset security data"""
        cloud_services = ["EC2", "S3", "RDS", "Lambda", "Azure VM", "Cloud Storage", "Kubernetes", "Container Registry"]
        
        self.cloud_assets = []
        
        for i in range(20):
            asset = {
                "asset_id": f"CLOUD-{i+1:03d}",
                "service": random.choice(cloud_services),
                "provider": random.choice(["AWS", "Azure", "GCP"]),
                "region": random.choice(["us-east-1", "eu-west-1", "ap-southeast-1", "us-west-2"]),
                "security_status": random.choice(["Secure", "Misconfigured", "Public Exposure", "Encrypted"]),
                "compliance": random.choice(["Compliant", "Non-Compliant", "At Risk"]),
                "last_audit": datetime.now() - timedelta(days=random.randint(1, 30)),
                "threats_detected": random.randint(0, 3),
                "encryption_status": random.choice(["Enabled", "Disabled", "Partial"])
            }
            self.cloud_assets.append(asset)
    
    def simulate_live_attack(self, attack_type: str):
        """Simulate a live cyber attack"""
        attack_id = f"LIVE-ATTACK-{datetime.now().strftime('%H%M%S')}-{random.randint(100,999)}"
        
        # Create alert for this attack
        alert = {
            "timestamp": datetime.now(),
            "type": "LIVE_ATTACK_SIMULATION",
            "severity": "Critical",
            "message": f"Live attack simulation initiated: {attack_type}",
            "attack_id": attack_id,
            "source": "Attack Simulator"
        }
        self.alert_history.append(alert)
        
        # Add to live threats
        self.live_threats.append({
            "threat_id": attack_id,
            "type": attack_type,
            "severity": "Critical",
            "confidence": 95,
            "first_detected": datetime.now(),
            "last_activity": datetime.now(),
            "source_country": random.choice(["China", "Russia", "North Korea", "Iran"]),
            "target_sector": "Internal",
            "indicators": [f"Live-{i}" for i in range(3)],
            "status": "Active",
            "assigned_to": "cyber_commander",
            "kill_chain_phase": "Exploitation",
            "impact_score": 9
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
                    "effectiveness": random.randint(80, 100),
                    "status": "Completed",
                    "response_time": random.randint(30, 300)  # seconds
                }
                self.defense_actions.append(defense_action)
                
                # Create success alert
                alert = {
                    "timestamp": datetime.now(),
                    "type": "DEFENSE_ACTION",
                    "severity": "Medium",
                    "message": f"Countermeasures deployed against {attack_id}",
                    "measures": measures,
                    "source": "Defense System"
                }
                self.alert_history.append(alert)
                
                self.last_update = datetime.now()
                return True
        return False
    
    def calculate_cyber_posture(self):
        """Calculate overall cyber security posture"""
        critical_threats = len([t for t in self.live_threats if t.get("severity") == "Critical"])
        high_threats = len([t for t in self.live_threats if t.get("severity") == "High"])
        active_incidents = len([t for t in self.live_threats if t.get("status") == "Active"])
        
        # Calculate based on multiple factors
        base_score = 100
        score = base_score - (critical_threats * 10) - (high_threats * 5) - (active_incidents * 3)
        
        # Adjust based on system health
        health_penalty = (100 - self.system_health["threat_detection_rate"]) / 2
        score -= health_penalty
        
        score = max(0, min(100, score))
        
        if score >= 85:
            return "EXCELLENT", "#00ff00", score
        elif score >= 70:
            return "STRONG", "#88ff00", score
        elif score >= 55:
            return "MODERATE", "#ffff00", score
        elif score >= 40:
            return "WEAK", "#ff6600", score
        else:
            return "CRITICAL", "#ff0000", score
    
    def get_threat_radar_data(self):
        """Generate data for threat radar visualization"""
        threats = []
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0.2, 0.9)
            severity = random.choice(["Low", "Medium", "High", "Critical"])
            threats.append({
                "angle": angle,
                "distance": distance,
                "severity": severity,
                "type": random.choice(["APT", "Malware", "DDoS", "Phishing"])
            })
        return threats
    
    def get_system_health_metrics(self):
        """Get current system health metrics with slight variations"""
        # Simulate realistic fluctuations
        for key in self.system_health:
            change = random.randint(-5, 5)
            self.system_health[key] = max(0, min(100, self.system_health[key] + change))
        
        return self.system_health

def cyber_login():
    """Display enhanced cyber terminal login"""
    st.markdown('<div class="main-header">🛡️ CYBER TERMINAL v3.0</div>', unsafe_allow_html=True)
    st.markdown("### ADVANCED THREAT OPERATIONS PLATFORM", unsafe_allow_html=True)
    
    # Add hologram effect background
    st.markdown("""
    <div class='hologram-effect' style='border-radius: 15px; padding: 20px; margin-bottom: 20px;'>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='dashboard-panel floating-element'>
            <h4 style='color: #00ff00;'>🚀 ENHANCED SYSTEM STATUS</h4>
            <p style='color: #00ff00;'>🟢 Threat Intelligence: AI-ENHANCED</p>
            <p style='color: #00ff00;'>🟢 Network Defense: QUANTUM ACTIVE</p>
            <p style='color: #00ff00;'>🟢 Endpoint Protection: BEHAVIORAL AI</p>
            <p style='color: #00ff00;'>🟢 Incident Response: AUTOMATED</p>
            <p style='color: #ffff00;'>🔸 Last System Scan: 47 seconds ago</p>
            <p style='color: #ffff00;'>🔸 Active Threats: AI Monitoring</p>
            <p style='color: #ffff00;'>🔸 Defense Readiness: OPTIMAL</p>
        </div>
        """, unsafe_allow_html=True)
        
        # System metrics visualization
        st.markdown("""
        <div class='cyber-card'>
            <h5>📊 SYSTEM METRICS</h5>
            <div style='margin: 15px 0;'>
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>Threat Detection</span>
                    <span>94%</span>
                </div>
                <div class='progress-cyber'>
                    <div class='progress-cyber-bar' style='width: 94%;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>System Performance</span>
                    <span>87%</span>
                </div>
                <div class='progress-cyber'>
                    <div class='progress-cyber-bar' style='width: 87%;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>AI Readiness</span>
                    <span>96%</span>
                </div>
                <div class='progress-cyber'>
                    <div class='progress-cyber-bar' style='width: 96%;'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("cyber_login"):
            st.markdown("### 🔐 TERMINAL ACCESS", unsafe_allow_html=True)
            
            username = st.text_input("👤 OPERATOR ID", placeholder="Enter your operator ID...")
            password = st.text_input("🔒 ACCESS CODE", type="password", placeholder="Enter your access code...")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🚀 INITIATE CYBER TERMINAL", use_container_width=True)
            with col_b:
                st.form_submit_button("🔄 RESET CREDENTIALS", use_container_width=True)
            
            if login_button:
                if username and password:
                    terminal = st.session_state.cyber_terminal
                    if terminal.authenticate_user(username, password):
                        st.session_state.user = terminal.cyber_team[username]
                        st.session_state.logged_in = True
                        
                        # Success animation
                        st.markdown("""
                        <div style='text-align: center; padding: 20px;'>
                            <h3 style='color: #00ff00;'>✓ ACCESS GRANTED</h3>
                            <p style='color: #00ff00;'>Initializing enhanced cyber terminal...</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a progress bar for dramatic effect
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        st.success("🎉 WELCOME TO CYBER TERMINAL v3.0")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("""
                        ❌ ACCESS DENIED 
                        
                        Invalid credentials detected. 
                        Please verify your operator ID and access code.
                        """)
                else:
                    st.warning("⚠️ ENTER CREDENTIALS FOR TERMINAL ACCESS")
    
    st.markdown("---")
    
    # Enhanced authorized personnel section
    st.markdown("### 🎯 AUTHORIZED PERSONNEL", unsafe_allow_html=True)
    
    cols = st.columns(4)
    roles = [
        {"role": "CYBER COMMANDER", "id": "cyber_commander", "code": "cyber123", "clearance": "TOP SECRET", "avatar": "👨‍💼"},
        {"role": "THREAT HUNTER", "id": "threat_hunter", "code": "cyber123", "clearance": "SECRET", "avatar": "👩‍💻"},
        {"role": "DEFENSE ANALYST", "id": "defense_analyst", "code": "cyber123", "clearance": "SECRET", "avatar": "👨‍🔬"},
        {"role": "FORENSICS EXPERT", "id": "forensics_expert", "code": "cyber123", "clearance": "SECRET", "avatar": "👩‍🔍"}
    ]
    
    for idx, role in enumerate(roles):
        with cols[idx]:
            st.markdown(f"""
            <div class='cyber-card' style='text-align: center;'>
                <div style='font-size: 2em;'>{role['avatar']}</div>
                <h4>{role['role']}</h4>
                <p><strong>ID:</strong> <code>{role['id']}</code></p>
                <p><strong>CODE:</strong> <code>{role['code']}</code></p>
                <p><strong>CLEARANCE:</strong> {role['clearance']}</p>
            </div>
            """, unsafe_allow_html=True)

def cyber_dashboard():
    """Display enhanced main cyber terminal dashboard"""
    terminal = st.session_state.cyber_terminal
    user = st.session_state.user
    
    # Enhanced Terminal Header with user info
    st.markdown(f"""
    <div style='
        background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); 
        padding: 20px; 
        border-bottom: 3px solid #00ff00; 
        margin-bottom: 20px;
        border-radius: 0 0 15px 15px;
    '>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: #00ff00; margin: 0;'>
                    🛡️ CYBER TERMINAL v3.0 ACTIVE
                </h1>
                <p style='color: #00ff00; margin: 5px 0;'>
                    OPERATOR: {user['first_name']} {user['last_name']} {user['avatar']} | 
                    ROLE: {user['role'].upper()} | 
                    CLEARANCE: {user['clearance']}
                </p>
            </div>
            <div style='text-align: right;'>
                <p style='color: #00ff00; margin: 0;'>SYSTEM TIME</p>
                <p style='color: #00ff00; margin: 0; font-size: 1.2em;'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Quick Actions Sidebar
    with st.sidebar:
        st.markdown("### ⚡ QUICK ACTIONS", unsafe_allow_html=True)
        
        # Action buttons with icons
        if st.button("🔄 FORCE SYSTEM REFRESH", use_container_width=True, key="refresh_main"):
            terminal.generate_network_activity()
            terminal.generate_live_threats()
            terminal.last_update = datetime.now()
            st.rerun()
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True, key="sim_attack"):
            attack_type = random.choice(["DDoS", "Ransomware", "Data Breach", "APT Intrusion", "Zero-Day Exploit"])
            attack_id = terminal.simulate_live_attack(attack_type)
            st.success(f"🎯 Live attack simulated: {attack_id}")
            time.sleep(0.5)
            st.rerun()
        
        if st.button("📊 GENERATE REPORT", use_container_width=True, key="gen_report"):
            st.info("📈 Comprehensive threat report generated and saved")
        
        if st.button("🛡️ RUN COMPLIANCE SCAN", use_container_width=True, key="compliance_scan"):
            st.info("🔍 Compliance scan initiated across all assets")
        
        st.markdown("---")
        st.markdown("### 🎮 TERMINAL MODULES", unsafe_allow_html=True)
        
        # Enhanced module selector with icons
        module = st.radio("SELECT MODULE", [
            "📊 ENHANCED DASHBOARD", 
            "🌐 QUANTUM NETWORK DEFENSE", 
            "💻 AI ENDPOINT SECURITY", 
            "🕵️ ADVANCED THREAT HUNTING", 
            "🔍 DIGITAL FORENSICS LAB", 
            "📡 GLOBAL THREAT INTELLIGENCE",
            "🚨 AUTOMATED INCIDENT RESPONSE", 
            "📈 PREDICTIVE ANALYTICS",
            "☁️ CLOUD SECURITY",
            "🔧 IOT DEFENSE"
        ], key="module_selector")
        
        st.markdown("---")
        st.markdown("### 🔔 RECENT ALERTS", unsafe_allow_html=True)
        
        # Show recent alerts
        recent_alerts = terminal.alert_history[-3:] if terminal.alert_history else []
        for alert in recent_alerts:
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }.get(alert.get("severity", "Low"), "#00ff00")
            
            st.markdown(f"""
            <div style='
                background: #1a1a1a; 
                padding: 8px; 
                margin: 5px 0; 
                border-left: 3px solid {severity_color};
                border-radius: 4px;
                font-size: 0.8em;
            '>
                <strong>{alert.get('type', 'Alert')}</strong><br>
                {alert.get('message', 'No message')}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚪 TERMINATE SESSION", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Route to selected module - FIXED: All modules now have proper function mappings
    if "ENHANCED DASHBOARD" in module:
        show_enhanced_dashboard(terminal)
    elif "QUANTUM NETWORK" in module:
        show_quantum_network_defense(terminal)
    elif "AI ENDPOINT" in module:
        show_ai_endpoint_security(terminal)
    elif "ADVANCED THREAT" in module:
        show_advanced_threat_hunting(terminal)
    elif "DIGITAL FORENSICS" in module:
        show_digital_forensics_lab(terminal)
    elif "GLOBAL THREAT" in module:
        show_global_threat_intelligence(terminal)
    elif "AUTOMATED INCIDENT" in module:
        show_automated_incident_response(terminal)
    elif "PREDICTIVE ANALYTICS" in module:
        show_predictive_analytics(terminal)
    elif "CLOUD SECURITY" in module:
        show_cloud_security(terminal)
    elif "IOT DEFENSE" in module:
        show_iot_defense(terminal)

def show_enhanced_dashboard(terminal):
    """Display enhanced cyber security dashboard"""
    
    # Real-time Cyber Posture Indicator
    posture, posture_color, posture_score = terminal.calculate_cyber_posture()
    st.markdown(f"""
    <div class='neon-border' style='text-align: center; padding: 25px; margin-bottom: 25px;'>
        <h1 style='color: {posture_color}; margin: 0; font-size: 2.5em;'>CYBER POSTURE: {posture}</h1>
        <h2 style='color: {posture_color}; margin: 10px 0; font-size: 3em;'>{posture_score}/100</h2>
        <div class='progress-cyber' style='margin: 0 auto; width: 60%;'>
            <div class='progress-cyber-bar' style='width: {posture_score}%;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Key Metrics with system health
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_threats = len([t for t in terminal.live_threats if t.get("severity") == "Critical"])
        st.markdown(f"""
        <div class='metric-glowing floating-element'>
            <h1 style='color: #ff0000; font-size: 2.5em;'>{critical_threats}</h1>
            <p>🚨 CRITICAL THREATS</p>
            <div class='progress-cyber'>
                <div class='progress-cyber-bar' style='width: {min(critical_threats * 10, 100)}%; background: #ff0000;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_incidents = len([t for t in terminal.live_threats if t.get("status") == "Active"])
        st.markdown(f"""
        <div class='metric-glowing floating-element'>
            <h1 style='color: #ff6600; font-size: 2.5em;'>{active_incidents}</h1>
            <p>🔥 ACTIVE INCIDENTS</p>
            <div class='progress-cyber'>
                <div class='progress-cyber-bar' style='width: {min(active_incidents * 15, 100)}%; background: #ff6600;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        network_alerts = len([a for a in terminal.ids_alerts if a.get("severity") in ["High", "Critical"]])
        st.markdown(f"""
        <div class='metric-glowing floating-element'>
            <h1 style='color: #ffff00; font-size: 2.5em;'>{network_alerts}</h1>
            <p>🌐 CRITICAL ALERTS</p>
            <div class='progress-cyber'>
                <div class='progress-cyber-bar' style='width: {min(network_alerts * 2, 100)}%; background: #ffff00;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        endpoints_at_risk = len([e for e in terminal.endpoint_telemetry if e.get("risk_score", 0) > 70])
        st.markdown(f"""
        <div class='metric-glowing floating-element'>
            <h1 style='color: #00ff00; font-size: 2.5em;'>{endpoints_at_risk}</h1>
            <p>💻 ENDPOINTS AT RISK</p>
            <div class='progress-cyber'>
                <div class='progress-cyber-bar' style='width: {min(endpoints_at_risk * 2, 100)}%; background: #00ff00;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # System Health and Threat Feed
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏥 SYSTEM HEALTH MONITOR")
        health_metrics = terminal.get_system_health_metrics()
        
        for metric, value in health_metrics.items():
            metric_name = metric.replace("_", " ").title()
            color = "#00ff00" if value > 80 else "#ffff00" if value > 60 else "#ff6600"
            
            st.markdown(f"""
            <div style='margin: 15px 0;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span>{metric_name}</span>
                    <span style='color: {color};'>{value}%</span>
                </div>
                <div class='progress-cyber'>
                    <div class='progress-cyber-bar' style='width: {value}%; background: {color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔥 LIVE THREAT FEED")
        
        # Add threat radar visualization
        threats = terminal.get_threat_radar_data()
        
        # Create a simple radar visualization using plotly
        fig = go.Figure()
        
        for threat in threats:
            color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }.get(threat["severity"], "#00ff00")
            
            fig.add_trace(go.Scatterpolar(
                r=[threat["distance"]],
                theta=[threat["angle"] * 180 / math.pi],
                mode='markers',
                marker=dict(
                    size=15,
                    color=color,
                    line=dict(width=2, color='white')
                ),
                name=threat["severity"],
                hovertemplate=f"<b>{threat['type']}</b><br>Severity: {threat['severity']}<extra></extra>"
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                angularaxis=dict(visible=True)
            ),
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#00ff00'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Real-time Activity Streams
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌐 LIVE NETWORK ACTIVITY")
        
        if terminal.network_activity:
            recent_activity = sorted(terminal.network_activity, 
                                   key=lambda x: x.get("timestamp", datetime.now()), 
                                   reverse=True)[:10]
            
            for activity in recent_activity:
                flagged = activity.get("flagged", False)
                flag_icon = "🚩" if flagged else "  "
                
                threat_score = activity.get("threat_score", 0)
                threat_color = "#ff0000" if threat_score > 80 else "#ffff00" if threat_score > 60 else "#00ff00"
                
                timestamp = activity.get("timestamp", datetime.now())
                source_ip = activity.get("source_ip", "0.0.0.0")
                dest_ip = activity.get("dest_ip", "0.0.0.0")
                protocol = activity.get("protocol", "UNKNOWN")
                
                st.markdown(f"""
                <div class='log-entry'>
                    <span style='color: #00ff00;'>[{timestamp.strftime('%H:%M:%S')}]</span>
                    {flag_icon} {source_ip} → {dest_ip}
                    <span style='color: #ffff00;'>{protocol}</span>
                    <span style='color: {threat_color}; float: right;'>Threat: {threat_score}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No network activity data available")
    
    with col2:
        st.markdown("### ⚡ SECURITY EVENTS")
        
        # Combine various event types
        all_events = []
        
        # Add IDS alerts
        for alert in terminal.ids_alerts[-5:]:
            all_events.append({
                "timestamp": alert.get("timestamp", datetime.now()),
                "type": "IDS Alert",
                "message": f"{alert.get('attack_type', 'Unknown')} from {alert.get('source_ip', 'Unknown')}",
                "severity": alert.get("severity", "Low")
            })
        
        # Add defense actions
        for action in terminal.defense_actions[-3:]:
            all_events.append({
                "timestamp": action.get("timestamp", datetime.now()),
                "type": "Defense Action",
                "message": f"Countermeasures deployed: {', '.join(action.get('measures_deployed', []))}",
                "severity": "Medium"
            })
        
        # Sort by timestamp
        all_events.sort(key=lambda x: x.get("timestamp", datetime.now()), reverse=True)
        
        for event in all_events[:8]:
            severity = event.get("severity", "Low")
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }.get(severity, "#00ff00")
            
            timestamp = event.get("timestamp", datetime.now())
            
            st.markdown(f"""
            <div class='log-entry'>
                <span style='color: {severity_color};'>[{timestamp.strftime('%H:%M:%S')}]</span>
                <strong>{event['type']}</strong>: {event['message']}
            </div>
            """, unsafe_allow_html=True)

# MISSING FUNCTION IMPLEMENTATIONS - ADDED BELOW

def show_quantum_network_defense(terminal):
    """Display quantum network defense module"""
    st.markdown("## 🌐 QUANTUM NETWORK DEFENSE")
    st.markdown("### AI-Powered Network Protection System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛡️ QUANTUM FIREWALL STATUS")
        
        firewall_stats = {
            "Total Rules": 1247,
            "Active Rules": 892,
            "Blocks Today": 2341,
            "Threats Prevented": 167
        }
        
        for stat, value in firewall_stats.items():
            st.markdown(f"""
            <div class='cyber-card' style='text-align: center;'>
                <h3 style='color: #00ff00; margin: 0;'>{value}</h3>
                <p style='margin: 0;'>{stat}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 NETWORK TRAFFIC ANALYSIS")
        
        # Create network traffic visualization
        protocols = {}
        for activity in terminal.network_activity[:200]:
            protocol = activity.get("protocol", "UNKNOWN")
            protocols[protocol] = protocols.get(protocol, 0) + 1
        
        if protocols:
            fig = px.pie(values=list(protocols.values()), names=list(protocols.keys()), 
                        title="Protocol Distribution")
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00',
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

def show_ai_endpoint_security(terminal):
    """Display AI endpoint security module"""
    st.markdown("## 💻 AI ENDPOINT SECURITY")
    st.markdown("### Behavioral Analysis & Machine Learning Protection")
    
    # Endpoint risk analysis
    high_risk = len([e for e in terminal.endpoint_telemetry if e.get("risk_score", 0) > 70])
    medium_risk = len([e for e in terminal.endpoint_telemetry if 40 <= e.get("risk_score", 0) <= 70])
    low_risk = len([e for e in terminal.endpoint_telemetry if e.get("risk_score", 0) < 40])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='threat-panel' style='text-align: center;'>
            <h1 style='color: #ff0000;'>{high_risk}</h1>
            <p>HIGH RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='defense-panel' style='text-align: center;'>
            <h1 style='color: #ffff00;'>{medium_risk}</h1>
            <p>MEDIUM RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='dashboard-panel' style='text-align: center;'>
            <h1 style='color: #00ff00;'>{low_risk}</h1>
            <p>LOW RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Endpoint details
    st.markdown("#### 🔍 ENDPOINT DETAILS")
    if st.checkbox("Show High Risk Endpoints"):
        high_risk_endpoints = [e for e in terminal.endpoint_telemetry if e.get("risk_score", 0) > 70]
        for endpoint in high_risk_endpoints[:5]:
            with st.expander(f"🚨 {endpoint['endpoint_id']} - Risk: {endpoint['risk_score']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**OS:** {endpoint.get('os_version', 'Unknown')}")
                    st.write(f"**AV Status:** {endpoint.get('antivirus_status', 'Unknown')}")
                    st.write(f"**Threats:** {endpoint.get('threats_detected', 0)}")
                with col2:
                    st.write(f"**Patch Level:** {endpoint.get('patch_level', 'Unknown')}")
                    st.write(f"**Last Scan:** {endpoint.get('last_scan', 'Never')}")

def show_advanced_threat_hunting(terminal):
    """Display advanced threat hunting module"""
    st.markdown("## 🕵️ ADVANCED THREAT HUNTING")
    st.markdown("### Proactive Threat Detection & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 HUNTING QUERIES")
        
        queries = [
            "Processes with network connections to known malicious IPs",
            "Suspicious PowerShell execution patterns", 
            "Unusual scheduled task creations",
            "Registry modifications by unknown processes",
            "Lateral movement attempts using WMI"
        ]
        
        for i, query in enumerate(queries):
            st.markdown(f"""
            <div class='cyber-card'>
                <strong>Query #{i+1}:</strong> {query}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Run Query #{i+1}", key=f"query_{i}"):
                st.success(f"Query executed: Found {random.randint(0, 5)} suspicious activities")
    
    with col2:
        st.markdown("#### 📊 HUNTING RESULTS")
        
        results = [
            {"type": "Suspicious Process", "endpoint": "WS-023", "confidence": 85, "timestamp": "2 hours ago"},
            {"type": "Network Anomaly", "endpoint": "SRV-005", "confidence": 92, "timestamp": "1 hour ago"},
            {"type": "Fileless Attack", "endpoint": "WS-042", "confidence": 78, "timestamp": "3 hours ago"}
        ]
        
        for result in results:
            confidence = result["confidence"]
            color = "#00ff00" if confidence > 90 else "#ffff00" if confidence > 75 else "#ff6600"
            
            st.markdown(f"""
            <div class='threat-panel'>
                <strong>{result['type']}</strong><br>
                Endpoint: {result['endpoint']} | 
                Confidence: <span style='color: {color};'>{confidence}%</span> |
                {result['timestamp']}
            </div>
            """, unsafe_allow_html=True)

def show_digital_forensics_lab(terminal):
    """Display digital forensics lab module"""
    st.markdown("## 🔍 DIGITAL FORENSICS LAB")
    st.markdown("### Advanced Forensic Analysis & Investigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧩 FORENSIC ARTIFACTS")
        
        artifacts = [
            {"type": "Memory Dump", "size": "4.2 GB", "status": "Analyzed", "findings": 3},
            {"type": "Disk Image", "size": "128 GB", "status": "In Progress", "findings": 12},
            {"type": "Network Capture", "size": "2.1 GB", "status": "Analyzed", "findings": 8},
            {"type": "Log Files", "size": "856 MB", "status": "Pending", "findings": 0}
        ]
        
        for artifact in artifacts:
            status_color = "#00ff00" if artifact["status"] == "Analyzed" else "#ffff00" if artifact["status"] == "In Progress" else "#ff6600"
            
            st.markdown(f"""
            <div class='cyber-card'>
                <strong>{artifact['type']}</strong><br>
                Size: {artifact['size']} | 
                Status: <span style='color: {status_color};'>{artifact['status']}</span> |
                Findings: {artifact['findings']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔬 MALWARE ANALYSIS")
        
        malware_samples = [
            {"name": "Trojan.Emotet", "risk": "High", "analysis": "Behavioral analysis completed"},
            {"name": "Ransomware.Ryuk", "risk": "Critical", "analysis": "Reverse engineering in progress"},
            {"name": "Backdoor.DarkComet", "risk": "High", "analysis": "Network analysis completed"}
        ]
        
        for malware in malware_samples:
            risk_color = "#ff0000" if malware["risk"] == "Critical" else "#ff6600"
            
            st.markdown(f"""
            <div class='threat-panel'>
                <strong>{malware['name']}</strong><br>
                Risk: <span style='color: {risk_color};'>{malware['risk']}</span><br>
                {malware['analysis']}
            </div>
            """, unsafe_allow_html=True)

def show_global_threat_intelligence(terminal):
    """Display global threat intelligence module"""
    st.markdown("## 📡 GLOBAL THREAT INTELLIGENCE")
    st.markdown("### Real-time Global Threat Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌍 ADVANCED PERSISTENT THREATS")
        
        for apt in terminal.threat_intel_db["advanced_persistent_threats"]:
            risk_color = "#ff0000" if apt["risk_level"] == "Critical" else "#ff6600"
            
            st.markdown(f"""
            <div class='threat-panel'>
                <strong>{apt['name']}</strong> | <span style='color: {risk_color};'>{apt['risk_level']}</span><br>
                Country: {apt['country']} | Targets: {', '.join(apt['targets'])}<br>
                Tactics: {', '.join(apt['tactics'])}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🦠 MALWARE FAMILIES")
        
        for malware in terminal.threat_intel_db["malware_families"]:
            detection_color = "#00ff00" if malware["detection_rate"] > 90 else "#ffff00"
            
            st.markdown(f"""
            <div class='cyber-card'>
                <strong>{malware['name']}</strong> | Type: {malware['type']}<br>
                Function: {malware['primary_function']} | Propagation: {malware['propagation']}<br>
                Detection: <span style='color: {detection_color};'>{malware['detection_rate']}%</span>
            </div>
            """, unsafe_allow_html=True)

def show_automated_incident_response(terminal):
    """Display automated incident response module"""
    st.markdown("## 🚨 AUTOMATED INCIDENT RESPONSE")
    st.markdown("### AI-Driven Incident Management")
    
    active_incidents = [t for t in terminal.live_threats if t.get("status") == "Active"]
    
    st.markdown(f"#### 🔥 ACTIVE INCIDENTS: {len(active_incidents)}")
    
    if not active_incidents:
        st.success("🎉 No active incidents requiring immediate attention")
        return
    
    for incident in active_incidents:
        severity = incident.get("severity", "Low")
        severity_color = "#ff0000" if severity == "Critical" else "#ff6600" if severity == "High" else "#ffff00"
        
        with st.expander(f"🚨 {incident['threat_id']} - {incident['type']} - Severity: {severity}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**First Detected:** {incident.get('first_detected', 'Unknown')}")
                st.write(f"**Source Country:** {incident.get('source_country', 'Unknown')}")
                st.write(f"**Confidence:** {incident.get('confidence', 0)}%")
            
            with col2:
                st.write(f"**Assigned To:** {incident.get('assigned_to', 'Unassigned')}")
                st.write(f"**Kill Chain:** {incident.get('kill_chain_phase', 'Unknown')}")
                st.write(f"**Impact Score:** {incident.get('impact_score', 0)}/10")
            
            # Response actions
            col3, col4, col5 = st.columns(3)
            with col3:
                if st.button("🛑 CONTAIN", key=f"contain_{incident['threat_id']}"):
                    measures = ["Network Isolation", "Endpoint Quarantine"]
                    if terminal.deploy_countermeasures(incident['threat_id'], measures):
                        st.success("✓ Threat contained successfully!")
            with col4:
                if st.button("🔍 INVESTIGATE", key=f"investigate_{incident['threat_id']}"):
                    st.info("🔍 Deep investigation initiated...")
            with col5:
                if st.button("📋 ESCALATE", key=f"escalate_{incident['threat_id']}"):
                    st.warning("⚠️ Incident escalated to Cyber Commander")

def show_predictive_analytics(terminal):
    """Display predictive analytics module"""
    st.markdown("## 📈 PREDICTIVE ANALYTICS")
    st.markdown("### AI-Powered Threat Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 THREAT TRENDS")
        
        # Generate sample trend data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        threats = [random.randint(5, 25) for _ in range(30)]
        
        fig = px.line(x=dates, y=threats, title="Daily Threat Detection (Last 30 Days)")
        fig.update_layout(
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#1a1a1a',
            font_color='#00ff00',
            xaxis_title="Date",
            yaxis_title="Threats Detected"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 ATTACK PREDICTION")
        
        predictions = [
            {"type": "Phishing Campaign", "probability": 85, "timeframe": "Next 48 hours"},
            {"type": "Ransomware Attack", "probability": 67, "timeframe": "Next 7 days"},
            {"type": "DDoS Attack", "probability": 42, "timeframe": "Next 24 hours"}
        ]
        
        for pred in predictions:
            prob_color = "#ff0000" if pred["probability"] > 80 else "#ff6600" if pred["probability"] > 60 else "#ffff00"
            
            st.markdown(f"""
            <div class='cyber-card'>
                <strong>{pred['type']}</strong><br>
                Probability: <span style='color: {prob_color};'>{pred['probability']}%</span><br>
                Timeframe: {pred['timeframe']}
            </div>
            """, unsafe_allow_html=True)

def show_cloud_security(terminal):
    """Display cloud security module"""
    st.markdown("## ☁️ CLOUD SECURITY")
    st.markdown("### Multi-Cloud Security Management")
    
    # Cloud asset overview
    st.markdown("#### 📊 CLOUD ASSET OVERVIEW")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        aws_assets = len([a for a in terminal.cloud_assets if a.get("provider") == "AWS"])
        st.markdown(f"""
        <div class='dashboard-panel' style='text-align: center;'>
            <h3 style='color: #ff9900;'>{aws_assets}</h3>
            <p>AWS Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        azure_assets = len([a for a in terminal.cloud_assets if a.get("provider") == "Azure"])
        st.markdown(f"""
        <div class='dashboard-panel' style='text-align: center;'>
            <h3 style='color: #0078d4;'>{azure_assets}</h3>
            <p>Azure Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gcp_assets = len([a for a in terminal.cloud_assets if a.get("provider") == "GCP"])
        st.markdown(f"""
        <div class='dashboard-panel' style='text-align: center;'>
            <h3 style='color: #4285f4;'>{gcp_assets}</h3>
            <p>GCP Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cloud security issues
    st.markdown("#### 🚨 CLOUD SECURITY ISSUES")
    
    misconfigured = [a for a in terminal.cloud_assets if a.get("security_status") == "Misconfigured"]
    for asset in misconfigured[:3]:
        st.markdown(f"""
        <div class='threat-panel'>
            <strong>{asset['asset_id']}</strong> - {asset['service']} ({asset['provider']})<br>
            Issue: Misconfiguration detected in {asset['region']}<br>
            Compliance: {asset.get('compliance', 'Unknown')}
        </div>
        """, unsafe_allow_html=True)

def show_iot_defense(terminal):
    """Display IoT defense module"""
    st.markdown("## 🔧 IOT DEFENSE")
    st.markdown("### IoT Device Security & Monitoring")
    
    # IoT device overview
    st.markdown("#### 📱 IOT DEVICE OVERVIEW")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vulnerable = len([d for d in terminal.iot_devices if d.get("security_status") == "Vulnerable"])
        st.markdown(f"""
        <div class='threat-panel' style='text-align: center;'>
            <h3 style='color: #ff0000;'>{vulnerable}</h3>
            <p>Vulnerable Devices</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        compromised = len([d for d in terminal.iot_devices if d.get("security_status") == "Compromised"])
        st.markdown(f"""
        <div class='threat-panel' style='text-align: center;'>
            <h3 style='color: #ff6600;'>{compromised}</h3>
            <p>Compromised Devices</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        secure = len([d for d in terminal.iot_devices if d.get("security_status") == "Secure"])
        st.markdown(f"""
        <div class='defense-panel' style='text-align: center;'>
            <h3 style='color: #00ff00;'>{secure}</h3>
            <p>Secure Devices</p>
        </div>
        """, unsafe_allow_html=True)
    
    # High risk IoT devices
    st.markdown("#### 🔍 HIGH RISK IOT DEVICES")
    
    high_risk_iot = [d for d in terminal.iot_devices if d.get("risk_score", 0) > 70]
    for device in high_risk_iot[:5]:
        st.markdown(f"""
        <div class='cyber-card'>
            <strong>{device['device_id']}</strong> - {device['type']}<br>
            IP: {device['ip_address']} | Risk Score: {device['risk_score']}<br>
            Firmware: {device['firmware_version']} | Vulnerabilities: {device['vulnerabilities']}
        </div>
        """, unsafe_allow_html=True)

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
