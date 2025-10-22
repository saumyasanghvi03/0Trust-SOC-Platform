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
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Enterprise IAM Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .alert-high {
        background-color: #ffe6cc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ff6600;
    }
    .alert-medium {
        background-color: #ffffcc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffcc00;
    }
    .ticket-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .app-card {
        border: 1px solid #1f77b4;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #e6f3ff;
    }
    .success-flash {
        background-color: #90EE90;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class EnterpriseIAMPlatform:
    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.last_update = datetime.now()
        self.initialize_enterprise_data()
    
    def initialize_enterprise_data(self):
        """Initialize comprehensive enterprise IAM data"""
        # Available applications
        self.applications = {
            "salesforce": {
                "name": "Salesforce CRM",
                "category": "CRM",
                "description": "Customer relationship management platform",
                "risk_level": "medium",
                "requires_approval": False
            },
            "workday": {
                "name": "Workday HR",
                "category": "HR",
                "description": "Human resources management system",
                "risk_level": "high",
                "requires_approval": True
            },
            "sap": {
                "name": "SAP ERP",
                "category": "ERP",
                "description": "Enterprise resource planning",
                "risk_level": "high",
                "requires_approval": True
            },
            "servicenow": {
                "name": "ServiceNow",
                "category": "ITSM",
                "description": "IT service management",
                "risk_level": "medium",
                "requires_approval": False
            },
            "slack": {
                "name": "Slack",
                "category": "Communication",
                "description": "Team collaboration tool",
                "risk_level": "low",
                "requires_approval": False
            },
            "github": {
                "name": "GitHub Enterprise",
                "category": "Development",
                "description": "Code repository and version control",
                "risk_level": "medium",
                "requires_approval": True
            },
            "tableau": {
                "name": "Tableau",
                "category": "Analytics",
                "description": "Business intelligence and analytics",
                "risk_level": "medium",
                "requires_approval": False
            },
            "okta": {
                "name": "Okta SSO",
                "category": "Security",
                "description": "Single sign-on and identity management",
                "risk_level": "high",
                "requires_approval": True
            }
        }
        
        # Departments
        self.departments = ["Finance", "HR", "IT", "Operations", "Sales", "Marketing", "R&D", "Legal"]
        
        # Predefined users
        self.users = {
            "admin": {
                "user_id": "admin",
                "password": self.hash_password("admin123"),
                "first_name": "System",
                "last_name": "Administrator",
                "email": "admin@company.com",
                "department": "IT",
                "role": "admin",
                "status": "active",
                "created_date": datetime.now() - timedelta(days=365),
                "last_login": None,
                "assigned_apps": list(self.applications.keys())
            },
            "user001": {
                "user_id": "user001",
                "password": self.hash_password("user123"),
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@company.com",
                "department": "Sales",
                "role": "user",
                "status": "active",
                "created_date": datetime.now() - timedelta(days=180),
                "last_login": None,
                "assigned_apps": ["salesforce", "slack", "tableau"]
            },
            "user002": {
                "user_id": "user002",
                "password": self.hash_password("user123"),
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@company.com",
                "department": "HR",
                "role": "user",
                "status": "active",
                "created_date": datetime.now() - timedelta(days=150),
                "last_login": None,
                "assigned_apps": ["workday", "slack", "servicenow"]
            },
            "user003": {
                "user_id": "user003",
                "password": self.hash_password("user123"),
                "first_name": "Mike",
                "last_name": "Chen",
                "email": "mike.chen@company.com",
                "department": "R&D",
                "role": "user",
                "status": "active",
                "created_date": datetime.now() - timedelta(days=120),
                "last_login": None,
                "assigned_apps": ["github", "slack", "servicenow"]
            }
        }
        
        # Access requests and tickets
        self.access_requests = []
        self.support_tickets = []
        self.access_logs = []
        self.iam_alerts = []
        
        # Generate initial data
        self.generate_initial_access_requests()
        self.generate_initial_tickets()
        self.generate_access_logs()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = "enterprise_iam_salt_2024"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username in self.users:
            user = self.users[username]
            if user["status"] == "active" and self.verify_password(password, user["password"]):
                # Update last login
                self.users[username]["last_login"] = datetime.now()
                return True
        return False
    
    def generate_initial_access_requests(self):
        """Generate some initial access requests"""
        requests_data = [
            {"user_id": "user001", "app_id": "github", "status": "pending", "reason": "Need access for project development"},
            {"user_id": "user002", "app_id": "tableau", "status": "approved", "reason": "HR analytics reporting"},
            {"user_id": "user003", "app_id": "sap", "status": "rejected", "reason": "No business justification provided"}
        ]
        
        for req_data in requests_data:
            request_id = f"req_{len(self.access_requests) + 1:06d}"
            self.access_requests.append({
                "request_id": request_id,
                "user_id": req_data["user_id"],
                "app_id": req_data["app_id"],
                "app_name": self.applications[req_data["app_id"]]["name"],
                "status": req_data["status"],
                "reason": req_data["reason"],
                "submitted_date": datetime.now() - timedelta(days=random.randint(1, 30)),
                "reviewed_date": datetime.now() - timedelta(days=random.randint(1, 15)) if req_data["status"] != "pending" else None,
                "reviewed_by": "admin" if req_data["status"] != "pending" else None
            })
    
    def generate_initial_tickets(self):
        """Generate some initial support tickets"""
        tickets_data = [
            {"user_id": "user001", "subject": "Cannot login to Salesforce", "priority": "high", "status": "open"},
            {"user_id": "user002", "subject": "Workday access issue", "priority": "medium", "status": "in_progress"},
            {"user_id": "user003", "subject": "GitHub 2FA reset", "priority": "high", "status": "resolved"}
        ]
        
        for ticket_data in tickets_data:
            ticket_id = f"tkt_{len(self.support_tickets) + 1:06d}"
            self.support_tickets.append({
                "ticket_id": ticket_id,
                "user_id": ticket_data["user_id"],
                "subject": ticket_data["subject"],
                "description": f"Detailed description for {ticket_data['subject']}",
                "priority": ticket_data["priority"],
                "status": ticket_data["status"],
                "category": "access_issue",
                "created_date": datetime.now() - timedelta(days=random.randint(1, 20)),
                "assigned_to": "admin",
                "last_updated": datetime.now() - timedelta(days=random.randint(1, 10))
            })
    
    def generate_access_logs(self):
        """Generate access logs for monitoring"""
        for i in range(500):  # Reduced for performance
            user_id = random.choice(list(self.users.keys()))
            user = self.users[user_id]
            
            # Only log access for assigned apps
            if not user["assigned_apps"]:
                continue
                
            app_id = random.choice(user["assigned_apps"])
            
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            access_event = {
                "log_id": f"log_{i:08d}",
                "user_id": user_id,
                "app_id": app_id,
                "app_name": self.applications[app_id]["name"],
                "timestamp": timestamp,
                "action": random.choice(["login", "view", "modify", "download"]),
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "location": random.choice(["corporate_network", "vpn", "home_office", "mobile"]),
                "success": random.random() > 0.05,  # 95% success rate
                "risk_score": random.randint(0, 100)
            }
            
            self.access_logs.append(access_event)
    
    def create_access_request(self, user_id: str, app_id: str, reason: str) -> str:
        """Create a new access request"""
        request_id = f"req_{len(self.access_requests) + 1:06d}"
        
        request = {
            "request_id": request_id,
            "user_id": user_id,
            "app_id": app_id,
            "app_name": self.applications[app_id]["name"],
            "status": "pending",
            "reason": reason,
            "submitted_date": datetime.now(),
            "reviewed_date": None,
            "reviewed_by": None
        }
        
        self.access_requests.append(request)
        self.last_update = datetime.now()
        return request_id
    
    def create_support_ticket(self, user_id: str, subject: str, description: str, priority: str, category: str) -> str:
        """Create a new support ticket"""
        ticket_id = f"tkt_{len(self.support_tickets) + 1:06d}"
        
        ticket = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "open",
            "category": category,
            "created_date": datetime.now(),
            "assigned_to": "admin",
            "last_updated": datetime.now()
        }
        
        self.support_tickets.append(ticket)
        self.last_update = datetime.now()
        return ticket_id
    
    def assign_application(self, user_id: str, app_id: str) -> bool:
        """Assign application access to user"""
        if user_id in self.users and app_id in self.applications:
            if app_id not in self.users[user_id]["assigned_apps"]:
                self.users[user_id]["assigned_apps"].append(app_id)
                self.last_update = datetime.now()
                return True
        return False
    
    def revoke_application(self, user_id: str, app_id: str) -> bool:
        """Revoke application access from user"""
        if user_id in self.users and app_id in self.applications:
            if app_id in self.users[user_id]["assigned_apps"]:
                self.users[user_id]["assigned_apps"].remove(app_id)
                self.last_update = datetime.now()
                return True
        return False
    
    def process_access_request(self, request_id: str, action: str, reviewed_by: str) -> bool:
        """Process an access request (approve/reject)"""
        for request in self.access_requests:
            if request["request_id"] == request_id and request["status"] == "pending":
                request["status"] = action
                request["reviewed_date"] = datetime.now()
                request["reviewed_by"] = reviewed_by
                
                if action == "approved":
                    self.assign_application(request["user_id"], request["app_id"])
                
                self.last_update = datetime.now()
                return True
        return False
    
    def update_ticket_status(self, ticket_id: str, status: str, updated_by: str) -> bool:
        """Update support ticket status"""
        for ticket in self.support_tickets:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = status
                ticket["last_updated"] = datetime.now()
                self.last_update = datetime.now()
                return True
        return False

