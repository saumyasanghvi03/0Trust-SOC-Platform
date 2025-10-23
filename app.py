import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import random
from typing import Dict, List
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CYBER TERMINAL v2.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #00ff00;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px #00ff00;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
        to { text-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
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
</style>
""", unsafe_allow_html=True)

class CyberTerminal:
    def __init__(self):
        self.last_update = datetime.now()
        self.initialize_data()
        
    def initialize_data(self):
        """Initialize all data structures"""
        # Cyber team credentials
        self.cyber_team = {
            "cyber_commander": {
                "user_id": "cyber_commander",
                "password": self.hash_password("cyber123"),
                "first_name": "Alex",
                "last_name": "Thorne",
                "role": "Commander",
                "clearance": "TOP SECRET"
            },
            "threat_hunter": {
                "user_id": "threat_hunter",
                "password": self.hash_password("cyber123"),
                "first_name": "Jordan",
                "last_name": "Reyes",
                "role": "Threat Hunter",
                "clearance": "SECRET"
            },
            "defense_analyst": {
                "user_id": "defense_analyst",
                "password": self.hash_password("cyber123"),
                "first_name": "Casey",
                "last_name": "Zhang",
                "role": "Defense Analyst",
                "clearance": "SECRET"
            }
        }
        
        # Initialize threat data
        self.active_threats = []
        self.network_activity = []
        self.endpoints = []
        self.ids_alerts = []
        
        # Generate initial data
        self.generate_initial_data()
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "cyber_terminal_2024"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        return self.hash_password(password) == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user"""
        if username in self.cyber_team:
            return self.verify_password(password, self.cyber_team[username]["password"])
        return False
    
    def generate_initial_data(self):
        """Generate initial threat and network data"""
        # Generate threats
        threat_types = ["Malware", "Phishing", "DDoS", "Data Breach", "APT Campaign"]
        severities = ["Critical", "High", "Medium", "Low"]
        
        for i in range(12):
            threat = {
                "id": f"THR-{i+1:06d}",
                "type": random.choice(threat_types),
                "severity": random.choice(severities),
                "confidence": random.randint(60, 99),
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 48)),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "status": random.choice(["Active", "Investigating", "Contained"])
            }
            self.active_threats.append(threat)
        
        # Generate network activity
        for i in range(100):
            activity = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(1, 300)),
                "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
                "bytes": random.randint(100, 100000),
                "threat_score": random.randint(0, 100),
                "flagged": random.random() < 0.15
            }
            self.network_activity.append(activity)
        
        # Generate endpoints
        for i in range(30):
            endpoint = {
                "id": f"WS-{i+1:03d}",
                "ip": f"10.0.10.{i+1}",
                "os": random.choice(["Windows 10", "Windows 11", "Linux"]),
                "status": random.choice(["Online", "Online", "Online", "Offline"]),
                "risk_score": random.randint(10, 95),
                "av_status": random.choice(["Protected", "Warning", "Critical"])
            }
            self.endpoints.append(endpoint)
        
        # Generate IDS alerts
        attack_types = ["Port Scan", "Brute Force", "SQL Injection", "XSS"]
        for i in range(50):
            alert = {
                "id": f"IDS-{i+1:06d}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 120)),
                "attack_type": random.choice(attack_types),
                "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "severity": random.choice(["Critical", "High", "Medium", "Low"]),
                "action": random.choice(["Blocked", "Alerted", "Allowed"])
            }
            self.ids_alerts.append(alert)
    
    def calculate_security_posture(self):
        """Calculate security posture"""
        critical = len([t for t in self.active_threats if t["severity"] == "Critical"])
        high = len([t for t in self.active_threats if t["severity"] == "High"])
        active = len([t for t in self.active_threats if t["status"] == "Active"])
        
        score = 100 - (critical * 10) - (high * 5) - (active * 3)
        score = max(0, min(100, score))
        
        if score >= 80:
            return "STRONG", "#00ff00", score
        elif score >= 60:
            return "MODERATE", "#ffff00", score
        elif score >= 40:
            return "WEAK", "#ff6600", score
        else:
            return "CRITICAL", "#ff0000", score
    
    def simulate_attack(self):
        """Simulate a new attack"""
        attack_types = ["Ransomware", "APT Intrusion", "DDoS", "Data Exfiltration"]
        threat = {
            "id": f"THR-{len(self.active_threats)+1:06d}",
            "type": random.choice(attack_types),
            "severity": "Critical",
            "confidence": random.randint(85, 99),
            "timestamp": datetime.now(),
            "source_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "dest_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "status": "Active"
        }
        self.active_threats.append(threat)
        self.last_update = datetime.now()
        return threat["id"]

