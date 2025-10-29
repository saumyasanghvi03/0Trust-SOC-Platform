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

# Advanced Cyber Terminal CSS with enterprise styling
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
    
    /* Enterprise-grade panels */
    .enterprise-panel {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .enterprise-panel:hover {
        border-color: #00ff00;
        box-shadow: 0 6px 25px rgba(0, 255, 0, 0.2);
    }
    
    .critical-panel {
        background: linear-gradient(135deg, #2a0a0a 0%, #1a0505 100%);
        border: 2px solid #ff4444;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        animation: critical-pulse 1.5s infinite;
    }
    
    @keyframes critical-pulse {
        0% { border-color: #ff4444; box-shadow: 0 0 10px rgba(255, 68, 68, 0.3); }
        50% { border-color: #ff0000; box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); }
        100% { border-color: #ff4444; box-shadow: 0 0 10px rgba(255, 68, 68, 0.3); }
    }
    
    .security-panel {
        background: linear-gradient(135deg, #0a2a0a 0%, #051a05 100%);
        border: 1px solid #00aa00;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #00ff00;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
    }
    
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        color: #00ff00;
        border-bottom: 1px solid #333;
        padding: 0.4rem 0;
        transition: all 0.2s ease;
    }
    
    .log-entry:hover {
        background-color: #1a1a1a;
    }
    
    .progress-enterprise {
        height: 8px;
        border-radius: 4px;
        background: #333;
        overflow: hidden;
        margin: 5px 0;
    }
    
    .progress-enterprise-bar {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #00ff00; }
    .status-warning { background-color: #ffff00; }
    .status-offline { background-color: #ff0000; }
    .status-maintenance { background-color: #ff6600; }
    
    .threat-level-critical { background: linear-gradient(135deg, #ff0000, #cc0000); }
    .threat-level-high { background: linear-gradient(135deg, #ff6600, #cc5500); }
    .threat-level-medium { background: linear-gradient(135deg, #ffff00, #cccc00); }
    .threat-level-low { background: linear-gradient(135deg, #00ff00, #00cc00); }
    
    .data-table {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.8em;
    }
    
    .data-table th {
        background: #1a1a1a;
        color: #00ff00;
        padding: 8px 12px;
        border-bottom: 1px solid #333;
    }
    
    .data-table td {
        padding: 6px 12px;
        border-bottom: 1px solid #222;
        color: #cccccc;
    }
    
    .data-table tr:hover {
        background-color: #1a1a1a;
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
        
        # Enterprise system health
        self.system_health = {
            "soc_platform": {"status": "online", "uptime": 0, "performance": 98},
            "siem_system": {"status": "online", "events_processed": 0, "latency": 45},
            "edr_platform": {"status": "online", "endpoints_monitored": 0, "threats_blocked": 0},
            "firewall_cluster": {"status": "online", "throughput_gbps": 12.5, "rules_active": 1247},
            "ids_ips": {"status": "online", "alerts_generated": 0, "attacks_blocked": 0},
            "threat_intel": {"status": "online", "feeds_active": 8, "iocs_loaded": 15420},
            "vulnerability_scanner": {"status": "online", "assets_scanned": 0, "vulnerabilities_found": 0}
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
                    "last_observed": "2024-01-15"
                },
                {
                    "name": "APT1", "country": "China", "alias": ["Comment Crew"],
                    "targets": ["Defense", "Technology", "Aerospace"], 
                    "tactics": ["Watering Hole", "Zero-Day", "Credential Theft"],
                    "tools": ["GH0ST RAT", "Poison Ivy", "SHOTPUT"],
                    "mitre_techniques": ["T1189", "T1133", "T1110"],
                    "attribution_confidence": "Very High",
                    "last_observed": "2024-01-20"
                }
            ],
            "malware_families": [
                {
                    "name": "Emotet", "type": "Banking Trojan", "first_seen": "2014",
                    "primary_function": "Credential Theft", "propagation": "Email, Network",
                    "detection_rate": 92, "prevalence": "High",
                    "associated_threats": ["TrickBot", "Ryuk"],
                    "ioc_count": 847
                },
                {
                    "name": "TrickBot", "type": "Modular Trojan", "first_seen": "2016",
                    "primary_function": "Information Stealer", "propagation": "Email, Exploit Kits",
                    "detection_rate": 88, "prevalence": "High",
                    "associated_threats": ["Ryuk", "Conti"],
                    "ioc_count": 923
                }
            ],
            "vulnerabilities": [
                {
                    "cve": "CVE-2021-44228", "name": "Log4Shell", "severity": "Critical",
                    "cvss_score": 10.0, "epss_score": 0.97,
                    "affected_software": ["Apache Log4j 2.0-beta9 - 2.14.1"],
                    "exploitation_status": "Active", "patch_status": "Available",
                    "known_exploited": True, "ransomware_used": True
                },
                {
                    "cve": "CVE-2021-34527", "name": "PrintNightmare", "severity": "Critical",
                    "cvss_score": 9.3, "epss_score": 0.89,
                    "affected_software": ["Windows Print Spooler"],
                    "exploitation_status": "Active", "patch_status": "Available",
                    "known_exploited": True, "ransomware_used": True
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
        # Base risk factors
        critical_threats = len([t for t in self.live_threats if t.get("severity") == "Critical"])
        high_threats = len([t for t in self.live_threats if t.get("severity") == "High"])
        active_incidents = len([t for t in self.live_threats if t.get("status") == "Active"])
        
        # System health factors
        system_health_score = sum([health["performance"] for health in self.system_health.values()]) / len(self.system_health)
        
        # Compliance factors
        compliance_score = sum([framework["score"] for framework in self.compliance_data.values()]) / len(self.compliance_data)
        
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
    
    def get_system_uptime(self):
        """Calculate system uptime"""
        uptime = datetime.now() - self.system_start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"

def enterprise_login():
    """Display enterprise SOC login"""
    st.markdown('<div class="main-header">🛡️ ENTERPRISE SOC PLATFORM v4.0</div>', unsafe_allow_html=True)
    st.markdown("### ENTERPRISE SECURITY OPERATIONS CENTER", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # System status dashboard
        st.markdown("""
        <div class="enterprise-panel">
            <h4 style='color: #00ff00; margin-bottom: 20px;'>🏢 ENTERPRISE SYSTEM STATUS</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0;'>98.7%</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Platform Uptime</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0;'>1,247</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Active Rules</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #ffff00; margin: 0;'>45</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Active Threats</p>
                </div>
                <div class='metric-card'>
                    <h3 style='color: #00ff00; margin: 0;'>92%</h3>
                    <p style='margin: 0; font-size: 0.9em;'>Compliance Score</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Security posture
        st.markdown("""
        <div class="security-panel">
            <h5 style='color: #00ff00;'>🔒 SECURITY POSTURE</h5>
            <div style='margin: 15px 0;'>
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>Endpoint Protection</span>
                    <span>98%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 98%; background: #00ff00;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>Network Security</span>
                    <span>95%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 95%; background: #00ff00;'></div>
                </div>
                
                <div style='display: flex; justify-content: space-between; margin: 8px 0;'>
                    <span>Cloud Security</span>
                    <span>88%</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: 88%; background: #ffff00;'></div>
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
                        
                        # Enterprise login sequence
                        with st.spinner("🔐 Authenticating with enterprise security services..."):
                            time.sleep(1)
                        
                        with st.spinner("🏢 Loading SOC dashboard and threat intelligence..."):
                            time.sleep(1)
                        
                        with st.spinner("📊 Initializing real-time monitoring systems..."):
                            time.sleep(1)
                        
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
    
    # Enterprise team access
    st.markdown("### 🏢 AUTHORIZED ENTERPRISE PERSONNEL", unsafe_allow_html=True)
    
    cols = st.columns(4)
    roles = [
        {"role": "SOC MANAGER", "id": "soc_manager", "code": "Enterprise2024!", "clearance": "TOP SECRET", "avatar": "👩‍💼"},
        {"role": "THREAT ANALYST", "id": "threat_analyst", "code": "ThreatHunter2024!", "clearance": "SECRET", "avatar": "👨‍🔬"},
        {"role": "INCIDENT RESPONDER", "id": "incident_responder", "code": "Incident2024!", "clearance": "SECRET", "avatar": "👩‍🚒"},
        {"role": "VULNERABILITY ANALYST", "id": "vuln_analyst", "code": "Vulnerability2024!", "clearance": "SECRET", "avatar": "👨‍💻"}
    ]
    
    for idx, role in enumerate(roles):
        with cols[idx]:
            st.markdown(f"""
            <div class='enterprise-panel' style='text-align: center;'>
                <div style='font-size: 2em;'>{role['avatar']}</div>
                <h4 style='color: #00ff00;'>{role['role']}</h4>
                <p><strong>ID:</strong> <code>{role['id']}</code></p>
                <p><strong>CLEARANCE:</strong> {role['clearance']}</p>
            </div>
            """, unsafe_allow_html=True)

def enterprise_dashboard():
    """Display enterprise SOC dashboard"""
    platform = st.session_state.soc_platform
    user = st.session_state.user
    
    # Enterprise Header - FIXED: Using .get() to handle missing keys safely
    st.markdown(f"""
    <div style='
        background: linear-gradient(90deg, #0a0a0a 0%, #1a1a1a 100%); 
        padding: 20px; 
        border-bottom: 2px solid #00ff00;
        margin-bottom: 20px;
    '>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: #00ff00; margin: 0; font-size: 2em;'>
                    🛡️ ENTERPRISE SOC PLATFORM v4.0
                </h1>
                <p style='color: #00ff00; margin: 5px 0;'>
                    OPERATOR: {user.get('first_name', '')} {user.get('last_name', '')} {user.get('avatar', '')} | 
                    ROLE: {user.get('role', '')} | 
                    DEPT: {user.get('department', 'N/A')} |
                    SHIFT: {user.get('shift', 'N/A')}
                </p>
            </div>
            <div style='text-align: right;'>
                <p style='color: #00ff00; margin: 0;'>ENTERPRISE ID: {platform.deployment_id}</p>
                <p style='color: #00ff00; margin: 0;'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enterprise Sidebar
    with st.sidebar:
        st.markdown("### ⚡ ENTERPRISE ACTIONS", unsafe_allow_html=True)
        
        if st.button("🔄 REFRESH ENTERPRISE DATA", use_container_width=True, key="refresh_enterprise"):
            platform.generate_enterprise_data()
            platform.last_update = datetime.now()
            st.rerun()
        
        if st.button("🚨 SIMULATE ENTERPRISE INCIDENT", use_container_width=True, key="sim_incident"):
            incident_types = ["Data Breach", "Ransomware Attack", "DDoS Attack", "Insider Threat"]
            incident_type = random.choice(incident_types)
            platform.log_security_event(
                event_type="INCIDENT_SIMULATION",
                severity="CRITICAL",
                message=f"Enterprise incident simulation: {incident_type}",
                user=user.get('user_id', 'unknown')
            )
            st.success(f"🎯 Enterprise incident simulated: {incident_type}")
            time.sleep(1)
            st.rerun()
        
        if st.button("📊 GENERATE EXECUTIVE REPORT", use_container_width=True, key="exec_report"):
            st.info("📈 Executive security report generated and sent to leadership")
        
        if st.button("🔍 RUN ENTERPRISE SCAN", use_container_width=True, key="enterprise_scan"):
            st.info("🔍 Enterprise-wide security assessment initiated")
        
        st.markdown("---")
        st.markdown("### 🎮 ENTERPRISE MODULES", unsafe_allow_html=True)
        
        module = st.radio("SELECT ENTERPRISE MODULE", [
            "📊 ENTERPRISE DASHBOARD", 
            "🌐 NETWORK OPERATIONS CENTER", 
            "💻 ENDPOINT SECURITY", 
            "🕵️ THREAT INTELLIGENCE", 
            "🔍 DIGITAL FORENSICS", 
            "🚨 INCIDENT COMMAND",
            "📈 RISK & COMPLIANCE", 
            "☁️ CLOUD SECURITY",
            "🔧 ASSET MANAGEMENT",
            "📋 VULNERABILITY MANAGEMENT"
        ], key="enterprise_module")
        
        st.markdown("---")
        st.markdown("### 🔔 ENTERPRISE ALERTS", unsafe_allow_html=True)
        
        # Show recent enterprise alerts
        recent_alerts = platform.alert_history[-5:] if platform.alert_history else []
        for alert in recent_alerts:
            severity_color = {
                "CRITICAL": "#ff0000",
                "HIGH": "#ff6600", 
                "MEDIUM": "#ffff00",
                "LOW": "#00ff00",
                "INFO": "#00ffff"
            }.get(alert.get("severity", "INFO"), "#00ffff")
            
            timestamp = alert.get("timestamp", datetime.now())
            if isinstance(timestamp, datetime):
                time_str = timestamp.strftime('%H:%M:%S')
            else:
                time_str = "Unknown"
            
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
                {alert.get('message', 'No message')}<br>
                <small>{time_str}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚪 SECURE LOGOUT", use_container_width=True, type="primary"):
            platform.log_security_event(
                event_type="USER_LOGOUT",
                severity="INFO",
                message=f"User {user.get('user_id', 'unknown')} logged out from enterprise SOC platform",
                user=user.get('user_id', 'unknown')
            )
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Route to selected enterprise module
    if "ENTERPRISE DASHBOARD" in module:
        show_enterprise_dashboard(platform)
    elif "NETWORK OPERATIONS" in module:
        show_network_operations(platform)
    elif "ENDPOINT SECURITY" in module:
        show_endpoint_security(platform)
    elif "THREAT INTELLIGENCE" in module:
        show_threat_intelligence(platform)
    elif "DIGITAL FORENSICS" in module:
        show_digital_forensics(platform)
    elif "INCIDENT COMMAND" in module:
        show_incident_command(platform)
    elif "RISK & COMPLIANCE" in module:
        show_risk_compliance(platform)
    elif "CLOUD SECURITY" in module:
        show_cloud_security(platform)
    elif "ASSET MANAGEMENT" in module:
        show_asset_management(platform)
    elif "VULNERABILITY MANAGEMENT" in module:
        show_vulnerability_management(platform)

def show_enterprise_dashboard(platform):
    """Display enterprise SOC dashboard"""
    
    # Enterprise Risk Score
    risk_level, risk_color, risk_score = platform.calculate_enterprise_risk_score()
    st.markdown(f"""
    <div class="enterprise-panel" style='text-align: center;'>
        <h1 style='color: {risk_color}; margin: 0;'>ENTERPRISE RISK LEVEL: {risk_level}</h1>
        <h2 style='color: {risk_color}; margin: 10px 0;'>{risk_score}/100</h2>
        <div class='progress-enterprise' style='margin: 0 auto; width: 80%;'>
            <div class='progress-enterprise-bar' style='width: {risk_score}%; background: {risk_color};'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enterprise Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_threats = len([t for t in platform.live_threats if t.get("severity") == "Critical"])
        st.markdown(f"""
        <div class="critical-panel" style='text-align: center;'>
            <h1 style='color: #ff0000; font-size: 2.5em;'>{critical_threats}</h1>
            <p>CRITICAL THREATS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_incidents = len([t for t in platform.live_threats if t.get("status") == "Active"])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h1 style='color: #ff6600; font-size: 2.5em;'>{active_incidents}</h1>
            <p>ACTIVE INCIDENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        endpoints_at_risk = len([e for e in platform.endpoint_telemetry if e.get("risk_score", 0) > 70])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h1 style='color: #ffff00; font-size: 2.5em;'>{endpoints_at_risk}</h1>
            <p>ENDPOINTS AT RISK</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        vulnerabilities = sum([asset.get("vulnerabilities", 0) for asset in platform.cloud_assets + platform.iot_devices])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h1 style='color: #ff4444; font-size: 2.5em;'>{vulnerabilities}</h1>
            <p>OPEN VULNERABILITIES</p>
        </div>
        """, unsafe_allow_html=True)
    
    # System Health and Real-time Monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏥 ENTERPRISE SYSTEM HEALTH")
        
        for system, health in platform.system_health.items():
            status_color = "#00ff00" if health.get("status") == "online" else "#ff0000"
            perf_color = "#00ff00" if health.get("performance", 0) > 90 else "#ffff00" if health.get("performance", 0) > 70 else "#ff0000"
            
            st.markdown(f"""
            <div class="enterprise-panel">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span class='status-indicator status-online'></span>
                        <strong>{system.replace('_', ' ').title()}</strong>
                    </div>
                    <div style='text-align: right;'>
                        <span style='color: {perf_color};'>{health.get('performance', 0)}%</span>
                    </div>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: {health.get("performance", 0)}%; background: {perf_color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📡 REAL-TIME THREAT FEED")
        
        # Show recent threats
        recent_threats = sorted(platform.live_threats, key=lambda x: x.get("last_activity", datetime.now()), reverse=True)[:8]
        
        for threat in recent_threats:
            severity = threat.get("severity", "Low")
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }.get(severity, "#00ff00")
            
            last_activity = threat.get("last_activity", datetime.now())
            threat_type = threat.get("type", "Unknown")
            source_country = threat.get("source_country", "Unknown")
            
            st.markdown(f"""
            <div class="log-entry">
                <span style='color: {severity_color};'>[{last_activity.strftime('%H:%M:%S')}]</span>
                <strong>{threat_type}</strong> | Source: {source_country} | Confidence: {threat.get('confidence', 0)}%
            </div>
            """, unsafe_allow_html=True)
    
    # Compliance and Risk Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 COMPLIANCE OVERVIEW")
        
        for framework, data in platform.compliance_data.items():
            status_color = "#00ff00" if data.get("status") == "Compliant" else "#ffff00" if data.get("status") == "Partially Compliant" else "#ff0000"
            
            st.markdown(f"""
            <div class="enterprise-panel">
                <div style='display: flex; justify-content: space-between;'>
                    <strong>{framework}</strong>
                    <span style='color: {status_color};'>{data.get('status', 'Unknown')}</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 0.9em;'>
                    <span>Score: {data.get('score', 0)}%</span>
                    <span>Controls: {data.get('controls_implemented', 0)}/{data.get('controls_total', 0)}</span>
                </div>
                <div class='progress-enterprise'>
                    <div class='progress-enterprise-bar' style='width: {data.get("score", 0)}%; background: {status_color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ ENTERPRISE RISKS")
        
        for risk, assessment in platform.risk_assessments.items():
            likelihood_color = {
                "High": "#ff0000",
                "Medium": "#ffff00", 
                "Low": "#00ff00"
            }.get(assessment.get("likelihood", "Low"), "#00ff00")
            
            impact_color = {
                "Critical": "#ff0000",
                "High": "#ff6600",
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }.get(assessment.get("impact", "Low"), "#00ff00")
            
            st.markdown(f"""
            <div class="enterprise-panel">
                <div style='display: flex; justify-content: space-between;'>
                    <strong>{risk}</strong>
                    <span style='color: {likelihood_color};'>Risk: {assessment.get('risk_score', 0)}</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 0.9em;'>
                    <span>Likelihood: <span style='color: {likelihood_color};'>{assessment.get('likelihood', 'Unknown')}</span></span>
                    <span>Impact: <span style='color: {impact_color};'>{assessment.get('impact', 'Unknown')}</span></span>
                </div>
                <div style='font-size: 0.8em; color: #cccccc;'>
                    Mitigation: {assessment.get('mitigation_status', 'Unknown')}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_network_operations(platform):
    """Display network operations center"""
    st.markdown("## 🌐 NETWORK OPERATIONS CENTER")
    st.markdown("### Enterprise Network Security Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 NETWORK TRAFFIC ANALYTICS")
        
        # Protocol distribution
        protocols = {}
        for activity in platform.network_activity[:500]:
            protocol = activity.get("protocol", "UNKNOWN")
            protocols[protocol] = protocols.get(protocol, 0) + 1
        
        if protocols:
            fig = px.pie(values=list(protocols.values()), names=list(protocols.keys()), 
                        title="Network Protocol Distribution")
            fig.update_layout(
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0a0a0a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🚨 SECURITY ALERTS")
        
        high_severity_alerts = [a for a in platform.ids_alerts if a.get("severity") in ["High", "Critical"]][:10]
        
        for alert in high_severity_alerts:
            severity = alert.get("severity", "Low")
            severity_color = "#ff0000" if severity == "Critical" else "#ff6600"
            
            st.markdown(f"""
            <div class="critical-panel">
                <strong>{alert.get('attack_type', 'Unknown')}</strong><br>
                Source: {alert.get('source_ip', '0.0.0.0')} → Dest: {alert.get('dest_ip', '0.0.0.0')}<br>
                Severity: <span style='color: {severity_color};'>{severity}</span> | 
                Action: {alert.get('action_taken', 'None')}
            </div>
            """, unsafe_allow_html=True)

def show_threat_intelligence(platform):
    """Display enterprise threat intelligence"""
    st.markdown("## 🕵️ ENTERPRISE THREAT INTELLIGENCE")
    st.markdown("### Advanced Threat Analysis & Hunting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌍 ADVANCED PERSISTENT THREATS")
        
        for apt in platform.threat_intel_db.get("advanced_persistent_threats", []):
            risk_color = "#ff0000" if apt.get("attribution_confidence") in ["Very High", "High"] else "#ff6600"
            
            st.markdown(f"""
            <div class="critical-panel">
                <strong>{apt.get('name', 'Unknown')}</strong> | <span style='color: {risk_color};'>{apt.get('country', 'Unknown')}</span><br>
                Targets: {', '.join(apt.get('targets', ['Unknown'])[:3])}<br>
                Confidence: {apt.get('attribution_confidence', 'Unknown')} | Last Seen: {apt.get('last_observed', 'Unknown')}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🦠 MALWARE ANALYSIS")
        
        for malware in platform.threat_intel_db.get("malware_families", []):
            prevalence_color = "#ff0000" if malware.get("prevalence") == "High" else "#ffff00"
            
            st.markdown(f"""
            <div class="enterprise-panel">
                <strong>{malware.get('name', 'Unknown')}</strong> | Type: {malware.get('type', 'Unknown')}<br>
                Detection: {malware.get('detection_rate', 0)}% | Prevalence: <span style='color: {prevalence_color};'>{malware.get('prevalence', 'Unknown')}</span><br>
                IOCs: {malware.get('ioc_count', 0)} | First Seen: {malware.get('first_seen', 'Unknown')}
            </div>
            """, unsafe_allow_html=True)

def show_incident_command(platform):
    """Display incident command center"""
    st.markdown("## 🚨 INCIDENT COMMAND CENTER")
    st.markdown("### Enterprise Incident Management & Response")
    
    active_incidents = [t for t in platform.live_threats if t.get("status") == "Active"]
    
    st.markdown(f"#### 🔥 ACTIVE ENTERPRISE INCIDENTS: {len(active_incidents)}")
    
    if not active_incidents:
        st.success("🎉 No active enterprise incidents requiring immediate response")
        return
    
    for incident in active_incidents:
        severity = incident.get("severity", "Low")
        severity_color = "#ff0000" if severity == "Critical" else "#ff6600"
        
        with st.expander(f"🚨 {incident.get('threat_id', 'Unknown')} - {incident.get('type', 'Unknown')} - Severity: {severity}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {incident.get('description', 'No description')}")
                st.write(f"**First Detected:** {incident.get('first_detected', 'Unknown')}")
                st.write(f"**Source Country:** {incident.get('source_country', 'Unknown')}")
                st.write(f"**Business Impact:** {incident.get('business_impact', 'Unknown')}")
            
            with col2:
                st.write(f"**Assigned To:** {incident.get('assigned_to', 'Unassigned')}")
                st.write(f"**Impact Score:** {incident.get('impact_score', 0)}/10")
                st.write(f"**Confidence:** {incident.get('confidence', 0)}%")
                st.write("**MITRE Techniques:**")
                for technique in incident.get("mitre_techniques", []):
                    st.write(f"  - {technique}")
            
            # Enterprise response actions
            col3, col4, col5, col6 = st.columns(4)
            with col3:
                if st.button("🛑 CONTAIN", key=f"contain_{incident.get('threat_id', 'unknown')}"):
                    st.success("✓ Enterprise containment procedures initiated")
            with col4:
                if st.button("🔍 INVESTIGATE", key=f"investigate_{incident.get('threat_id', 'unknown')}"):
                    st.info("🔍 Deep forensic investigation launched")
            with col5:
                if st.button("📋 ESCALATE", key=f"escalate_{incident.get('threat_id', 'unknown')}"):
                    st.warning("⚠️ Incident escalated to CISO and executive team")
            with col6:
                if st.button("📊 REPORT", key=f"report_{incident.get('threat_id', 'unknown')}"):
                    st.info("📈 Executive incident report generated")

def show_risk_compliance(platform):
    """Display risk and compliance dashboard"""
    st.markdown("## 📈 RISK & COMPLIANCE DASHBOARD")
    st.markdown("### Enterprise Risk Management & Regulatory Compliance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 ENTERPRISE RISK ASSESSMENT")
        
        risks_data = []
        for risk, assessment in platform.risk_assessments.items():
            risks_data.append({
                "Risk": risk,
                "Score": assessment.get("risk_score", 0),
                "Likelihood": assessment.get("likelihood", "Unknown"),
                "Impact": assessment.get("impact", "Unknown"),
                "Status": assessment.get("mitigation_status", "Unknown")
            })
        
        if risks_data:
            risks_df = pd.DataFrame(risks_data)
            
            # Create risk heatmap
            fig = px.bar(risks_df, x="Risk", y="Score", color="Score",
                        title="Enterprise Risk Scores",
                        color_continuous_scale="reds")
            fig.update_layout(
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0a0a0a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📋 COMPLIANCE FRAMEWORKS")
        
        compliance_data = []
        for framework, data in platform.compliance_data.items():
            compliance_data.append({
                "Framework": framework,
                "Score": data.get("score", 0),
                "Status": data.get("status", "Unknown"),
                "Controls": f"{data.get('controls_implemented', 0)}/{data.get('controls_total', 0)}"
            })
        
        if compliance_data:
            compliance_df = pd.DataFrame(compliance_data)
            
            fig = px.bar(compliance_df, x="Framework", y="Score", color="Status",
                        title="Compliance Framework Scores")
            fig.update_layout(
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0a0a0a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)

def show_endpoint_security(platform):
    """Display endpoint security dashboard"""
    st.markdown("## 💻 ENTERPRISE ENDPOINT SECURITY")
    st.markdown("### Advanced Endpoint Protection & Monitoring")
    
    # Endpoint risk analysis
    high_risk = len([e for e in platform.endpoint_telemetry if e.get("risk_score", 0) > 70])
    medium_risk = len([e for e in platform.endpoint_telemetry if 40 <= e.get("risk_score", 0) <= 70])
    low_risk = len([e for e in platform.endpoint_telemetry if e.get("risk_score", 0) < 40])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="critical-panel" style='text-align: center;'>
            <h1 style='color: #ff0000;'>{high_risk}</h1>
            <p>HIGH RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h1 style='color: #ffff00;'>{medium_risk}</h1>
            <p>MEDIUM RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="security-panel" style='text-align: center;'>
            <h1 style='color: #00ff00;'>{low_risk}</h1>
            <p>LOW RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Endpoint details
    st.markdown("#### 🔍 ENDPOINT DETAILS")
    if st.checkbox("Show High Risk Endpoints"):
        high_risk_endpoints = [e for e in platform.endpoint_telemetry if e.get("risk_score", 0) > 70]
        for endpoint in high_risk_endpoints[:5]:
            with st.expander(f"🚨 {endpoint.get('endpoint_id', 'Unknown')} - Risk: {endpoint.get('risk_score', 0)}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**OS:** {endpoint.get('os_version', 'Unknown')}")
                    st.write(f"**AV Status:** {endpoint.get('antivirus_status', 'Unknown')}")
                    st.write(f"**Threats:** {endpoint.get('threats_detected', 0)}")
                with col2:
                    st.write(f"**Patch Level:** {endpoint.get('patch_level', 'Unknown')}")
                    st.write(f"**Last Scan:** {endpoint.get('last_scan', 'Never')}")

def show_digital_forensics(platform):
    """Display digital forensics lab"""
    st.markdown("## 🔍 ENTERPRISE DIGITAL FORENSICS")
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
            <div class="enterprise-panel">
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
            <div class="critical-panel">
                <strong>{malware['name']}</strong><br>
                Risk: <span style='color: {risk_color};'>{malware['risk']}</span><br>
                {malware['analysis']}
            </div>
            """, unsafe_allow_html=True)

def show_cloud_security(platform):
    """Display cloud security dashboard"""
    st.markdown("## ☁️ ENTERPRISE CLOUD SECURITY")
    st.markdown("### Multi-Cloud Security Management")
    
    # Cloud asset overview
    st.markdown("#### 📊 CLOUD ASSET OVERVIEW")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        aws_assets = len([a for a in platform.cloud_assets if a.get("provider") == "AWS"])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #ff9900;'>{aws_assets}</h3>
            <p>AWS Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        azure_assets = len([a for a in platform.cloud_assets if a.get("provider") == "Azure"])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #0078d4;'>{azure_assets}</h3>
            <p>Azure Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gcp_assets = len([a for a in platform.cloud_assets if a.get("provider") == "GCP"])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #4285f4;'>{gcp_assets}</h3>
            <p>GCP Assets</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cloud security issues
    st.markdown("#### 🚨 CLOUD SECURITY ISSUES")
    
    misconfigured = [a for a in platform.cloud_assets if a.get("security_status") == "Misconfigured"]
    for asset in misconfigured[:3]:
        st.markdown(f"""
        <div class="critical-panel">
            <strong>{asset.get('asset_id', 'Unknown')}</strong> - {asset.get('service', 'Unknown')} ({asset.get('provider', 'Unknown')})<br>
            Issue: Misconfiguration detected in {asset.get('region', 'Unknown')}<br>
            Compliance: {asset.get('compliance', 'Unknown')}
        </div>
        """, unsafe_allow_html=True)

def show_asset_management(platform):
    """Display asset management dashboard"""
    st.markdown("## 🔧 ENTERPRISE ASSET MANAGEMENT")
    st.markdown("### Comprehensive Asset Inventory & Security")
    
    total_assets = len(platform.endpoint_telemetry) + len(platform.iot_devices) + len(platform.cloud_assets)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #00ff00;'>{total_assets}</h3>
            <p>TOTAL ASSETS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #00ff00;'>{len(platform.endpoint_telemetry)}</h3>
            <p>ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #00ff00;'>{len(platform.iot_devices)}</h3>
            <p>IOT DEVICES</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #00ff00;'>{len(platform.cloud_assets)}</h3>
            <p>CLOUD ASSETS</p>
        </div>
        """, unsafe_allow_html=True)

def show_vulnerability_management(platform):
    """Display vulnerability management dashboard"""
    st.markdown("## 📋 ENTERPRISE VULNERABILITY MANAGEMENT")
    st.markdown("### Vulnerability Assessment & Patch Management")
    
    # Vulnerability statistics
    critical_vulns = len([v for v in platform.threat_intel_db.get("vulnerabilities", []) if v.get("severity") == "Critical"])
    high_vulns = len([v for v in platform.threat_intel_db.get("vulnerabilities", []) if v.get("severity") == "High"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="critical-panel" style='text-align: center;'>
            <h3 style='color: #ff0000;'>{critical_vulns}</h3>
            <p>CRITICAL VULNERABILITIES</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #ff6600;'>{high_vulns}</h3>
            <p>HIGH VULNERABILITIES</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_vulns = sum([asset.get("vulnerabilities", 0) for asset in platform.iot_devices])
        st.markdown(f"""
        <div class="enterprise-panel" style='text-align: center;'>
            <h3 style='color: #ffff00;'>{total_vulns}</h3>
            <p>ASSET VULNERABILITIES</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Critical vulnerabilities
    st.markdown("#### 🚨 CRITICAL VULNERABILITIES")
    
    for vuln in platform.threat_intel_db.get("vulnerabilities", [])[:3]:
        if vuln.get("severity") == "Critical":
            st.markdown(f"""
            <div class="critical-panel">
                <strong>{vuln.get('cve', 'Unknown')} - {vuln.get('name', 'Unknown')}</strong><br>
                CVSS: {vuln.get('cvss_score', 'Unknown')} | EPSS: {vuln.get('epss_score', 'Unknown')}<br>
                Status: {vuln.get('exploitation_status', 'Unknown')} | Known Exploited: {vuln.get('known_exploited', 'Unknown')}
            </div>
            """, unsafe_allow_html=True)

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
