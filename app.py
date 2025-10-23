import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import random
import time
from collections import deque
import warnings

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Aegis Cyber Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED UI/UX STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    /* Main body and background */
    .stApp {
        background-color: #0a0c27;
        color: #e0e0e0;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Header */
    .aegis-header {
        font-size: 3rem;
        color: #00ffdd;
        text-align: center;
        text-shadow: 0 0 15px #00ffdd;
        letter-spacing: 4px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    /* Posture Bar */
    .posture-bar {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 2rem;
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 2px;
        transition: all 0.5s ease;
    }

    /* Cards */
    .metric-card, .info-card {
        background: rgba(20, 25, 60, 0.5);
        border: 1px solid #2a3e63;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ffdd;
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8a9cbb;
        text-transform: uppercase;
    }

    /* Terminal/Log Window */
    .terminal-window {
        background-color: #050614;
        border: 1px solid #2a3e63;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.9em;
        height: 450px;
        overflow-y: scroll;
        white-space: pre-wrap;
    }
    .terminal-window::-webkit-scrollbar { display: none; } /* Hide scrollbar */
    .terminal-window { -ms-overflow-style: none; scrollbar-width: none; }

    /* Badges for Severity */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-critical { background-color: #ff0055; color: white; }
    .badge-high { background-color: #ff8c00; color: white; }
    .badge-medium { background-color: #ffd700; color: black; }
    .badge-low { background-color: #00ffdd; color: black; }

    /* Kill Chain Styling */
    .kill-chain-stage {
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        text-align: center;
        color: #e0e0e0;
        border: 1px solid #2a3e63;
        background: #14193c;
    }
    .kill-chain-stage.active {
        border-color: #ff0055;
        background: #4d001a;
        box-shadow: 0 0 10px #ff0055;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER CLASSES & DATA ---

class ThreatIntel:
    """Manages Threat Intelligence Data"""
    APT_GROUPS = {
        "FIN7": {"country": "Russia", "motivation": "Financial", "targets": ["Retail", "Hospitality"]},
        "APT41": {"country": "China", "motivation": "Espionage/Financial", "targets": ["Tech", "Gaming", "Healthcare"]},
        "LAZARUS": {"country": "North Korea", "motivation": "Financial/Sabotage", "targets": ["Crypto", "Finance"]},
    }
    MALWARE = {
        "Ryuk": {"type": "Ransomware", "vector": "Phishing/TrickBot"},
        "Emotet": {"type": "Trojan/Downloader", "vector": "Malspam"},
        "Cobalt Strike": {"type": "C2 Framework", "vector": "Multiple"},
    }
    IOC_TYPES = {
        "md5": lambda: hashlib.md5(str(random.random()).encode()).hexdigest(),
        "sha256": lambda: hashlib.sha256(str(random.random()).encode()).hexdigest(),
        "domain": lambda: f"{random.choice(['core', 'gate', 'update', 'cdn'])}.{random.choice(['fast-serv', 'net-link', 'cloud-host'])}.{random.choice(['com', 'net', 'to'])}",
        "ip": lambda: f"{random.randint(45,220)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    }
    WORLD_CAPITALS = {
        'Russia': (55.75, 37.61), 'China': (39.90, 116.40), 'North Korea': (39.03, 125.75),
        'USA': (38.90, -77.03), 'Germany': (52.52, 13.40), 'Brazil': (-15.79, -47.88),
        'Iran': (35.68, 51.38), 'Nigeria': (9.07, 7.49)
    }

class MITRE:
    """Manages MITRE ATT&CK Data"""
    TACTICS = {
        "TA0001": "Initial Access",
        "TA0002": "Execution",
        "TA0005": "Defense Evasion",
        "TA0007": "Discovery",
        "TA0006": "Credential Access",
        "TA0003": "Persistence",
        "TA0011": "Command and Control",
        "TA0010": "Exfiltration",
        "TA0040": "Impact"
    }

class KillChain:
    """Manages Cyber Kill Chain Stages"""
    STAGES = [
        "Reconnaissance", "Weaponization", "Delivery", "Exploitation",
        "Installation", "Command & Control", "Actions on Objectives"
    ]

# --- MAIN SIMULATION CLASS ---

class AegisPlatform:
    def __init__(self):
        # One-time initialization of static assets
        self.operators = {
            "commander": {"name": "Alex Thorne", "role": "SOC Commander", "pass": self.hash("alpha-one")},
            "analyst": {"name": "Casey Zhang", "role": "Tier 2 Analyst", "pass": self.hash("bravo-seven")},
            "hunter": {"name": "Jordan Reyes", "role": "Threat Hunter", "pass": self.hash("charlie-three")}
        }

    def initialize_session(self):
        """Initializes session-specific data. Called on new session/login."""
        st.session_state.incidents = {}
        st.session_state.event_log = deque(maxlen=200)
        st.session_state.posture_score = 95
        st.session_state.last_update = time.time()
        self.log_event("AEGIS System Initialized. Awaiting Operator.", "INFO")
        
    def hash(self, password):
        return hashlib.sha256(f"aegis_salt_{password}".encode()).hexdigest()

    def log_event(self, message, level="INFO"):
        colors = {"CRITICAL": "#ff0055", "HIGH": "#ff8c00", "MEDIUM": "#ffd700", "INFO": "#00ffdd"}
        log_entry = f"<span style='color:{colors.get(level, '#e0e0e0')}'>[{datetime.now():%H:%M:%S} {level}]</span> {message}"
        st.session_state.event_log.appendleft(log_entry)

    def update_simulation(self):
        """Heartbeat of the simulation, runs periodically."""
        now = time.time()
        if now - st.session_state.get('last_update', 0) > 3: # Update every 3 seconds
            # Degrade posture slightly over time if no action is taken
            if st.session_state.posture_score > 30 and any(inc['status'] == 'Active' for inc in st.session_state.incidents.values()):
                st.session_state.posture_score = max(30, st.session_state.posture_score - 1)
                self.log_event("Posture degrading due to unresolved active threats.", "MEDIUM")
            st.session_state.last_update = now

    def simulate_attack(self):
        """Generates a new, complex incident."""
        incident_id = f"INC-{random.randint(1000, 9999)}"
        apt = random.choice(list(ThreatIntel.APT_GROUPS.keys()))
        malware = random.choice(list(ThreatIntel.MALWARE.keys()))
        target_asset = f"SRV-DB-{random.randint(1,5)}"
        source_country = ThreatIntel.APT_GROUPS[apt]["country"]
        
        # Correlated IoCs for this attack
        ioc_ip = ThreatIntel.IOC_TYPES['ip']()
        ioc_domain = ThreatIntel.IOC_TYPES['domain']()
        ioc_hash = ThreatIntel.IOC_TYPES['sha256']()

        incident = {
            "id": incident_id,
            "title": f"{malware} Ransomware Deployment by {apt}",
            "status": "Active", # Active, In-Progress, Contained, Closed
            "severity": "CRITICAL",
            "timestamp": datetime.now(),
            "kill_chain_stage": 3, # Starts at Exploitation
            "assigned_to": "Unassigned",
            "tactic": MITRE.TACTICS["TA0002"], # Execution
            "intel": {
                "apt_group": apt,
                "malware": malware,
                "source_country": source_country,
                "source_coords": ThreatIntel.WORLD_CAPITALS[source_country],
                "target_asset": target_asset,
                "target_coords": ThreatIntel.WORLD_CAPITALS['USA']
            },
            "iocs": {
                "IP Address": ioc_ip,
                "Domain": ioc_domain,
                "File Hash (SHA256)": ioc_hash,
            },
            "timeline": [f"{datetime.now():%H:%M:%S} - Initial breach detected on {target_asset} from {ioc_ip}."]
        }
        st.session_state.incidents[incident_id] = incident
        self.log_event(f"CRITICAL Threat: {incident['title']} detected!", "CRITICAL")
        st.session_state.posture_score = max(20, st.session_state.posture_score - 25)

# --- UI RENDERING FUNCTIONS ---

def render_login(platform):
    st.markdown('<div class="aegis-header">AEGIS</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #8a9cbb;'>OPERATOR AUTHENTICATION</h3>", unsafe_allow_html=True)
            username = st.selectbox("Operator ID", options=list(platform.operators.keys()))
            password = st.text_input("Access Code", type="password")
            submitted = st.form_submit_button("CONNECT", use_container_width=True)

            if submitted:
                if platform.hash(password) == platform.operators[username]["pass"]:
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    platform.initialize_session() # Initialize a fresh session on login
                    st.success("Authentication Confirmed. Initializing Dashboard...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Access Denied. Invalid Credentials.")

def render_dashboard(platform):
    user_info = platform.operators[st.session_state.user]

    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"### Welcome, {user_info['name']}")
        st.caption(user_info['role'])
        st.markdown("---")
        if st.button("🚨 SIMULATE NEW ATTACK", use_container_width=True):
            platform.simulate_attack()
            st.rerun()
        
        st.markdown("### Modules")
        module = st.radio("Select Module", ["Dashboard", "Incidents", "Threat Intelligence", "Kill Chain Analysis"], label_visibility="collapsed")
        
        st.markdown("---")
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- Main Content ---
    st.markdown('<div class="aegis-header">AEGIS CYBER COMMAND</div>', unsafe_allow_html=True)
    
    # Posture Bar
    score = st.session_state.posture_score
    if score >= 85: status, color = "OPTIMAL", "#00ffdd"
    elif score >= 60: status, color = "STABLE", "#7fff00"
    elif score >= 40: status, color = "DEGRADED", "#ffd700"
    else: status, color = "CRITICAL", "#ff0055"
    st.markdown(f"""
    <div class="posture-bar" style="border: 2px solid {color}; color: {color}; box-shadow: 0 0 15px {color}60;">
        SECURITY POSTURE: {status} | SYSTEM INTEGRITY: {score}%
    </div>
    """, unsafe_allow_html=True)

    if module == "Dashboard":
        render_main_dashboard(platform)
    elif module == "Incidents":
        render_incidents(platform)
    elif module == "Threat Intelligence":
        render_threat_intel(platform)
    elif module == "Kill Chain Analysis":
        render_kill_chain(platform)

def render_main_dashboard(platform):
    # --- Key Metrics ---
    c1, c2, c3 = st.columns(3)
    active_incidents = [inc for inc in st.session_state.incidents.values() if inc['status'] == 'Active']
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ff0055;">{len(active_incidents)}</div>
            <div class="metric-label">Active Critical Incidents</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        in_progress = len([inc for inc in st.session_state.incidents.values() if inc['status'] == 'In-Progress'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ffd700;">{in_progress}</div>
            <div class="metric-label">Incidents Under Review</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        total_iocs = sum(len(inc['iocs']) for inc in st.session_state.incidents.values())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #00ffdd;">{total_iocs}</div>
            <div class="metric-label">Total Indicators of Compromise</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # --- Map and Log ---
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("#### Global Threat Activity")
        render_threat_map()
    with c2:
        st.markdown("#### Live Event Stream")
        log_html = '<div class="terminal-window">' + "".join([f"<div>{log}</div>" for log in st.session_state.event_log]) + '</div>'
        st.markdown(log_html, unsafe_allow_html=True)

def render_threat_map():
    if not st.session_state.incidents:
        st.info("No active threats to display on map.")
        return

    map_data = []
    for inc in st.session_state.incidents.values():
        if inc['status'] == 'Active':
            map_data.append({
                "lat": inc['intel']['source_coords'][0], "lon": inc['intel']['source_coords'][1],
                "country": inc['intel']['source_country'], "type": "origin"
            })
            map_data.append({
                "lat": inc['intel']['target_coords'][0], "lon": inc['intel']['target_coords'][1],
                "country": "USA", "type": "target"
            })
    
    df = pd.DataFrame(map_data)
    
    fig = go.Figure()
    # Add attack lines
    for inc in st.session_state.incidents.values():
        if inc['status'] == 'Active':
            fig.add_trace(go.Scattergeo(
                lon = [inc['intel']['source_coords'][1], inc['intel']['target_coords'][1]],
                lat = [inc['intel']['source_coords'][0], inc['intel']['target_coords'][0]],
                mode = 'lines',
                line = dict(width = 1.5, color = '#ff0055'),
                opacity = 0.6
            ))

    # Add points
    fig.add_trace(go.Scattergeo(
        lon = df['lon'], lat = df['lat'], text = df['country'],
        mode = 'markers',
        marker = dict(
            size = 10,
            color = df['type'].map({'origin': '#ff0055', 'target': '#00ffdd'}),
            line = dict(width = 1, color = 'white'),
            sizemode = 'area'
        )
    ))

    fig.update_layout(
        showlegend = False,
        geo = dict(
            scope = 'world',
            projection_type = 'natural earth',
            bgcolor = 'rgba(0,0,0,0)',
            landcolor = '#2a3e63',
            subunitcolor = '#14193c'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_incidents(platform):
    st.markdown("### Incident Response Cases")
    active_cases = {k: v for k, v in st.session_state.incidents.items() if v['status'] != 'Closed'}
    
    if not active_cases:
        st.success("No active incidents. System is clear.")
        return

    for inc_id, inc in active_cases.items():
        with st.expander(f"**{inc['id']}**: {inc['title']} | Status: {inc['status']}"):
            c1, c2 = st.columns([2,1])
            with c1:
                st.markdown(f"**Severity:** <span class='badge badge-{inc['severity'].lower()}'>{inc['severity']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Detected:** {inc['timestamp']:%Y-%m-%d %H:%M:%S}")
                st.markdown(f"**Assigned To:** {inc['assigned_to']}")
                st.markdown("**Indicators of Compromise (IoCs):**")
                for key, val in inc['iocs'].items():
                    st.code(f"{key}: {val}")
            
            with c2:
                st.markdown("**Response Actions**")
                if inc['status'] == 'Active':
                    if st.button("Assign & Investigate", key=f"assign_{inc_id}", use_container_width=True):
                        st.session_state.incidents[inc_id]['status'] = 'In-Progress'
                        st.session_state.incidents[inc_id]['assigned_to'] = platform.operators[st.session_state.user]['name']
                        platform.log_event(f"{inc_id} assigned to {st.session_state.incidents[inc_id]['assigned_to']}", "INFO")
                        st.rerun()
                
                if inc['status'] == 'In-Progress':
                    if st.button("Contain Threat", key=f"contain_{inc_id}", use_container_width=True):
                        st.session_state.incidents[inc_id]['status'] = 'Contained'
                        st.session_state.posture_score = min(100, st.session_state.posture_score + 15)
                        platform.log_event(f"Threat for {inc_id} has been contained.", "HIGH")
                        st.rerun()
                
                if inc['status'] == 'Contained':
                    if st.button("Close Case", key=f"close_{inc_id}", use_container_width=True):
                        st.session_state.incidents[inc_id]['status'] = 'Closed'
                        platform.log_event(f"Incident case {inc_id} resolved and closed.", "INFO")
                        st.rerun()

def render_threat_intel(platform):
    st.markdown("### Threat Intelligence Database")
    tab1, tab2, tab3 = st.tabs(["APT Groups", "Malware Index", "Indicators of Compromise"])

    with tab1:
        for apt, data in ThreatIntel.APT_GROUPS.items():
            st.markdown(f"<div class='info-card' style='margin-bottom:1rem;'><h4>{apt} ({data['country']})</h4>"
                        f"<li><b>Motivation:</b> {data['motivation']}</li>"
                        f"<li><b>Primary Targets:</b> {', '.join(data['targets'])}</li></div>", unsafe_allow_html=True)
    with tab2:
        for malware, data in ThreatIntel.MALWARE.items():
            st.markdown(f"<div class='info-card' style='margin-bottom:1rem;'><h4>{malware}</h4>"
                        f"<li><b>Type:</b> {data['type']}</li>"
                        f"<li><b>Common Vector:</b> {data['vector']}</li></div>", unsafe_allow_html=True)
    with tab3:
        st.markdown("#### Known Malicious Indicators")
        iocs = []
        for inc in st.session_state.incidents.values():
            for type, val in inc['iocs'].items():
                iocs.append({"Incident": inc['id'], "Indicator Type": type, "Value": val})
        if iocs:
            st.dataframe(pd.DataFrame(iocs), use_container_width=True)
        else:
            st.info("No IoCs from active incidents.")
            
def render_kill_chain(platform):
    st.markdown("### Cyber Kill Chain Analysis")
    active_incident = next((inc for inc in st.session_state.incidents.values() if inc['status'] in ['Active', 'In-Progress']), None)
    
    if not active_incident:
        st.success("No active incidents to analyze.")
        return

    st.info(f"Displaying analysis for **{active_incident['id']}**: {active_incident['title']}")
    
    cols = st.columns(len(KillChain.STAGES))
    current_stage = active_incident['kill_chain_stage']
    
    for i, stage in enumerate(KillChain.STAGES):
        with cols[i]:
            active_class = "active" if i == current_stage else ""
            st.markdown(f"<div class='kill-chain-stage {active_class}'>{stage}</div>", unsafe_allow_html=True)

# --- APP EXECUTION ---

def main():
    if 'platform' not in st.session_state:
        st.session_state.platform = AegisPlatform()
    
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        render_login(st.session_state.platform)
    else:
        st.session_state.platform.update_simulation()
        render_dashboard(st.session_state.platform)
        time.sleep(3) # Auto-refresh interval
        st.rerun()

if __name__ == "__main__":
    main()
