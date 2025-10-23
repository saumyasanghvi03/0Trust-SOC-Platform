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
import uuid
from typing import Dict, List, Any
import warnings
from collections import defaultdict, deque
import base64
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AEGIS CYBER COMMAND CENTER",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Cyber Terminal CSS with professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    .main {
        background-color: #0a0e27;
        background-image: 
            linear-gradient(rgba(0, 255, 0, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 0, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 900;
        color: #00ff41;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 
            0 0 10px #00ff41,
            0 0 20px #00ff41,
            0 0 30px #00ff41,
            0 0 40px #00ff41;
        animation: glow-pulse 2s ease-in-out infinite alternate;
        letter-spacing: 5px;
    }
    
    @keyframes glow-pulse {
        from { 
            text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41;
            transform: scale(1);
        }
        to { 
            text-shadow: 0 0 20px #00ff41, 0 0 30px #00ff41, 0 0 40px #00ff41, 0 0 50px #00ff41;
            transform: scale(1.02);
        }
    }
    
    .cyber-subheader {
        text-align: center;
        color: #0ff;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.2rem;
        letter-spacing: 3px;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px #0ff;
    }
    
    .terminal-window {
        background: #000;
        border: 2px solid #00ff41;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41;
        font-size: 0.9rem;
        height: 400px;
        overflow-y: auto;
        box-shadow: 
            0 0 20px rgba(0, 255, 65, 0.3),
            inset 0 0 20px rgba(0, 255, 65, 0.05);
        position: relative;
    }
    
    .terminal-window::before {
        content: "● ● ●";
        position: absolute;
        top: -25px;
        left: 10px;
        color: #ff5f56;
        font-size: 20px;
        letter-spacing: 5px;
    }
    
    .terminal-window::-webkit-scrollbar {
        width: 10px;
    }
    
    .terminal-window::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    .terminal-window::-webkit-scrollbar-thumb {
        background: #00ff41;
        border-radius: 5px;
    }
    
    .log-line {
        margin: 3px 0;
        padding: 2px 5px;
        border-left: 2px solid transparent;
        transition: all 0.2s ease;
    }
    
    .log-line:hover {
        background: rgba(0, 255, 65, 0.1);
        border-left: 2px solid #00ff41;
        transform: translateX(5px);
    }
    
    .log-critical {
        color: #ff0040;
        text-shadow: 0 0 5px #ff0040;
        animation: blink 1s infinite;
    }
    
    .log-high {
        color: #ff6b00;
    }
    
    .log-medium {
        color: #ffeb3b;
    }
    
    .log-low {
        color: #00ff41;
    }
    
    @keyframes blink {
        0%, 50%, 100% { opacity: 1; }
        25%, 75% { opacity: 0.7; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #0f1729 100%);
        border: 1px solid #00ff41;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 255, 65, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(0, 255, 65, 0.1),
            transparent
        );
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 30px rgba(0, 255, 65, 0.4);
        border-color: #0ff;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        font-family: 'Share Tech Mono', monospace;
        margin: 10px 0;
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        color: #888;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .threat-card {
        background: linear-gradient(135deg, #2d0a0a 0%, #1a0505 100%);
        border: 1px solid #ff0040;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 0, 64, 0.3);
        transition: all 0.3s ease;
        animation: pulse-red 3s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { 
            box-shadow: 0 0 15px rgba(255, 0, 64, 0.3);
            border-color: #ff0040;
        }
        50% { 
            box-shadow: 0 0 25px rgba(255, 0, 64, 0.6);
            border-color: #ff3366;
        }
    }
    
    .threat-card:hover {
        transform: scale(1.02);
    }
    
    .status-bar {
        background: linear-gradient(90deg, #1a1f3a 0%, #0f1729 100%);
        border: 1px solid #00ff41;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .command-input {
        background: #000;
        border: 2px solid #00ff41;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        padding: 10px;
        width: 100%;
        border-radius: 5px;
        font-size: 1rem;
    }
    
    .command-input:focus {
        outline: none;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }
    
    .cyber-btn {
        background: linear-gradient(135deg, #00ff41 0%, #00aa2b 100%);
        border: none;
        color: #000;
        padding: 12px 24px;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 255, 65, 0.3);
    }
    
    .cyber-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 65, 0.5);
        background: linear-gradient(135deg, #44ff66 0%, #00cc33 100%);
    }
    
    .cyber-btn-danger {
        background: linear-gradient(135deg, #ff0040 0%, #cc0033 100%);
        color: #fff;
    }
    
    .cyber-btn-danger:hover {
        background: linear-gradient(135deg, #ff3366 0%, #ff0044 100%);
        box-shadow: 0 6px 20px rgba(255, 0, 64, 0.5);
    }
    
    .network-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
        gap: 5px;
        padding: 20px;
        background: #000;
        border: 2px solid #00ff41;
        border-radius: 8px;
    }
    
    .network-node {
        width: 40px;
        height: 40px;
        background: #00ff41;
        border-radius: 50%;
        transition: all 0.3s ease;
        opacity: 0.3;
    }
    
    .network-node.active {
        opacity: 1;
        box-shadow: 0 0 15px #00ff41;
        animation: node-pulse 2s infinite;
    }
    
    .network-node.threat {
        background: #ff0040;
        opacity: 1;
        box-shadow: 0 0 15px #ff0040;
        animation: node-pulse 1s infinite;
    }
    
    @keyframes node-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .radar-container {
        position: relative;
        width: 100%;
        max-width: 400px;
        height: 400px;
        margin: 0 auto;
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
        width: 200%;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00ff41 50%, transparent 100%);
        top: 50%;
        left: 50%;
        transform-origin: 0% 50%;
        animation: radar-spin 4s linear infinite;
    }
    
    @keyframes radar-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .timeline-event {
        position: relative;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #00ff41;
        background: linear-gradient(90deg, rgba(0, 255, 65, 0.1) 0%, transparent 100%);
        transition: all 0.3s ease;
    }
    
    .timeline-event:hover {
        background: linear-gradient(90deg, rgba(0, 255, 65, 0.2) 0%, transparent 100%);
        transform: translateX(5px);
    }
    
    .timeline-event::before {
        content: "●";
        position: absolute;
        left: -8px;
        top: 15px;
        color: #00ff41;
        font-size: 20px;
    }
    
    .heatmap-cell {
        display: inline-block;
        width: 12px;
        height: 12px;
        margin: 1px;
        border-radius: 2px;
        transition: all 0.2s ease;
    }
    
    .heatmap-cell:hover {
        transform: scale(1.5);
        z-index: 10;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .badge-critical {
        background: #ff0040;
        color: #fff;
        box-shadow: 0 0 10px rgba(255, 0, 64, 0.5);
    }
    
    .badge-high {
        background: #ff6b00;
        color: #fff;
    }
    
    .badge-medium {
        background: #ffeb3b;
        color: #000;
    }
    
    .badge-low {
        background: #00ff41;
        color: #000;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #1a1f3a;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff41 0%, #00aa2b 100%);
        border-radius: 4px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    .ip-address {
        font-family: 'Share Tech Mono', monospace;
        color: #0ff;
        background: rgba(0, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.9em;
    }
    
    .stButton>button {
        font-family: 'Share Tech Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

class MITREAttack:
    """MITRE ATT&CK Framework Integration"""
    
    TACTICS = {
        "TA0001": "Initial Access",
        "TA0002": "Execution",
        "TA0003": "Persistence",
        "TA0004": "Privilege Escalation",
        "TA0005": "Defense Evasion",
        "TA0006": "Credential Access",
        "TA0007": "Discovery",
        "TA0008": "Lateral Movement",
        "TA0009": "Collection",
        "TA0010": "Exfiltration",
        "TA0011": "Command and Control",
        "TA0040": "Impact"
    }
    
    TECHNIQUES = {
        "T1566": {"name": "Phishing", "tactic": "TA0001"},
        "T1059": {"name": "Command and Scripting Interpreter", "tactic": "TA0002"},
        "T1053": {"name": "Scheduled Task/Job", "tactic": "TA0003"},
        "T1078": {"name": "Valid Accounts", "tactic": "TA0004"},
        "T1027": {"name": "Obfuscated Files or Information", "tactic": "TA0005"},
        "T1003": {"name": "OS Credential Dumping", "tactic": "TA0006"},
        "T1083": {"name": "File and Directory Discovery", "tactic": "TA0007"},
        "T1021": {"name": "Remote Services", "tactic": "TA0008"},
        "T1005": {"name": "Data from Local System", "tactic": "TA0009"},
        "T1041": {"name": "Exfiltration Over C2 Channel", "tactic": "TA0010"},
        "T1071": {"name": "Application Layer Protocol", "tactic": "TA0011"},
        "T1486": {"name": "Data Encrypted for Impact", "tactic": "TA0040"}
    }
    
    @staticmethod
    def get_random_technique():
        technique_id = random.choice(list(MITREAttack.TECHNIQUES.keys()))
        technique = MITREAttack.TECHNIQUES[technique_id]
        return {
            "id": technique_id,
            "name": technique["name"],
            "tactic": MITREAttack.TACTICS[technique["tactic"]]
        }

class ThreatIntelligence:
    """Enhanced Threat Intelligence Database"""
    
    # Real APT groups with realistic attributes
    APT_GROUPS = {
        "APT28": {
            "country": "Russia",
            "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm"],
            "targets": ["Government", "Military", "Security"],
            "ttps": ["Spear Phishing", "Zero-Day Exploits", "Custom Malware"],
            "active_since": "2007"
        },
        "APT29": {
            "country": "Russia",
            "aliases": ["Cozy Bear", "The Dukes"],
            "targets": ["Government", "Think Tanks", "Healthcare"],
            "ttps": ["Stealth", "Advanced Malware", "Long-term Persistence"],
            "active_since": "2008"
        },
        "APT41": {
            "country": "China",
            "aliases": ["Barium", "Winnti"],
            "targets": ["Healthcare", "Telecommunications", "Technology"],
            "ttps": ["Supply Chain Attacks", "Rootkits", "Data Theft"],
            "active_since": "2012"
        },
        "Lazarus": {
            "country": "North Korea",
            "aliases": ["Hidden Cobra", "Guardians of Peace"],
            "targets": ["Financial", "Cryptocurrency", "Media"],
            "ttps": ["Destructive Attacks", "Financial Fraud", "Ransomware"],
            "active_since": "2009"
        }
    }
    
    # Realistic malware families
    MALWARE_FAMILIES = {
        "Emotet": {
            "type": "Banking Trojan/Loader",
            "first_seen": "2014",
            "capabilities": ["Credential Theft", "Lateral Movement", "Malware Delivery"],
            "c2_protocol": "HTTP/HTTPS",
            "persistence": ["Registry", "Scheduled Tasks"]
        },
        "TrickBot": {
            "type": "Banking Trojan",
            "first_seen": "2016",
            "capabilities": ["Banking Fraud", "Reconnaissance", "Lateral Movement"],
            "c2_protocol": "HTTPS",
            "persistence": ["Services", "Scheduled Tasks"]
        },
        "Ryuk": {
            "type": "Ransomware",
            "first_seen": "2018",
            "capabilities": ["File Encryption", "Shadow Copy Deletion", "Network Propagation"],
            "c2_protocol": "N/A (No C2)",
            "persistence": ["One-time execution"]
        },
        "Cobalt Strike": {
            "type": "Post-Exploitation Framework",
            "first_seen": "2012",
            "capabilities": ["Remote Access", "Lateral Movement", "Credential Dumping"],
            "c2_protocol": "HTTP/HTTPS/DNS",
            "persistence": ["Services", "DLL Hijacking"]
        }
    }
    
    # Real CVEs
    CRITICAL_CVES = [
        {
            "id": "CVE-2021-44228",
            "name": "Log4Shell",
            "cvss": 10.0,
            "description": "Apache Log4j2 Remote Code Execution",
            "affected": ["Log4j 2.0-beta9 to 2.15.0"],
            "published": "2021-12-10"
        },
        {
            "id": "CVE-2021-34527",
            "name": "PrintNightmare",
            "cvss": 8.8,
            "description": "Windows Print Spooler RCE",
            "affected": ["Windows Server", "Windows 10/11"],
            "published": "2021-07-02"
        },
        {
            "id": "CVE-2020-1472",
            "name": "Zerologon",
            "cvss": 10.0,
            "description": "Netlogon Elevation of Privilege",
            "affected": ["Windows Server 2008-2019"],
            "published": "2020-08-17"
        },
        {
            "id": "CVE-2023-23397",
            "name": "Outlook Elevation of Privilege",
            "cvss": 9.8,
            "description": "Microsoft Outlook Privilege Escalation",
            "affected": ["Microsoft Outlook"],
            "published": "2023-03-14"
        }
    ]

class CyberTerminal:
    """Advanced Cyber Security Operations Terminal"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = datetime.now()
        self.initialize_security()
        self.initialize_data_streams()
        
    def initialize_security(self):
        """Initialize security and authentication"""
        self.operators = {
            "admin": {
                "password": self.hash_password("cyber2024"),
                "name": "Dr. Alex Morgan",
                "role": "Chief Security Officer",
                "clearance": "COSMIC TOP SECRET",
                "badge_id": "CSO-001",
                "specializations": ["Strategic Defense", "Incident Command", "Threat Intelligence"]
            },
            "analyst": {
                "password": self.hash_password("cyber2024"),
                "name": "Jordan Chen",
                "role": "Senior Threat Analyst",
                "clearance": "TOP SECRET",
                "badge_id": "STA-042",
                "specializations": ["Malware Analysis", "Threat Hunting", "Forensics"]
            },
            "hunter": {
                "password": self.hash_password("cyber2024"),
                "name": "Taylor Rivera",
                "role": "Threat Hunter",
                "clearance": "SECRET",
                "badge_id": "THN-087",
                "specializations": ["Behavioral Analysis", "IOC Development", "SIEM Analytics"]
            }
        }
    
    def hash_password(self, password: str) -> str:
        """Secure password hashing"""
        salt = "aegis_cyber_terminal_2024"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def initialize_data_streams(self):
        """Initialize real-time data streams"""
        # Live event streams
        self.event_stream = deque(maxlen=1000)
        self.network_stream = deque(maxlen=500)
        self.threat_stream = deque(maxlen=200)
        
        # Active threats and incidents
        self.active_threats = []
        self.incidents = []
        self.alerts = []
        
        # Network topology
        self.network_segments = self.generate_network_topology()
        
        # Endpoints
        self.endpoints = self.generate_endpoints()
        
        # Generate initial data
        self.populate_initial_data()
        
        # Command history
        self.command_history = []
    
    def generate_network_topology(self):
        """Generate realistic network topology"""
        segments = {
            "DMZ": {
                "subnet": "10.0.1.0/24",
                "devices": ["Web Server", "Mail Server", "DNS Server"],
                "risk_level": "High"
            },
            "Corporate": {
                "subnet": "10.0.10.0/24",
                "devices": ["Workstations", "Printers", "VOIP"],
                "risk_level": "Medium"
            },
            "Servers": {
                "subnet": "10.0.20.0/24",
                "devices": ["File Server", "Database", "Application Server"],
                "risk_level": "Critical"
            },
            "Management": {
                "subnet": "10.0.30.0/24",
                "devices": ["SIEM", "Firewall", "IDS/IPS"],
                "risk_level": "Critical"
            }
        }
        return segments
    
    def generate_endpoints(self):
        """Generate endpoint inventory"""
        endpoints = []
        
        # Workstations
        for i in range(1, 51):
            endpoints.append({
                "id": f"WS-{i:03d}",
                "type": "Workstation",
                "os": random.choice(["Windows 11 Pro", "Windows 10 Enterprise"]),
                "ip": f"10.0.10.{i}",
                "user": f"user{i:03d}",
                "status": random.choice(["Online", "Online", "Online", "Offline"]),
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "risk_score": random.randint(10, 95),
                "av_status": random.choice(["Protected", "Protected", "Warning", "Critical"]),
                "patches_pending": random.randint(0, 15)
            })
        
        # Servers
        server_types = ["File Server", "Database", "Web Server", "Mail Server", "App Server"]
        for i, srv_type in enumerate(server_types, 1):
            endpoints.append({
                "id": f"SRV-{i:03d}",
                "type": "Server",
                "os": random.choice(["Windows Server 2022", "Windows Server 2019", "Linux Ubuntu 22.04"]),
                "ip": f"10.0.20.{i}",
                "service": srv_type,
                "status": "Online",
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 10)),
                "risk_score": random.randint(15, 75),
                "av_status": "Protected",
                "patches_pending": random.randint(0, 5)
            })
        
        return endpoints
    
    def populate_initial_data(self):
        """Populate with initial threat data"""
        # Generate initial threats
        for _ in range(random.randint(8, 15)):
            self.generate_threat_event()
        
        # Generate network events
        for _ in range(100):
            self.generate_network_event()
    
    def generate_threat_event(self):
        """Generate realistic threat event"""
        threat_types = [
            "Malware Detection",
            "Suspicious Network Activity", 
            "Unauthorized Access Attempt",
            "Data Exfiltration",
            "Phishing Campaign",
            "Brute Force Attack",
            "Port Scan",
            "Command and Control",
            "Lateral Movement"
        ]
        
        severities = ["Critical", "High", "Medium", "Low"]
        severity = random.choices(severities, weights=[10, 25, 40, 25])[0]
        
        threat = {
            "id": f"THR-{len(self.active_threats) + 1:06d}",
            "type": random.choice(threat_types),
            "severity": severity,
            "confidence": random.randint(65, 99),
            "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 240)),
            "source_ip": self.generate_external_ip(),
            "dest_ip": random.choice([e["ip"] for e in self.endpoints if e["status"] == "Online"]),
            "mitre_technique": MITREAttack.get_random_technique(),
            "status": random.choice(["Active", "Active", "Active", "Investigating", "Contained"]),
            "iocs": [self.generate_ioc() for _ in range(random.randint(2, 5))],
            "affected_assets": random.randint(1, 10),
            "analyst_assigned": random.choice(list(self.operators.keys())),
            "notes": []
        }
        
        self.active_threats.append(threat)
        self.log_event(f"[THREAT] {threat['severity']} - {threat['type']} detected from {threat['source_ip']}", severity)
        return threat
    
    def generate_network_event(self):
        """Generate network traffic event"""
        protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS", "SSH", "RDP", "SMB"]
        common_ports = [80, 443, 22, 21, 25, 53, 3389, 445, 3306, 8080]
        
        event = {
            "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 300)),
            "protocol": random.choice(protocols),
            "source_ip": random.choice([self.generate_external_ip(), self.generate_internal_ip()]),
            "dest_ip": self.generate_internal_ip(),
            "source_port": random.randint(1024, 65535),
            "dest_port": random.choice(common_ports),
            "bytes": random.randint(100, 1000000),
            "packets": random.randint(10, 10000),
            "threat_score": random.randint(0, 100),
            "action": random.choices(["Allow", "Block", "Alert"], weights=[85, 10, 5])[0]
        }
        
        self.network_stream.append(event)
        return event
    
    def generate_external_ip(self):
        """Generate realistic external IP"""
        ranges = [
            (1, 126),    # Class A
            (128, 191),  # Class B
            (192, 223)   # Class C
        ]
        first = random.choice(ranges)
        return f"{random.randint(first[0], first[1])}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def generate_internal_ip(self):
        """Generate internal IP"""
        return f"10.0.{random.randint(1, 30)}.{random.randint(1, 254)}"
    
    def generate_ioc(self):
        """Generate Indicator of Compromise"""
        ioc_types = [
            ("IP", lambda: self.generate_external_ip()),
            ("Domain", lambda: f"{random.choice(['malware', 'phish', 'exploit', 'bad'])}{random.randint(100, 999)}.{random.choice(['com', 'net', 'org', 'info'])}"),
            ("Hash", lambda: hashlib.md5(str(random.random()).encode()).hexdigest()),
            ("File", lambda: f"{random.choice(['invoice', 'document', 'update', 'report'])}.{random.choice(['exe', 'dll', 'scr', 'bat'])}")
        ]
        
        ioc_type, generator = random.choice(ioc_types)
        return {
            "type": ioc_type,
            "value": generator(),
            "confidence": random.randint(70, 99)
        }
    
    def log_event(self, message: str, severity: str = "Info"):
        """Log event to stream"""
        event = {
            "timestamp": datetime.now(),
            "severity": severity,
            "message": message
        }
        self.event_stream.append(event)
    
    def execute_command(self, command: str, user: str):
        """Execute terminal command"""
        self.command_history.append({
            "timestamp": datetime.now(),
            "user": user,
            "command": command
        })
        
        cmd_parts = command.strip().lower().split()
        if not cmd_parts:
            return "Command required"
        
        cmd = cmd_parts[0]
        
        # Command routing
        if cmd == "help":
            return self.cmd_help()
        elif cmd == "status":
            return self.cmd_status()
        elif cmd == "threats":
            return self.cmd_threats()
        elif cmd == "scan":
            return self.cmd_scan(cmd_parts)
        elif cmd == "block":
            return self.cmd_block(cmd_parts)
        elif cmd == "isolate":
            return self.cmd_isolate(cmd_parts)
        elif cmd == "investigate":
            return self.cmd_investigate(cmd_parts)
        elif cmd == "clear":
            return "clear"
        else:
            return f"Unknown command: {cmd}. Type 'help' for available commands."
    
    def cmd_help(self):
        """Show help"""
        return """
╔══════════════════════════════════════════════════════════╗
║              AEGIS TERMINAL COMMAND REFERENCE            ║
╠══════════════════════════════════════════════════════════╣
║ status              - Show system status                 ║
║ threats             - List active threats                ║
║ scan <target>       - Initiate security scan            ║
║ block <ip>          - Block IP address                  ║
║ isolate <endpoint>  - Isolate endpoint                  ║
║ investigate <id>    - Investigate threat                ║
║ clear               - Clear terminal                     ║
║ help                - Show this help                     ║
╚══════════════════════════════════════════════════════════╝
        """
    
    def cmd_status(self):
        """System status"""
        critical = len([t for t in self.active_threats if t["severity"] == "Critical"])
        high = len([t for t in self.active_threats if t["severity"] == "High"])
        
        return f"""
SYSTEM STATUS: OPERATIONAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Threats: {len(self.active_threats)} | Critical: {critical} | High: {high}
Endpoints: {len([e for e in self.endpoints if e['status'] == 'Online'])}/{len(self.endpoints)} Online
Network: PROTECTED | Firewall: ACTIVE | IDS: ENABLED
Last Update: {datetime.now().strftime('%H:%M:%S')}
        """
    
    def cmd_threats(self):
        """List threats"""
        if not self.active_threats:
            return "No active threats detected"
        
        output = "\nACTIVE THREATS:\n" + "="*60 + "\n"
        for threat in sorted(self.active_threats, key=lambda x: x["timestamp"], reverse=True)[:10]:
            output += f"{threat['id']} | {threat['severity']:8} | {threat['type']}\n"
            output += f"  Source: {threat['source_ip']} → {threat['dest_ip']}\n"
            output += f"  Status: {threat['status']} | Confidence: {threat['confidence']}%\n"
            output += "-"*60 + "\n"
        
        return output
    
    def cmd_scan(self, parts):
        """Initiate scan"""
        target = parts[1] if len(parts) > 1 else "all"
        self.log_event(f"Security scan initiated on {target}", "Info")
        return f"Initiating security scan on {target}...\nScan ID: SCAN-{random.randint(1000, 9999)}"
    
    def cmd_block(self, parts):
        """Block IP"""
        if len(parts) < 2:
            return "Usage: block <ip_address>"
        
        ip = parts[1]
        self.log_event(f"IP {ip} blocked via firewall", "Warning")
        return f"✓ IP {ip} has been blocked across all network segments"
    
    def cmd_isolate(self, parts):
        """Isolate endpoint"""
        if len(parts) < 2:
            return "Usage: isolate <endpoint_id>"
        
        endpoint_id = parts[1]
        self.log_event(f"Endpoint {endpoint_id} isolated", "Warning")
        return f"✓ Endpoint {endpoint_id} has been isolated from the network"
    
    def cmd_investigate(self, parts):
        """Investigate threat"""
        if len(parts) < 2:
            return "Usage: investigate <threat_id>"
        
        threat_id = parts[1]
        self.log_event(f"Investigation started: {threat_id}", "Info")
        return f"Investigation case opened for {threat_id}\nCase ID: INV-{random.randint(1000, 9999)}"
    
    def calculate_security_posture(self):
        """Calculate overall security posture"""
        base_score = 100
        
        # Threat impact
        for threat in self.active_threats:
            if threat["status"] == "Active":
                if threat["severity"] == "Critical":
                    base_score -= 15
                elif threat["severity"] == "High":
                    base_score -= 8
                elif threat["severity"] == "Medium":
                    base_score -= 3
        
        # Endpoint health
        at_risk = len([e for e in self.endpoints if e["risk_score"] > 70])
        base_score -= at_risk * 2
        
        # Normalize
        score = max(0, min(100, base_score))
        
        if score >= 85:
            return score, "OPTIMAL", "#00ff41"
        elif score >= 70:
            return score, "STRONG", "#7fff00"
        elif score >= 50:
            return score, "MODERATE", "#ffeb3b"
        elif score >= 30:
            return score, "DEGRADED", "#ff6b00"
        else:
            return score, "CRITICAL", "#ff0040"

# Initialize session state
if 'terminal' not in st.session_state:
    st.session_state.terminal = CyberTerminal()
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.terminal_output = []

def render_login():
    """Render authentication screen"""
    st.markdown('<div class="main-header">⬢ AEGIS ⬢</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-subheader">CYBER COMMAND CENTER</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="status-bar">
            <div style="text-align: center;">
                <h3 style="color: #00ff41; margin: 0;">⬡ AUTHENTICATION REQUIRED ⬡</h3>
                <p style="color: #888;">Enter credentials to access terminal</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            operator_id = st.text_input("🔐 OPERATOR ID", placeholder="Enter operator ID")
            access_code = st.text_input("🔑 ACCESS CODE", type="password", placeholder="Enter access code")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("⚡ AUTHENTICATE", use_container_width=True)
            with col_b:
                clear = st.form_submit_button("✖ CLEAR", use_container_width=True)
            
            if submit:
                terminal = st.session_state.terminal
                if operator_id in terminal.operators:
                    if terminal.hash_password(access_code) == terminal.operators[operator_id]["password"]:
                        st.session_state.authenticated = True
                        st.session_state.current_user = operator_id
                        terminal.log_event(f"Operator {terminal.operators[operator_id]['name']} authenticated", "Info")
                        st.success("✓ AUTHENTICATION SUCCESSFUL")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("✗ ACCESS DENIED - Invalid credentials")
                        terminal.log_event(f"Failed authentication attempt for {operator_id}", "Warning")
                else:
                    st.error("✗ ACCESS DENIED - Unknown operator")
    
    # Demo credentials
    st.markdown("---")
    st.markdown("### 🎫 AUTHORIZED OPERATORS")
    
    col1, col2, col3 = st.columns(3)
    
    terminal = st.session_state.terminal
    operators_list = list(terminal.operators.items())
    
    for idx, (op_id, op_data) in enumerate(operators_list):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 10px;">👤</div>
                <strong>{op_data['name']}</strong><br>
                <span class="metric-label">{op_data['role']}</span><br>
                <code style="color: #00ff41;">ID: {op_id}</code><br>
                <code style="color: #0ff;">CODE: cyber2024</code><br>
                <span class="badge badge-low">{op_data['clearance']}</span>
            </div>
            """, unsafe_allow_html=True)

def render_dashboard():
    """Render main dashboard"""
    terminal = st.session_state.terminal
    user = terminal.operators[st.session_state.current_user]
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1f3a 0%, #0f1729 100%); padding: 20px; border-bottom: 3px solid #00ff41; margin-bottom: 20px; border-radius: 10px;">
        <h1 style="color: #00ff41; margin: 0; text-align: center; font-family: 'Share Tech Mono', monospace; letter-spacing: 3px;">
            ⬡ AEGIS CYBER COMMAND CENTER ⬡
        </h1>
        <div style="text-align: center; color: #0ff; margin-top: 10px; font-family: 'Share Tech Mono', monospace;">
            OPERATOR: {user['name']} | {user['role']} | CLEARANCE: {user['clearance']} | SESSION: {terminal.session_id}
        </div>
        <div style="text-align: center; color: #888; font-family: 'Share Tech Mono', monospace; font-size: 0.9em;">
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | SYSTEM: OPERATIONAL | DEFCON: 3
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚡ QUICK ACTIONS")
        
        if st.button("🔄 REFRESH DATA", use_container_width=True):
            terminal.generate_threat_event()
            for _ in range(10):
                terminal.generate_network_event()
            st.rerun()
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True):
            threat = terminal.generate_threat_event()
            threat["severity"] = "Critical"
            threat["status"] = "Active"
            st.success(f"Attack simulated: {threat['id']}")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎯 MODULES")
        
        module = st.radio("", [
            "📊 Command Dashboard",
            "🌐 Network Defense",
            "💻 Endpoint Security",
            "🔍 Threat Intelligence",
            "🚨 Active Incidents",
            "📡 Live Monitoring",
            "🎮 Terminal Console",
            "📈 Analytics"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("🚪 TERMINATE SESSION", use_container_width=True):
            terminal.log_event(f"Operator {user['name']} logged out", "Info")
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
    
    # Route to modules
    if "Command Dashboard" in module:
        render_command_dashboard(terminal, user)
    elif "Network Defense" in module:
        render_network_defense(terminal, user)
    elif "Endpoint Security" in module:
        render_endpoint_security(terminal, user)
    elif "Threat Intelligence" in module:
        render_threat_intelligence(terminal, user)
    elif "Active Incidents" in module:
        render_active_incidents(terminal, user)
    elif "Live Monitoring" in module:
        render_live_monitoring(terminal, user)
    elif "Terminal Console" in module:
        render_terminal_console(terminal, user)
    elif "Analytics" in module:
        render_analytics(terminal, user)

def render_command_dashboard(terminal, user):
    """Main command dashboard"""
    
    # Security posture
    score, status, color = terminal.calculate_security_posture()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1f3a 0%, #0f1729 100%); padding: 30px; border: 3px solid {color}; border-radius: 10px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 30px {color}50;">
        <h1 style="color: {color}; margin: 0; font-size: 3rem; text-shadow: 0 0 20px {color};">
            SECURITY POSTURE: {status}
        </h1>
        <h2 style="color: {color}; margin: 10px 0; font-size: 2.5rem;">
            {score}/100
        </h2>
        <div class="progress-bar" style="max-width: 600px; margin: 20px auto;">
            <div class="progress-fill" style="width: {score}%; background: {color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    critical_threats = len([t for t in terminal.active_threats if t["severity"] == "Critical"])
    active_incidents = len([t for t in terminal.active_threats if t["status"] == "Active"])
    endpoints_online = len([e for e in terminal.endpoints if e["status"] == "Online"])
    network_events = len(terminal.network_stream)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ff0040;">{critical_threats}</div>
            <div class="metric-label">CRITICAL THREATS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ff6b00;">{active_incidents}</div>
            <div class="metric-label">ACTIVE INCIDENTS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #00ff41;">{endpoints_online}</div>
            <div class="metric-label">ENDPOINTS ONLINE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #0ff;">{network_events}</div>
            <div class="metric-label">NETWORK EVENTS</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time feeds
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 ACTIVE THREATS")
        
        active_threats = [t for t in terminal.active_threats if t["status"] == "Active"][:5]
        
        if active_threats:
            for threat in active_threats:
                severity_color = {
                    "Critical": "#ff0040",
                    "High": "#ff6b00",
                    "Medium": "#ffeb3b",
                    "Low": "#00ff41"
                }[threat["severity"]]
                
                st.markdown(f"""
                <div class="threat-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #fff; font-size: 1.1em;">{threat['type']}</strong><br>
                            <span style="color: #888;">{threat['id']}</span> | 
                            <span class="ip-address">{threat['source_ip']}</span> → 
                            <span class="ip-address">{threat['dest_ip']}</span>
                        </div>
                        <div>
                            <span class="badge badge-{threat['severity'].lower()}">{threat['severity']}</span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; color: #aaa; font-size: 0.9em;">
                        MITRE: {threat['mitre_technique']['id']} - {threat['mitre_technique']['name']}<br>
                        Confidence: {threat['confidence']}% | Assets: {threat['affected_assets']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active threats detected")
    
    with col2:
        st.markdown("### 📡 LIVE EVENT STREAM")
        
        st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
        
        events = list(terminal.event_stream)[-15:]
        for event in reversed(events):
            severity_class = f"log-{event['severity'].lower()}"
            timestamp = event['timestamp'].strftime('%H:%M:%S')
            st.markdown(f"""
            <div class="log-line {severity_class}">
                [{timestamp}] {event['message']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Network activity visualization
    st.markdown("### 🌐 NETWORK ACTIVITY MAP")
    
    # Create network traffic heatmap
    hours = list(range(24))
    current_hour = datetime.now().hour
    
    # Generate activity data for last 24 hours
    activity_data = []
    for hour in hours:
        count = random.randint(50, 500)
        activity_data.append(count)
    
    fig = go.Figure(data=go.Bar(
        x=hours,
        y=activity_data,
        marker=dict(
            color=activity_data,
            colorscale=[[0, '#00ff41'], [0.5, '#ffeb3b'], [1, '#ff0040']],
            showscale=True
        )
    ))
    
    fig.update_layout(
        title="Network Traffic (Last 24 Hours)",
        xaxis_title="Hour",
        yaxis_title="Events",
        paper_bgcolor='#0a0e27',
        plot_bgcolor='#1a1f3a',
        font_color='#00ff41',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_network_defense(terminal, user):
    """Network defense module"""
    st.markdown("## 🌐 NETWORK DEFENSE OPERATIONS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🛡️ FIREWALL STATUS")
        
        # Network segments
        for segment_name, segment_data in terminal.network_segments.items():
            risk_color = {
                "Critical": "#ff0040",
                "High": "#ff6b00",
                "Medium": "#ffeb3b",
                "Low": "#00ff41"
            }[segment_data["risk_level"]]
            
            with st.expander(f"📍 {segment_name} Network - {segment_data['subnet']}", expanded=True):
                st.markdown(f"""
                <div style="background: #1a1f3a; padding: 15px; border-left: 4px solid {risk_color}; border-radius: 5px;">
                    <strong>Risk Level:</strong> <span style="color: {risk_color};">{segment_data['risk_level']}</span><br>
                    <strong>Devices:</strong> {', '.join(segment_data['devices'])}
                </div>
                """, unsafe_allow_html=True)
                
                # Actions
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"🔒 Lock Down {segment_name}", key=f"lock_{segment_name}"):
                        terminal.log_event(f"{segment_name} network segment locked down", "Warning")
                        st.success(f"✓ {segment_name} segment isolated")
                
                with col_b:
                    if st.button(f"🔍 Scan {segment_name}", key=f"scan_{segment_name}"):
                        terminal.log_event(f"Security scan initiated on {segment_name}", "Info")
                        st.info(f"Scanning {segment_name}...")
    
    with col2:
        st.markdown("### 📊 TRAFFIC STATS")
        
        # Protocol distribution
        protocols = defaultdict(int)
        for event in terminal.network_stream:
            protocols[event['protocol']] += 1
        
        if protocols:
            fig = go.Figure(data=[go.Pie(
                labels=list(protocols.keys()),
                values=list(protocols.values()),
                hole=0.4,
                marker=dict(colors=['#00ff41', '#0ff', '#ffeb3b', '#ff6b00'])
            )])
            
            fig.update_layout(
                paper_bgcolor='#0a0e27',
                font_color='#00ff41',
                height=300,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # IDS/IPS Alerts
    st.markdown("### 🚨 INTRUSION DETECTION ALERTS")
    
    # Generate some IDS alerts
    ids_alerts = []
    for _ in range(10):
        alert = {
            "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 120)),
            "signature": f"ET-{random.randint(1000, 9999)}",
            "message": random.choice([
                "Suspicious Outbound Connection",
                "Port Scan Detected",
                "SQL Injection Attempt",
                "Brute Force Login Attempt",
                "Malware C2 Communication"
            ]),
            "source": terminal.generate_external_ip(),
            "dest": terminal.generate_internal_ip(),
            "severity": random.choice(["Critical", "High", "Medium", "Low"]),
            "action": random.choice(["Blocked", "Alerted", "Allowed"])
        }
        ids_alerts.append(alert)
    
    # Display as table
    df = pd.DataFrame(ids_alerts)
    df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime('%H:%M:%S'))
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

def render_endpoint_security(terminal, user):
    """Endpoint security module"""
    st.markdown("## 💻 ENDPOINT SECURITY MANAGEMENT")
    
    # Risk overview
    col1, col2, col3, col4 = st.columns(4)
    
    critical_endpoints = len([e for e in terminal.endpoints if e["risk_score"] > 80])
    high_risk = len([e for e in terminal.endpoints if 60 < e["risk_score"] <= 80])
    medium_risk = len([e for e in terminal.endpoints if 40 < e["risk_score"] <= 60])
    low_risk = len([e for e in terminal.endpoints if e["risk_score"] <= 40])
    
    with col1:
        st.metric("🔴 Critical", critical_endpoints)
    with col2:
        st.metric("🟠 High Risk", high_risk)
    with col3:
        st.metric("🟡 Medium Risk", medium_risk)
    with col4:
        st.metric("🟢 Low Risk", low_risk)
    
    # Endpoint list
    st.markdown("### 📋 ENDPOINT INVENTORY")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox("Type", ["All", "Workstation", "Server"])
    with col2:
        filter_status = st.selectbox("Status", ["All", "Online", "Offline"])
    with col3:
        filter_risk = st.selectbox("Risk", ["All", "Critical", "High", "Medium", "Low"])
    
    # Filter endpoints
    filtered = terminal.endpoints.copy()
    
    if filter_type != "All":
        filtered = [e for e in filtered if e["type"] == filter_type]
    
    if filter_status != "All":
        filtered = [e for e in filtered if e["status"] == filter_status]
    
    if filter_risk != "All":
        risk_ranges = {
            "Critical": (80, 100),
            "High": (60, 80),
            "Medium": (40, 60),
            "Low": (0, 40)
        }
        min_risk, max_risk = risk_ranges[filter_risk]
        filtered = [e for e in filtered if min_risk < e["risk_score"] <= max_risk]
    
    # Display endpoints
    for endpoint in filtered[:20]:
        risk_color = "#ff0040" if endpoint["risk_score"] > 80 else "#ff6b00" if endpoint["risk_score"] > 60 else "#ffeb3b" if endpoint["risk_score"] > 40 else "#00ff41"
        
        with st.expander(f"{'🖥️' if endpoint['type'] == 'Workstation' else '🖧'} {endpoint['id']} - {endpoint['ip']} - Risk: {endpoint['risk_score']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Type:** {endpoint['type']}<br>
                **OS:** {endpoint['os']}<br>
                **IP:** <span class="ip-address">{endpoint['ip']}</span><br>
                **Status:** {endpoint['status']}
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Risk Score:** <span style="color: {risk_color};">{endpoint['risk_score']}</span><br>
                **AV Status:** {endpoint['av_status']}<br>
                **Patches Pending:** {endpoint['patches_pending']}<br>
                **Last Seen:** {endpoint['last_seen'].strftime('%H:%M:%S')}
                """, unsafe_allow_html=True)
            
            # Actions
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🔄 Scan", key=f"scan_{endpoint['id']}"):
                    st.info(f"Scanning {endpoint['id']}...")
            
            with col_b:
                if st.button("🔒 Isolate", key=f"isolate_{endpoint['id']}"):
                    terminal.log_event(f"Endpoint {endpoint['id']} isolated", "Warning")
                    st.warning(f"✓ {endpoint['id']} isolated")
            
            with col_c:
                if st.button("📊 Details", key=f"details_{endpoint['id']}"):
                    st.info("Detailed analysis coming soon...")

def render_threat_intelligence(terminal, user):
    """Threat intelligence module"""
    st.markdown("## 📡 THREAT INTELLIGENCE PLATFORM")
    
    tab1, tab2, tab3 = st.tabs(["🌍 APT Groups", "🦠 Malware Families", "🕳️ Vulnerabilities"])
    
    with tab1:
        st.markdown("### Advanced Persistent Threats")
        
        for apt_name, apt_data in ThreatIntelligence.APT_GROUPS.items():
            with st.expander(f"🎯 {apt_name} - {apt_data['country']}", expanded=False):
                st.markdown(f"""
                <div class="threat-card">
                    <strong>Aliases:</strong> {', '.join(apt_data['aliases'])}<br>
                    <strong>Active Since:</strong> {apt_data['active_since']}<br>
                    <strong>Primary Targets:</strong> {', '.join(apt_data['targets'])}<br>
                    <strong>TTPs:</strong> {', '.join(apt_data['ttps'])}
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Malware Families")
        
        for malware_name, malware_data in ThreatIntelligence.MALWARE_FAMILIES.items():
            with st.expander(f"🦠 {malware_name}", expanded=False):
                st.markdown(f"""
                <div style="background: #1a1f3a; padding: 15px; border-left: 4px solid #ff6b00; border-radius: 5px;">
                    <strong>Type:</strong> {malware_data['type']}<br>
                    <strong>First Seen:</strong> {malware_data['first_seen']}<br>
                    <strong>Capabilities:</strong> {', '.join(malware_data['capabilities'])}<br>
                    <strong>C2 Protocol:</strong> {malware_data['c2_protocol']}<br>
                    <strong>Persistence:</strong> {', '.join(malware_data['persistence'])}
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Critical Vulnerabilities")
        
        for cve in ThreatIntelligence.CRITICAL_CVES:
            severity_color = "#ff0040" if cve["cvss"] >= 9.0 else "#ff6b00"
            
            with st.expander(f"🕳️ {cve['id']} - {cve['name']} (CVSS: {cve['cvss']})", expanded=False):
                st.markdown(f"""
                <div style="background: #1a1f3a; padding: 15px; border-left: 4px solid {severity_color}; border-radius: 5px;">
                    <strong>CVSS Score:</strong> <span style="color: {severity_color};">{cve['cvss']}</span><br>
                    <strong>Description:</strong> {cve['description']}<br>
                    <strong>Affected:</strong> {', '.join(cve['affected'])}<br>
                    <strong>Published:</strong> {cve['published']}
                </div>
                """, unsafe_allow_html=True)

def render_active_incidents(terminal, user):
    """Active incidents module"""
    st.markdown("## 🚨 INCIDENT RESPONSE")
    
    active_threats = [t for t in terminal.active_threats if t["status"] == "Active"]
    
    if not active_threats:
        st.success("✓ No active incidents requiring attention")
        return
    
    st.warning(f"⚠️ {len(active_threats)} ACTIVE INCIDENTS REQUIRE ATTENTION")
    
    for threat in active_threats:
        severity_color = {
            "Critical": "#ff0040",
            "High": "#ff6b00",
            "Medium": "#ffeb3b",
            "Low": "#00ff41"
        }[threat["severity"]]
        
        with st.expander(f"🚨 {threat['id']} - {threat['type']} [{threat['severity']}]", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="threat-card">
                    <h4 style="color: {severity_color}; margin-top: 0;">INCIDENT DETAILS</h4>
                    <strong>Type:</strong> {threat['type']}<br>
                    <strong>Severity:</strong> <span class="badge badge-{threat['severity'].lower()}">{threat['severity']}</span><br>
                    <strong>Confidence:</strong> {threat['confidence']}%<br>
                    <strong>Detected:</strong> {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>Source:</strong> <span class="ip-address">{threat['source_ip']}</span><br>
                    <strong>Target:</strong> <span class="ip-address">{threat['dest_ip']}</span><br>
                    <strong>Affected Assets:</strong> {threat['affected_assets']}<br>
                    <strong>Analyst:</strong> {threat['analyst_assigned']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**MITRE ATT&CK Mapping:**")
                st.markdown(f"""
                <div style="background: #1a1f3a; padding: 10px; border-left: 3px solid #0ff; border-radius: 5px;">
                    <strong>{threat['mitre_technique']['id']}</strong> - {threat['mitre_technique']['name']}<br>
                    <strong>Tactic:</strong> {threat['mitre_technique']['tactic']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Indicators of Compromise:**")
                for ioc in threat['iocs']:
                    st.markdown(f"- **{ioc['type']}:** `{ioc['value']}` (Confidence: {ioc['confidence']}%)")
            
            with col2:
                st.markdown("### 🎯 RESPONSE ACTIONS")
                
                if st.button("🔒 CONTAIN", key=f"contain_{threat['id']}", use_container_width=True):
                    threat['status'] = "Contained"
                    terminal.log_event(f"Threat {threat['id']} contained", "Info")
                    st.success("✓ Threat contained")
                    st.rerun()
                
                if st.button("🚫 BLOCK SOURCE IP", key=f"block_{threat['id']}", use_container_width=True):
                    terminal.log_event(f"IP {threat['source_ip']} blocked", "Warning")
                    st.success(f"✓ {threat['source_ip']} blocked")
                
                if st.button("🔍 DEEP INVESTIGATION", key=f"investigate_{threat['id']}", use_container_width=True):
                    st.info("Investigation initiated...")
                
                if st.button("📋 GENERATE REPORT", key=f"report_{threat['id']}", use_container_width=True):
                    st.info("Generating incident report...")
                
                st.markdown("### 📝 NOTES")
                note = st.text_area("Add note", key=f"note_{threat['id']}", height=100)
                if st.button("💾 Save Note", key=f"save_note_{threat['id']}"):
                    threat['notes'].append({
                        "timestamp": datetime.now(),
                        "analyst": user['name'],
                        "note": note
                    })
                    st.success("Note saved")

def render_live_monitoring(terminal, user):
    """Live monitoring module"""
    st.markdown("## 📡 LIVE NETWORK MONITORING")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌊 NETWORK TRAFFIC STREAM")
        
        st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
        
        recent_network = list(terminal.network_stream)[-20:]
        for event in reversed(recent_network):
            threat_class = "log-critical" if event['threat_score'] > 80 else "log-high" if event['threat_score'] > 60 else "log-medium" if event['threat_score'] > 40 else "log-low"
            action_icon = "🚫" if event['action'] == "Block" else "⚠️" if event['action'] == "Alert" else "✓"
            
            st.markdown(f"""
            <div class="log-line {threat_class}">
                [{event['timestamp'].strftime('%H:%M:%S')}] {action_icon} {event['protocol']} | 
                {event['source_ip']}:{event['source_port']} → {event['dest_ip']}:{event['dest_port']} | 
                {event['bytes']} bytes | Threat: {event['threat_score']}%
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 THREAT DETECTION STREAM")
        
        st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
        
        threat_events = [e for e in terminal.event_stream if e['severity'] in ['Critical', 'High', 'Warning']][-20:]
        for event in reversed(threat_events):
            severity_class = f"log-{event['severity'].lower()}"
            
            st.markdown(f"""
            <div class="log-line {severity_class}">
                [{event['timestamp'].strftime('%H:%M:%S')}] [{event['severity']}] {event['message']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh
    if st.button("🔄 AUTO-REFRESH (5s)", use_container_width=True):
        time.sleep(5)
        terminal.generate_network_event()
        st.rerun()
    
    # Traffic visualization
    st.markdown("### 📊 REAL-TIME TRAFFIC ANALYSIS")
    
    # Generate time series data
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
        line=dict(color='#00ff41', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 65, 0.2)'
    ))
    
    fig.update_layout(
        title="Network Traffic (Last 60 seconds)",
        xaxis_title="Time",
        yaxis_title="Packets/sec",
        paper_bgcolor='#0a0e27',
        plot_bgcolor='#1a1f3a',
        font_color='#00ff41',
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_terminal_console(terminal, user):
    """Interactive terminal console"""
    st.markdown("## 🎮 CYBER TERMINAL CONSOLE")
    
    st.markdown("""
    <div class="status-bar">
        <strong>AEGIS TERMINAL v2.0</strong> | Session: {0} | Operator: {1}
    </div>
    """.format(terminal.session_id, user['name']), unsafe_allow_html=True)
    
    # Terminal output
    st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
    
    # Display output history
    for output in st.session_state.terminal_output:
        st.markdown(f'<div class="log-line">{output}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Command input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        command = st.text_input(
            "Command",
            key="terminal_command",
            placeholder="Enter command (type 'help' for commands)",
            label_visibility="collapsed"
        )
    
    with col2:
        execute = st.button("⚡ EXECUTE", use_container_width=True)
    
    if execute and command:
        # Add command to output
        st.session_state.terminal_output.append(f"<span style='color: #0ff;'>operator@aegis:~$</span> {command}")
        
        # Execute command
        result = terminal.execute_command(command, user['name'])
        
        if result == "clear":
            st.session_state.terminal_output = []
        else:
            # Add result to output
            st.session_state.terminal_output.append(result)
        
        # Keep last 50 commands
        if len(st.session_state.terminal_output) > 50:
            st.session_state.terminal_output = st.session_state.terminal_output[-50:]
        
        st.rerun()
    
    # Command history
    if terminal.command_history:
        with st.expander("📜 Command History"):
            for cmd in reversed(terminal.command_history[-10:]):
                st.markdown(f"`[{cmd['timestamp'].strftime('%H:%M:%S')}]` {cmd['user']}: `{cmd['command']}`")

def render_analytics(terminal, user):
    """Analytics and reporting module"""
    st.markdown("## 📈 CYBER SECURITY ANALYTICS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 THREAT TRENDS")
        
        # Generate trend data
        days = [(datetime.now() - timedelta(days=x)).strftime('%m-%d') for x in range(30, 0, -1)]
        critical_threats = [random.randint(0, 5) for _ in range(30)]
        high_threats = [random.randint(2, 10) for _ in range(30)]
        medium_threats = [random.randint(5, 15) for _ in range(30)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=days, y=critical_threats, name='Critical', mode='lines', line=dict(color='#ff0040', width=2)))
        fig.add_trace(go.Scatter(x=days, y=high_threats, name='High', mode='lines', line=dict(color='#ff6b00', width=2)))
        fig.add_trace(go.Scatter(x=days, y=medium_threats, name='Medium', mode='lines', line=dict(color='#ffeb3b', width=2)))
        
        fig.update_layout(
            title="Threat Detection Trends (30 Days)",
            xaxis_title="Date",
            yaxis_title="Count",
            paper_bgcolor='#0a0e27',
            plot_bgcolor='#1a1f3a',
            font_color='#00ff41',
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 ATTACK VECTORS")
        
        attack_types = {}
        for threat in terminal.active_threats:
            attack_types[threat['type']] = attack_types.get(threat['type'], 0) + 1
        
        if attack_types:
            fig = go.Figure(data=[go.Bar(
                x=list(attack_types.values()),
                y=list(attack_types.keys()),
                orientation='h',
                marker=dict(color='#00ff41')
            )])
            
            fig.update_layout(
                title="Attack Type Distribution",
                xaxis_title="Count",
                yaxis_title="Attack Type",
                paper_bgcolor='#0a0e27',
                plot_bgcolor='#1a1f3a',
                font_color='#00ff41',
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # MITRE ATT&CK heatmap
    st.markdown("### 🗺️ MITRE ATT&CK TECHNIQUE COVERAGE")
    
    techniques_used = defaultdict(int)
    for threat in terminal.active_threats:
        techniques_used[threat['mitre_technique']['name']] += 1
    
    if techniques_used:
        fig = go.Figure(data=go.Bar(
            x=list(techniques_used.keys()),
            y=list(techniques_used.values()),
            marker=dict(
                color=list(techniques_used.values()),
                colorscale=[[0, '#00ff41'], [0.5, '#ffeb3b'], [1, '#ff0040']]
            )
        ))
        
        fig.update_layout(
            title="MITRE ATT&CK Techniques Detected",
            xaxis_title="Technique",
            yaxis_title="Occurrences",
            paper_bgcolor='#0a0e27',
            plot_bgcolor='#1a1f3a',
            font_color='#00ff41',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Export options
    st.markdown("### 📥 EXPORT OPTIONS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 DAILY REPORT", use_container_width=True):
            st.success("✓ Daily report generated")
    
    with col2:
        if st.button("📊 THREAT SUMMARY", use_container_width=True):
            st.success("✓ Threat summary exported")
    
    with col3:
        if st.button("🔍 FORENSIC PACKAGE", use_container_width=True):
            st.success("✓ Forensic data packaged")

def main():
    """Main application entry point"""
    
    # Check authentication
    if not st.session_state.authenticated:
        render_login()
    else:
        render_dashboard()
        
        # Auto-generate events periodically
        if random.random() < 0.1:  # 10% chance per render
            st.session_state.terminal.generate_network_event()

if __name__ == "__main__":
    main()