def auto_refresh():
    """Auto-refresh the app when data changes"""
    if 'platform' in st.session_state and 'last_refresh' in st.session_state:
        platform = st.session_state.platform
        if platform.last_update > st.session_state.last_refresh:
            st.session_state.last_refresh = platform.last_update
            st.rerun()

def login_page():
    """Display login page"""
    st.markdown('<div class="main-header">🔐 Enterprise IAM Platform</div>', unsafe_allow_html=True)
    st.markdown("### Identity and Access Management System")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://img.icons8.com/color/96/000000/security-checked.png", width=100)
    
    with col2:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if username and password:
                    platform = st.session_state.platform
                    if platform.authenticate_user(username, password):
                        st.session_state.user = platform.users[username]
                        st.session_state.logged_in = True
                        st.session_state.last_refresh = platform.last_update
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
    
    # Demo credentials
    st.markdown("---")
    st.subheader("Demo Credentials")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Admin Access:**")
        st.write("Username: `admin`")
        st.write("Password: `admin123`")
    
    with col2:
        st.write("**User Access:**")
        st.write("Username: `user001`")
        st.write("Password: `user123`")
        st.write("Username: `user002`")
        st.write("Password: `user123`")

def admin_dashboard():
    """Display admin dashboard"""
    platform = st.session_state.platform
    user = st.session_state.user
    
    # Auto-refresh
    auto_refresh()
    
    st.sidebar.title(f"👋 Welcome, {user['first_name']}")
    st.sidebar.markdown(f"**Role:** {user['role'].title()}")
    st.sidebar.markdown(f"**Department:** {user['department']}")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    # Admin navigation
    page = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "👥 User Management", 
        "🔐 Access Control",
        "📋 Access Requests",
        "🎫 Support Tickets",
        "📈 Analytics & Reports"
    ])
    
    if page == "📊 Dashboard":
        show_admin_dashboard(platform)
    elif page == "👥 User Management":
        show_user_management(platform)
    elif page == "🔐 Access Control":
        show_access_control(platform)
    elif page == "📋 Access Requests":
        show_access_requests(platform)
    elif page == "🎫 Support Tickets":
        show_support_tickets(platform)
    elif page == "📈 Analytics & Reports":
        show_analytics_reports(platform)

