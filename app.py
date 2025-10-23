import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import random
import time
from collections import deque, defaultdict
import warnings
import networkx as nx
from typing import Dict, List, Tuple

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Cyber Warfare Simulation Platform",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        color: #e0e7ff;
        font-family: 'Orbitron', sans-serif;
    }
    
    .warfare-header {
        background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 50%, #dc2626 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 40px rgba(220, 38, 38, 0.5);
        animation: pulse-red 3s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 40px rgba(220, 38, 38, 0.5); }
        50% { box-shadow: 0 0 60px rgba(220, 38, 38, 0.8); }
    }
    
    .warfare-header h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.8);
        letter-spacing: 4px;
    }
    
    .red-team-panel {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border: 2px solid #dc2626;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.3);
        animation: glow-red 2s infinite;
    }
    
    @keyframes glow-red {
        0%, 100% { border-color: #dc2626; }
        50% { border-color: #ef4444; }
    }
    
    .blue-team-panel {
        background: linear-gradient(135deg, #0c4a6e 0%, #075985 100%);
        border: 2px solid #0ea5e9;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.3);
        animation: glow-blue 2s infinite;
    }
    
    @keyframes glow-blue {
        0%, 100% { border-color: #0ea5e9; }
        50% { border-color: #38bdf8; }
    }
    
    .attack-card {
        background: rgba(127, 29, 29, 0.3);
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .attack-card:hover {
        background: rgba(127, 29, 29, 0.5);
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.5);
    }
    
    .defense-card {
        background: rgba(12, 74, 110, 0.3);
        border-left: 4px solid #0ea5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .defense-card:hover {
        background: rgba(12, 74, 110, 0.5);
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.5);
    }
    
    .metric-warfare {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value-red {
        font-size: 3rem;
        font-weight: 900;
        color: #ef4444;
        text-shadow: 0 0 10px #ef4444;
    }
    
    .metric-value-blue {
        font-size: 3rem;
        font-weight: 900;
        color: #38bdf8;
        text-shadow: 0 0 10px #38bdf8;
    }
    
    .kill-chain-stage {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 6px;
        padding: 0.8rem;
        margin: 0.3rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .kill-chain-stage.active {
        background: rgba(127, 29, 29, 0.8);
        border-color: #dc2626;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.6);
        animation: pulse-stage 1s infinite;
    }
    
    @keyframes pulse-stage {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .live-terminal {
        background: #000;
        border: 2px solid #475569;
        border-radius: 8px;
        padding: 1rem;
        height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    
    .live-terminal::-webkit-scrollbar {
        width: 8px;
    }
    
    .live-terminal::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    .badge-attack {
        background: #7f1d1d;
        color: #fecaca;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .badge-defense {
        background: #0c4a6e;
        color: #bae6fd;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .score-board {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #6366f1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .action-button {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        border: none;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .action-button:hover {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.6);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# === CORE CLASSES ===

class MITREAttackFramework:
    """MITRE ATT&CK Framework Integration"""
    
    TACTICS = {
        "Reconnaissance": ["Active Scanning", "Gather Victim Network Info", "Search Open Websites"],
        "Initial Access": ["Phishing", "Exploit Public-Facing App", "Valid Accounts"],
        "Execution": ["Command Scripting", "User Execution", "Scheduled Task"],
        "Persistence": ["Create Account", "Boot/Logon Scripts", "Registry Run Keys"],
        "Privilege Escalation": ["Sudo/Sudo Caching", "Exploitation", "Access Token Manipulation"],
        "Defense Evasion": ["Obfuscation", "Disable Security Tools", "Clear Logs"],
        "Credential Access": ["Brute Force", "Credential Dumping", "Keylogging"],
        "Discovery": ["Network Service Scan", "System Information", "Account Discovery"],
        "Lateral Movement": ["Remote Services", "Exploitation of Remote Services", "Internal Spearphishing"],
        "Collection": ["Data from Local System", "Screen Capture", "Email Collection"],
        "Exfiltration": ["Exfil Over C2 Channel", "Exfil to Cloud Storage", "Automated Exfil"],
        "Impact": ["Data Encrypted for Impact", "Service Stop", "Resource Hijacking"]
    }
    
    @staticmethod
    def get_attack_sequence():
        """Generate realistic attack sequence"""
        sequence = []
        tactics = list(MITREAttackFramework.TACTICS.keys())
        
        # Realistic attack flow
        attack_flow = ["Reconnaissance", "Initial Access", "Execution", "Persistence", 
                      "Privilege Escalation", "Defense Evasion", "Discovery", 
                      "Lateral Movement", "Collection", "Exfiltration", "Impact"]
        
        for tactic in attack_flow:
            if tactic in MITREAttackFramework.TACTICS:
                technique = random.choice(MITREAttackFramework.TACTICS[tactic])
                sequence.append({"tactic": tactic, "technique": technique})
        
        return sequence

class NetworkTopology:
    """Network Infrastructure Simulation"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.build_network()
    
    def build_network(self):
        """Build realistic network topology"""
        # Internet
        self.graph.add_node("Internet", type="external", compromised=False)
        
        # DMZ
        dmz_assets = ["Web-Server-01", "Mail-Server-01", "DNS-Server-01"]
        for asset in dmz_assets:
            self.graph.add_node(asset, type="dmz", compromised=False, value=5)
            self.graph.add_edge("Internet", asset)
        
        # Firewall
        self.graph.add_node("Firewall", type="security", compromised=False)
        for asset in dmz_assets:
            self.graph.add_edge(asset, "Firewall")
        
        # Internal Network
        internal_subnets = {
            "Corporate": ["WS-Corp-01", "WS-Corp-02", "WS-Corp-03", "File-Server-01"],
            "Finance": ["WS-Fin-01", "WS-Fin-02", "DB-Finance-01"],
            "Engineering": ["WS-Eng-01", "WS-Eng-02", "WS-Eng-03", "DB-Product-01"],
            "Executive": ["WS-Exec-01", "Email-Server-01"]
        }
        
        for subnet, assets in internal_subnets.items():
            for asset in assets:
                value = 10 if "DB" in asset or "Exec" in asset else 3
                self.graph.add_node(asset, type=subnet, compromised=False, value=value)
                self.graph.add_edge("Firewall", asset)
        
        # Domain Controller
        self.graph.add_node("DC-01", type="critical", compromised=False, value=20)
        self.graph.add_edge("Firewall", "DC-01")
        
        # Backup Server
        self.graph.add_node("Backup-Server-01", type="critical", compromised=False, value=15)
        self.graph.add_edge("Firewall", "Backup-Server-01")
    
    def get_initial_targets(self):
        """Get possible initial compromise targets"""
        return [n for n in self.graph.nodes() if self.graph.nodes[n].get('type') == 'dmz']
    
    def get_neighbors(self, node):
        """Get accessible nodes from current position"""
        return list(self.graph.successors(node))
    
    def compromise_node(self, node):
        """Mark node as compromised"""
        self.graph.nodes[node]['compromised'] = True
    
    def get_compromised_nodes(self):
        """Get all compromised nodes"""
        return [n for n in self.graph.nodes() if self.graph.nodes[n].get('compromised', False)]
    
    def get_node_value(self, node):
        """Get strategic value of node"""
        return self.graph.nodes[node].get('value', 1)

class AttackCampaign:
    """Red Team Attack Campaign"""
    
    def __init__(self, campaign_id, attack_type, difficulty):
        self.id = campaign_id
        self.attack_type = attack_type
        self.difficulty = difficulty
        self.status = "Planning"
        self.current_stage = 0
        self.attack_sequence = MITREAttackFramework.get_attack_sequence()
        self.compromised_assets = []
        self.data_exfiltrated = 0
        self.detected = False
        self.success_probability = 0.0
        self.started_at = None
        self.ended_at = None
        self.score = 0
        self.stealth_level = random.randint(60, 95)
    
    def advance_stage(self):
        """Progress to next attack stage"""
        if self.current_stage < len(self.attack_sequence):
            self.current_stage += 1
            return True
        return False
    
    def get_current_tactic(self):
        """Get current MITRE tactic"""
        if self.current_stage < len(self.attack_sequence):
            return self.attack_sequence[self.current_stage]
        return None
    
    def calculate_success(self):
        """Calculate attack success probability"""
        base_probability = {
            "Easy": 0.8,
            "Medium": 0.6,
            "Hard": 0.4
        }
        
        # Adjust based on stealth and detection
        prob = base_probability.get(self.difficulty, 0.5)
        
        if self.detected:
            prob *= 0.3  # Much harder if detected
        
        prob *= (self.stealth_level / 100)
        
        return min(0.95, prob)

class DefenseAction:
    """Blue Team Defense Action"""
    
    def __init__(self, action_type, target, effectiveness):
        self.action_type = action_type
        self.target = target
        self.effectiveness = effectiveness
        self.timestamp = datetime.now()
        self.success = random.random() < effectiveness

class CyberWarfareSimulation:
    """Main Simulation Engine"""
    
    def __init__(self):
        self.network = NetworkTopology()
        self.active_campaigns = {}
        self.event_log = deque(maxlen=500)
        self.defense_actions = []
        self.red_team_score = 0
        self.blue_team_score = 0
        self.simulation_running = False
        self.detection_alerts = deque(maxlen=100)
        self.current_time = datetime.now()
        
        # Security Controls
        self.security_controls = {
            "Firewall": {"enabled": True, "effectiveness": 0.7},
            "IDS/IPS": {"enabled": True, "effectiveness": 0.6},
            "EDR": {"enabled": True, "effectiveness": 0.8},
            "SIEM": {"enabled": True, "effectiveness": 0.7},
            "Network Segmentation": {"enabled": True, "effectiveness": 0.5},
            "MFA": {"enabled": True, "effectiveness": 0.9}
        }
        
        self.log_event("Cyber Warfare Simulation initialized", "SYSTEM", "blue")
    
    def log_event(self, message, level="INFO", team="neutral"):
        """Log simulation event"""
        colors = {
            "CRITICAL": "#dc2626",
            "HIGH": "#f97316",
            "MEDIUM": "#eab308",
            "INFO": "#6366f1",
            "SUCCESS": "#22c55e",
            "ATTACK": "#dc2626",
            "DEFENSE": "#0ea5e9"
        }
        
        team_colors = {
            "red": "#dc2626",
            "blue": "#0ea5e9",
            "neutral": "#94a3b8"
        }
        
        timestamp = self.current_time.strftime('%H:%M:%S')
        color = colors.get(level, team_colors.get(team, '#94a3b8'))
        
        log_entry = f"<span style='color: {color}'>[{timestamp}]</span> <strong>[{level}]</strong> {message}"
        self.event_log.appendleft(log_entry)
    
    def launch_attack_campaign(self, attack_type, difficulty):
        """Launch new Red Team campaign"""
        campaign_id = f"RED-{len(self.active_campaigns) + 1:03d}"
        
        campaign = AttackCampaign(campaign_id, attack_type, difficulty)
        campaign.status = "Active"
        campaign.started_at = self.current_time
        
        self.active_campaigns[campaign_id] = campaign
        
        self.log_event(f"🚨 Attack Campaign Launched: {campaign_id} - {attack_type} ({difficulty})", "ATTACK", "red")
        
        return campaign_id
    
    def execute_attack_stage(self, campaign_id):
        """Execute attack stage"""
        if campaign_id not in self.active_campaigns:
            return False
        
        campaign = self.active_campaigns[campaign_id]
        tactic = campaign.get_current_tactic()
        
        if not tactic:
            return False
        
        # Simulate attack execution
        success_prob = campaign.calculate_success()
        success = random.random() < success_prob
        
        if success:
            # Attack stage succeeded
            campaign.advance_stage()
            campaign.score += 10
            self.red_team_score += 10
            
            # Check if detected
            detection_prob = 0.3 * (1 - campaign.stealth_level / 100)
            for control_name, control in self.security_controls.items():
                if control["enabled"]:
                    detection_prob += control["effectiveness"] * 0.1
            
            if random.random() < detection_prob:
                campaign.detected = True
                campaign.stealth_level = max(20, campaign.stealth_level - 20)
                self.log_event(f"⚠️ Attack Detected: {campaign.id} - {tactic['tactic']}", "CRITICAL", "blue")
                self.create_detection_alert(campaign, tactic)
            else:
                self.log_event(f"🔴 Attack Stage Success: {campaign.id} - {tactic['technique']}", "ATTACK", "red")
            
            # Compromise asset if applicable
            if tactic['tactic'] in ["Initial Access", "Lateral Movement"]:
                self.compromise_random_asset(campaign)
            
            return True
        else:
            campaign.detected = True
            self.log_event(f"🔴 Attack Stage Failed: {campaign.id} - {tactic['technique']}", "MEDIUM", "red")
            return False
    
    def compromise_random_asset(self, campaign):
        """Compromise a network asset"""
        if not campaign.compromised_assets:
            # Initial compromise
            targets = self.network.get_initial_targets()
        else:
            # Lateral movement
            current_position = campaign.compromised_assets[-1]
            targets = self.network.get_neighbors(current_position)
            targets = [t for t in targets if t not in campaign.compromised_assets]
        
        if targets:
            target = random.choice(targets)
            self.network.compromise_node(target)
            campaign.compromised_assets.append(target)
            
            value = self.network.get_node_value(target)
            campaign.score += value * 5
            self.red_team_score += value * 5
            
            self.log_event(f"💀 Asset Compromised: {target} by {campaign.id}", "CRITICAL", "red")
    
    def create_detection_alert(self, campaign, tactic):
        """Create security alert"""
        alert = {
            "id": f"ALERT-{len(self.detection_alerts) + 1:04d}",
            "campaign": campaign.id,
            "tactic": tactic['tactic'],
            "technique": tactic['technique'],
            "severity": "Critical" if campaign.current_stage > 5 else "High",
            "timestamp": self.current_time,
            "investigated": False,
            "mitigated": False
        }
        
        self.detection_alerts.appendleft(alert)
    
    def execute_defense_action(self, action_type, target, campaign_id=None):
        """Execute Blue Team defense action"""
        effectiveness = {
            "Investigate Alert": 0.8,
            "Block IP": 0.9,
            "Isolate Asset": 0.95,
            "Kill Process": 0.85,
            "Patch Vulnerability": 0.7,
            "Enable Security Control": 0.6,
            "Hunt Threats": 0.5,
            "Forensic Analysis": 0.7
        }
        
        action = DefenseAction(action_type, target, effectiveness.get(action_type, 0.5))
        self.defense_actions.append(action)
        
        if action.success:
            self.blue_team_score += 15
            self.log_event(f"🔵 Defense Success: {action_type} on {target}", "DEFENSE", "blue")
            
            # Impact on active campaign
            if campaign_id and campaign_id in self.active_campaigns:
                campaign = self.active_campaigns[campaign_id]
                campaign.stealth_level = max(10, campaign.stealth_level - 30)
                campaign.detected = True
                
                # Potentially stop the attack
                if random.random() < 0.4:
                    campaign.status = "Neutralized"
                    self.log_event(f"✅ Campaign Neutralized: {campaign_id}", "SUCCESS", "blue")
            
            return True
        else:
            self.log_event(f"🔵 Defense Failed: {action_type} on {target}", "MEDIUM", "blue")
            return False
    
    def update_simulation(self):
        """Update simulation state"""
        self.current_time = datetime.now()
        
        # Auto-progress active campaigns
        for campaign_id, campaign in list(self.active_campaigns.items()):
            if campaign.status == "Active" and not campaign.detected:
                # Random chance to auto-advance
                if random.random() < 0.3:
                    self.execute_attack_stage(campaign_id)
            
            # Check if campaign completed
            if campaign.current_stage >= len(campaign.attack_sequence):
                campaign.status = "Completed"
                campaign.ended_at = self.current_time
                self.log_event(f"🏁 Campaign Completed: {campaign_id}", "CRITICAL", "red")

# === SESSION STATE INITIALIZATION ===

if 'warfare_sim' not in st.session_state:
    st.session_state.warfare_sim = CyberWarfareSimulation()
    st.session_state.authenticated = False
    st.session_state.user_team = None
    st.session_state.last_update = time.time()

# === AUTHENTICATION ===

def render_team_selection():
    """Team selection screen"""
    
    st.markdown("""
    <div class="warfare-header">
        <h1>⚔️ CYBER WARFARE SIMULATION ⚔️</h1>
        <p style="font-size: 1.5rem; margin: 1rem 0;">Red Team vs Blue Team Combat Training</p>
        <p style="opacity: 0.9;">Advanced Attack & Defense Simulation Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🎯 SELECT YOUR TEAM")
        
        team_choice = st.radio(
            "Choose your side:",
            ["🔴 Red Team (Offensive Security)", "🔵 Blue Team (Defensive Security)", "👁️ Observer Mode"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if "Red Team" in team_choice:
                st.markdown("""
                <div class="red-team-panel">
                    <h3 style="color: #ef4444; margin: 0;">🔴 RED TEAM</h3>
                    <p style="margin: 1rem 0;">Offensive Security</p>
                    <ul style="text-align: left;">
                        <li>Launch attack campaigns</li>
                        <li>Exploit vulnerabilities</li>
                        <li>Evade detection</li>
                        <li>Compromise assets</li>
                        <li>Exfiltrate data</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        with col_b:
            if "Blue Team" in team_choice:
                st.markdown("""
                <div class="blue-team-panel">
                    <h3 style="color: #38bdf8; margin: 0;">🔵 BLUE TEAM</h3>
                    <p style="margin: 1rem 0;">Defensive Security</p>
                    <ul style="text-align: left;">
                        <li>Detect threats</li>
                        <li>Investigate alerts</li>
                        <li>Neutralize attacks</li>
                        <li>Secure assets</li>
                        <li>Hunt adversaries</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("⚡ ENTER BATTLEFIELD", use_container_width=True):
            if "Red Team" in team_choice:
                st.session_state.user_team = "red"
            elif "Blue Team" in team_choice:
                st.session_state.user_team = "blue"
            else:
                st.session_state.user_team = "observer"
            
            st.session_state.authenticated = True
            st.success("✓ Access Granted - Entering Combat Zone")
            time.sleep(0.5)
            st.rerun()

# === MAIN DASHBOARD ===

def render_warfare_dashboard():
    """Main warfare simulation dashboard"""
    sim = st.session_state.warfare_sim
    team = st.session_state.user_team
    
    # Update simulation
    now = time.time()
    if now - st.session_state.last_update > 2:  # Update every 2 seconds
        sim.update_simulation()
        st.session_state.last_update = now
    
    # Header
    team_name = {
        "red": "🔴 RED TEAM - OFFENSIVE OPS",
        "blue": "🔵 BLUE TEAM - DEFENSIVE OPS",
        "observer": "👁️ OBSERVER MODE"
    }
    
    st.markdown(f"""
    <div class="warfare-header">
        <h1>{team_name.get(team, 'CYBER WARFARE')}</h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {team_name.get(team, 'MODE')}")
        
        st.markdown("---")
        st.markdown("### 📊 SIMULATION CONTROL")
        
        if st.button("🔄 Update Simulation", use_container_width=True):
            sim.update_simulation()
            st.rerun()
        
        if st.button("🔥 Auto-Progress ON/OFF", use_container_width=True):
            sim.simulation_running = not sim.simulation_running
        
        st.markdown("---")
        st.markdown("### 🎯 QUICK STATS")
        st.metric("Red Team Score", sim.red_team_score)
        st.metric("Blue Team Score", sim.blue_team_score)
        st.metric("Active Campaigns", len([c for c in sim.active_campaigns.values() if c.status == "Active"]))
        st.metric("Compromised Assets", len(sim.network.get_compromised_nodes()))
        
        st.markdown("---")
        
        if st.button("🚪 Exit Simulation", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Scoreboard
    render_scoreboard(sim)
    
    st.markdown("---")
    
    # Team-specific interface
    if team == "red":
        render_red_team_interface(sim)
    elif team == "blue":
        render_blue_team_interface(sim)
    else:
        render_observer_interface(sim)

def render_scoreboard(sim):
    """Render score comparison"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="score-board">
            <h2 style="color: #ef4444; margin: 0;">🔴 RED TEAM</h2>
            <h1 style="color: #ef4444; font-size: 4rem; margin: 1rem 0;">{sim.red_team_score}</h1>
            <p style="color: #94a3b8;">Offensive Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_score = sim.red_team_score + sim.blue_team_score
        if total_score > 0:
            red_pct = (sim.red_team_score / total_score) * 100
            blue_pct = (sim.blue_team_score / total_score) * 100
        else:
            red_pct = blue_pct = 50
        
        fig = go.Figure(data=[
            go.Bar(name='Red Team', x=[sim.red_team_score], y=['Score'], orientation='h', marker_color='#dc2626'),
            go.Bar(name='Blue Team', x=[sim.blue_team_score], y=['Score'], orientation='h', marker_color='#0ea5e9')
        ])
        
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e7ff',
            height=200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown(f"""
        <div class="score-board">
            <h2 style="color: #38bdf8; margin: 0;">🔵 BLUE TEAM</h2>
            <h1 style="color: #38bdf8; font-size: 4rem; margin: 1rem 0;">{sim.blue_team_score}</h1>
            <p style="color: #94a3b8;">Defensive Score</p>
        </div>
        """, unsafe_allow_html=True)

def render_red_team_interface(sim):
    """Red Team operational interface"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Attack Campaigns", "💀 Compromised Assets", "📊 Network Map", "📡 Attack Logs"])
    
    with tab1:
        st.markdown("### 🔴 OFFENSIVE OPERATIONS")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Launch New Attack")
            
            attack_type = st.selectbox("Attack Type", [
                "APT Campaign",
                "Ransomware Attack",
                "Data Breach",
                "Supply Chain Attack",
                "Insider Threat Simulation",
                "Zero-Day Exploit"
            ])
            
            difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
            
            if st.button("🚀 LAUNCH ATTACK", use_container_width=True):
                campaign_id = sim.launch_attack_campaign(attack_type, difficulty)
                st.success(f"✓ Campaign {campaign_id} Launched!")
                time.sleep(0.5)
                st.rerun()
        
        with col2:
            st.markdown("#### Active Attack Campaigns")
            
            active_campaigns = {k: v for k, v in sim.active_campaigns.items() if v.status == "Active"}
            
            if not active_campaigns:
                st.info("No active campaigns. Launch an attack to begin.")
            else:
                for campaign_id, campaign in active_campaigns.items():
                    with st.expander(f"**{campaign_id}** - {campaign.attack_type} ({campaign.difficulty})"):
                        
                        # Progress bar
                        progress = campaign.current_stage / len(campaign.attack_sequence)
                        st.progress(progress, text=f"Stage {campaign.current_stage}/{len(campaign.attack_sequence)}")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.metric("Campaign Score", campaign.score)
                            st.metric("Stealth Level", f"{campaign.stealth_level}%")
                        
                        with col_b:
                            st.metric("Assets Compromised", len(campaign.compromised_assets))
                            detected_status = "🚨 DETECTED" if campaign.detected else "✅ STEALTHY"
                            st.metric("Detection Status", detected_status)
                        
                        # Current tactic
                        current_tactic = campaign.get_current_tactic()
                        if current_tactic:
                            st.markdown(f"**Current Stage:** {current_tactic['tactic']} - {current_tactic['technique']}")
                        
                        # Actions
                        col_x, col_y = st.columns(2)
                        
                        with col_x:
                            if st.button(f"⚡ Execute Stage", key=f"exec_{campaign_id}"):
                                success = sim.execute_attack_stage(campaign_id)
                                if success:
                                    st.success("✓ Stage executed successfully!")
                                else:
                                    st.error("✗ Stage execution failed!")
                                time.sleep(0.5)
                                st.rerun()
                        
                        with col_y:
                            if st.button(f"🛑 Abort Campaign", key=f"abort_{campaign_id}"):
                                sim.active_campaigns[campaign_id].status = "Aborted"
                                sim.log_event(f"Campaign aborted: {campaign_id}", "INFO", "red")
                                st.rerun()
    
    with tab2:
        st.markdown("### 💀 COMPROMISED NETWORK ASSETS")
        
        compromised = sim.network.get_compromised_nodes()
        
        if not compromised:
            st.info("No assets compromised yet. Continue attacking to gain foothold.")
        else:
            for asset in compromised:
                value = sim.network.get_node_value(asset)
                asset_type = sim.network.graph.nodes[asset].get('type', 'unknown')
                
                st.markdown(f"""
                <div class="attack-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-size: 1.1rem;">{asset}</strong><br>
                            <span style="color: #94a3b8;">Type: {asset_type} | Value: {value}</span>
                        </div>
                        <div>
                            <span class="badge-attack">COMPROMISED</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        render_network_visualization(sim, "red")
    
    with tab4:
        render_event_log(sim, "red")

def render_blue_team_interface(sim):
    """Blue Team operational interface"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Security Alerts", "🔍 Threat Hunting", "🛡️ Security Controls", "📡 Defense Logs"])
    
    with tab1:
        st.markdown("### 🔵 SECURITY OPERATIONS CENTER")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Quick Actions")
            
            if st.button("🔍 Hunt for Threats", use_container_width=True):
                success = sim.execute_defense_action("Hunt Threats", "Network", None)
                if success:
                    st.success("✓ Threat hunt completed!")
                st.rerun()
            
            if st.button("🔒 Isolate All Compromised", use_container_width=True):
                compromised = sim.network.get_compromised_nodes()
                for asset in compromised:
                    sim.execute_defense_action("Isolate Asset", asset, None)
                st.success(f"✓ Isolated {len(compromised)} assets!")
                st.rerun()
            
            if st.button("📊 Run Forensics", use_container_width=True):
                sim.execute_defense_action("Forensic Analysis", "All Systems", None)
                st.success("✓ Forensic analysis initiated!")
                st.rerun()
        
        with col2:
            st.markdown("#### Active Security Alerts")
            
            if not sim.detection_alerts:
                st.success("✓ No active security alerts. System is clean.")
            else:
                for alert in list(sim.detection_alerts)[:10]:
                    severity_badge = "badge-attack" if alert['severity'] == "Critical" else "badge-defense"
                    
                    with st.expander(f"**{alert['id']}** - {alert['tactic']} [{alert['severity']}]"):
                        st.write(f"**Campaign:** {alert['campaign']}")
                        st.write(f"**Technique:** {alert['technique']}")
                        st.write(f"**Timestamp:** {alert['timestamp'].strftime('%H:%M:%S')}")
                        st.write(f"**Investigated:** {'✅ Yes' if alert['investigated'] else '❌ No'}")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            if not alert['investigated'] and st.button(f"🔍 Investigate", key=f"inv_{alert['id']}"):
                                success = sim.execute_defense_action("Investigate Alert", alert['id'], alert['campaign'])
                                if success:
                                    alert['investigated'] = True
                                    st.success("✓ Investigation complete!")
                                st.rerun()
                        
                        with col_b:
                            if alert['investigated'] and not alert['mitigated']:
                                if st.button(f"🛡️ Mitigate", key=f"mit_{alert['id']}"):
                                    success = sim.execute_defense_action("Block IP", alert['campaign'], alert['campaign'])
                                    if success:
                                        alert['mitigated'] = True
                                        st.success("✓ Threat mitigated!")
                                    st.rerun()
    
    with tab2:
        st.markdown("### 🔍 THREAT HUNTING OPERATIONS")
        
        st.markdown("#### Compromised Assets Detected")
        
        compromised = sim.network.get_compromised_nodes()
        
        if not compromised:
            st.success("✓ No compromised assets detected. Network is secure.")
        else:
            st.error(f"🚨 {len(compromised)} assets have been compromised!")
            
            for asset in compromised:
                asset_type = sim.network.graph.nodes[asset].get('type', 'unknown')
                
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    st.markdown(f"**{asset}** ({asset_type})")
                
                with col_b:
                    st.markdown(f"<span class='badge-attack'>COMPROMISED</span>", unsafe_allow_html=True)
                
                with col_c:
                    if st.button(f"🔒 Isolate", key=f"isolate_{asset}"):
                        sim.execute_defense_action("Isolate Asset", asset, None)
                        st.success(f"✓ {asset} isolated!")
                        st.rerun()
    
    with tab3:
        st.markdown("### 🛡️ SECURITY CONTROLS MANAGEMENT")
        
        for control_name, control_data in sim.security_controls.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{control_name}**")
                st.progress(control_data['effectiveness'], text=f"Effectiveness: {int(control_data['effectiveness'] * 100)}%")
            
            with col2:
                status = "🟢 ENABLED" if control_data['enabled'] else "🔴 DISABLED"
                st.markdown(status)
            
            with col3:
                if control_data['enabled']:
                    if st.button(f"Disable", key=f"disable_{control_name}"):
                        sim.security_controls[control_name]['enabled'] = False
                        sim.log_event(f"Security control disabled: {control_name}", "MEDIUM", "blue")
                        st.rerun()
                else:
                    if st.button(f"Enable", key=f"enable_{control_name}"):
                        sim.execute_defense_action("Enable Security Control", control_name, None)
                        sim.security_controls[control_name]['enabled'] = True
                        st.rerun()
    
    with tab4:
        render_event_log(sim, "blue")

def render_observer_interface(sim):
    """Observer mode interface"""
    
    tab1, tab2, tab3 = st.tabs(["📊 Battle Overview", "🌐 Network Status", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 👁️ CYBER WARFARE OVERVIEW")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Red Team Status")
            
            active_red = len([c for c in sim.active_campaigns.values() if c.status == "Active"])
            completed_red = len([c for c in sim.active_campaigns.values() if c.status == "Completed"])
            
            st.metric("Active Campaigns", active_red)
            st.metric("Completed Campaigns", completed_red)
            st.metric("Total Score", sim.red_team_score)
        
        with col2:
            st.markdown("#### 🔵 Blue Team Status")
            
            alerts = len(sim.detection_alerts)
            defenses = len(sim.defense_actions)
            
            st.metric("Active Alerts", alerts)
            st.metric("Defense Actions", defenses)
            st.metric("Total Score", sim.blue_team_score)
        
        st.markdown("---")
        
        st.markdown("#### ⚔️ Active Engagements")
        
        for campaign_id, campaign in sim.active_campaigns.items():
            if campaign.status == "Active":
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    st.markdown(f"**{campaign_id}** - {campaign.attack_type}")
                
                with col_b:
                    detection = "🚨 DETECTED" if campaign.detected else "✅ UNDETECTED"
                    st.markdown(detection)
                
                with col_c:
                    st.progress(campaign.current_stage / len(campaign.attack_sequence))
    
    with tab2:
        render_network_visualization(sim, "observer")
    
    with tab3:
        render_analytics(sim)

def render_network_visualization(sim, team):
    """Render network topology visualization"""
    st.markdown("### 🌐 NETWORK TOPOLOGY")
    
    # Create network visualization using plotly
    G = sim.network.graph
    
    # Generate layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Prepare node data
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Color based on compromise status
        if G.nodes[node].get('compromised', False):
            node_color.append('#dc2626')  # Red for compromised
        elif G.nodes[node].get('type') == 'critical':
            node_color.append('#eab308')  # Yellow for critical
        elif G.nodes[node].get('type') == 'security':
            node_color.append('#0ea5e9')  # Blue for security
        else:
            node_color.append('#6366f1')  # Purple for normal
        
        node_text.append(node)
        node_size.append(G.nodes[node].get('value', 1) * 5 + 10)
    
    # Prepare edge data
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='#475569'),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='#1e293b')
        ),
        text=node_text,
        textposition='top center',
        textfont=dict(size=8, color='#e0e7ff'),
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.5)',
        height=600,
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🔴 **Compromised**")
    with col2:
        st.markdown("🟡 **Critical Asset**")
    with col3:
        st.markdown("🔵 **Security Control**")
    with col4:
        st.markdown("🟣 **Normal Asset**")

def render_event_log(sim, team):
    """Render event log"""
    st.markdown("### 📡 LIVE EVENT STREAM")
    
    filter_team = st.selectbox("Filter by Team", ["All", "Red Team", "Blue Team", "System"])
    
    log_html = '<div class="live-terminal">'
    
    for log in sim.event_log:
        # Simple filter logic
        if filter_team == "Red Team" and "RED" not in log and "Attack" not in log:
            continue
        if filter_team == "Blue Team" and "BLUE" not in log and "Defense" not in log:
            continue
        if filter_team == "System" and "SYSTEM" not in log:
            continue
        
        log_html += f'<div style="margin: 0.3rem 0;">{log}</div>'
    
    log_html += '</div>'
    
    st.markdown(log_html, unsafe_allow_html=True)

def render_analytics(sim):
    """Render analytics dashboard"""
    st.markdown("### 📈 WARFARE ANALYTICS")
    
    # Campaign timeline
    st.markdown("#### Campaign Timeline")
    
    campaign_data = []
    for campaign_id, campaign in sim.active_campaigns.items():
        campaign_data.append({
            "Campaign": campaign_id,
            "Type": campaign.attack_type,
            "Status": campaign.status,
            "Score": campaign.score,
            "Progress": f"{campaign.current_stage}/{len(campaign.attack_sequence)}"
        })
    
    if campaign_data:
        df = pd.DataFrame(campaign_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No campaigns launched yet")
    
    # Score over time (simulated)
    st.markdown("#### Score Progression")
    
    time_points = list(range(0, 11))
    red_scores = [0] + [sim.red_team_score * (i/10) + random.randint(-10, 10) for i in range(1, 11)]
    blue_scores = [0] + [sim.blue_team_score * (i/10) + random.randint(-10, 10) for i in range(1, 11)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_points, y=red_scores, name='Red Team', line=dict(color='#dc2626', width=3)))
    fig.add_trace(go.Scatter(x=time_points, y=blue_scores, name='Blue Team', line=dict(color='#0ea5e9', width=3)))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        font_color='#e0e7ff',
        height=400,
        xaxis_title="Time",
        yaxis_title="Score"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# === MAIN APP ===

def main():
    if not st.session_state.authenticated:
        render_team_selection()
    else:
        render_warfare_dashboard()

if __name__ == "__main__":
    main()