# Initialize session state
def init_session_state():
    if 'terminal' not in st.session_state:
        st.session_state.terminal = CyberTerminal()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def login_screen():
    """Display login screen"""
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
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("login_form", clear_on_submit=True):
            st.markdown("**TERMINAL ACCESS**")
            username = st.text_input("OPERATOR ID")
            password = st.text_input("ACCESS CODE", type="password")
            login_button = st.form_submit_button("🚀 INITIATE CYBER TERMINAL")
            
            if login_button:
                if username and password:
                    terminal = st.session_state.terminal
                    if terminal.authenticate_user(username, password):
                        st.session_state.user = terminal.cyber_team[username]
                        st.session_state.logged_in = True
                        st.success("✓ ACCESS GRANTED")
                        st.rerun()
                    else:
                        st.error("✗ ACCESS DENIED - Invalid credentials")
                else:
                    st.warning("Enter credentials")
    
    # Demo credentials
    st.markdown("---")
    st.markdown("**AUTHORIZED PERSONNEL**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("ID: cyber_commander\nCODE: cyber123")
    with col2:
        st.code("ID: threat_hunter\nCODE: cyber123")
    with col3:
        st.code("ID: defense_analyst\nCODE: cyber123")

def dashboard_screen():
    """Display main dashboard"""
    terminal = st.session_state.terminal
    user = st.session_state.user
    
    # Header
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%); padding: 15px; border-bottom: 3px solid #00ff00; margin-bottom: 20px;'>
        <h2 style='color: #00ff00; margin: 0; text-align: center;'>
            🛡️ CYBER TERMINAL | {user['first_name']} {user['last_name']} | {user['role'].upper()}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("**QUICK ACTIONS**")
        
        if st.button("🔄 REFRESH", use_container_width=True):
            terminal.generate_initial_data()
            st.rerun()
        
        if st.button("🚨 SIMULATE ATTACK", use_container_width=True):
            attack_id = terminal.simulate_attack()
            st.success(f"Attack simulated: {attack_id}")
            st.rerun()
        
        st.markdown("---")
        module = st.radio("MODULE", [
            "📊 Dashboard",
            "🌐 Network Defense",
            "💻 Endpoints",
            "🚨 Incidents",
            "📈 Analytics"
        ])
        
        st.markdown("---")
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Route to module
    if "Dashboard" in module:
        show_dashboard(terminal)
    elif "Network" in module:
        show_network(terminal)
    elif "Endpoints" in module:
        show_endpoints(terminal)
    elif "Incidents" in module:
        show_incidents(terminal)
    elif "Analytics" in module:
        show_analytics(terminal)

def show_dashboard(terminal):
    """Main dashboard view"""
    # Security posture
    posture, color, score = terminal.calculate_security_posture()
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); padding: 20px; border: 3px solid {color}; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h1 style='color: {color}; margin: 0;'>SECURITY POSTURE: {posture}</h1>
        <h2 style='color: {color};'>SCORE: {score}/100</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    critical = len([t for t in terminal.active_threats if t["severity"] == "Critical"])
    active = len([t for t in terminal.active_threats if t["status"] == "Active"])
    alerts = len(terminal.ids_alerts)
    at_risk = len([e for e in terminal.endpoints if e["risk_score"] > 70])
    
    with col1:
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ff0000;'>{critical}</h1>
            <p>CRITICAL THREATS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ff6600;'>{active}</h1>
            <p>ACTIVE INCIDENTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #ffff00;'>{alerts}</h1>
            <p>IDS ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-glowing'>
            <h1 style='color: #00ff00;'>{at_risk}</h1>
            <p>AT-RISK ENDPOINTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Threat feed
    st.markdown("### 🔥 ACTIVE THREAT FEED")
    
    recent_threats = sorted(terminal.active_threats, key=lambda x: x["timestamp"], reverse=True)[:10]
    
    for threat in recent_threats:
        severity_color = {
            "Critical": "#ff0000",
            "High": "#ff6600",
            "Medium": "#ffff00",
            "Low": "#00ff00"
        }[threat["severity"]]
        
        st.markdown(f"""
        <div class='log-entry' style='border-left: 3px solid {severity_color};'>
            [{threat['timestamp'].strftime('%H:%M:%S')}] {threat['id']} | {threat['type']} | 
            {threat['source_ip']} → {threat['dest_ip']} | 
            <span style='color: {severity_color};'>{threat['severity']}</span> | 
            {threat['status']}
        </div>
        """, unsafe_allow_html=True)

