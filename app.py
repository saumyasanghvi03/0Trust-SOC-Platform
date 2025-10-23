# CODEBASE 2: Nexus IT Operations
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import random
import time
from collections import deque
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Nexus IT Operations", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');
    .stApp {background-color: #0d1117; color: #c9d1d9; font-family: 'Roboto Mono', monospace;}
    .nexus-header {font-size: 2.5rem; color: #58a6ff; text-align: center; margin-bottom: 1.5rem;}
    .metric-card {background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; transition: all 0.2s ease-in-out;}
    .metric-card:hover {border-color: #58a6ff;}
    .metric-value {font-size: 2.5rem; font-weight: bold; color: #f0f6fc;}
    .metric-label {font-size: 0.8rem; color: #8b949e; text-transform: uppercase;}
    .status-badge {padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: bold;}
    .status-ok {background-color: #238636; color: white;}
    .status-degraded {background-color: #d29922; color: black;}
    .status-outage {background-color: #da3633; color: white;}
    .incident-card {background: #161b22; border-left: 4px solid; border-radius: 5px; padding: 15px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

class NexusPlatform:
    def __init__(self):
        self.ops_team = {
            "lead_ops": {"name": "Maria Garcia", "role": "Lead Ops Engineer", "pass": self.hash("nexus123")},
            "sec_eng": {"name": "Kenji Tanaka", "role": "Security Engineer", "pass": self.hash("nexus123")}
        }
        self.services = {
            "Auth API": {"status": "Operational", "latency": random.randint(50, 150)},
            "Billing Service": {"status": "Operational", "latency": random.randint(80, 200)},
            "Customer DB": {"status": "Operational", "load": random.randint(20, 60)},
        }
        self.initialize_session_data()

    def initialize_session_data(self):
        st.session_state.incidents = {}
        st.session_state.network_nodes = []
        st.session_state.last_update = time.time()
        self.generate_nodes()
        self.generate_incidents()
        
    def hash(self, password):
        return hashlib.sha256(f"nexus_ops_{password}".encode()).hexdigest()

    def generate_nodes(self):
        nodes = []
        # Core routers
        nodes.append({"id": "core-rtr-1", "group": "network", "label": "Core Router 1", "size": 20})
        nodes.append({"id": "core-rtr-2", "group": "network", "label": "Core Router 2", "size": 20})
        # App Servers
        for i in range(3): nodes.append({"id": f"web-app-{i}", "group": "apps", "label": f"Web App {i}", "size": 15})
        # DB Servers
        for i in range(2): nodes.append({"id": f"db-prod-{i}", "group": "databases", "label": f"DB {i}", "size": 18})
        # Workstations
        for i in range(5): nodes.append({"id": f"ws-eng-{i}", "group": "users", "label": f"ENG WS {i}", "size": 10})
        st.session_state.network_nodes = nodes

    def generate_incidents(self):
        types = ["High DB Load", "API Latency Spike", "Compliance Flag: GDPR Data Access", "Cloud Security: S3 Bucket Misconfiguration"]
        for i in range(5):
            inc_id = f"TICKET-{datetime.now():%m%d}-{random.randint(100,999)}"
            st.session_state.incidents[inc_id] = {
                "id": inc_id,
                "title": random.choice(types),
                "severity": random.choice(["High", "Medium"]),
                "status": "New", # New, Investigating, Resolved
                "timestamp": datetime.now() - timedelta(minutes=random.randint(5, 120)),
                "assigned_to": "Unassigned"
            }

    def update_simulation(self):
        if time.time() - st.session_state.last_update > 5:
            # Randomly degrade a service
            if random.random() < 0.2:
                svc_name = random.choice(list(self.services.keys()))
                self.services[svc_name]["status"] = "Degraded"
                self.services[svc_name]["latency"] *= 2
                inc_id = f"TICKET-{datetime.now():%m%d}-{random.randint(100,999)}"
                st.session_state.incidents[inc_id] = {
                    "id": inc_id, "title": f"Service Degraded: {svc_name}", "severity": "High",
                    "status": "New", "timestamp": datetime.now(), "assigned_to": "Unassigned"
                }
            st.session_state.last_update = time.time()

def login_screen(platform):
    st.markdown('<div class="nexus-header">🌐 Nexus IT Operations</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.form("login_form"):
            st.markdown("<h3 style='text-align:center;'>Operator Login</h3>", unsafe_allow_html=True)
            username = st.selectbox("Operator ID", options=platform.ops_team.keys())
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Access Platform", use_container_width=True):
                if platform.hash(password) == platform.ops_team[username]["pass"]:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    platform.initialize_session_data()
                    st.rerun()
                else:
                    st.error("Access Denied.")

def dashboard(platform):
    user_info = platform.ops_team[st.session_state.user]
    st.markdown('<div class="nexus-header">🌐 Nexus IT Operations</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"### {user_info['name']}")
        st.caption(user_info['role'])
        st.markdown("---")
        module = st.radio("Navigation", ["Dashboard", "Service Health", "Incident Tickets", "Network Topology"])
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if module == "Dashboard":
        render_main_dashboard(platform)
    elif module == "Service Health":
        render_service_health(platform)
    elif module == "Incident Tickets":
        render_incident_tickets(platform)
    elif module == "Network Topology":
        render_network_topology()

def render_main_dashboard(platform):
    # Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        ok_services = len([s for s in platform.services.values() if s['status'] == 'Operational'])
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{ok_services}/{len(platform.services)}</div><div class='metric-label'>Services Operational</div></div>", unsafe_allow_html=True)
    with c2:
        new_incidents = len([i for i in st.session_state.incidents.values() if i['status'] == 'New'])
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#da3633;'>{new_incidents}</div><div class='metric-label'>New Incidents</div></div>", unsafe_allow_html=True)
    with c3:
        avg_latency = np.mean([s['latency'] for s in platform.services.values()])
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{avg_latency:.0f}ms</div><div class='metric-label'>Average API Latency</div></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### High Priority Incidents")
    high_prio = [i for i in st.session_state.incidents.values() if i['severity'] in ['Critical', 'High'] and i['status'] == 'New']
    if not high_prio:
        st.success("No high priority incidents at this time.")
    for inc in high_prio[:5]:
        color = "#da3633" if inc['severity'] == "Critical" else "#d29922"
        st.markdown(f"<div class='incident-card' style='border-left-color:{color};'><strong>{inc['title']}</strong><br><small>Opened: {inc['timestamp']:%H:%M:%S} | Status: {inc['status']}</small></div>", unsafe_allow_html=True)

def render_service_health(platform):
    st.header("Core Service Status")
    for name, data in platform.services.items():
        status_class = "status-ok" if data['status'] == 'Operational' else "status-degraded" if data['status'] == 'Degraded' else "status-outage"
        st.markdown(f"<div class='metric-card' style='margin-bottom:1rem;'><h4>{name} <span class='status-badge {status_class}'>{data['status']}</span></h4>"
                    f"Latency: {data.get('latency', 'N/A')}ms | DB Load: {data.get('load', 'N/A')}%</div>", unsafe_allow_html=True)

def render_incident_tickets(platform):
    st.header("Incident Ticket Queue")
    for id, inc in st.session_state.incidents.items():
        if inc['status'] == 'Resolved': continue
        color = "#d29922" if inc['severity'] == "Medium" else "#da3633"
        with st.expander(f"[{inc['status']}] {inc['id']} - {inc['title']}"):
            st.markdown(f"Severity: <strong style='color:{color};'>{inc['severity']}</strong> | Assigned to: {inc['assigned_to']}", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            if inc['status'] == 'New':
                if c1.button("Acknowledge & Assign to Me", key=f"ack_{id}", use_container_width=True):
                    st.session_state.incidents[id]['status'] = 'Investigating'
                    st.session_state.incidents[id]['assigned_to'] = st.session_state.platform.ops_team[st.session_state.user]['name']
                    st.rerun()
            if inc['status'] == 'Investigating':
                if c1.button("Escalate to Engineering", key=f"esc_{id}", use_container_width=True): st.info("Ticket escalated.")
                if c2.button("Resolve Ticket", key=f"res_{id}", use_container_width=True):
                    st.session_state.incidents[id]['status'] = 'Resolved'
                    st.rerun()

def render_network_topology():
    st.header("Internal Network Topology")
    nodes = st.session_state.network_nodes
    if not nodes:
        st.warning("Network node data not available.")
        return

    # Create positions for nodes
    pos = {node['id']: (random.uniform(0, 1), random.uniform(0, 1)) for node in nodes}
    
    # Create Edges
    edges = [('core-rtr-1', 'core-rtr-2')]
    for node in nodes:
        if 'web-app' in node['id']: edges.append(('core-rtr-1', node['id']))
        if 'db-prod' in node['id']: edges.append(('core-rtr-2', node['id']))
        if 'ws-eng' in node['id']: edges.append(('core-rtr-1', node['id']))

    edge_x, edge_y = [], []
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = [pos[node['id']][0] for node in nodes]
    node_y = [pos[node['id']][1] for node in nodes]
    
    group_colors = {"network": "#58a6ff", "apps": "#1f6feb", "databases": "#8957e5", "users": "#238636"}
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#30363d')))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=[n['label'] for n in nodes],
                             textposition="bottom center",
                             marker=dict(size=[n['size'] for n in nodes], 
                                         color=[group_colors[n['group']] for n in nodes]),
                             hoverinfo='text'))
    
    fig.update_layout(showlegend=False, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      paper_bgcolor="#0d1117", plot_bgcolor="#0d1117", margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

def main():
    if 'platform' not in st.session_state:
        st.session_state.platform = NexusPlatform()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        st.session_state.platform.update_simulation()
        dashboard(st.session_state.platform)
        time.sleep(5)
        st.rerun()
    else:
        login_screen(st.session_state.platform)

if __name__ == "__main__":
    main()
