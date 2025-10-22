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
from cryptography.fernet import Fernet
import ipaddress
import re
warnings.filterwarnings('ignore')

# Page configuration with dark theme
st.set_page_config(
    page_title="SOC Operations Terminal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SOC Terminal CSS with dark theme and cyber aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00ff00;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px #00ff00;
    }
    .soc-terminal {
        background-color: #0a0a0a;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #00ff00;
        color: #00ff00;
    }
    .alert-critical {
        background-color: #330000;
        padding: 0.5rem;
        border-radius: 3px;
        border-left: 4px solid #ff0000;
        color: #ff0000;
        animation: blink 2s infinite;
    }
    .alert-high {
        background-color: #331100;
        padding: 0.5rem;
        border-radius: 3px;
        border-left: 4px solid #ff6600;
        color: #ff6600;
    }
    .alert-medium {
        background-color: #333300;
        padding: 0.5rem;
        border-radius: 3px;
        border-left: 4px solid #ffff00;
        color: #ffff00;
    }
    .alert-low {
        background-color: #003300;
        padding: 0.5rem;
        border-radius: 3px;
        border-left: 4px solid #00ff00;
        color: #00ff00;
    }
    .incident-card {
        border: 1px solid #444;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #1a1a1a;
        color: #00ff00;
    }
    .threat-indicator {
        background-color: #002200;
        border: 1px solid #00ff00;
        border-radius: 3px;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #00ff00;
        border-bottom: 1px solid #333;
        padding: 0.2rem 0;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    .soc-progress {
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00);
        height: 5px;
        border-radius: 2px;
    }
    .terminal-text {
        font-family: 'Courier New', monospace;
        color: #00ff00;
    }
