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

st.set_page_config(
    page_title="Aegis Enterprise IT Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Enterprise Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: #e0e7ff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .enterprise-header {
        background: linear-gradient(135deg, #3730a3 0%, #4f46e5 50%, #6366f1 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3);
    }
    
    .enterprise-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
    }
    
    .status-panel {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    
    .metric-enterprise {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .metric-enterprise:hover {
        border-left-color: #818cf8;
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    .metric-value-enterprise {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .live-feed {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        height: 500px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
    }
    
    .live-feed::-webkit-scrollbar {
        width: 8px;
    }
    
    .live-feed::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    .badge-enterprise {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .badge-critical { background: #7f1d1d; color: #fca5a5; }
    .badge-high { background: #7c2d12; color: #fdba74; }
    .badge-medium { background: #713f12; color: #fde047; }
    .badge-low { background: #14532d; color: #86efac; }
    .badge-operational { background: #1e3a8a; color: #93c5fd; }
    
    .infrastructure-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .infrastructure-card:hover {
        border-color: #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

class EnterpriseITPlatform:
    """Enterprise IT Infrastructure Management Platform"""
    
    def __init__(self):
        self.company = "Global Tech Enterprises"
        self.init_enterprise_data()
    
    def init_enterprise_data(self):
        """Initialize enterprise infrastructure"""
        
        # IT Leadership
        self.it_leadership = {
            "cto": {
                "username": "cto",
                "password": self.hash("Enterprise@2024"),
                "name": "Dr. Marcus Chen",
                "title": "Chief Technology Officer",
                "department": "Executive Leadership"
            },
            "it_director": {
                "username": "it_director",
                "password": self.hash("Enterprise@2024"),
                "name": "Jennifer Walsh",
                "title": "IT Infrastructure Director",
                "department": "IT Operations"
            },
            "security_officer": {
                "username": "security_officer",
                "password": self.hash("Enterprise@2024"),
                "name": "David Kumar",
                "title": "Chief Security Officer",
                "department": "InfoSec"
            }
        }
        
        # Global Infrastructure
        self.data_centers = {
            "DC-US-EAST": {"location": "Virginia, USA", "capacity": "15000 servers", "uptime": 99.99},
            "DC-US-WEST": {"location": "Oregon, USA", "capacity": "12000 servers", "uptime": 99.98},
            "DC-EU-CENTRAL": {"location": "Frankfurt, Germany", "capacity": "10000 servers", "uptime": 99.97},
            "DC-ASIA-PAC": {"location": "Singapore", "capacity": "8000 servers", "uptime": 99.96}
        }
        
        # Business Applications
        self.business_apps = []
        self.generate_business_apps()
        
        # Network Infrastructure
        self.network_devices = []
        self.generate_network_devices()
        
        # Data Pipeline
        self.data_pipelines = []
        self.generate_data_pipelines()
        
        # Real-time Metrics
        self.metrics_stream = deque(maxlen=500)
        self.generate_metrics()
        
        # Incidents
        self.incidents = {}
        
        # Audit Log
        self.audit_log = deque(maxlen=1000)
        self.log_audit("System initialized", "SYSTEM")
    
    def hash(self, password):
        return hashlib.sha256(f"enterprise_{password}".encode()).hexdigest()
    
    def log_audit(self, message, level="INFO"):
        colors = {
            "CRITICAL": "#ef4444",
            "HIGH": "#f97316",
            "MEDIUM": "#eab308",
            "INFO": "#6366f1",
            "SUCCESS": "#22c55e"
        }
        
        log_entry = f"<span style='color: {colors.get(level, '#94a3b8')}'>[{datetime.now():%H:%M:%S}]</span> <strong>[{level}]</strong> {message}"
        self.audit_log.appendleft(log_entry)
    
    def generate_business_apps(self):
        """Generate business application inventory"""
        apps = [
            {"name": "SAP ERP", "category": "ERP", "criticality": "Critical", "users": 5400},
            {"name": "Salesforce CRM", "category": "CRM", "criticality": "High", "users": 3200},
            {"name": "Microsoft 365", "category": "Productivity", "criticality": "Critical", "users": 12500},
            {"name": "Workday HCM", "category": "HR", "criticality": "High", "users": 1800},
            {"name": "Tableau Analytics", "category": "BI", "criticality": "Medium", "users": 850},
            {"name": "Jira Software", "category": "DevOps", "criticality": "High", "users": 2100},
            {"name": "ServiceNow ITSM", "category": "ITSM", "criticality": "Critical", "users": 600},
            {"name": "Confluence", "category": "Collaboration", "criticality": "Medium", "users": 4500}
        ]
        
        for app in apps:
            app.update({
                "status": random.choice(["Operational", "Operational", "Operational", "Degraded"]),
                "response_time_ms": random.randint(50, 500),
                "error_rate": round(random.uniform(0, 2.5), 2),
                "availability": round(random.uniform(99.5, 99.99), 2),
                "last_deployment": datetime.now() - timedelta(days=random.randint(1, 90))
            })
            self.business_apps.append(app)
    
    def generate_network_devices(self):
        """Generate network infrastructure"""
        device_types = [
            {"type": "Core Router", "count": 12},
            {"type": "Distribution Switch", "count": 48},
            {"type": "Access Switch", "count": 320},
            {"type": "Firewall", "count": 24},
            {"type": "Load Balancer", "count": 16},
            {"type": "VPN Gateway", "count": 8}
        ]
        
        for device_type in device_types:
            for i in range(device_type["count"]):
                device = {
                    "device_id": f"{device_type['type'].replace(' ', '-').upper()}-{i+1:03d}",
                    "type": device_type['type'],
                    "location": random.choice(list(self.data_centers.keys())),
                    "status": random.choice(["Online", "Online", "Online", "Warning"]),
                    "cpu_usage": random.randint(10, 85),
                    "memory_usage": random.randint(30, 90),
                    "uptime_days": random.randint(1, 365),
                    "throughput_gbps": round(random.uniform(0.5, 10), 2)
                }
                self.network_devices.append(device)
    
    def generate_data_pipelines(self):
        """Generate data pipeline monitoring"""
        pipelines = [
            {"name": "Customer Data ETL", "source": "PostgreSQL", "destination": "Snowflake"},
            {"name": "Sales Analytics", "source": "Salesforce API", "destination": "BigQuery"},
            {"name": "Log Aggregation", "source": "CloudWatch", "destination": "Elasticsearch"},
            {"name": "Real-time Events", "source": "Kafka", "destination": "Redshift"},
            {"name": "Backup Sync", "source": "Production DB", "destination": "S3 Glacier"}
        ]
        
        for pipeline in pipelines:
            pipeline.update({
                "status": random.choice(["Running", "Running", "Running", "Failed"]),
                "records_processed": random.randint(10000, 5000000),
                "last_run": datetime.now() - timedelta(hours=random.randint(1, 24)),
                "avg_duration_min": random.randint(5, 120),
                "success_rate": round(random.uniform(95, 100), 1)
            })
            self.data_pipelines.append(pipeline)
    
    def generate_metrics(self):
        """Generate real-time system metrics"""
        for _ in range(100):
            metric = {
                "timestamp": datetime.now() - timedelta(seconds=random.randint(0, 300)),
                "cpu_cluster": round(random.uniform(30, 75), 1),
                "memory_cluster": round(random.uniform(45, 85), 1),
                "network_throughput_gbps": round(random.uniform(5, 25), 2),
                "active_sessions": random.randint(8000, 15000),
                "api_requests_per_sec": random.randint(500, 3000)
            }
            self.metrics_stream.append(metric)
    
    def create_incident(self):
        """Create a new IT incident"""
        incident_types = [
            "Service Degradation",
            "Database Performance Issue",
            "Network Connectivity Problem",
            "Application Error Spike",
            "Storage Capacity Alert",
            "Security Vulnerability Detected"
        ]
        
        incident_id = f"INC-{random.randint(10000, 99999)}"
        
        incident = {
            "id": incident_id,
            "title": random.choice(incident_types),
            "severity": random.choice(["Critical", "High", "Medium"]),
            "status": "Open",
            "created": datetime.now(),
            "affected_service": random.choice([app["name"] for app in self.business_apps]),
            "impact": f"{random.randint(100, 5000)} users affected",
            "assigned_to": "Incident Response Team",
            "timeline": [f"{datetime.now():%H:%M:%S} - Incident detected and logged"]
        }
        
        self.incidents[incident_id] = incident
        self.log_audit(f"New incident created: {incident_id} - {incident['title']}", "CRITICAL")
        
        return incident_id
    
    def calculate_health_score(self):
        """Calculate overall IT infrastructure health"""
        
        # Application health
        operational_apps = len([app for app in self.business_apps if app["status"] == "Operational"])
        app_health = (operational_apps / len(self.business_apps)) * 30
        
        # Network health
        online_devices = len([dev for dev in self.network_devices if dev["status"] == "Online"])
        network_health = (online_devices / len(self.network_devices)) * 25
        
        # Pipeline health
        running_pipelines = len([p for p in self.data_pipelines if p["status"] == "Running"])
        pipeline_health = (running_pipelines / len(self.data_pipelines)) * 20
        
        # Incident penalty
        open_incidents = len([inc for inc in self.incidents.values() if inc["status"] == "Open"])
        incident_penalty = open_incidents * 5
        
        # Data center uptime
        avg_uptime = sum(dc["uptime"] for dc in self.data_centers.values()) / len(self.data_centers)
        dc_health = (avg_uptime / 100) * 25
        
        total_health = app_health + network_health + pipeline_health + dc_health - incident_penalty
        total_health = max(0, min(100, total_health))
        
        return round(total_health, 1)

# Initialize Platform
if 'enterprise_platform' not in st.session_state:
    st.session_state.enterprise_platform = EnterpriseITPlatform()
    st.session_state.enterprise_auth = False
    st.session_state.enterprise_user = None

def render_enterprise_login():
    """Enterprise Login Portal"""
    platform = st.session_state.enterprise_platform
    
    st.markdown(f"""
    <div class="enterprise-header">
        <h1>🛡️ {platform.company}</h1>
        <p style="font-size: 1.5rem; margin: 0.5rem 0;">Enterprise IT Command Center</p>
        <p style="opacity: 0.8;">Infrastructure Management & Security Operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔐 Executive Access Portal</h2>", unsafe_allow_html=True)
        
        with st.form("enterprise_login"):
            username = st.text_input("👤 Username", placeholder="Enter your corporate username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("🚀 Access Command Center", use_container_width=True)
            
            if submit:
                if username in platform.it_leadership and platform.hash(password) == platform.it_leadership[username]["password"]:
                    st.session_state.enterprise_auth = True
                    st.session_state.enterprise_user = username
                    platform.log_audit(f"Login successful: {platform.it_leadership[username]['name']}", "INFO")
                    st.success("✓ Authentication Successful")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("✗ Authentication Failed")
        
        st.markdown("---")
        st.markdown("### 👥 Executive Access Credentials")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **CTO**  
            Username: `cto`  
            Password: `Enterprise@2024`
            """)
        
        with col2:
            st.markdown("""
            **IT Director**  
            Username: `it_director`  
            Password: `Enterprise@2024`
            """)
        
        with col3:
            st.markdown("""
            **Security Officer**  
            Username: `security_officer`  
            Password: `Enterprise@2024`
            """)

def render_enterprise_dashboard():
    """Enterprise Command Center Dashboard"""
    platform = st.session_state.enterprise_platform
    user = platform.it_leadership[st.session_state.enterprise_user]
    
    # Header
    st.markdown(f"""
    <div class="enterprise-header">
        <h1>🛡️ {platform.company} - IT Command Center</h1>
        <p style="margin: 0.5rem 0;">Welcome, {user['name']} | {user['title']}</p>
        <p style="opacity: 0.8;">{datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {user['name']}")
        st.caption(user['title'])
        st.caption(user['department'])
        
        st.markdown("---")
        
        module = st.radio("🎛️ Command Modules", [
            "🏠 Executive Dashboard",
            "💼 Business Applications",
            "🌐 Network Infrastructure",
            "📊 Data Operations",
            "🚨 Incident Management",
            "🏢 Data Centers",
            "📈 Real-time Analytics"
        ])
        
        st.markdown("---")
        
        if st.button("🔥 SIMULATE INCIDENT", use_container_width=True):
            inc_id = platform.create_incident()
            st.warning(f"Incident {inc_id} created!")
            st.rerun()
        
        if st.button("🔄 Refresh", use_container_width=True):
            platform.generate_metrics()
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.enterprise_auth = False
            st.rerun()
    
    # Route modules
    if "Executive Dashboard" in module:
        render_executive_dashboard(platform)
    elif "Business Applications" in module:
        render_business_apps(platform)
    elif "Network Infrastructure" in module:
        render_network_infra(platform)
    elif "Data Operations" in module:
        render_data_ops(platform)
    elif "Incident Management" in module:
        render_incident_mgmt(platform)
    elif "Data Centers" in module:
        render_data_centers(platform)
    elif "Real-time Analytics" in module:
        render_realtime_analytics(platform)

def render_executive_dashboard(platform):
    """Executive Overview Dashboard"""
    
    # Health Score
    health_score = platform.calculate_health_score()
    
    if health_score >= 95:
        health_status = "EXCELLENT"
        health_color = "#22c55e"
    elif health_score >= 85:
        health_status = "GOOD"
        health_color = "#6366f1"
    elif health_score >= 70:
        health_status = "FAIR"
        health_color = "#eab308"
    else:
        health_status = "CRITICAL"
        health_color = "#ef4444"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 3rem; border-radius: 12px; text-align: center; border: 3px solid {health_color}; margin-bottom: 2rem;">
        <h2 style="margin: 0; color: {health_color}; font-size: 2rem;">INFRASTRUCTURE HEALTH: {health_status}</h2>
        <h1 style="margin: 1rem 0; font-size: 5rem; color: {health_color};">{health_score}%</h1>
        <p style="opacity: 0.8;">Global IT Infrastructure Status</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_apps = len(platform.business_apps)
        operational = len([app for app in platform.business_apps if app["status"] == "Operational"])
        st.markdown(f"""
        <div class="metric-enterprise">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">BUSINESS APPLICATIONS</div>
            <div class="metric-value-enterprise">{operational}/{total_apps}</div>
            <div style="font-size: 0.85rem; color: #64748b;">Operational</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_devices = len(platform.network_devices)
        online = len([dev for dev in platform.network_devices if dev["status"] == "Online"])
        st.markdown(f"""
        <div class="metric-enterprise">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">NETWORK DEVICES</div>
            <div class="metric-value-enterprise">{online}/{total_devices}</div>
            <div style="font-size: 0.85rem; color: #64748b;">Online</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        open_incidents = len([inc for inc in platform.incidents.values() if inc["status"] == "Open"])
        st.markdown(f"""
        <div class="metric-enterprise">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">ACTIVE INCIDENTS</div>
            <div class="metric-value-enterprise" style="background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{open_incidents}</div>
            <div style="font-size: 0.85rem; color: #64748b;">Requiring Attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_dc_uptime = sum(dc["uptime"] for dc in platform.data_centers.values()) / len(platform.data_centers)
        st.markdown(f"""
        <div class="metric-enterprise">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">DATA CENTER UPTIME</div>
            <div class="metric-value-enterprise">{avg_dc_uptime:.2f}%</div>
            <div style="font-size: 0.85rem; color: #64748b;">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts and Live Feed
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Infrastructure Performance")
        
        # Time series data
        metrics_df = pd.DataFrame(list(platform.metrics_stream))
        metrics_df = metrics_df.sort_values('timestamp')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=metrics_df['timestamp'],
            y=metrics_df['cpu_cluster'],
            name='CPU Usage %',
            line=dict(color='#6366f1', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=metrics_df['timestamp'],
            y=metrics_df['memory_cluster'],
            name='Memory Usage %',
            line=dict(color='#8b5cf6', width=2)
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font_color='#e0e7ff',
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📡 Live Audit Log")
        
        log_html = '<div class="live-feed">'
        for log in list(platform.audit_log)[:25]:
            log_html += f'<div style="margin: 0.3rem 0; font-size: 0.85rem;">{log}</div>'
        log_html += '</div>'
        
        st.markdown(log_html, unsafe_allow_html=True)

def render_business_apps(platform):
    """Business Applications Dashboard"""
    st.markdown("### 💼 Business-Critical Applications")
    
    for app in platform.business_apps:
        criticality_badge = f"badge-{app['criticality'].lower()}"
        status_badge = "badge-operational" if app["status"] == "Operational" else "badge-critical"
        
        with st.expander(f"**{app['name']}** ({app['category']}) - {app['users']} Users"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Status:** <span class='badge-enterprise {status_badge}'>{app['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Criticality:** <span class='badge-enterprise {criticality_badge}'>{app['criticality']}</span>", unsafe_allow_html=True)
                st.write(f"**Active Users:** {app['users']}")
            
            with col2:
                st.write(f"**Response Time:** {app['response_time_ms']} ms")
                st.write(f"**Error Rate:** {app['error_rate']}%")
                st.write(f"**Availability:** {app['availability']}%")
            
            with col3:
                st.write(f"**Last Deployment:** {app['last_deployment'].strftime('%Y-%m-%d')}")
                if st.button(f"📊 View Metrics", key=f"metrics_{app['name']}"):
                    st.info("Detailed metrics loading...")

def render_network_infra(platform):
    """Network Infrastructure Dashboard"""
    st.markdown("### 🌐 Global Network Infrastructure")
    
    # Filter
    filter_type = st.selectbox("Device Type", ["All"] + list(set(dev["type"] for dev in platform.network_devices)))
    
    devices = platform.network_devices
    if filter_type != "All":
        devices = [dev for dev in devices if dev["type"] == filter_type]
    
    st.markdown(f"**Showing {len(devices)} devices**")
    
    # Device grid
    for device in devices[:20]:
        status_badge = "badge-operational" if device["status"] == "Online" else "badge-high"
        
        st.markdown(f"""
        <div class="infrastructure-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{device['device_id']}</strong><br>
                    <span style="color: #94a3b8;">{device['type']} | {device['location']}</span>
                </div>
                <div>
                    <span class='badge-enterprise {status_badge}'>{device['status']}</span>
                </div>
            </div>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">CPU</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">{device['cpu_usage']}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Memory</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">{device['memory_usage']}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Uptime</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">{device['uptime_days']}d</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Throughput</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">{device['throughput_gbps']} Gbps</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_data_ops(platform):
    """Data Operations Dashboard"""
    st.markdown("### 📊 Data Pipeline Operations")
    
    for pipeline in platform.data_pipelines:
        status_badge = "badge-operational" if pipeline["status"] == "Running" else "badge-critical"
        
        with st.expander(f"**{pipeline['name']}** - {pipeline['source']} → {pipeline['destination']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Status:** <span class='badge-enterprise {status_badge}'>{pipeline['status']}</span>", unsafe_allow_html=True)
                st.write(f"**Records Processed:** {pipeline['records_processed']:,}")
                st.write(f"**Success Rate:** {pipeline['success_rate']}%")
            
            with col2:
                st.write(f"**Last Run:** {pipeline['last_run'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Avg Duration:** {pipeline['avg_duration_min']} minutes")
                if st.button(f"▶️ Trigger Run", key=f"run_{pipeline['name']}"):
                    st.success("Pipeline execution started")

def render_incident_mgmt(platform):
    """Incident Management Dashboard"""
    st.markdown("### 🚨 IT Incident Management")
    
    if not platform.incidents:
        st.success("✓ No active incidents - All systems operational")
        return
    
    for inc_id, incident in platform.incidents.items():
        severity_badge = f"badge-{incident['severity'].lower()}"
        
        with st.expander(f"**{inc_id}** - {incident['title']} [{incident['severity']}]"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Severity:** <span class='badge-enterprise {severity_badge}'>{incident['severity']}</span>", unsafe_allow_html=True)
                st.write(f"**Status:** {incident['status']}")
                st.write(f"**Affected Service:** {incident['affected_service']}")
                st.write(f"**Impact:** {incident['impact']}")
                st.write(f"**Created:** {incident['created'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col2:
                if incident['status'] == 'Open':
                    if st.button("🔍 Investigate", key=f"inv_{inc_id}"):
                        platform.incidents[inc_id]['status'] = 'Investigating'
                        platform.log_audit(f"Investigation started: {inc_id}", "INFO")
                        st.rerun()
                elif incident['status'] == 'Investigating':
                    if st.button("✓ Resolve", key=f"res_{inc_id}"):
                        platform.incidents[inc_id]['status'] = 'Resolved'
                        platform.log_audit(f"Incident resolved: {inc_id}", "SUCCESS")
                        st.rerun()

def render_data_centers(platform):
    """Data Centers Dashboard"""
    st.markdown("### 🏢 Global Data Center Operations")
    
    for dc_id, dc in platform.data_centers.items():
        uptime_color = "#22c55e" if dc["uptime"] >= 99.95 else "#eab308"
        
        st.markdown(f"""
        <div class="infrastructure-card">
            <h3 style="margin: 0; color: #818cf8;">{dc_id}</h3>
            <p style="color: #94a3b8; margin: 0.5rem 0;">{dc['location']}</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">Capacity</div>
                    <div style="font-size: 1.5rem; font-weight: 600;">{dc['capacity']}</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">Uptime</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {uptime_color};">{dc['uptime']}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">Status</div>
                    <div><span class='badge-enterprise badge-operational'>OPERATIONAL</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_realtime_analytics(platform):
    """Real-time Analytics Dashboard"""
    st.markdown("### 📈 Real-time System Analytics")
    
    # Generate fresh metrics
    platform.generate_metrics()
    
    metrics_df = pd.DataFrame(list(platform.metrics_stream))
    metrics_df = metrics_df.sort_values('timestamp')
    
    # Multiple charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### System Resource Utilization")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=metrics_df['timestamp'], y=metrics_df['cpu_cluster'], name='CPU %', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=metrics_df['timestamp'], y=metrics_df['memory_cluster'], name='Memory %', fill='tozeroy'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.8)', font_color='#e0e7ff', height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Active Sessions & API Traffic")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=metrics_df['timestamp'], y=metrics_df['active_sessions'], name='Sessions'))
        fig.add_trace(go.Scatter(x=metrics_df['timestamp'], y=metrics_df['api_requests_per_sec'], name='API Req/s'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.8)', font_color='#e0e7ff', height=300)
        st.plotly_chart(fig, use_container_width=True)

def main():
    if not st.session_state.enterprise_auth:
        render_enterprise_login()
    else:
        render_enterprise_dashboard()

if __name__ == "__main__":
    main()
