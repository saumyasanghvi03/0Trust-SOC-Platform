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
    page_title="Zero Trust SOC Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === STYLING ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    .soc-header {
        background: linear-gradient(135deg, #0c4a6e 0%, #0ea5e9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(14, 165, 233, 0.3);
    }
    
    .soc-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .metric-soc {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #64748b;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0ea5e9;
    }
    
    .live-terminal {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        height: 400px;
        overflow-y: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    
    .live-terminal::-webkit-scrollbar {
        width: 8px;
    }
    
    .live-terminal::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    .badge-risk-high {
        background: #dc2626;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .badge-risk-medium {
        background: #f59e0b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .badge-risk-low {
        background: #10b981;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .action-button {
        background: linear-gradient(135deg, #0c4a6e 0%, #0ea5e9 100%);
        border: none;
        color: white;
        padding: 0.7rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    
    .alert-card {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .alert-card.critical {
        border-left-color: #dc2626;
    }
    
    .alert-card:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(249, 115, 22, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# === CORE ZERO TRUST CLASSES ===

class ZeroTrustPolicyEngine:
    """Enforces dynamic access policies based on identity, device, behavior, context"""
    
    def __init__(self):
        self.policies = {
            "default_deny": True,
            "require_mfa": True,
            "max_session_age_minutes": 30,
            "device_compliance_required": True,
            "geo_fence_countries": ["US", "CA", "GB", "DE"],
            "risk_score_threshold_block": 80,
            "risk_score_threshold_mfa_stepup": 50
        }
    
    def evaluate_access_request(self, user, device, location, time, behavior_score=0):
        risk_score = 0
        
        if location not in self.policies["geo_fence_countries"]:
            risk_score += 40
        
        if not device.get("is_compliant", False):
            risk_score += 30
        
        session_age_minutes = (datetime.now() - user.get("last_auth", datetime.min)).total_seconds() / 60
        if session_age_minutes > self.policies["max_session_age_minutes"]:
            risk_score += int(session_age_minutes / 10)  # +10 per 10 mins over limit
        
        risk_score += behavior_score
        risk_score = min(100, risk_score)
        
        decision = "DENY" if risk_score >= self.policies["risk_score_threshold_block"] else \
                   "STEPUP" if risk_score >= self.policies["risk_score_threshold_mfa_stepup"] else "ALLOW"
        
        return {
            "decision": decision,
            "risk_score": risk_score,
            "reasons": self._get_risk_reasons(risk_score, location, device, user),
            "timestamp": datetime.now()
        }
    
    def _get_risk_reasons(self, score, location, device, user):
        reasons = []
        if location not in self.policies["geo_fence_countries"]:
            reasons.append("Suspicious Geo Location")
        if not device.get("is_compliant"):
            reasons.append("Non-compliant Device")
        if score > 70:
            reasons.append("Anomalous Behavior Detected")
        return reasons


class IdentityProvider:
    """Simulates IdP with MFA, SSO, Conditional Access"""
    
    def __init__(self):
        self.users = {
            "alice@company.com": {"role": "admin", "mfa_enabled": True, "last_auth": datetime.now()},
            "bob@company.com": {"role": "user", "mfa_enabled": False, "last_auth": datetime.now() - timedelta(minutes=45)},
            "charlie@company.com": {"role": "contractor", "mfa_enabled": True, "last_auth": datetime.now()},
            "diana@company.com": {"role": "finance", "mfa_enabled": True, "last_auth": datetime.now() - timedelta(minutes=15)},
            "evan@company.com": {"role": "engineer", "mfa_enabled": True, "last_auth": datetime.now()}
        }
    
    def authenticate(self, email, password, mfa_code=None):
        if email in self.users and password == "valid_password":  # Simulated auth
            user = self.users[email]
            if user["mfa_enabled"] and not mfa_code:
                return {"status": "MFA_REQUIRED", "user": email}
            user["last_auth"] = datetime.now()
            return {"status": "SUCCESS", "user": email, "session_token": hashlib.sha256(email.encode()).hexdigest()[:16]}
        return {"status": "FAILED"}


class DeviceComplianceManager:
    """Tracks endpoint compliance: disk encryption, patch level, EDR presence"""
    
    def __init__(self):
        self.devices = {
            "WS-001": {"encrypted": True, "patched": True, "edr_running": True, "owner": "alice@company.com"},
            "WS-002": {"encrypted": False, "patched": True, "edr_running": True, "owner": "bob@company.com"},
            "LAP-003": {"encrypted": True, "patched": False, "edr_running": False, "owner": "charlie@company.com"},
            "FIN-004": {"encrypted": True, "patched": True, "edr_running": True, "owner": "diana@company.com"},
            "DEV-005": {"encrypted": True, "patched": True, "edr_running": True, "owner": "evan@company.com"}
        }
    
    def is_compliant(self, device_id):
        dev = self.devices.get(device_id, {})
        return dev.get("encrypted", False) and dev.get("patched", False) and dev.get("edr_running", False)
    
    def get_device_risk(self, device_id):
        dev = self.devices.get(device_id, {})
        risk = 0
        if not dev.get("encrypted", False): risk += 30
        if not dev.get("patched", False): risk += 40
        if not dev.get("edr_running", False): risk += 30
        return min(100, risk)


class ZeroTrustNetwork:
    """Network with micro-segmentation, zones, and policy-governed communication"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.build_microsegmented_network()
    
    def build_microsegmented_network(self):
        # Define Zones
        zones = ["Public", "User", "Privileged", "Finance", "HR", "Engineering", "Critical-Infra"]
        
        # Assets per zone
        assets = {
            "Public": ["Web-Server", "API-Gateway"],
            "User": ["WS-001", "WS-002", "WS-003"],
            "Privileged": ["Admin-WS-01", "Jump-Host-01"],
            "Finance": ["Fin-App-01", "DB-Finance-01"],
            "HR": ["HR-Portal", "DB-HR-01"],
            "Engineering": ["Dev-WS-005", "CI-CD-Server"],
            "Critical-Infra": ["DC-01", "Backup-Server", "SIEM-Server"]
        }
        
        # Add nodes with zone attribute
        for zone, asset_list in assets.items():
            for asset in asset_list:
                value = 10 if "DB" in asset or "DC" in asset or "SIEM" in asset else 3
                self.graph.add_node(asset, zone=zone, compromised=False, value=value)
        
        # Define allowed flows (micro-segmentation rules)
        self.allowed_flows = [
            ("User", "Public"),
            ("Privileged", "User"),
            ("Privileged", "Finance"),
            ("Privileged", "HR"),
            ("Privileged", "Engineering"),
            ("Privileged", "Critical-Infra"),
            ("Engineering", "Public"),
            ("Finance", "Critical-Infra"),
            ("HR", "Critical-Infra"),
            ("User", "Engineering"),  # Dev tools access
        ]
        
        # Create edges ONLY if flow is allowed
        for src_zone, dst_zone in self.allowed_flows:
            for src in assets.get(src_zone, []):
                for dst in assets.get(dst_zone, []):
                    self.graph.add_edge(src, dst, policy=f"{src_zone}→{dst_zone}")
    
    def attempt_access(self, source, target, auth_context):
        """Check if access is allowed under Zero Trust policy"""
        if not self.graph.has_edge(source, target):
            return False, "POLICY_DENY: Flow not permitted by micro-segmentation"
        
        risk_score = auth_context.get("risk_score", 0)
        if risk_score > 90:
            return False, f"RISK_DENY: Critical risk ({risk_score})"
        
        return True, "ACCESS_GRANTED"


class ZeroTrustSOC:
    """Main SOC Orchestration Engine"""
    
    def __init__(self):
        self.network = ZeroTrustNetwork()
        self.idp = IdentityProvider()
        self.policy_engine = ZeroTrustPolicyEngine()
        self.device_manager = DeviceComplianceManager()
        self.event_log = deque(maxlen=500)
        self.active_alerts = deque(maxlen=100)
        self.access_requests = []
        self.risk_scores = defaultdict(int)  # per user/device
        self.current_time = datetime.now()
        
        self.log_event("Zero Trust SOC Platform Initialized", "INFO", "system")
    
    def log_event(self, message, level="INFO", category="system"):
        colors = {
            "CRITICAL": "#dc2626",
            "HIGH": "#f97316",
            "MEDIUM": "#eab308",
            "INFO": "#6366f1",
            "SUCCESS": "#10b981",
            "POLICY": "#8b5cf6",
            "ACCESS": "#06b6d4"
        }
        timestamp = self.current_time.strftime('%H:%M:%S')
        color = colors.get(level, '#94a3b8')
        log_entry = f"<span style='color: {color}'>[{timestamp}]</span> <strong>[{level}]</strong> {message}"
        self.event_log.appendleft(log_entry)
    
    def simulate_access_request(self, user_email, device_id, target_asset, location="US"):
        """Simulate user trying to access a system — core ZTNA flow"""
        
        # 1. Authenticate User
        auth_result = self.idp.authenticate(user_email, "valid_password")
        if auth_result["status"] != "SUCCESS":
            self.log_event(f"AUTH FAILED for {user_email}", "HIGH", "access")
            return False
        
        # 2. Check Device Compliance
        device_compliant = self.device_manager.is_compliant(device_id)
        device_risk = self.device_manager.get_device_risk(device_id)
        
        # 3. Evaluate Policy
        user_obj = self.idp.users[user_email]
        context = {
            "user": user_email,
            "device": {"id": device_id, "is_compliant": device_compliant},
            "location": location,
            "time": datetime.now(),
            "behavior_score": device_risk + random.randint(-10, 30)  # Simulate UEBA noise
        }
        
        policy_decision = self.policy_engine.evaluate_access_request(
            user=user_obj,
            device=context["device"],
            location=context["location"],
            time=context["time"],
            behavior_score=context["behavior_score"]
        )
        
        # 4. Enforce Network Policy
        source_asset = device_id
        access_granted, reason = self.network.attempt_access(source_asset, target_asset, policy_decision)
        
        if policy_decision["decision"] == "DENY" or not access_granted:
            full_reason = "; ".join(policy_decision["reasons"] + [reason])
            self.log_event(f"ACCESS DENIED: {user_email} → {target_asset} | Risk: {policy_decision['risk_score']} | {full_reason}", "CRITICAL", "policy")
            self.create_alert(user_email, target_asset, policy_decision, full_reason)
            return False
        else:
            self.log_event(f"ACCESS GRANTED: {user_email} → {target_asset} | Risk: {policy_decision['risk_score']}", "SUCCESS", "access")
            return True
    
    def create_alert(self, user, asset, policy_decision, reason):
        alert = {
            "id": f"ZT-{len(self.active_alerts)+1:04d}",
            "user": user,
            "target_asset": asset,
            "risk_score": policy_decision["risk_score"],
            "reasons": policy_decision["reasons"] + [reason],
            "timestamp": datetime.now(),
            "status": "OPEN",
            "auto_contained": False
        }
        self.active_alerts.appendleft(alert)
        self.risk_scores[user] += max(5, int(policy_decision["risk_score"] / 10))  # Escalate risk profile
    
    def auto_contain_threat(self, alert_id):
        """Automatically isolate device or disable account if risk > 90"""
        for alert in self.active_alerts:
            if alert["id"] == alert_id and alert["risk_score"] > 90 and not alert["auto_contained"]:
                # Simulate disabling account or quarantining device
                alert["status"] = "CONTAINED"
                alert["auto_contained"] = True
                self.log_event(f"AUTO CONTAINMENT: Account {alert['user']} disabled due to critical risk ({alert['risk_score']})", "CRITICAL", "response")
                return True
        return False

    def update_simulation(self):
        """Update internal clock and auto-process high-risk alerts"""
        self.current_time = datetime.now()
        # Auto-contain any new critical alerts
        for alert in list(self.active_alerts):
            if alert["risk_score"] > 90 and not alert["auto_contained"]:
                self.auto_contain_threat(alert["id"])

# === SESSION STATE INITIALIZATION ===

if 'soc_sim' not in st.session_state:
    st.session_state.soc_sim = ZeroTrustSOC()
    st.session_state.authenticated = True
    st.session_state.last_update = time.time()

# === MAIN DASHBOARD ===

def render_soc_dashboard():
    sim = st.session_state.soc_sim
    
    # Auto-update every 3 seconds
    now = time.time()
    if now - st.session_state.last_update > 3:
        sim.update_simulation()
        st.session_state.last_update = now
    
    # Header
    st.markdown("""
    <div class="soc-header">
        <h1>🛡️ ZERO TRUST SOC PLATFORM</h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;">Continuous Verification · Micro-Segmentation · Adaptive Access</p>
        <p>{}</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
    
    # Sidebar Metrics
    with st.sidebar:
        st.markdown("### 📊 SOC OVERVIEW")
        
        total_requests = len(sim.event_log)
        denied_requests = sum(1 for e in sim.event_log if "ACCESS DENIED" in e)
        open_alerts = len([a for a in sim.active_alerts if a["status"] == "OPEN"])
        contained_alerts = len([a for a in sim.active_alerts if a["status"] == "CONTAINED"])
        
        st.metric("Total Access Requests", total_requests)
        st.metric("Denied Requests", denied_requests)
        st.metric("Open Alerts", open_alerts)
        st.metric("Auto-Contained", contained_alerts)
        
        st.markdown("---")
        st.markdown("### ⚙️ SIMULATION CONTROL")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("🧪 Generate Test Requests", use_container_width=True):
            test_requests = [
                ("alice@company.com", "WS-001", "DB-Finance-01", "US"),
                ("bob@company.com", "WS-002", "HR-Portal", "RU"),
                ("charlie@company.com", "LAP-003", "SIEM-Server", "CN"),
                ("diana@company.com", "FIN-004", "Backup-Server", "US"),
                ("evan@company.com", "DEV-005", "CI-CD-Server", "US"),
            ]
            for req in test_requests:
                sim.simulate_access_request(*req)
            st.success("✓ 5 test requests simulated")
            time.sleep(1)
            st.rerun()
        
        st.markdown("---")
        st.caption("Zero Trust SOC Platform v1.0")

    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚦 Live Access Approvals",
        "📊 Risk Dashboard",
        "🌐 Micro-Segmentation Map",
        "🚨 Active Alerts",
        "📈 Identity & Device Analytics"
    ])
    
    with tab1:
        render_live_access_requests(sim)
    
    with tab2:
        render_risk_heatmap(sim)
    
    with tab3:
        render_microsegmentation_map(sim)
    
    with tab4:
        render_soc_alerts(sim)
    
    with tab5:
        render_identity_analytics(sim)


def render_live_access_requests(sim):
    st.markdown("### 🚦 REAL-TIME ACCESS REQUESTS")
    
    sample_requests = [
        ("alice@company.com", "WS-001", "DB-Finance-01", "US"),
        ("bob@company.com", "WS-002", "HR-Portal", "RU"),
        ("charlie@company.com", "LAP-003", "SIEM-Server", "CN"),
        ("diana@company.com", "FIN-004", "Backup-Server", "US"),
        ("evan@company.com", "DEV-005", "CI-CD-Server", "US"),
    ]
    
    for i, req in enumerate(sample_requests):
        user, device, target, loc = req
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{user}** → `{target}`")
        with col2:
            compliant = "✅" if sim.device_manager.is_compliant(device) else "⚠️"
            st.markdown(f"`{device}` {compliant}")
        with col3:
            st.markdown(f"📍 {loc}")
        
        with col4:
            if st.button("▶️ Simulate", key=f"simulate_{i}"):
                result = sim.simulate_access_request(user, device, target, loc)
                st.rerun()
                time.sleep(0.1)


def render_risk_heatmap(sim):
    st.markdown("### 🌡️ USER & DEVICE RISK HEATMAP")
    
    data = []
    for user in sim.idp.users.keys():
        device = next((d for d, info in sim.device_manager.devices.items() if info["owner"] == user), "Unknown")
        device_risk = sim.device_manager.get_device_risk(device) if device != "Unknown" else 50
        user_risk = sim.risk_scores[user]
        total_risk = min(100, int((device_risk + user_risk) / 2))
        
        data.append({
            "User": user,
            "Device": device,
            "Device Risk": device_risk,
            "Behavior Risk": user_risk,
            "Total Risk Score": total_risk
        })
    
    df = pd.DataFrame(data)
    
    if not df.empty:
        fig = px.bar(
            df, 
            x="User", 
            y="Total Risk Score", 
            color="Total Risk Score",
            color_continuous_scale=["#10b981", "#f59e0b", "#dc2626"],
            title="Identity Risk Profile (Combined Device + Behavior)",
            labels={"Total Risk Score": "Risk Score (0-100)"}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#e2e8f0',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df.style.applymap(
            lambda x: 'background-color: #10b981' if isinstance(x, int) and x < 40 else
                      'background-color: #f59e0b' if isinstance(x, int) and x < 80 else
                      'background-color: #dc2626' if isinstance(x, int) else '',
            subset=['Total Risk Score']
        ), use_container_width=True, hide_index=True)


def render_microsegmentation_map(sim):
    st.markdown("### 🌐 MICRO-SEGMENTATION NETWORK MAP")
    
    G = sim.network.graph
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    node_size = []
    node_labels = []
    
    zone_colors = {
        "Public": "#60a5fa",
        "User": "#8b5cf6",
        "Privileged": "#f97316",
        "Finance": "#ef4444",
        "HR": "#f59e0b",
        "Engineering": "#10b981",
        "Critical-Infra": "#ec4899"
    }
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        zone = G.nodes[node].get('zone', 'Unknown')
        node_color.append(zone_colors.get(zone, '#94a3b8'))
        
        node_text.append(f"{node}<br><i>{zone}</i>")
        node_labels.append(node)
        node_size.append(G.nodes[node].get('value', 3) * 8 + 10)
    
    fig = go.Figure()
    
    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='#64748b'),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='#1e293b')
        ),
        text=node_labels,
        textposition="top center",
        textfont=dict(size=9, color='#e2e8f0'),
        hovertext=node_text,
        hoverinfo="text",
        showlegend=False
    ))
    
    fig.update_layout(
        title="Micro-Segmented Network Zones",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.5)',
        height=600,
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    cols = st.columns(len(zone_colors))
    for i, (zone, color) in enumerate(zone_colors.items()):
        with cols[i]:
            st.markdown(f"<div style='text-align:center'><span style='color:{color}; font-weight:bold'>{zone}</span></div>", unsafe_allow_html=True)