</style>
""", unsafe_allow_html=True)

class SOCOperationsTerminal:
    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.last_update = datetime.now()
        self.initialize_soc_data()
    
    def initialize_soc_data(self):
        """Initialize SOC operations data"""
        # Threat intelligence feeds
        self.threat_feeds = {
            "malware_hashes": [
                "a1b2c3d4e5f6789012345678901234567",
                "f1e2d3c4b5a6987654321098765432109",
                "5f4e3d2c1b0a98765432109876543210"
            ],
            "suspicious_ips": [
                "192.168.1.100", "10.0.0.99", "172.16.0.55",
                "203.0.113.15", "198.51.100.23"
            ],
            "malicious_domains": [
                "malicious-site.com", "phishing-attack.net",
                "bad-domain.org", "suspicious-link.io"
            ]
        }
        
        # SIEM rules and alerts
        self.siem_rules = {
            "RULE_001": {"name": "Multiple Failed Logins", "severity": "High", "category": "Authentication"},
            "RULE_002": {"name": "Unusual After-Hours Access", "severity": "Medium", "category": "Access Control"},
            "RULE_003": {"name": "Data Exfiltration Attempt", "severity": "Critical", "category": "Data Loss"},
            "RULE_004": {"name": "Malware Detection", "severity": "Critical", "category": "Malware"},
            "RULE_005": {"name": "Privilege Escalation", "severity": "High", "category": "Access Control"},
            "RULE_006": {"name": "Suspicious Network Traffic", "severity": "Medium", "category": "Network"},
            "RULE_007": {"name": "Ransomware Activity", "severity": "Critical", "category": "Malware"}
        }
        
        # SOC team members
        self.soc_team = {
            "soc_manager": {
                "user_id": "soc_manager",
                "password": self.hash_password("soc123"),
                "first_name": "Sarah",
                "last_name": "Chen",
                "role": "soc_manager",
                "shift": "Day",
                "expertise": ["Incident Response", "Threat Hunting", "Forensics"]
            },
            "analyst1": {
                "user_id": "analyst1",
                "password": self.hash_password("soc123"),
                "first_name": "Mike",
                "last_name": "Rodriguez",
                "role": "soc_analyst",
                "shift": "Night",
                "expertise": ["Network Security", "Malware Analysis"]
            },
            "analyst2": {
                "user_id": "analyst2",
                "password": self.hash_password("soc123"),
                "first_name": "Lisa",
                "last_name": "Park",
                "role": "soc_analyst",
                "shift": "Day",
                "expertise": ["SIEM Management", "Threat Intelligence"]
            }
        }
        
        # Initialize data structures
        self.security_incidents = []
        self.siem_alerts = []
        self.threat_intel = []
        self.network_logs = []
        self.endpoint_logs = []
        self.firewall_logs = []
        self.incident_response_actions = []
        
        # Generate initial SOC data
        self.generate_security_incidents()
        self.generate_siem_alerts()
        self.generate_network_logs()
        self.generate_threat_intel()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = "soc_terminal_salt_2024"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate SOC team member"""
        if username in self.soc_team:
            user = self.soc_team[username]
            if self.verify_password(password, user["password"]):
                return True
        return False
    
    def generate_security_incidents(self):
        """Generate realistic security incidents"""
        incident_types = [
            "Malware Infection", "Phishing Attack", "Data Breach", 
            "DDoS Attack", "Insider Threat", "Ransomware", "APT Attack"
        ]
        
        statuses = ["New", "Investigating", "Contained", "Resolved", "Escalated"]
        priorities = ["Low", "Medium", "High", "Critical"]
        
        for i in range(15):
            incident_id = f"INC-{2024}-{i+1:04d}"
            incident_type = random.choice(incident_types)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            
            incident = {
                "incident_id": incident_id,
                "title": f"{incident_type} - Case {i+1}",
                "type": incident_type,
                "status": status,
                "priority": priority,
                "assigned_to": random.choice(list(self.soc_team.keys())),
                "created_time": datetime.now() - timedelta(hours=random.randint(1, 72)),
                "last_updated": datetime.now() - timedelta(hours=random.randint(0, 12)),
                "description": f"Security incident involving {incident_type.lower()} detected in the network.",
                "affected_assets": random.randint(1, 50),
                "severity_score": random.randint(1, 100),
                "mitigation_status": random.choice(["Not Started", "In Progress", "Completed"]),
                "related_alerts": []
            }
            
            self.security_incidents.append(incident)
    
    def generate_siem_alerts(self):
        """Generate SIEM security alerts"""
        for i in range(50):
            rule_id = random.choice(list(self.siem_rules.keys()))
            rule = self.siem_rules[rule_id]
            
            alert = {
                "alert_id": f"ALERT-{i+1:06d}",
                "rule_id": rule_id,
                "rule_name": rule["name"],
                "severity": rule["severity"],
                "category": rule["category"],
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 240)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "destination_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user": f"user{random.randint(1, 1000)}",
                "description": f"Detected {rule['name'].lower()} from source IP",
                "status": random.choice(["New", "In Review", "Escalated", "Closed"]),
                "confidence": random.randint(50, 100)
            }
            
            self.siem_alerts.append(alert)
    
    def generate_network_logs(self):
        """Generate network security logs"""
        protocols = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH"]
        actions = ["ALLOW", "DENY", "DROP"]
        
        for i in range(200):
            log = {
                "log_id": f"NET-{i+1:08d}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 480)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "destination_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "source_port": random.randint(1024, 65535),
                "destination_port": random.randint(1, 1024),
                "protocol": random.choice(protocols),
                "action": random.choice(actions),
                "bytes_sent": random.randint(100, 100000),
                "bytes_received": random.randint(100, 50000),
                "threat_indicator": random.random() < 0.1  # 10% are threats
            }
            
            self.network_logs.append(log)
    
    def generate_threat_intel(self):
        """Generate threat intelligence data"""
        threat_types = ["Malware", "Phishing", "C2 Server", "Exploit Kit", "Botnet"]
        
        for i in range(20):
            intel = {
                "id": f"THREAT-{i+1:04d}",
                "type": random.choice(threat_types),
                "indicator": random.choice(self.threat_feeds["malicious_domains"]),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "first_seen": datetime.now() - timedelta(days=random.randint(1, 30)),
                "last_seen": datetime.now() - timedelta(hours=random.randint(1, 24)),
                "source": random.choice(["Internal", "External Feed", "Partner", "Open Source"]),
                "confidence": random.randint(70, 100)
            }
            
            self.threat_intel.append(intel)
    
    def create_incident_response_action(self, incident_id: str, action: str, analyst: str, details: str):
        """Create incident response action"""
        action_id = f"IR-{len(self.incident_response_actions) + 1:06d}"
        
        ir_action = {
            "action_id": action_id,
            "incident_id": incident_id,
            "action": action,
            "analyst": analyst,
            "details": details,
            "timestamp": datetime.now(),
            "status": "Completed"
        }
        
        self.incident_response_actions.append(ir_action)
        self.last_update = datetime.now()
        return action_id
    
    def update_incident_status(self, incident_id: str, new_status: str, updated_by: str):
        """Update incident status"""
        for incident in self.security_incidents:
            if incident["incident_id"] == incident_id:
                incident["status"] = new_status
                incident["last_updated"] = datetime.now()
                incident["assigned_to"] = updated_by
                self.last_update = datetime.now()
                return True
        return False
    
    def escalate_alert(self, alert_id: str, new_severity: str, analyst: str):
        """Escalate SIEM alert severity"""
        for alert in self.siem_alerts:
            if alert["alert_id"] == alert_id:
                alert["severity"] = new_severity
                alert["status"] = "Escalated"
                self.last_update = datetime.now()
                
                # Log the escalation
                self.create_incident_response_action(
                    "SYSTEM", 
                    "Alert Escalation", 
                    analyst, 
                    f"Alert {alert_id} escalated to {new_severity}"
                )
                return True
        return False
    
    def calculate_threat_level(self):
        """Calculate overall threat level based on current alerts"""
        critical_alerts = len([a for a in self.siem_alerts if a["severity"] == "Critical"])
        high_alerts = len([a for a in self.siem_alerts if a["severity"] == "High"])
        
        if critical_alerts > 5:
            return "CRITICAL", "#ff0000"
        elif critical_alerts > 2 or high_alerts > 10:
            return "HIGH", "#ff6600"
        elif high_alerts > 5:
            return "ELEVATED", "#ffff00"
        else:
            return "NORMAL", "#00ff00"