def user_dashboard():
    """Display user dashboard"""
    platform = st.session_state.platform
    user = st.session_state.user
    
    # Auto-refresh
    auto_refresh()
    
    st.sidebar.title(f"👋 Welcome, {user['first_name']}")
    st.sidebar.markdown(f"**Role:** {user['role'].title()}")
    st.sidebar.markdown(f"**Department:** {user['department']}")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    # User navigation
    page = st.sidebar.radio("Navigation", [
        "🏠 My Dashboard",
        "📱 My Applications", 
        "🔐 Request Access",
        "🎫 My Tickets",
        "📊 My Activity"
    ])
    
    if page == "🏠 My Dashboard":
        show_user_dashboard(platform)
    elif page == "📱 My Applications":
        show_my_applications(platform)
    elif page == "🔐 Request Access":
        show_request_access(platform)
    elif page == "🎫 My Tickets":
        show_my_tickets(platform)
    elif page == "📊 My Activity":
        show_my_activity(platform)

def show_admin_dashboard(platform):
    """Display admin dashboard overview"""
    st.header("Admin Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(platform.users)
        st.metric("Total Users", total_users)
    
    with col2:
        pending_requests = len([r for r in platform.access_requests if r["status"] == "pending"])
        st.metric("Pending Requests", pending_requests, delta_color="inverse")
    
    with col3:
        open_tickets = len([t for t in platform.support_tickets if t["status"] == "open"])
        st.metric("Open Tickets", open_tickets, delta_color="inverse")
    
    with col4:
        total_apps = len(platform.applications)
        st.metric("Managed Applications", total_apps)
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Access Requests")
        recent_requests = sorted(platform.access_requests, key=lambda x: x["submitted_date"], reverse=True)[:5]
        if recent_requests:
            for req in recent_requests:
                status_color = "🟡" if req["status"] == "pending" else "🟢" if req["status"] == "approved" else "🔴"
                st.write(f"{status_color} **{req['user_id']}** - {req['app_name']} - *{req['status']}*")
        else:
            st.info("No access requests")
    
    with col2:
        st.subheader("Recent Support Tickets")
        recent_tickets = sorted(platform.support_tickets, key=lambda x: x["created_date"], reverse=True)[:5]
        if recent_tickets:
            for ticket in recent_tickets:
                priority_color = "🔴" if ticket["priority"] == "high" else "🟡" if ticket["priority"] == "medium" else "🟢"
                st.write(f"{priority_color} **{ticket['user_id']}** - {ticket['subject']}")
        else:
            st.info("No support tickets")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👥 Manage Users"):
            pass  # Navigation handled by radio
    
    with col2:
        if st.button("🔐 Review Requests"):
            pass
    
    with col3:
        if st.button("🎫 Handle Tickets"):
            pass

def show_user_management(platform):
    """Display user management interface"""
    st.header("User Management")
    
    # Users table
    users_data = []
    for user_id, user_info in platform.users.items():
        users_data.append({
            "User ID": user_id,
            "Name": f"{user_info['first_name']} {user_info['last_name']}",
            "Email": user_info["email"],
            "Department": user_info["department"],
            "Role": user_info["role"],
            "Status": user_info["status"],
            "Assigned Apps": len(user_info["assigned_apps"]),
            "Last Login": user_info["last_login"]
        })
    
    users_df = pd.DataFrame(users_data)
    st.dataframe(users_df, use_container_width=True)
    
    # User actions
    st.subheader("User Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_user = st.selectbox("Select User", list(platform.users.keys()))
    
    with col2:
        action = st.selectbox("Action", ["View Details", "Edit User", "Reset Password", "Deactivate User"])
    
    with col3:
        if st.button("Execute Action"):
            if action == "View Details":
                user_info = platform.users[selected_user]
                st.subheader(f"User Details: {selected_user}")
                st.write(f"**Name:** {user_info['first_name']} {user_info['last_name']}")
                st.write(f"**Email:** {user_info['email']}")
                st.write(f"**Department:** {user_info['department']}")
                st.write(f"**Role:** {user_info['role']}")
                st.write(f"**Status:** {user_info['status']}")
                st.write(f"**Assigned Applications:** {', '.join(user_info['assigned_apps'])}")

def show_access_control(platform):
    """Display access control management"""
    st.header("Access Control Management")
    
    # Application access matrix
    st.subheader("Application Access Matrix")
    
    # Create access matrix
    users = list(platform.users.keys())
    apps = list(platform.applications.keys())
    
    access_matrix = []
    for user_id in users:
        user_access = []
        for app_id in apps:
            has_access = app_id in platform.users[user_id]["assigned_apps"]
            user_access.append(has_access)
        access_matrix.append(user_access)
    
    # Display as dataframe
    matrix_df = pd.DataFrame(
        access_matrix,
        index=[f"{platform.users[uid]['first_name']} {platform.users[uid]['last_name']}" for uid in users],
        columns=[platform.applications[aid]["name"] for aid in apps]
    )
    
    # Apply styling for better visualization
    def color_boolean(val):
        color = 'background-color: #90EE90' if val else 'background-color: #FFCCCB'
        return color
    
    st.dataframe(matrix_df.style.applymap(color_boolean))
    
    # Grant/Revoke access
    st.subheader("Grant/Revoke Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_user = st.selectbox("Select User", [uid for uid in platform.users.keys() if uid != "admin"])
    
    with col2:
        selected_app = st.selectbox("Select Application", list(platform.applications.keys()))
    
    with col3:
        current_access = selected_app in platform.users[selected_user]["assigned_apps"]
        st.write(f"Current Access: {'✅ Granted' if current_access else '❌ Not Granted'}")
        
        col1, col2 = st.columns(2)
        with col1:
            if not current_access and st.button("Grant Access"):
                if platform.assign_application(selected_user, selected_app):
                    st.success(f"Access to {platform.applications[selected_app]['name']} granted to {selected_user}")
                    st.rerun()
        with col2:
            if current_access and st.button("Revoke Access"):
                if platform.revoke_application(selected_user, selected_app):
                    st.success(f"Access to {platform.applications[selected_app]['name']} revoked from {selected_user}")
                    st.rerun()

def show_access_requests(platform):
    """Display access request management"""
    st.header("Access Request Management")
    
    # Filter requests
    status_filter = st.selectbox("Filter by Status", ["all", "pending", "approved", "rejected"])
    
    filtered_requests = platform.access_requests
    if status_filter != "all":
        filtered_requests = [r for r in platform.access_requests if r["status"] == status_filter]
    
    if filtered_requests:
        for request in filtered_requests:
            with st.expander(f"📋 {request['app_name']} - {request['user_id']} - {request['status'].title()}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**User:** {request['user_id']}")
                    st.write(f"**Application:** {request['app_name']}")
                    st.write(f"**Reason:** {request['reason']}")
                    st.write(f"**Submitted:** {request['submitted_date'].strftime('%Y-%m-%d %H:%M')}")
                    
                    if request["reviewed_date"]:
                        st.write(f"**Reviewed:** {request['reviewed_date'].strftime('%Y-%m-%d %H:%M')}")
                        st.write(f"**Reviewed By:** {request['reviewed_by']}")
                
                with col2:
                    if request["status"] == "pending":
                        if st.button("Approve", key=f"approve_{request['request_id']}"):
                            if platform.process_access_request(request["request_id"], "approved", st.session_state.user["user_id"]):
                                st.success("Request approved!")
                                st.rerun()
                        
                        if st.button("Reject", key=f"reject_{request['request_id']}"):
                            if platform.process_access_request(request["request_id"], "rejected", st.session_state.user["user_id"]):
                                st.success("Request rejected!")
                                st.rerun()
                    else:
                        st.write(f"Status: {request['status'].title()}")
    else:
        st.info("No access requests found with the selected filter")

def show_support_tickets(platform):
    """Display support ticket management"""
    st.header("Support Ticket Management")
    
    # Filter tickets
    status_filter = st.selectbox("Filter by Status", ["all", "open", "in_progress", "resolved"])
    
    filtered_tickets = platform.support_tickets
    if status_filter != "all":
        filtered_tickets = [t for t in platform.support_tickets if t["status"] == status_filter]
    
    if filtered_tickets:
        for ticket in filtered_tickets:
            priority_color = "🔴" if ticket["priority"] == "high" else "🟡" if ticket["priority"] == "medium" else "🟢"
            
            with st.expander(f"{priority_color} {ticket['subject']} - {ticket['user_id']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**User:** {ticket['user_id']}")
                    st.write(f"**Subject:** {ticket['subject']}")
                    st.write(f"**Description:** {ticket['description']}")
                    st.write(f"**Priority:** {ticket['priority'].title()}")
                    st.write(f"**Category:** {ticket['category'].replace('_', ' ').title()}")
                    st.write(f"**Created:** {ticket['created_date'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Assigned To:** {ticket['assigned_to']}")
                
                with col2:
                    current_status = ticket["status"]
                    new_status = st.selectbox(
                        "Update Status", 
                        ["open", "in_progress", "resolved"],
                        index=["open", "in_progress", "resolved"].index(current_status),
                        key=f"status_{ticket['ticket_id']}"
                    )
                    
                    if new_status != current_status:
                        if st.button("Update Status", key=f"update_{ticket['ticket_id']}"):
                            if platform.update_ticket_status(ticket["ticket_id"], new_status, st.session_state.user["user_id"]):
                                st.success("Ticket status updated!")
                                st.rerun()
    else:
        st.info("No support tickets found with the selected filter")

def show_analytics_reports(platform):
    """Display analytics and reports"""
    st.header("Analytics & Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Application usage
        st.subheader("Application Usage")
        app_usage = {}
        for log in platform.access_logs:
            app_name = log["app_name"]
            app_usage[app_name] = app_usage.get(app_name, 0) + 1
        
        if app_usage:
            fig = px.pie(values=list(app_usage.values()), names=list(app_usage.keys()))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No usage data available")
    
    with col2:
        # Access requests by status
        st.subheader("Access Requests Status")
        request_status = {}
        for req in platform.access_requests:
            status = req["status"]
            request_status[status] = request_status.get(status, 0) + 1
        
        if request_status:
            fig = px.bar(x=list(request_status.keys()), y=list(request_status.values()))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No access request data available")
    
    # Generate reports
    st.subheader("Generate Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 User Access Report"):
            st.success("User Access Report generated!")
    
    with col2:
        if st.button("🔐 Compliance Report"):
            st.success("Compliance Report generated!")
    
    with col3:
        if st.button("📈 Usage Analytics"):
            st.success("Usage Analytics Report generated!")

def show_user_dashboard(platform):
    """Display user dashboard overview"""
    user = st.session_state.user
    
    st.header(f"Welcome, {user['first_name']} {user['last_name']}")
    
    # User metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        assigned_apps_count = len(user["assigned_apps"])
        st.metric("My Applications", assigned_apps_count)
    
    with col2:
        my_requests = len([r for r in platform.access_requests if r["user_id"] == user["user_id"]])
        st.metric("My Requests", my_requests)
    
    with col3:
        my_tickets = len([t for t in platform.support_tickets if t["user_id"] == user["user_id"]])
        st.metric("My Tickets", my_tickets)
    
    with col4:
        recent_logins = len([log for log in platform.access_logs if log["user_id"] == user["user_id"] and log["action"] == "login"])
        st.metric("Recent Logins", recent_logins)
    
    # Quick access to applications
    st.subheader("Quick Access to Applications")
    
    if user["assigned_apps"]:
        cols = st.columns(3)
        for idx, app_id in enumerate(user["assigned_apps"][:6]):
            app = platform.applications[app_id]
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="app-card">
                    <h4>{app['name']}</h4>
                    <p>{app['description']}</p>
                    <small>Category: {app['category']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Launch", key=f"launch_{app_id}"):
                    st.success(f"Launching {app['name']}...")
    else:
        st.info("You don't have access to any applications yet. Request access below.")
    
    # Recent activity
    st.subheader("My Recent Activity")
    user_logs = [log for log in platform.access_logs if log["user_id"] == user["user_id"]]
    recent_logs = sorted(user_logs, key=lambda x: x["timestamp"], reverse=True)[:5]
    
    if recent_logs:
        for log in recent_logs:
            success_icon = "✅" if log["success"] else "❌"
            st.write(f"{success_icon} **{log['app_name']}** - {log['action']} - {log['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("No recent activity found")

def show_my_applications(platform):
    """Display user's assigned applications"""
    user = st.session_state.user
    
    st.header("My Applications")
    
    if user["assigned_apps"]:
        for app_id in user["assigned_apps"]:
            app = platform.applications[app_id]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="app-card">
                    <h3>{app['name']}</h3>
                    <p><strong>Description:</strong> {app['description']}</p>
                    <p><strong>Category:</strong> {app['category']}</p>
                    <p><strong>Risk Level:</strong> {app['risk_level'].title()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Launch Application", key=f"open_{app_id}"):
                    st.success(f"Opening {app['name']}...")
                
                if st.button("View Details", key=f"details_{app_id}"):
                    st.info(f"Detailed information about {app['name']}")
    else:
        st.info("You don't have access to any applications yet.")
        st.markdown("Visit the **Request Access** page to request application access.")

def show_request_access(platform):
    """Display access request interface"""
    user = st.session_state.user
    
    st.header("Request Application Access")
    
    # Available applications (excluding already assigned)
    available_apps = [app_id for app_id in platform.applications.keys() if app_id not in user["assigned_apps"]]
    
    if available_apps:
        with st.form("access_request_form"):
            st.subheader("New Access Request")
            
            selected_app = st.selectbox(
                "Select Application",
                available_apps,
                format_func=lambda x: platform.applications[x]["name"]
            )
            
            reason = st.text_area(
                "Business Justification",
                placeholder="Explain why you need access to this application..."
            )
            
            submitted = st.form_submit_button("Submit Request")
            
            if submitted:
                if reason.strip():
                    request_id = platform.create_access_request(user["user_id"], selected_app, reason)
                    st.success(f"Access request submitted successfully! Request ID: {request_id}")
                else:
                    st.error("Please provide a business justification for your access request")
    else:
        st.success("🎉 You already have access to all available applications!")
    
    # Show request history
    st.subheader("My Access Requests")
    my_requests = [r for r in platform.access_requests if r["user_id"] == user["user_id"]]
    
    if my_requests:
        for request in sorted(my_requests, key=lambda x: x["submitted_date"], reverse=True):
            status_icon = "🟡" if request["status"] == "pending" else "🟢" if request["status"] == "approved" else "🔴"
            
            with st.expander(f"{status_icon} {request['app_name']} - {request['status'].title()}"):
                st.write(f"**Request ID:** {request['request_id']}")
                st.write(f"**Application:** {request['app_name']}")
                st.write(f"**Reason:** {request['reason']}")
                st.write(f"**Submitted:** {request['submitted_date'].strftime('%Y-%m-%d %H:%M')}")
                
                if request["reviewed_date"]:
                    st.write(f"**Reviewed:** {request['reviewed_date'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Reviewed By:** {request['reviewed_by']}")
    else:
        st.info("You haven't submitted any access requests yet.")

def show_my_tickets(platform):
    """Display user's support tickets"""
    user = st.session_state.user
    
    st.header("My Support Tickets")
    
    # Create new ticket
    with st.form("new_ticket_form"):
        st.subheader("Create New Ticket")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Subject")
            category = st.selectbox("Category", ["access_issue", "technical_issue", "password_reset", "other"])
        
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"])
            description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Ticket")
        
        if submitted:
            if subject and description:
                ticket_id = platform.create_support_ticket(
                    user["user_id"], subject, description, priority, category
                )
                st.success(f"Support ticket created successfully! Ticket ID: {ticket_id}")
            else:
                st.error("Please fill in all required fields")
    
    # Show ticket history
    st.subheader("My Ticket History")
    my_tickets = [t for t in platform.support_tickets if t["user_id"] == user["user_id"]]
    
    if my_tickets:
        for ticket in sorted(my_tickets, key=lambda x: x["created_date"], reverse=True):
            priority_color = "🔴" if ticket["priority"] == "high" else "🟡" if ticket["priority"] == "medium" else "🟢"
            status_icon = "🟡" if ticket["status"] == "open" else "🔵" if ticket["status"] == "in_progress" else "🟢"
            
            with st.expander(f"{priority_color} {ticket['subject']} - {status_icon} {ticket['status'].replace('_', ' ').title()}"):
                st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                st.write(f"**Subject:** {ticket['subject']}")
                st.write(f"**Description:** {ticket['description']}")
                st.write(f"**Priority:** {ticket['priority'].title()}")
                st.write(f"**Category:** {ticket['category'].replace('_', ' ').title()}")
                st.write(f"**Status:** {ticket['status'].replace('_', ' ').title()}")
                st.write(f"**Created:** {ticket['created_date'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Assigned To:** {ticket['assigned_to']}")
                st.write(f"**Last Updated:** {ticket['last_updated'].strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("You haven't created any support tickets yet.")

def show_my_activity(platform):
    """Display user's activity logs"""
    user = st.session_state.user
    
    st.header("My Activity Logs")
    
    user_logs = [log for log in platform.access_logs if log["user_id"] == user["user_id"]]
    
    if user_logs:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            app_filter = st.selectbox("Filter by Application", ["all"] + list(set(log["app_name"] for log in user_logs)))
        
        with col2:
            action_filter = st.selectbox("Filter by Action", ["all"] + list(set(log["action"] for log in user_logs)))
        
        with col3:
            success_filter = st.selectbox("Filter by Status", ["all", "success", "failed"])
        
        # Apply filters
        filtered_logs = user_logs
        if app_filter != "all":
            filtered_logs = [log for log in filtered_logs if log["app_name"] == app_filter]
        if action_filter != "all":
            filtered_logs = [log for log in filtered_logs if log["action"] == action_filter]
        if success_filter != "all":
            filtered_logs = [log for log in filtered_logs if log["success"] == (success_filter == "success")]
        
        # Display logs
        for log in sorted(filtered_logs, key=lambda x: x["timestamp"], reverse=True)[:20]:
            success_icon = "✅" if log["success"] else "❌"
            st.write(f"{success_icon} **{log['app_name']}** - {log['action']} - {log['timestamp'].strftime('%Y-%m-%d %H:%M')} - {log['location']}")
    else:
        st.info("No activity logs found for your account.")

def main():
    # Initialize platform in session state
    if 'platform' not in st.session_state:
        st.session_state.platform = EnterpriseIAMPlatform()
    
    # Initialize login state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.last_refresh = datetime.now()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        # Route to appropriate dashboard based on role
        if st.session_state.user["role"] == "admin":
            admin_dashboard()
        else:
            user_dashboard()

if __name__ == "__main__":
    main()