def render_soc_alerts(sim):
    st.markdown("### 🚨 ACTIVE SECURITY ALERTS")
    
    if not sim.active_alerts:
        st.success("✅ No active alerts. All systems nominal.")
    else:
        open_alerts = [a for a in sim.active_alerts if a["status"] == "OPEN"]
        contained_alerts = [a for a in sim.active_alerts if a["status"] == "CONTAINED"]
        
        if open_alerts:
            st.markdown("#### 🔴 OPEN ALERTS — REQUIRES ACTION")
            for alert in open_alerts:
                with st.expander(f"**{alert['id']}** — {alert['user']} → {alert['target_asset']}"):
                    st.markdown(f"**Risk Score:** {alert['risk_score']}/100")
                    st.markdown("**Reasons:**")
                    for reason in alert["reasons"]:
                        st.markdown(f"- {reason}")
                    st.markdown(f"**Timestamp:** {alert['timestamp'].strftime('%H:%M:%S')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Investigate", key=f"investigate_{alert['id']}"):
                            # Simulate investigation
                            sim.log_event(f"ALERT INVESTIGATED: {alert['id']} by SOC Analyst", "INFO", "response")
                            st.success("Investigation logged.")
                            st.rerun()
                    with col2:
                        if st.button("🛡️ Contain Now", key=f"contain_{alert['id']}"):
                            if sim.auto_contain_threat(alert['id']):
                                st.success("✅ Threat contained automatically.")
                            else:
                                st.error("Containment failed — manual intervention required.")
                            st.rerun()
        
        if contained_alerts:
            st.markdown("#### 🟢 CONTAINED — NO FURTHER ACTION")
            for alert in contained_alerts[:5]:  # Show last 5
                st.markdown(f"""
                <div class="alert-card">
                    <strong>{alert['id']}</strong>: {alert['user']} → {alert['target_asset']}<br>
                    <small>Risk: {alert['risk_score']} | {alert['timestamp'].strftime('%H:%M')}</small>
                    <span class="badge-risk-high">CONTAINED</span>
                </div>
                """, unsafe_allow_html=True)