def auto_refresh():
    """Auto-refresh the SOC terminal"""
    if 'soc_terminal' in st.session_state and 'last_refresh' in st.session_state:
        soc = st.session_state.soc_terminal
        if soc.last_update > st.session_state.last_refresh:
            st.session_state.last_refresh = soc.last_update
            st.rerun()

def soc_login_page():
    """Display SOC login page"""
    st.markdown('<div class="main-header">🛡️ SOC OPERATIONS TERMINAL</div>', unsafe_allow_html=True)
    st.markdown("### SECURITY OPERATIONS CENTER - CLASSIFIED ACCESS ONLY", unsafe_allow_html=True)
    
    # Terminal-style login
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #1a1a1a; padding: 20px; border: 1px solid #00ff00; border-radius: 5px;'>
        <h4 style='color: #00ff00;'>SYSTEM STATUS: ONLINE</h4>
        <p style='color: #00ff00;'>Threat Level: <span style='color: #ffff00;'>ELEVATED</span></p>
        <p style='color: #00ff00;'>Last Incident: 5 minutes ago</p>
        <p style='color: #00ff00;'>Active Alerts: 23</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("soc_login_form"):
            st.markdown("**TERMINAL ACCESS**", unsafe_allow_html=True)
            username = st.text_input("OPERATOR ID")
            password = st.text_input("ACCESS CODE", type="password")
            login_button = st.form_submit_button("🔐 INITIATE SESSION")
            
            if login_button:
                if username and password:
                    soc = st.session_state.soc_terminal
                    if soc.authenticate_user(username, password):
                        st.session_state.user = soc.soc_team[username]
                        st.session_state.logged_in = True
                        st.session_state.last_refresh = soc.last_update
                        st.success("ACCESS GRANTED - WELCOME TO SOC TERMINAL")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED - INVALID CREDENTIALS")
                else:
                    st.warning("ENTER CREDENTIALS FOR SYSTEM ACCESS")
    
    # Demo credentials
    st.markdown("---")
    st.markdown("**DEMO ACCESS CREDENTIALS**", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**SOC MANAGER**", unsafe_allow_html=True)
        st.markdown("ID: `soc_manager`", unsafe_allow_html=True)
        st.markdown("CODE: `soc123`", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**ANALYST 1**", unsafe_allow_html=True)
        st.markdown("ID: `analyst1`", unsafe_allow_html=True)
        st.markdown("CODE: `soc123`", unsafe_allow_html=True)
    
    with col3:
        st.markdown("**ANALYST 2**", unsafe_allow_html=True)
        st.markdown("ID: `analyst2`", unsafe_allow_html=True)
        st.markdown("CODE: `soc123`", unsafe_allow_html=True)

def soc_dashboard():
    """Display SOC main dashboard"""
    soc = st.session_state.soc_terminal
    user = st.session_state.user
    
    # Auto-refresh
    auto_refresh()
    
    # SOC Terminal Header
    st.markdown(f"""
    <div style='background-color: #1a1a1a; padding: 10px; border-bottom: 2px solid #00ff00; margin-bottom: 20px;'>
        <h3 style='color: #00ff00; margin: 0;'>SOC TERMINAL | OPERATOR: {user['first_name']} {user['last_name']} | ROLE: {user['role'].upper()}</h3>
        <p style='color: #00ff00; margin: 0; font-size: 0.9em;'>LAST UPDATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with quick actions
    with st.sidebar:
        st.markdown("**QUICK ACTIONS**", unsafe_allow_html=True)
        
        if st.button("🔄 FORCE REFRESH"):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        if st.button("🚨 NEW INCIDENT"):
            st.session_state.show_new_incident = True
        
        if st.button("📊 SYSTEM STATUS"):
            st.session_state.show_system_status = True
        
        st.markdown("---")
        st.markdown("**NAVIGATION**", unsafe_allow_html=True)
        
        if st.button("🚪 LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Main SOC Dashboard
    show_soc_dashboard(soc)

def show_soc_dashboard(soc):
    """Display SOC dashboard with security overview"""
    
    # Threat Level Banner
    threat_level, threat_color = soc.calculate_threat_level()
    st.markdown(f"""
    <div style='background-color: #1a1a1a; padding: 15px; border: 2px solid {threat_color}; border-radius: 5px; margin-bottom: 20px;'>
        <h2 style='color: {threat_color}; text-align: center; margin: 0;'>CURRENT THREAT LEVEL: {threat_level}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Security Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_alerts = len([a for a in soc.siem_alerts if a["severity"] == "Critical"])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: #ff0000;'>{critical_alerts}</h3>
            <p>CRITICAL ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_incidents = len([i for i in soc.security_incidents if i["status"] in ["New", "Investigating"]])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: #ff6600;'>{active_incidents}</h3>
            <p>ACTIVE INCIDENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_alerts = len(soc.siem_alerts)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: #ffff00;'>{total_alerts}</h3>
            <p>TOTAL ALERTS (24H)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_response_time = "15m"  # This would be calculated in real implementation
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: #00ff00;'>{avg_response_time}</h3>
            <p>AVG RESPONSE TIME</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time Security Monitoring
    st.markdown("## 📡 REAL-TIME SECURITY MONITORING")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Alert Severity Distribution
        st.markdown("### ALERT SEVERITY DISTRIBUTION")
        severity_counts = {}
        for alert in soc.siem_alerts:
            severity = alert["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        if severity_counts:
            fig = px.pie(
                values=list(severity_counts.values()), 
                names=list(severity_counts.keys()),
                color=list(severity_counts.keys()),
                color_discrete_map={
                    'Critical': '#ff0000',
                    'High': '#ff6600', 
                    'Medium': '#ffff00',
                    'Low': '#00ff00'
                }
            )
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Incident Status Overview
        st.markdown("### INCIDENT STATUS OVERVIEW")
        status_counts = {}
        for incident in soc.security_incidents:
            status = incident["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig = px.bar(
                x=list(status_counts.keys()),
                y=list(status_counts.values()),
                color=list(status_counts.keys())
            )
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00',
                xaxis_title="Status",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Critical Alerts
    st.markdown("## 🚨 RECENT CRITICAL ALERTS")
    critical_alerts = [a for a in soc.siem_alerts if a["severity"] == "Critical"][:5]
    
    if critical_alerts:
        for alert in critical_alerts:
            alert_class = "alert-critical"
            
            st.markdown(f'<div class="{alert_class}">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{alert['rule_name']}**", unsafe_allow_html=True)
                st.markdown(f"Source: {alert['source_ip']} → Dest: {alert['destination_ip']}", unsafe_allow_html=True)
                st.markdown(f"Time: {alert['timestamp'].strftime('%H:%M:%S')}", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"Status: **{alert['status']}**", unsafe_allow_html=True)
                st.markdown(f"Confidence: {alert['confidence']}%", unsafe_allow_html=True)
            
            with col3:
                if st.button("ESCALATE", key=f"escalate_{alert['alert_id']}"):
                    soc.escalate_alert(alert["alert_id"], "Critical", st.session_state.user["user_id"])
                    st.rerun()
                
                if st.button("DETAILS", key=f"details_{alert['alert_id']}"):
                    st.session_state.selected_alert = alert["alert_id"]
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-low'>No critical alerts at this time</div>", unsafe_allow_html=True)
    
    # Active Incidents
    st.markdown("## 🚧 ACTIVE SECURITY INCIDENTS")
    active_incidents = [i for i in soc.security_incidents if i["status"] in ["New", "Investigating"]][:5]
    
    if active_incidents:
        for incident in active_incidents:
            priority_class = f"alert-{incident['priority'].lower()}"
            
            st.markdown(f'<div class="{priority_class}">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{incident['title']}**", unsafe_allow_html=True)
                st.markdown(f"ID: {incident['incident_id']}", unsafe_allow_html=True)
                st.markdown(f"Type: {incident['type']}", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"Priority: **{incident['priority']}**", unsafe_allow_html=True)
                st.markdown(f"Assigned: {incident['assigned_to']}", unsafe_allow_html=True)
                st.markdown(f"Severity Score: {incident['severity_score']}/100", unsafe_allow_html=True)
            
            with col3:
                new_status = st.selectbox(
                    "Update Status",
                    ["New", "Investigating", "Contained", "Resolved"],
                    index=["New", "Investigating", "Contained", "Resolved"].index(incident["status"]),
                    key=f"status_{incident['incident_id']}"
                )
                
                if new_status != incident["status"]:
                    if st.button("UPDATE", key=f"update_{incident['incident_id']}"):
                        soc.update_incident_status(incident["incident_id"], new_status, st.session_state.user["user_id"])
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Real-time Log Feed (simulated)
    st.markdown("## 📊 REAL-TIME SECURITY LOGS")
    
    # Show recent network logs
    recent_logs = soc.network_logs[-10:]  # Last 10 logs
    for log in reversed(recent_logs):
        log_color = "#ff0000" if log["threat_indicator"] else "#00ff00"
        st.markdown(f"""
        <div class="log-entry">
            <span style='color: {log_color};'>[{log['timestamp'].strftime('%H:%M:%S')}]</span>
            {log['source_ip']}:{log['source_port']} → {log['destination_ip']}:{log['destination_port']}
            <span style='color: #ffff00;'>{log['protocol']}</span> 
            <span style='color: #ff6600;'>{log['action']}</span>
        </div>
        """, unsafe_allow_html=True)

def incident_management(soc):
    """Display incident management interface"""
    st.markdown("## 🚧 INCIDENT MANAGEMENT")
    
    # Incident filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "Investigating", "Contained", "Resolved"])
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        type_filter = st.selectbox("Filter by Type", ["All"] + list(set(i["type"] for i in soc.security_incidents)))
    
    # Apply filters
    filtered_incidents = soc.security_incidents
    if status_filter != "All":
        filtered_incidents = [i for i in filtered_incidents if i["status"] == status_filter]
    if priority_filter != "All":
        filtered_incidents = [i for i in filtered_incidents if i["priority"] == priority_filter]
    if type_filter != "All":
        filtered_incidents = [i for i in filtered_incidents if i["type"] == type_filter]
    
    # Display incidents
    for incident in sorted(filtered_incidents, key=lambda x: x["created_time"], reverse=True):
        priority_class = f"alert-{incident['priority'].lower()}"
        
        with st.expander(f"{incident['incident_id']} - {incident['title']} - {incident['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Incident Details**", unsafe_allow_html=True)
                st.markdown(f"Type: {incident['type']}", unsafe_allow_html=True)
                st.markdown(f"Priority: {incident['priority']}", unsafe_allow_html=True)
                st.markdown(f"Status: {incident['status']}", unsafe_allow_html=True)
                st.markdown(f"Created: {incident['created_time'].strftime('%Y-%m-%d %H:%M')}", unsafe_allow_html=True)
                st.markdown(f"Last Updated: {incident['last_updated'].strftime('%Y-%m-%d %H:%M')}", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Response Details**", unsafe_allow_html=True)
                st.markdown(f"Assigned To: {incident['assigned_to']}", unsafe_allow_html=True)
                st.markdown(f"Affected Assets: {incident['affected_assets']}", unsafe_allow_html=True)
                st.markdown(f"Severity Score: {incident['severity_score']}/100", unsafe_allow_html=True)
                st.markdown(f"Mitigation: {incident['mitigation_status']}", unsafe_allow_html=True)
            
            st.markdown(f"**Description:** {incident['description']}", unsafe_allow_html=True)
            
            # Incident response actions
            st.markdown("**Incident Response Actions**", unsafe_allow_html=True)
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col1:
                if st.button("📋 Start Investigation", key=f"invest_{incident['incident_id']}"):
                    soc.update_incident_status(incident["incident_id"], "Investigating", st.session_state.user["user_id"])
                    st.rerun()
            
            with action_col2:
                if st.button("🛡️ Mark Contained", key=f"contain_{incident['incident_id']}"):
                    soc.update_incident_status(incident["incident_id"], "Contained", st.session_state.user["user_id"])
                    st.rerun()
            
            with action_col3:
                if st.button("✅ Mark Resolved", key=f"resolve_{incident['incident_id']}"):
                    soc.update_incident_status(incident["incident_id"], "Resolved", st.session_state.user["user_id"])
                    st.rerun()
            
            # Add notes/actions
            with st.form(f"action_form_{incident['incident_id']}"):
                action_note = st.text_area("Add Action/Note")
                if st.form_submit_button("Add to Incident Log"):
                    if action_note:
                        soc.create_incident_response_action(
                            incident["incident_id"],
                            "Note Added",
                            st.session_state.user["user_id"],
                            action_note
                        )
                        st.success("Action logged successfully!")
                        st.rerun()

def threat_intelligence(soc):
    """Display threat intelligence dashboard"""
    st.markdown("## 🕵️ THREAT INTELLIGENCE DASHBOARD")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 ACTIVE THREATS")
        for threat in soc.threat_intel[-5:]:
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600", 
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }[threat["severity"]]
            
            st.markdown(f"""
            <div class="threat-indicator">
                <strong style='color: {severity_color};'>{threat['type']}</strong><br>
                Indicator: {threat['indicator']}<br>
                Severity: {threat['severity']} | Confidence: {threat['confidence']}%<br>
                Last Seen: {threat['last_seen'].strftime('%Y-%m-%d %H:%M')}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 THREAT FEED ACTIVITY")
        
        # Threat type distribution
        threat_types = {}
        for threat in soc.threat_intel:
            t_type = threat["type"]
            threat_types[t_type] = threat_types.get(t_type, 0) + 1
        
        if threat_types:
            fig = px.pie(values=list(threat_types.values()), names=list(threat_types.keys()))
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Threat Intelligence Feed
    st.markdown("### 📡 THREAT INTELLIGENCE FEED")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**SUSPICIOUS IPs**", unsafe_allow_html=True)
        for ip in soc.threat_feeds["suspicious_ips"][:5]:
            st.markdown(f"`{ip}`", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**MALWARE HASHES**", unsafe_allow_html=True)
        for hash_val in soc.threat_feeds["malware_hashes"][:3]:
            st.markdown(f"`{hash_val[:16]}...`", unsafe_allow_html=True)
    
    with col3:
        st.markdown("**MALICIOUS DOMAINS**", unsafe_allow_html=True)
        for domain in soc.threat_feeds["malicious_domains"][:5]:
            st.markdown(f"`{domain}`", unsafe_allow_html=True)

def forensics_analysis(soc):
    """Display digital forensics and analysis tools"""
    st.markdown("## 🔍 DIGITAL FORENSICS & ANALYSIS")
    
    tab1, tab2, tab3 = st.tabs(["Network Analysis", "Endpoint Analysis", "Malware Analysis"])
    
    with tab1:
        st.markdown("### 🌐 NETWORK TRAFFIC ANALYSIS")
        
        # Network traffic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_connections = len(soc.network_logs)
            st.metric("Total Connections", total_connections)
        
        with col2:
            blocked_connections = len([log for log in soc.network_logs if log["action"] in ["DENY", "DROP"]])
            st.metric("Blocked Connections", blocked_connections)
        
        with col3:
            suspicious_ips = len(set([log["source_ip"] for log in soc.network_logs if log["threat_indicator"]]))
            st.metric("Suspicious IPs", suspicious_ips)
        
        with col4:
            data_transferred = sum([log["bytes_sent"] + log["bytes_received"] for log in soc.network_logs])
            st.metric("Data Transferred", f"{data_transferred/1024/1024:.1f} MB")
        
        # Protocol distribution
        st.markdown("**Protocol Distribution**", unsafe_allow_html=True)
        protocol_counts = {}
        for log in soc.network_logs:
            protocol = log["protocol"]
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
        
        if protocol_counts:
            fig = px.bar(x=list(protocol_counts.keys()), y=list(protocol_counts.values()))
            fig.update_layout(
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                font_color='#00ff00'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 💻 ENDPOINT SECURITY ANALYSIS")
        
        # Simulated endpoint data
        endpoints = [
            {"hostname": "WS-001", "status": "Compromised", "last_seen": "2 minutes ago", "threats": 3},
            {"hostname": "SRV-005", "status": "Suspicious", "last_seen": "15 minutes ago", "threats": 1},
            {"hostname": "LAP-023", "status": "Clean", "last_seen": "1 hour ago", "threats": 0},
            {"hostname": "WS-042", "status": "Compromised", "last_seen": "5 minutes ago", "threats": 2},
            {"hostname": "SRV-012", "status": "Clean", "last_seen": "30 minutes ago", "threats": 0}
        ]
        
        for endpoint in endpoints:
            status_color = "#ff0000" if endpoint["status"] == "Compromised" else "#ffff00" if endpoint["status"] == "Suspicious" else "#00ff00"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border: 1px solid {status_color}; border-radius: 3px;'>
                <strong>{endpoint['hostname']}</strong> | 
                Status: <span style='color: {status_color};'>{endpoint['status']}</span> | 
                Threats: {endpoint['threats']} | 
                Last Seen: {endpoint['last_seen']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🦠 MALWARE ANALYSIS")
        
        st.markdown("**Recent Malware Detections**", unsafe_allow_html=True)
        malware_samples = [
            {"name": "Trojan.Generic", "hash": "a1b2c3d4e5f6789012345678901234567", "severity": "High"},
            {"name": "Ransomware.Cryptolocker", "hash": "f1e2d3c4b5a6987654321098765432109", "severity": "Critical"},
            {"name": "Backdoor.DarkComet", "hash": "5f4e3d2c1b0a98765432109876543210", "severity": "High"}
        ]
        
        for malware in malware_samples:
            severity_color = "#ff0000" if malware["severity"] == "Critical" else "#ff6600"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 10px; margin: 5px 0; border: 1px solid {severity_color}; border-radius: 3px;'>
                <strong>{malware['name']}</strong><br>
                Hash: <code>{malware['hash']}</code><br>
                Severity: <span style='color: {severity_color};'>{malware['severity']}</span>
            </div>
            """, unsafe_allow_html=True)

def main():
    # Initialize SOC terminal in session state
    if 'soc_terminal' not in st.session_state:
        st.session_state.soc_terminal = SOCOperationsTerminal()
    
    # Initialize login state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.last_refresh = datetime.now()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        soc_login_page()
    else:
        soc_dashboard()

if __name__ == "__main__":
    main()