def show_network(terminal):
    """Network defense view"""
    st.markdown("## 🌐 NETWORK DEFENSE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Network Traffic")
        
        # Protocol distribution
        protocols = {}
        for activity in terminal.network_activity:
            proto = activity["protocol"]
            protocols[proto] = protocols.get(proto, 0) + 1
        
        if protocols:
            fig = px.pie(values=list(protocols.values()), names=list(protocols.keys()), 
                        title="Traffic by Protocol")
            fig.update_layout(paper_bgcolor='#1a1a1a', font_color='#00ff00')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### IDS Alerts")
        
        # Recent alerts
        recent_alerts = sorted(terminal.ids_alerts, key=lambda x: x["timestamp"], reverse=True)[:10]
        
        for alert in recent_alerts:
            severity_color = {
                "Critical": "#ff0000",
                "High": "#ff6600",
                "Medium": "#ffff00",
                "Low": "#00ff00"
            }[alert["severity"]]
            
            st.markdown(f"""
            <div style='background: #1a1a1a; padding: 10px; margin: 5px 0; border-left: 3px solid {severity_color};'>
                <strong>{alert['attack_type']}</strong> | {alert['source_ip']}<br>
                Severity: <span style='color: {severity_color};'>{alert['severity']}</span> | 
                Action: {alert['action']}
            </div>
            """, unsafe_allow_html=True)

def show_endpoints(terminal):
    """Endpoint security view"""
    st.markdown("## 💻 ENDPOINT SECURITY")
    
    # Status overview
    col1, col2, col3 = st.columns(3)
    
    online = len([e for e in terminal.endpoints if e["status"] == "Online"])
    critical = len([e for e in terminal.endpoints if e["risk_score"] > 80])
    protected = len([e for e in terminal.endpoints if e["av_status"] == "Protected"])
    
    with col1:
        st.metric("Online", f"{online}/{len(terminal.endpoints)}")
    with col2:
        st.metric("Critical Risk", critical)
    with col3:
        st.metric("Protected", protected)
    
    # Endpoint list
    st.markdown("### Endpoint Status")
    
    high_risk = [e for e in terminal.endpoints if e["risk_score"] > 70]
    
    for endpoint in high_risk[:10]:
        risk_color = "#ff0000" if endpoint["risk_score"] > 80 else "#ff6600"
        
        with st.expander(f"{endpoint['id']} - Risk: {endpoint['risk_score']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**IP:** {endpoint['ip']}")
                st.write(f"**OS:** {endpoint['os']}")
            with col2:
                st.write(f"**Status:** {endpoint['status']}")
                st.write(f"**AV:** {endpoint['av_status']}")

def show_incidents(terminal):
    """Incident response view"""
    st.markdown("## 🚨 ACTIVE INCIDENTS")
    
    active_threats = [t for t in terminal.active_threats if t["status"] == "Active"]
    
    if not active_threats:
        st.success("No active incidents")
        return
    
    for threat in active_threats:
        severity_color = {
            "Critical": "#ff0000",
            "High": "#ff6600",
            "Medium": "#ffff00",
            "Low": "#00ff00"
        }[threat["severity"]]
        
        with st.expander(f"🚨 {threat['id']} - {threat['type']} [{threat['severity']}]"):
            st.markdown(f"""
            <div class='threat-panel'>
                <strong>Source:</strong> {threat['source_ip']}<br>
                <strong>Target:</strong> {threat['dest_ip']}<br>
                <strong>Confidence:</strong> {threat['confidence']}%<br>
                <strong>Detected:</strong> {threat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛑 Contain", key=f"contain_{threat['id']}"):
                    threat['status'] = "Contained"
                    st.success("Threat contained")
                    st.rerun()
            with col2:
                if st.button("🚫 Block IP", key=f"block_{threat['id']}"):
                    st.success(f"IP {threat['source_ip']} blocked")
            with col3:
                if st.button("🔍 Investigate", key=f"investigate_{threat['id']}"):
                    st.info("Investigation initiated")

def show_analytics(terminal):
    """Analytics view"""
    st.markdown("## 📈 ANALYTICS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Threat Trends")
        
        # Generate trend data
        days = [(datetime.now() - timedelta(days=x)).strftime('%m-%d') for x in range(7, 0, -1)]
        counts = [random.randint(5, 20) for _ in range(7)]
        
        fig = px.line(x=days, y=counts, title="Threats (Last 7 Days)")
        fig.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#00ff00')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Attack Types")
        
        attack_types = {}
        for threat in terminal.active_threats:
            attack_types[threat['type']] = attack_types.get(threat['type'], 0) + 1
        
        fig = px.bar(x=list(attack_types.keys()), y=list(attack_types.values()), 
                    title="Attack Distribution")
        fig.update_layout(paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#00ff00')
        st.plotly_chart(fig, use_container_width=True)

def main():
    init_session_state()
    
    if not st.session_state.logged_in:
        login_screen()
    else:
        dashboard_screen()

if __name__ == "__main__":
    main()