def render_identity_analytics(sim):
    st.markdown("### 📈 IDENTITY & DEVICE COMPLIANCE ANALYTICS")
    
    # Device Compliance Chart
    device_data = []
    for device_id, info in sim.device_manager.devices.items():
        compliant = sim.device_manager.is_compliant(device_id)
        risk = sim.device_manager.get_device_risk(device_id)
        device_data.append({
            "Device": device_id,
            "Owner": info["owner"],
            "Compliant": "Yes" if compliant else "No",
            "Risk Score": risk
        })
    
    df_devices = pd.DataFrame(device_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Device Compliance Status")
        fig1 = px.pie(df_devices, names="Compliant", title="Endpoint Compliance Rate", color_discrete_sequence=["#10b981", "#f97316"])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Device Risk Distribution")
        fig2 = px.histogram(df_devices, x="Risk Score", nbins=5, title="Device Risk Scores", color_discrete_sequence=["#8b5cf6"])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0')
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("#### Detailed Device Registry")
    st.dataframe(df_devices.style.applymap(
        lambda x: 'background-color: #10b981' if x == "Yes" else 'background-color: #f97316' if x == "No" else '',
        subset=['Compliant']
    ).applymap(
        lambda x: 'color: #10b981' if x < 40 else 'color: #f59e0b' if x < 80 else 'color: #dc2626',
        subset=['Risk Score']
    ), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Event Log
    st.markdown("### 📡 LIVE EVENT STREAM")
    filter_level = st.selectbox("Filter Events By Severity", ["All", "CRITICAL", "HIGH", "MEDIUM", "SUCCESS", "INFO"])
    
    log_html = '<div class="live-terminal">'
    for log in sim.event_log:
        if filter_level != "All" and f"[{filter_level}]" not in log:
            continue
        log_html += f'<div style="margin: 0.2rem 0; line-height: 1.3;">{log}</div>'
    log_html += '</div>'
    
    st.markdown(log_html, unsafe_allow_html=True)


# === MAIN APP ===

def main():
    render_soc_dashboard()

if __name__ == "__main__":
    main()
