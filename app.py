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
import uuid

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CYBER TERMINAL v4.0 - ENTERPRISE SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Cyber Terminal CSS with enhanced enterprise styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
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
    
    /* Enhanced Enterprise Panels */
    .enterprise-panel {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .enterprise-panel:hover {
        border-color: #00ff00;
        box-shadow: 0 12px 40px rgba(0, 255, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .critical-panel {
        background: linear-gradient(135deg, #2a0a0a 0%, #1a0505 100%);
        border: 2px solid #ff4444;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        animation: critical-pulse 2s infinite;
        backdrop-filter: blur(10px);
    }
    
    @keyframes critical-pulse {
        0% { border-color: #ff4444; box-shadow: 0 0 10px rgba(255, 68, 68, 0.3); }
        50% { border-color: #ff0000; box-shadow: 0 0 25px rgba(255, 0, 0, 0.8); }
        100% { border-color: #ff4444; box-shadow: 0 0 10px rgba(255, 68, 68, 0.3); }
    }
    
    .security-panel {
        background: linear-gradient(135deg, #0a2a0a 0%, #051a05 100%);
        border: 1px solid #00aa00;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ff00;
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.3);
    }
    
    .glass-card {
        background: rgba(26, 26, 26, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        margin: 10px 0;
    }
    
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        color: #00ff00;
        border-bottom: 1px solid #333;
        padding: 0.6rem 0;
        transition: all 0.2s ease;
        border-radius: 4px;
        padding-left: 10px;
    }
    
    .log-entry:hover {
        background-color: rgba(0, 255, 0, 0.1);
        transform: translateX(5px);
    }
    
    .progress-enterprise {
        height: 12px;
        border-radius: 6px;
        background: #333;
        overflow: hidden;
        margin: 8px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .progress-enterprise-bar {
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        box-shadow: 0 0 10px currentColor;
    }
    
    .status-online { background-color: #00ff00; animation: pulse-green 2s infinite; }
    .status-warning { background-color: #ffff00; animation: pulse-yellow 2s infinite; }
    .status-offline { background-color: #ff0000; animation: pulse-red 2s infinite; }
    .status-maintenance { background-color: #ff6600; animation: pulse-orange 2s infinite; }
    
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    
    .threat-level-critical { background: linear-gradient(135deg, #ff0000, #cc0000); }
    .threat-level-high { background: linear-gradient(135deg, #ff6600, #cc5500); }
    .threat-level-medium { background: linear-gradient(135deg, #ffff00, #cccc00); }
    .threat-level-low { background: linear-gradient(135deg, #00ff00, #00cc00); }
    
    .data-table {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.8em;
        overflow: hidden;
    }
    
    .data-table th {
        background: #1a1a1a;
        color: #00ff00;
        padding: 12px 15px;
        border-bottom: 1px solid #333;
        font-weight: 600;
    }
    
    .data-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #222;
        color: #cccccc;
    }
    
    .data-table tr:hover {
        background-color: rgba(0, 255, 0, 0.1);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #00ff00;
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        color: #00ff00;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ff00, #00cc00);
        color: #000000;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        transform: translateY(-2px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff00;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00cc00;
    }
</style>
""", unsafe_allow_html=True)

class EnterpriseSOCPlatform:
    def __init__(self):
        self.platform_version = "4.0"
        self.deployment_id = str(uuid.uuid4())[:8]
        self.last_update = datetime.now()
        self.system_start_time = datetime.now()
        self.alert_history = []
        self.incident_counter = 0
        self.threat_intelligence_feeds = {}
        self.compliance_frameworks = {}
        self.risk_assessments = {}
        self.asset_inventory = {}
        self.vulnerability_database = {}
        
        # Enhanced system health with performance metrics for all components
        self.system_health = {
            "soc_platform": {"status": "online", "uptime": 0, "performance": 98, "latency": 5},
            "siem_system": {"status": "online", "events_processed": 1250000, "latency": 45, "performance": 95},
            "edr_platform": {"status": "online", "endpoints_monitored": 2500, "threats_blocked": 147, "performance": 92},
            "firewall_cluster": {"status": "online", "throughput_gbps": 12.5, "rules_active": 1247, "performance": 96},
            "ids_ips": {"status": "online", "alerts_generated": 324, "attacks_blocked": 89, "performance": 94},
            "threat_intel": {"status": "online", "feeds_active": 8, "iocs_loaded": 15420, "performance": 90},
            "vulnerability_scanner": {"status": "online", "assets_scanned": 850, "vulnerabilities_found": 127, "performance": 88}
        }
        
        self.initialize_enterprise_platform()
        
    def initialize_enterprise_platform(self):
        """Initialize enterprise-grade SOC platform"""
        # Enhanced threat intelligence with real-world data
        self.threat_intel_db = {
            "advanced_persistent_threats": [
                {
                    "name": "APT29", "country": "Russia", "alias": ["Cozy Bear", "The Dukes"],
                    "targets": ["Government", "Healthcare", "Research"], 
                    "tactics": ["Spear Phishing", "Custom Malware", "Supply Chain"],
                    "tools": ["WELLMESS", "WELLMAIL", "Cobalt Strike"],
                    "mitre_techniques": ["T1566.001", "T1059.003", "T1588.002"],
                    "attribution_confidence": "High",
                    "last_observed": "2024-01-15",
                    "risk_level": "Critical"
                },
                {
                    "name": "APT1", "country": "China", "alias": ["Comment Crew"],
                    "targets": ["Defense", "Technology", "Aerospace"], 
                    "tactics": ["Watering Hole", "Zero-Day", "Credential Theft"],
                    "tools": ["GH0ST RAT", "Poison Ivy", "SHOTPUT"],
                    "mitre_techniques": ["T1189", "T1133", "T1110"],
                    "attribution_confidence": "Very High",
                    "last_observed": "2024-01-20",
                    "risk_level": "Critical"
                }
            ],
            "malware_families": [
                {
                    "name": "Emotet", "type": "Banking Trojan", "first_seen": "2014",
                    "primary_function": "Credential Theft", "propagation": "Email, Network",
                    "detection_rate": 92, "prevalence": "High",
                    "associated_threats": ["TrickBot", "Ryuk"],
                    "ioc_count": 847,
                    "risk_level": "High"
                },
                {
                    "name": "TrickBot", "type": "Modular Trojan", "first_seen": "2016",
                    "primary_function": "Information Stealer", "propagation": "Email, Exploit Kits",
                    "detection_rate": 88, "prevalence": "High",
                    "associated_threats": ["Ryuk", "Conti"],
                    "ioc_count": 923,
                    "risk_level": "High"
                }
            ],
            "vulnerabilities": [
                {
                    "cve": "CVE-2021-44228", "name": "Log4Shell", "severity": "Critical",
                    "cvss_score": 10.0, "epss_score": 0.97,
                    "affected_software": ["Apache Log4j 2.0-beta9 - 2.14.1"],
                    "exploitation_status": "Active", "patch_status": "Available",
                    "known_exploited": True, "ransomware_used": True,
                    "risk_level": "Critical"
                },
                {
                    "cve": "CVE-2021-34527", "name": "PrintNightmare", "severity": "Critical",
                    "cvss_score": 9.3, "epss_score": 0.89,
                    "affected_software": ["Windows Print Spooler"],
                    "exploitation_status": "Active", "patch_status": "Available",
                    "known_exploited": True, "ransomware_used": True,
                    "risk_level": "Critical"
                }
            ]
        }
        
        # Enhanced SOC team with enterprise roles
        self.cyber_team = {
            "soc_manager": {
                "user_id": "soc_manager",
                "password": self.hash_password("Enterprise2024!"),
                "first_name": "Sarah",
                "last_name": "Chen",
                "role": "SOC Manager",
                "clearance": "TOP SECRET",
                "department": "Security Operations",
                "shift": "Day",
                "specializations": ["Incident Management", "Team Leadership", "Strategy"],
                "certifications": ["CISSP", "CISM", "GCIH"],
                "avatar": "👩‍💼"
            },
            "threat_analyst": {
                "user_id": "threat_analyst",
                "password": self.hash_password("ThreatHunter2024!"),
                "first_name": "Marcus",
                "last_name": "Rodriguez",
                "role": "Threat Analyst",
                "clearance": "SECRET",
                "department": "Threat Intelligence",
                "shift": "Day",
                "specializations": ["Malware Analysis", "Threat Hunting", "Digital Forensics"],
                "certifications": ["GCFA", "GNFA", "GREMM"],
                "avatar": "👨‍🔬"
            },
            "incident_responder": {
                "user_id": "incident_responder",
                "password": self.hash_password("Incident2024!"),
                "first_name": "Jessica",
                "last_name": "Kim",
                "role": "Incident Responder",
                "clearance": "SECRET",
                "department": "Incident Response",
                "shift": "24/7 Rotation",
                "specializations": ["Incident Response", "Forensics", "Containment"],
                "certifications": ["GCIH", "GCFA", "GNFA"],
                "avatar": "👩‍🚒"
            },
            "vulnerability_analyst": {
                "user_id": "vuln_analyst",
                "password": self.hash_password("Vulnerability2024!"),
                "first_name": "David",
                "last_name": "Thompson",
                "role": "Vulnerability Analyst",
                "clearance": "SECRET",
                "department": "Vulnerability Management",
                "shift": "Day",
                "specializations": ["Vulnerability Assessment", "Patch Management", "Risk Analysis"],
                "certifications": ["GCPN", "GSEC", "CEH"],
                "avatar": "👨‍💻"
            }
        }
        
        # Initialize enterprise data structures
        self.security_incidents = []
        self.live_threats = []
        self.network_activity = []
        self.endpoint_telemetry = []
        self.ids_alerts = []
        self.honeypot_data = []
        self.defense_actions = []
        self.iot_devices = []
        self.cloud_assets = []
        self.compliance_data = {}
        self.risk_assessments = {}
        
        # Generate initial enterprise data
        self.generate_enterprise_data()
        
        # Start real-time data simulation
        self.start_real_time_simulation()
    
    def hash_password(self, password: str) -> str:
        """Enterprise-grade password hashing"""
        salt = "EnterpriseSOC2024SecureSalt"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against enterprise hash"""
        return self.hash_password(password) == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Enterprise authentication with logging"""
        if username in self.cyber_team:
            user = self.cyber_team[username]
            if self.verify_password(password, user["password"]):
                # Log successful authentication
                self.log_security_event(
                    event_type="AUTH_SUCCESS",
                    severity="INFO",
                    message=f"Successful authentication for user: {username}",
                    user=username
                )
                return True
            else:
                # Log failed authentication
                self.log_security_event(
                    event_type="AUTH_FAILED",
                    severity="HIGH",
                    message=f"Failed authentication attempt for user: {username}",
                    user=username
                )
        return False
    
    def log_security_event(self, event_type: str, severity: str, message: str, user: str = "SYSTEM"):
        """Enterprise security event logging"""
        event = {
            "event_id": f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000,9999)}",
            "timestamp": datetime.now(),
            "type": event_type,
            "severity": severity,
            "message": message,
            "user": user,
            "source_ip": "127.0.0.1" if user == "SYSTEM" else "10.1.1.100"
        }
        self.alert_history.append(event)
    
    def generate_enterprise_data(self):
        """Generate enterprise-scale realistic data"""
        self.generate_live_threats()
        self.generate_network_activity()
        self.generate_endpoint_telemetry()
        self.generate_ids_alerts()
        self.generate_honeypot_data()
        self.generate_iot_devices()
        self.generate_cloud_assets()
        self.generate_compliance_data()
        self.generate_risk_assessments()
    
    def generate_live_threats(self):
        """Generate realistic enterprise threats"""
        threat_scenarios = [
            {
                "type": "APT Campaign", 
                "description": "Suspected nation-state actor conducting reconnaissance",
                "ttps": ["T1595.001", "T1589.001", "T1592.002"]
            },
            {
                "type": "Ransomware Activity", 
                "description": "Ransomware group scanning for vulnerable services",
                "ttps": ["T1560.001", "T1486", "T1490"]
            },
            {
                "type": "Insider Threat", 
                "description": "Unusual data access patterns detected",
                "ttps": ["T1074.001", "T1020", "T1030"]
            },
            {
                "type": "Supply Chain Attack", 
                "description": "Compromised third-party software update",
                "ttps": ["T1195.002", "T1105", "T1059.003"]
            }
        ]
        
        for i in range(20):
            scenario = random.choice(threat_scenarios)
            threat = {
                "threat_id": f"THREAT-{datetime.now().strftime('%Y%m%d')}-{i+1:04d}",
                "type": scenario["type"],
                "description": scenario["description"],
                "severity": random.choice(["High", "Critical"]),
                "confidence": random.randint(75, 95),
                "first_detected": datetime.now() - timedelta(hours=random.randint(1, 168)),
                "last_activity": datetime.now() - timedelta(minutes=random.randint(1, 120)),
                "source_country": random.choice(["Russia", "China", "North Korea", "Iran", "Unknown"]),
                "target_sector": "Enterprise",
                "mitre_techniques": scenario["ttps"],
                "indicators": [f"IOC-{j}" for j in range(random.randint(3, 8))],
                "status": random.choice(["Active", "Contained", "Investigating"]),
                "assigned_to": random.choice(list(self.cyber_team.keys())),
                "impact_score": random.randint(6, 10),
                "business_impact": random.choice(["Data Theft", "Service Disruption", "Financial Loss", "Reputation Damage"])
            }
            self.live_threats.append(threat)
    
    def generate_network_activity(self):
        """Generate enterprise-scale network traffic"""
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "RDP", "SMB", "FTP", "ICMP"]
        services = ["Web Server", "Database", "File Share", "DNS Server", "Mail Server", "VPN", "API Gateway"]
        
        self.network_activity = []
        
        for i in range(2000):  # Enterprise-scale data
            # Simulate realistic traffic patterns (more during business hours)
            hour = datetime.now().hour
            if 9 <= hour <= 17:  # Business hours
                traffic_multiplier = random.uniform(1.5, 3.0)
            else:
                traffic_multiplier = random.uniform(0.3, 0.8)
            
            activity = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 600)),
                "session_id": f"SESS-{random.randint(100000,999999)}",
                "source_ip": f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "dest_ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                "source_port": random.randint(1024, 65535),
                "dest_port": random.choice([80, 443, 22, 53, 25, 3389, 445, 21]),
                "protocol": random.choice(protocols),
                "service": random.choice(services),
                "bytes_sent": int(random.randint(100, 1000000) * traffic_multiplier),
                "bytes_received": int(random.randint(100, 500000) * traffic_multiplier),
                "duration_seconds": random.randint(1, 300),
                "threat_score": random.randint(0, 100),
                "geo_location": random.choice(["Internal", "USA", "Germany", "Japan", "Brazil", "India"]),
                "user_agent": random.choice(["Browser", "API Client", "Mobile App", "Script"]),
                "encrypted": random.random() < 0.8,
                "flagged": random.random() < 0.1
            }
            self.network_activity.append(activity)
    
    def generate_endpoint_telemetry(self):
        """Generate enterprise endpoint security data"""
        departments = ["HR", "Finance", "IT", "Sales", "Marketing", "Engineering", "Executive"]
        os_versions = ["Windows 10 Enterprise", "Windows 11 Enterprise", "macOS 13.4", "Ubuntu 22.04 LTS", "RHEL 8.6"]
        
        self.endpoint_telemetry = []
        
        for i in range(500):  # Enterprise endpoint count
            endpoint = {
                "endpoint_id": f"EP-{i+1:05d}",
                "hostname": f"WS-{random.choice(['NYC', 'LON', 'TOK', 'SF'])}-{i+1:04d}",
                "ip_address": f"10.1.{random.randint(1,50)}.{random.randint(1,254)}",
                "mac_address": f"02:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}",
                "os_version": random.choice(os_versions),
                "department": random.choice(departments),
                "last_seen": datetime.now() - timedelta(minutes=random.randint(1, 60)),
                "antivirus_status": random.choice(["Enabled", "Enabled", "Enabled", "Outdated"]),
                "threats_detected": random.randint(0, 2),
                "suspicious_processes": random.sample(["powershell.exe", "cmd.exe", "wmic.exe", "regsvr32.exe"], random.randint(0, 1)),
                "network_connections": random.randint(5, 50),
                "risk_score": random.randint(0, 100),
                "patch_level": random.choice(["Current", "1-2 weeks behind", "Critical updates missing"]),
                "encryption_status": random.choice(["Enabled", "Enabled", "Partial"]),
                "last_scan": datetime.now() - timedelta(days=random.randint(0, 7)),
                "user_activity": random.choice(["Active", "Idle", "Offline"]),
                "compliance_status": random.choice(["Compliant", "At Risk", "Non-Compliant"]),
                "criticality": random.choice(["Low", "Medium", "High", "Critical"])
            }
            self.endpoint_telemetry.append(endpoint)
    
    def generate_ids_alerts(self):
        """Generate enterprise IDS/IPS alerts"""
        attack_types = [
            "Port Scan", "Brute Force", "SQL Injection", "XSS", "DDoS", 
            "Malware Download", "Data Theft", "Zero-Day Exploit", "Credential Stuffing",
            "Lateral Movement", "Privilege Escalation", "Command Injection"
        ]
        
        self.ids_alerts = []
        
        for i in range(300):
            alert = {
                "alert_id": f"IDS-{datetime.now().strftime('%Y%m%d')}-{i+1:05d}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 480)),
                "attack_type": random.choice(attack_types),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "signature": f"SIG-{random.randint(10000, 99999)}",
                "action_taken": random.choice(["Allowed", "Blocked", "Alerted", "Quarantined"]),
                "confidence": random.randint(70, 99),
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
                "payload_info": f"Malicious payload detected: {random.choice(['Exploit kit', 'Ransomware', 'Trojan', 'Backdoor'])}",
                "mitre_technique": random.choice(["T1055", "T1068", "T1071", "T1082", "T1105"]),
                "sensor_location": random.choice(["DMZ", "Internal", "Cloud", "Branch"]),
                "false_positive": random.random() < 0.15
            }
            self.ids_alerts.append(alert)
    
    def generate_honeypot_data(self):
        """Generate enterprise honeypot interaction data"""
        self.honeypot_data = []
        
        for i in range(50):
            interaction = {
                "honeypot_id": f"HONEY-{i+1:03d}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 72)),
                "attacker_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "attacker_country": random.choice(["China", "Russia", "USA", "Brazil", "Vietnam", "Iran"]),
                "attack_type": random.choice(["SSH Brute Force", "Web Exploit", "Database Attack", "Service Scan"]),
                "credentials_tried": random.randint(1, 100),
                "malware_dropped": random.random() < 0.4,
                "data_captured": random.randint(0, 10000),
                "threat_level": random.choice(["Low", "Medium", "High", "Critical"]),
                "campaign_id": f"CAMP-{random.randint(10000, 99999)}" if random.random() < 0.3 else None,
                "asn_organization": random.choice(["China Telecom", "OVH SAS", "Amazon.com", "Digital Ocean", "Unknown"])
            }
            self.honeypot_data.append(interaction)
    
    def generate_iot_devices(self):
        """Generate enterprise IoT device inventory"""
        iot_types = ["Smart Camera", "Thermostat", "Smart Lock", "Industrial Sensor", "Medical Device", "Vehicle System", "Printer", "VoIP Phone"]
        
        self.iot_devices = []
        
        for i in range(100):
            device = {
                "device_id": f"IOT-{i+1:04d}",
                "type": random.choice(iot_types),
                "ip_address": f"10.2.{random.randint(1,50)}.{random.randint(1,254)}",
                "mac_address": f"02:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}",
                "firmware_version": f"v{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "last_seen": datetime.now() - timedelta(hours=random.randint(1, 24)),
                "security_status": random.choice(["Secure", "Vulnerable", "Compromised", "Unknown"]),
                "vulnerabilities": random.randint(0, 5),
                "network_traffic": random.randint(10, 1000),
                "risk_score": random.randint(0, 100),
                "department": random.choice(["Facilities", "IT", "Operations", "Medical"]),
                "criticality": random.choice(["Low", "Medium", "High"])
            }
            self.iot_devices.append(device)
    
    def generate_cloud_assets(self):
        """Generate enterprise cloud asset inventory"""
        cloud_services = ["EC2", "S3", "RDS", "Lambda", "Azure VM", "Cloud Storage", "Kubernetes", "Container Registry", "Load Balancer", "Database"]
        
        self.cloud_assets = []
        
        for i in range(150):
            asset = {
                "asset_id": f"CLOUD-{i+1:05d}",
                "service": random.choice(cloud_services),
                "provider": random.choice(["AWS", "Azure", "GCP"]),
                "region": random.choice(["us-east-1", "eu-west-1", "ap-southeast-1", "us-west-2"]),
                "security_status": random.choice(["Secure", "Misconfigured", "Public Exposure", "Encrypted"]),
                "compliance": random.choice(["Compliant", "Non-Compliant", "At Risk"]),
                "last_audit": datetime.now() - timedelta(days=random.randint(1, 90)),
                "threats_detected": random.randint(0, 3),
                "encryption_status": random.choice(["Enabled", "Disabled", "Partial"]),
                "cost_monthly": round(random.uniform(50, 5000), 2),
                "owner": random.choice(["IT", "Development", "Marketing", "Finance"]),
                "criticality": random.choice(["Low", "Medium", "High", "Critical"])
            }
            self.cloud_assets.append(asset)
    
    def generate_compliance_data(self):
        """Generate enterprise compliance framework data"""
        frameworks = {
            "NIST CSF": {
                "status": "Compliant",
                "last_assessment": datetime.now() - timedelta(days=30),
                "score": 92,
                "controls_implemented": 145,
                "controls_total": 150
            },
            "ISO 27001": {
                "status": "Compliant", 
                "last_assessment": datetime.now() - timedelta(days=60),
                "score": 88,
                "controls_implemented": 112,
                "controls_total": 114
            },
            "PCI DSS": {
                "status": "Partially Compliant",
                "last_assessment": datetime.now() - timedelta(days=45),
                "score": 78,
                "controls_implemented": 10,
                "controls_total": 12
            },
            "HIPAA": {
                "status": "Compliant",
                "last_assessment": datetime.now() - timedelta(days=90),
                "score": 95,
                "controls_implemented": 45,
                "controls_total": 45
            }
        }
        self.compliance_data = frameworks
    
    def generate_risk_assessments(self):
        """Generate enterprise risk assessment data"""
        risks = {
            "Data Breach": {
                "likelihood": "High",
                "impact": "Critical",
                "risk_score": 85,
                "mitigation_status": "In Progress",
                "last_assessment": datetime.now() - timedelta(days=15)
            },
            "Ransomware Attack": {
                "likelihood": "Medium",
                "impact": "Critical", 
                "risk_score": 75,
                "mitigation_status": "Partially Mitigated",
                "last_assessment": datetime.now() - timedelta(days=30)
            },
            "Insider Threat": {
                "likelihood": "Low",
                "impact": "High",
                "risk_score": 45,
                "mitigation_status": "Monitored",
                "last_assessment": datetime.now() - timedelta(days=60)
            },
            "Supply Chain Compromise": {
                "likelihood": "Medium",
                "impact": "High",
                "risk_score": 65,
                "mitigation_status": "Planned",
                "last_assessment": datetime.now() - timedelta(days=45)
            }
        }
        self.risk_assessments = risks
    
    def start_real_time_simulation(self):
        """Start real-time data simulation"""
        self.last_update = datetime.now()
    
    def calculate_enterprise_risk_score(self):
        """Calculate enterprise risk score based on multiple factors"""
        try:
            # Base risk factors with safe dictionary access
            critical_threats = len([t for t in self.live_threats if t.get("severity") == "Critical"])
            high_threats = len([t for t in self.live_threats if t.get("severity") == "High"])
            active_incidents = len([t for t in self.live_threats if t.get("status") == "Active"])
            
            # System health factors with safe access
            system_health_score = sum([health.get("performance", 0) for health in self.system_health.values()]) / len(self.system_health)
            
            # Compliance factors with safe access
            compliance_score = sum([framework.get("score", 0) for framework in self.compliance_data.values()]) / len(self.compliance_data)
            
            # Calculate composite score
            base_score = 100
            score = base_score
            score -= (critical_threats * 8) + (high_threats * 4) + (active_incidents * 3)
            score -= (100 - system_health_score) * 0.1
            score -= (100 - compliance_score) * 0.1
            
            score = max(0, min(100, score))
            
            if score >= 85:
                return "LOW", "#00ff00", score
            elif score >= 70:
                return "MEDIUM", "#ffff00", score
            elif score >= 50:
                return "HIGH", "#ff6600", score
            else:
                return "CRITICAL", "#ff0000", score
        except Exception as e:
            # Fallback in case of calculation error
            return "MEDIUM", "#ffff00", 75
    
    def get_system_uptime(self):
        """Calculate system uptime"""
        uptime = datetime.now() - self.system_start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"

def enterprise_login():
    """Display enhanced enterprise SOC login"""
    st.markdown('<div class="main-header">🛡️ ENTERPRISE SOC PLATFORM v4.0</div>', unsafe_allow_html=True)
    st.markdown("### ENTERPRISE SECURITY OPERATIONS CENTER", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Enhanced System status dashboard
        st.markdown("""
        <div class="enterprise-panel">
            <h4 style='color: #00ff00; margin-bottom: 20px; text-align: center;'>🏢 ENTERPRISE SYSTEM STATUS</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0; font-size: 2em;'>98.7%</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Platform Uptime</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0; font-size: 2em;'>1,247</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Active Rules</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #ffff00; margin: 0; font-size: 2em;'>45</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Active Threats</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0; font-size: 2em;'>92%</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Compliance Score</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Security posture
        st.markdown("""
        <div class="security-panel">
            <h5 style='color: #00ff00; text-align: center;'>🔒 SECURITY POSTURE</h5>
            <div style='margin: 15px 0;'>
                <div style='display: flex; justify-content: space-between; margin: 12px 0;'>
                    <span>Endpoint Protection</span>
                    <span>98%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 98%; background: #00ff00;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 12px 0;'>
                    <span>Network Security</span>
                    <span>95%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 95%; background: #00ff00;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 12px 0;'>
                    <span>Cloud Security</span>
                    <span>88%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 88%; background: #ffff00;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 12px 0;'>
                    <span>Threat Detection</span>
                    <span>94%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 94%; background: #00ff00;'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("enterprise_login"):
            st.markdown("### 🔐 ENTERPRISE ACCESS", unsafe_allow_html=True)
            st.markdown("**Secure Authentication Required**", unsafe_allow_html=True)
            
            username = st.text_input("👤 ENTERPRISE USER ID", placeholder="Enter your enterprise user ID...")
            password = st.text_input("🔒 ACCESS CREDENTIALS", type="password", placeholder="Enter your secure credentials...")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🚀 INITIATE SOC PLATFORM", use_container_width=True)
            with col_b:
                if st.form_submit_button("🆘 EMERGENCY ACCESS", use_container_width=True):
                    st.warning("Emergency access protocol initiated. Security team notified.")
            
            if login_button:
                if username and password:
                    platform = st.session_state.soc_platform
                    if platform.authenticate_user(username, password):
                        st.session_state.user = platform.cyber_team[username]
                        st.session_state.logged_in = True
                        
                        # Enhanced login sequence with progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            if i < 25:
                                status_text.text("🔐 Authenticating with enterprise security services...")
                            elif i < 50:
                                status_text.text("🏢 Loading SOC dashboard and threat intelligence...")
                            elif i < 75:
                                status_text.text("📊 Initializing real-time monitoring systems...")
                            else:
                                status_text.text("🎯 Establishing secure connection to enterprise network...")
                            time.sleep(0.02)
                        
                        st.success("🎉 ENTERPRISE SOC PLATFORM ACCESS GRANTED")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("""
                        ❌ ACCESS DENIED - SECURITY ALERT
                        
                        Invalid credentials detected. 
                        This attempt has been logged and security team notified.
                        """)
                else:
                    st.warning("⚠️ ENTERPRISE CREDENTIALS REQUIRED FOR ACCESS")
    
    st.markdown("---")
    
    # Enhanced Enterprise team access
    st.markdown("### 🏢 AUTHORIZED ENTERPRISE PERSONNEL", unsafe_allow_html=True)
    
    cols = st.columns(4)
    roles = [
        {"role": "SOC MANAGER", "id": "soc_manager", "code": "Enterprise2024!", "clearance": "TOP SECRET", "avatar": "👩‍💼", "color": "#00ff00"},
        {"role": "THREAT ANALYST", "id": "threat_analyst", "code": "ThreatHunter2024!", "clearance": "SECRET", "avatar": "👨‍🔬", "color": "#ffff00"},
        {"role": "INCIDENT RESPONDER", "id": "incident_responder", "code": "Incident2024!", "clearance": "SECRET", "avatar": "👩‍🚒", "color": "#ff6600"},
        {"role": "VULNERABILITY ANALYST", "id": "vuln_analyst", "code": "Vulnerability2024!", "clearance": "SECRET", "avatar": "👨‍💻", "color": "#00ffff"}
    ]
    
    for idx, role in enumerate(roles):
        with cols[idx]:
            st.markdown(f"""
            <div class='enterprise-panel' style='text-align: center; border-left: 4px solid {role["color"]};'>
                <div style='font-size: 2.5em;'>{role['avatar']}</div>
                <h4 style='color: {role["color"]};'>{role['role']}</h4>
                <p><strong>ID:</strong> <code style='background: #1a1a1a; padding: 2px 6px; border-radius: 4px;'>{role['id']}</code></p>
                <p><strong>CLEARANCE:</strong> {role['clearance']}</p>
            </div>
            """, unsafe_allow_html=True)

# [Rest of the functions remain the same with enhanced UI elements...]

def main():
    # Initialize enterprise SOC platform in session state
    if 'soc_platform' not in st.session_state:
        st.session_state.soc_platform = EnterpriseSOCPlatform()
    
    # Initialize login state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        enterprise_login()
    else:
        enterprise_dashboard()

if __name__ == "__main__":
    main()
