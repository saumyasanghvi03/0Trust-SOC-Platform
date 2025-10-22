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
import uuid
import asyncio
warnings.filterwarnings('ignore')

# Page configuration with enhanced settings
st.set_page_config(
    page_title="Enterprise IAM Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with animations
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .alert-high {
        background-color: #ffe6cc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ff6600;
        animation: pulse 2s infinite;
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
        transition: all 0.3s ease;
    }
    .ticket-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .app-card {
        border: 1px solid #1f77b4;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #e6f3ff;
        transition: all 0.3s ease;
    }
    .app-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .success-flash {
        animation: flashGreen 2s ease-in-out;
    }
    .notification-badge {
        background-color: #ff4b4b;
        color: white;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 0.8em;
        margin-left: 5px;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    @keyframes flashGreen {
        0% { background-color: transparent; }
        50% { background-color: #90EE90; }
        100% { background-color: transparent; }
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
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
        # Available applications with enhanced metadata
        self.applications = {
            "salesforce": {
                "name": "Salesforce CRM",
                "category": "CRM",
                "description": "Customer relationship management platform",
                "risk_level": "medium",
                "requires_approval": False,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Confidential",
                "compliance": ["SOC2", "GDPR"],
                "owner": "IT Department",
                "last_audit": datetime.now() - timedelta(days=30)
            },
            "workday": {
                "name": "Workday HR",
                "category": "HR",
                "description": "Human resources management system",
                "risk_level": "high",
                "requires_approval": True,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Highly Confidential",
                "compliance": ["SOC2", "SOX", "GDPR"],
                "owner": "HR Department",
                "last_audit": datetime.now() - timedelta(days=45)
            },
            "sap": {
                "name": "SAP ERP",
                "category": "ERP",
                "description": "Enterprise resource planning",
                "risk_level": "high",
                "requires_approval": True,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Highly Confidential",
                "compliance": ["SOC2", "SOX", "ISO27001"],
                "owner": "Finance Department",
                "last_audit": datetime.now() - timedelta(days=60)
            },
            "servicenow": {
                "name": "ServiceNow",
                "category": "ITSM",
                "description": "IT service management",
                "risk_level": "medium",
                "requires_approval": False,
                "sso_enabled": True,
                "mfa_required": False,
                "data_classification": "Internal",
                "compliance": ["SOC2"],
                "owner": "IT Department",
                "last_audit": datetime.now() - timedelta(days=25)
            },
            "slack": {
                "name": "Slack Enterprise",
                "category": "Communication",
                "description": "Team collaboration tool",
                "risk_level": "low",
                "requires_approval": False,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Internal",
                "compliance": ["SOC2"],
                "owner": "IT Department",
                "last_audit": datetime.now() - timedelta(days=15)
            },
            "github": {
                "name": "GitHub Enterprise",
                "category": "Development",
                "description": "Code repository and version control",
                "risk_level": "medium",
                "requires_approval": True,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Confidential",
                "compliance": ["SOC2"],
                "owner": "R&D Department",
                "last_audit": datetime.now() - timedelta(days=40)
            },
            "tableau": {
                "name": "Tableau Server",
                "category": "Analytics",
                "description": "Business intelligence and analytics",
                "risk_level": "medium",
                "requires_approval": False,
                "sso_enabled": True,
                "mfa_required": False,
                "data_classification": "Confidential",
                "compliance": ["SOC2"],
                "owner": "Analytics Team",
                "last_audit": datetime.now() - timedelta(days=35)
            },
            "okta": {
                "name": "Okta SSO",
                "category": "Security",
                "description": "Single sign-on and identity management",
                "risk_level": "high",
                "requires_approval": True,
                "sso_enabled": True,
                "mfa_required": True,
                "data_classification": "Highly Confidential",
                "compliance": ["SOC2", "ISO27001"],
                "owner": "Security Team",
                "last_audit": datetime.now() - timedelta(days=20)
            }
        }
        
        # Departments with managers
        self.departments = {
            "Finance": {"manager": "CFO", "user_count": 45},
            "HR": {"manager": "CHRO", "user_count": 25},
            "IT": {"manager": "CTO", "user_count": 85},
            "Operations": {"manager": "COO", "user_count": 120},
            "Sales": {"manager": "Sales Director", "user_count": 65},
            "Marketing": {"manager": "CMO", "user_count": 35},
            "R&D": {"manager": "R&D Director", "user_count": 55},
            "Legal": {"manager": "General Counsel", "user_count": 15}
        }
        
        # Predefined users with enhanced profiles
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
                "last_login": datetime.now() - timedelta(hours=2),
                "last_password_change": datetime.now() - timedelta(days=30),
                "mfa_enabled": True,
                "assigned_apps": list(self.applications.keys()),
                "job_title": "IAM Administrator",
                "employee_id": "EMP001",
                "location": "Headquarters",
                "manager": "CTO"
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
                "last_login": datetime.now() - timedelta(hours=5),
                "last_password_change": datetime.now() - timedelta(days=45),
                "mfa_enabled": True,
                "assigned_apps": ["salesforce", "slack", "tableau"],
                "job_title": "Sales Executive",
                "employee_id": "EMP045",
                "location": "New York",
                "manager": "Sales Manager"
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
                "last_login": datetime.now() - timedelta(hours=1),
                "last_password_change": datetime.now() - timedelta(days=60),
                "mfa_enabled": False,
                "assigned_apps": ["workday", "slack", "servicenow"],
                "job_title": "HR Specialist",
                "employee_id": "EMP078",
                "location": "Chicago",
                "manager": "HR Manager"
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
                "last_login": datetime.now() - timedelta(hours=8),
                "last_password_change": datetime.now() - timedelta(days=25),
                "mfa_enabled": True,
                "assigned_apps": ["github", "slack", "servicenow"],
                "job_title": "Software Engineer",
                "employee_id": "EMP112",
                "location": "San Francisco",
                "manager": "Engineering Manager"
            }
        }
        
        # Enhanced data structures
        self.access_requests = []
        self.support_tickets = []
        self.access_logs = []
        self.iam_alerts = []
        self.audit_logs = []
        self.notifications = []
        
        # Generate enhanced initial data
        self.generate_initial_access_requests()
        self.generate_initial_tickets()
        self.generate_access_logs()
        self.generate_audit_logs()
        self.generate_notifications()
    
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
                # Update last login and log the event
                self.users[username]["last_login"] = datetime.now()
                self.log_audit_event(
                    user_id=username,
                    action="login",
                    resource="system",
                    status="success",
                    details="User logged in successfully"
                )
                return True
            else:
                self.log_audit_event(
                    user_id=username,
                    action="login",
                    resource="system",
                    status="failed",
                    details="Invalid credentials"
                )
        return False
    
    def log_audit_event(self, user_id: str, action: str, resource: str, status: str, details: str):
        """Log audit event for compliance"""
        audit_event = {
            "audit_id": f"audit_{len(self.audit_logs) + 1:06d}",
            "timestamp": datetime.now(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "status": status,
            "details": details,
            "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        }
        self.audit_logs.append(audit_event)
        self.last_update = datetime.now()
    
    def generate_initial_access_requests(self):
        """Generate some initial access requests"""
        requests_data = [
            {"user_id": "user001", "app_id": "github", "status": "pending", "reason": "Need access for project development", "priority": "high"},
            {"user_id": "user002", "app_id": "tableau", "status": "approved", "reason": "HR analytics reporting", "priority": "medium"},
            {"user_id": "user003", "app_id": "sap", "status": "rejected", "reason": "No business justification provided", "priority": "low"},
            {"user_id": "user001", "app_id": "okta", "status": "pending", "reason": "Need SSO access for new project", "priority": "high"}
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
                "priority": req_data["priority"],
                "submitted_date": datetime.now() - timedelta(days=random.randint(1, 30)),
                "reviewed_date": datetime.now() - timedelta(days=random.randint(1, 15)) if req_data["status"] != "pending" else None,
                "reviewed_by": "admin" if req_data["status"] != "pending" else None,
                "estimated_completion": datetime.now() + timedelta(days=2) if req_data["status"] == "pending" else None
            })
    
    def generate_initial_tickets(self):
        """Generate some initial support tickets"""
        tickets_data = [
            {"user_id": "user001", "subject": "Cannot login to Salesforce", "priority": "high", "status": "open"},
            {"user_id": "user002", "subject": "Workday access issue", "priority": "medium", "status": "in_progress"},
            {"user_id": "user003", "subject": "GitHub 2FA reset", "priority": "high", "status": "resolved"},
            {"user_id": "user001", "subject": "Slack integration problem", "priority": "medium", "status": "open"}
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
                "last_updated": datetime.now() - timedelta(days=random.randint(1, 10)),
                "sla_status": "within_sla" if random.random() > 0.3 else "breached"
            })
    
    def generate_access_logs(self):
        """Generate access logs for monitoring"""
        for i in range(1000):
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
                "action": random.choice(["login", "view", "modify", "download", "upload", "delete"]),
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "location": random.choice(["corporate_network", "vpn", "home_office", "mobile"]),
                "device": random.choice(["Windows 10", "MacOS", "iOS", "Android"]),
                "success": random.random() > 0.05,  # 95% success rate
                "risk_score": random.randint(0, 100),
                "session_duration": random.randint(60, 3600) if random.random() > 0.3 else 0
            }
            
            self.access_logs.append(access_event)
    
    def generate_audit_logs(self):
        """Generate audit logs for compliance"""
        actions = ["create_user", "modify_user", "delete_user", "grant_access", "revoke_access", "password_change"]
        for i in range(500):
            user_id = random.choice(list(self.users.keys()))
            timestamp = datetime.now() - timedelta(days=random.randint(0, 180))
            
            audit_event = {
                "audit_id": f"audit_{i:06d}",
                "timestamp": timestamp,
                "user_id": user_id,
                "action": random.choice(actions),
                "resource": random.choice(list(self.applications.keys())),
                "status": random.choice(["success", "failed"]),
                "details": f"Action performed on {random.choice(list(self.applications.keys()))}",
                "ip_address": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}"
            }
            self.audit_logs.append(audit_event)
    
    def generate_notifications(self):
        """Generate system notifications"""
        notification_types = ["security_alert", "access_request", "ticket_update", "system_maintenance"]
        for i in range(10):
            self.notifications.append({
                "id": f"notif_{i:04d}",
                "type": random.choice(notification_types),
                "title": f"Notification {i+1}",
                "message": f"This is notification message #{i+1}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 48)),
                "read": False,
                "priority": random.choice(["low", "medium", "high"])
            })
    
    def create_access_request(self, user_id: str, app_id: str, reason: str, priority: str = "medium") -> str:
        """Create a new access request"""
        request_id = f"req_{len(self.access_requests) + 1:06d}"
        
        request = {
            "request_id": request_id,
            "user_id": user_id,
            "app_id": app_id,
            "app_name": self.applications[app_id]["name"],
            "status": "pending",
            "reason": reason,
            "priority": priority,
            "submitted_date": datetime.now(),
            "reviewed_date": None,
            "reviewed_by": None,
            "estimated_completion": datetime.now() + timedelta(days=2)
        }
        
        self.access_requests.append(request)
        
        # Log audit event
        self.log_audit_event(
            user_id=user_id,
            action="create_access_request",
            resource=app_id,
            status="success",
            details=f"Access request created for {self.applications[app_id]['name']}"
        )
        
        # Create notification
        self.notifications.append({
            "id": f"notif_{len(self.notifications) + 1:04d}",
            "type": "access_request",
            "title": f"New Access Request from {user_id}",
            "message": f"User {user_id} requested access to {self.applications[app_id]['name']}",
            "timestamp": datetime.now(),
            "read": False,
            "priority": "medium"
        })
        
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
            "last_updated": datetime.now(),
            "sla_status": "within_sla"
        }
        
        self.support_tickets.append(ticket)
        
        # Log audit event
        self.log_audit_event(
            user_id=user_id,
            action="create_ticket",
            resource="helpdesk",
            status="success",
            details=f"Support ticket created: {subject}"
        )
        
        self.last_update = datetime.now()
        return ticket_id
    
    def assign_application(self, user_id: str, app_id: str) -> bool:
        """Assign application access to user"""
        if user_id in self.users and app_id in self.applications:
            if app_id not in self.users[user_id]["assigned_apps"]:
                self.users[user_id]["assigned_apps"].append(app_id)
                
                # Log audit event
                self.log_audit_event(
                    user_id="admin",  # Assuming admin performs this action
                    action="grant_access",
                    resource=app_id,
                    status="success",
                    details=f"Access granted to {app_id} for user {user_id}"
                )
                
                self.last_update = datetime.now()
                return True
        return False
    
    def revoke_application(self, user_id: str, app_id: str) -> bool:
        """Revoke application access from user"""
        if user_id in self.users and app_id in self.applications:
            if app_id in self.users[user_id]["assigned_apps"]:
                self.users[user_id]["assigned_apps"].remove(app_id)
                
                # Log audit event
                self.log_audit_event(
                    user_id="admin",  # Assuming admin performs this action
                    action="revoke_access",
                    resource=app_id,
                    status="success",
                    details=f"Access revoked from {app_id} for user {user_id}"
                )
                
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
                
                # Log audit event
                self.log_audit_event(
                    user_id=reviewed_by,
                    action=f"{action}_access_request",
                    resource=request["app_id"],
                    status="success",
                    details=f"Access request {action} for {request['app_id']}"
                )
                
                self.last_update = datetime.now()
                return True
        return False
    
    def update_ticket_status(self, ticket_id: str, status: str, updated_by: str) -> bool:
        """Update support ticket status"""
        for ticket in self.support_tickets:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = status
                ticket["last_updated"] = datetime.now()
                
                # Log audit event
                self.log_audit_event(
                    user_id=updated_by,
                    action="update_ticket",
                    resource="helpdesk",
                    status="success",
                    details=f"Ticket {ticket_id} status updated to {status}"
                )
                
                self.last_update = datetime.now()
                return True
        return False
    
    def mark_notification_read(self, notification_id: str):
        """Mark notification as read"""
        for notification in self.notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                self.last_update = datetime.now()
                break

def auto_refresh():
    """Auto-refresh the app when data changes"""
    if 'platform' in st.session_state:
        platform = st.session_state.platform
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = platform.last_update
        
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
                        time.sleep(1)  # Brief pause for user to see success message
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
    
    # Sidebar with notifications
    with st.sidebar:
        st.title(f"👋 Welcome, {user['first_name']}")
        st.markdown(f"**Role:** {user['role'].title()}")
        st.markdown(f"**Department:** {user['department']}")
        
        # Notifications
        unread_notifications = [n for n in platform.notifications if not n["read"]]
        if unread_notifications:
            st.markdown(f"### 🔔 Notifications <span class='notification-badge'>{len(unread_notifications)}</span>", unsafe_allow_html=True)
            for notification in unread_notifications[:3]:  # Show only 3 latest
                with st.expander(f"{notification['title']}", expanded=False):
                    st.write(notification["message"])
                    if st.button("Mark as Read", key=f"read_{notification['id']}"):
                        platform.mark_notification_read(notification["id"])
                        st.rerun()
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Admin navigation with enhanced options
    page = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "👥 User Management", 
        "🔐 Access Control",
        "📋 Access Requests",
        "🎫 Support Tickets",
        "📈 Analytics & Reports",
        "🔒 Security Center",
        "⚙️ System Settings"
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
    elif page == "🔒 Security Center":
        show_security_center(platform)
    elif page == "⚙️ System Settings":
        show_system_settings(platform)

def user_dashboard():
    """Display user dashboard"""
    platform = st.session_state.platform
    user = st.session_state.user
    
    # Auto-refresh
    auto_refresh()
    
    # Sidebar with user info
    with st.sidebar:
        st.title(f"👋 Welcome, {user['first_name']}")
        st.markdown(f"**Role:** {user['role'].title()}")
        st.markdown(f"**Department:** {user['department']}")
        st.markdown(f"**Job Title:** {user['job_title']}")
        
        # Quick stats
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.markdown(f"**Applications:** {len(user['assigned_apps'])}")
        
        my_requests = len([r for r in platform.access_requests if r["user_id"] == user["user_id"]])
        st.markdown(f"**My Requests:** {my_requests}")
        
        my_tickets = len([t for t in platform.support_tickets if t["user_id"] == user["user_id"]])
        st.markdown(f"**My Tickets:** {my_tickets}")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # User navigation with enhanced options
    page = st.sidebar.radio("Navigation", [
        "🏠 My Dashboard",
        "📱 My Applications", 
        "🔐 Request Access",
        "🎫 My Tickets",
        "📊 My Activity",
        "👤 My Profile",
        "🛡️ Security Settings"
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
    elif page == "👤 My Profile":
        show_my_profile(platform)
    elif page == "🛡️ Security Settings":
        show_security_settings(platform)

def show_admin_dashboard(platform):
    """Display admin dashboard overview with enhanced features"""
    st.header("Admin Dashboard")
    
    # Real-time metrics with progress bars
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(platform.users)
        st.metric("Total Users", total_users)
        st.progress(total_users / 500)  # Assuming 500 as target
    
    with col2:
        pending_requests = len([r for r in platform.access_requests if r["status"] == "pending"])
        st.metric("Pending Requests", pending_requests, delta_color="inverse")
        st.progress(min(pending_requests / 20, 1.0))  # Assuming 20 as threshold
    
    with col3:
        open_tickets = len([t for t in platform.support_tickets if t["status"] == "open"])
        st.metric("Open Tickets", open_tickets, delta_color="inverse")
        st.progress(min(open_tickets / 15, 1.0))  # Assuming 15 as threshold
    
    with col4:
        total_apps = len(platform.applications)
        st.metric("Managed Applications", total_apps)
        st.progress(total_apps / 12)  # Assuming 12 as target
    
    # Enhanced charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Application usage heatmap
        st.subheader("Application Usage Heatmap")
        app_usage_data = []
        for app_id, app_info in platform.applications.items():
            usage_count = len([log for log in platform.access_logs if log["app_id"] == app_id])
            app_usage_data.append({
                "Application": app_info["name"],
                "Category": app_info["category"],
                "Usage": usage_count,
                "Risk": app_info["risk_level"]
            })
        
        if app_usage_data:
            usage_df = pd.DataFrame(app_usage_data)
            fig = px.treemap(usage_df, path=['Category', 'Application'], values='Usage',
                            color='Risk', color_discrete_map={'low': 'green', 'medium': 'orange', 'high': 'red'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Department-wise access distribution
        st.subheader("Access by Department")
        dept_access = {}
        for user_id, user_info in platform.users.items():
            dept = user_info["department"]
            if dept not in dept_access:
                dept_access[dept] = 0
            dept_access[dept] += len(user_info["assigned_apps"])
        
        if dept_access:
            fig = px.pie(values=list(dept_access.values()), names=list(dept_access.keys()))
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity with time indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Access Requests")
        recent_requests = sorted(platform.access_requests, key=lambda x: x["submitted_date"], reverse=True)[:5]
        if recent_requests:
            for req in recent_requests:
                time_diff = datetime.now() - req["submitted_date"]
                hours_ago = time_diff.total_seconds() / 3600
                
                if hours_ago < 1:
                    time_indicator = "🟢 Just now"
                elif hours_ago < 24:
                    time_indicator = "🟡 Today"
                else:
                    time_indicator = "🔴 Older"
                
                status_color = "🟡" if req["status"] == "pending" else "🟢" if req["status"] == "approved" else "🔴"
                st.write(f"{status_color} **{req['user_id']}** - {req['app_name']} - {time_indicator}")
        else:
            st.info("No access requests")
    
    with col2:
        st.subheader("System Health")
        # Simulated system health metrics
        health_metrics = {
            "IAM Service": {"status": "healthy", "uptime": "99.9%"},
            "Database": {"status": "healthy", "uptime": "99.95%"},
            "SSO Gateway": {"status": "degraded", "uptime": "98.2%"},
            "Audit Logs": {"status": "healthy", "uptime": "100%"}
        }
        
        for service, metrics in health_metrics.items():
            status_icon = "🟢" if metrics["status"] == "healthy" else "🟡" if metrics["status"] == "degraded" else "🔴"
            st.write(f"{status_icon} **{service}** - {metrics['uptime']} uptime")
    
    # Quick actions with enhanced options
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.session_state.radio = "👥 User Management"
            st.rerun()
    
    with col2:
        if st.button("🔐 Review Requests", use_container_width=True):
            st.session_state.radio = "📋 Access Requests"
            st.rerun()
    
    with col3:
        if st.button("🎫 Handle Tickets", use_container_width=True):
            st.session_state.radio = "🎫 Support Tickets"
            st.rerun()
    
    with col4:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.radio = "📈 Analytics & Reports"
            st.rerun()

def show_user_management(platform):
    """Display enhanced user management interface"""
    st.header("User Management")
    
    # User search and filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("Search Users")
    with col2:
        dept_filter = st.selectbox("Department", ["All"] + list(platform.departments.keys()))
    with col3:
        status_filter = st.selectbox("Status", ["All", "active", "inactive"])
    
    # Filter users
    filtered_users = {}
    for user_id, user_info in platform.users.items():
        if search_term and search_term.lower() not in user_id.lower() and search_term.lower() not in user_info["first_name"].lower() and search_term.lower() not in user_info["last_name"].lower():
            continue
        if dept_filter != "All" and user_info["department"] != dept_filter:
            continue
        if status_filter != "All" and user_info["status"] != status_filter:
            continue
        filtered_users[user_id] = user_info
    
    # Users table with enhanced information
    users_data = []
    for user_id, user_info in filtered_users.items():
        last_login = user_info["last_login"]
        if last_login:
            days_since_login = (datetime.now() - last_login).days
            login_status = "Active" if days_since_login < 30 else "Inactive"
        else:
            login_status = "Never"
        
        users_data.append({
            "User ID": user_id,
            "Name": f"{user_info['first_name']} {user_info['last_name']}",
            "Email": user_info["email"],
            "Department": user_info["department"],
            "Role": user_info["role"],
            "Status": user_info["status"],
            "Assigned Apps": len(user_info["assigned_apps"]),
            "Last Login": user_info["last_login"],
            "Login Status": login_status,
            "MFA": "✅" if user_info["mfa_enabled"] else "❌"
        })
    
    users_df = pd.DataFrame(users_data)
    st.dataframe(users_df, use_container_width=True)
    
    # User actions with enhanced options
    st.subheader("User Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_user = st.selectbox("Select User", list(platform.users.keys()))
    
    with col2:
        action = st.selectbox("Action", ["View Details", "Edit User", "Reset Password", "Enable MFA", "Deactivate User", "Export User Data"])
    
    with col3:
        if st.button("Execute Action"):
            if action == "View Details":
                user_info = platform.users[selected_user]
                st.subheader(f"User Details: {selected_user}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {user_info['first_name']} {user_info['last_name']}")
                    st.write(f"**Email:** {user_info['email']}")
                    st.write(f"**Department:** {user_info['department']}")
                    st.write(f"**Job Title:** {user_info['job_title']}")
                    st.write(f"**Employee ID:** {user_info['employee_id']}")
                
                with col2:
                    st.write(f"**Role:** {user_info['role']}")
                    st.write(f"**Status:** {user_info['status']}")
                    st.write(f"**MFA Enabled:** {user_info['mfa_enabled']}")
                    st.write(f"**Last Login:** {user_info['last_login']}")
                    st.write(f"**Location:** {user_info['location']}")
                
                st.subheader("Assigned Applications")
                if user_info["assigned_apps"]:
                    for app_id in user_info["assigned_apps"]:
                        app = platform.applications[app_id]
                        st.write(f"• {app['name']} ({app['category']}) - Risk: {app['risk_level']}")
                else:
                    st.info("No applications assigned")
            
            elif action == "Reset Password":
                st.success(f"Password reset initiated for {selected_user}")
                # In real implementation, this would send a reset email

def show_access_control(platform):
    """Display enhanced access control management"""
    st.header("Access Control Management")
    
    # Bulk operations
    st.subheader("Bulk Operations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bulk_users = st.multiselect("Select Users", [uid for uid in platform.users.keys() if uid != "admin"])
    with col2:
        bulk_apps = st.multiselect("Select Applications", list(platform.applications.keys()))
    with col3:
        bulk_action = st.selectbox("Action", ["Grant Access", "Revoke Access"])
    
    if st.button("Execute Bulk Operation"):
        if bulk_users and bulk_apps:
            success_count = 0
            for user_id in bulk_users:
                for app_id in bulk_apps:
                    if bulk_action == "Grant Access":
                        if platform.assign_application(user_id, app_id):
                            success_count += 1
                    else:
                        if platform.revoke_application(user_id, app_id):
                            success_count += 1
            
            st.success(f"Bulk operation completed: {success_count} actions performed")
        else:
            st.error("Please select both users and applications")
    
    # Application access matrix with enhanced visualization
    st.subheader("Application Access Matrix")
    
    # Create access matrix
    users = [uid for uid in platform.users.keys() if uid != "admin"]
    apps = list(platform.applications.keys())
    
    # Display as interactive matrix
    matrix_data = []
    for user_id in users:
        user_row = {"User": f"{platform.users[user_id]['first_name']} {platform.users[user_id]['last_name']}"}
        for app_id in apps:
            has_access = app_id in platform.users[user_id]["assigned_apps"]
            user_row[platform.applications[app_id]["name"]] = "✅" if has_access else "❌"
        matrix_data.append(user_row)
    
    if matrix_data:
        matrix_df = pd.DataFrame(matrix_data)
        st.dataframe(matrix_df, use_container_width=True)
    
    # Individual access management
    st.subheader("Individual Access Management")
    
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

# ... (Other admin functions would follow similar enhanced patterns)

def show_user_dashboard(platform):
    """Display enhanced user dashboard overview"""
    user = st.session_state.user
    
    st.header(f"Welcome, {user['first_name']} {user['last_name']}")
    
    # Enhanced user metrics with progress indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        assigned_apps_count = len(user["assigned_apps"])
        st.metric("My Applications", assigned_apps_count)
        st.progress(assigned_apps_count / len(platform.applications))
    
    with col2:
        my_requests = len([r for r in platform.access_requests if r["user_id"] == user["user_id"]])
        st.metric("My Requests", my_requests)
        st.progress(min(my_requests / 10, 1.0))
    
    with col3:
        my_tickets = len([t for t in platform.support_tickets if t["user_id"] == user["user_id"]])
        st.metric("My Tickets", my_tickets)
        st.progress(min(my_tickets / 5, 1.0))
    
    with col4:
        recent_logins = len([log for log in platform.access_logs if log["user_id"] == user["user_id"] and log["action"] == "login"])
        st.metric("Recent Logins", recent_logins)
        st.progress(min(recent_logins / 50, 1.0))
    
    # Enhanced quick access to applications
    st.subheader("Quick Access to Applications")
    
    if user["assigned_apps"]:
        cols = st.columns(3)
        for idx, app_id in enumerate(user["assigned_apps"][:6]):
            app = platform.applications[app_id]
            with cols[idx % 3]:
                risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}[app["risk_level"]]
                
                st.markdown(f"""
                <div class="app-card">
                    <h4>{app['name']} {risk_color}</h4>
                    <p>{app['description']}</p>
                    <small>Category: {app['category']}</small><br>
                    <small>SSO: {'✅' if app['sso_enabled'] else '❌'}</small>
                    <small>MFA: {'✅' if app['mfa_required'] else '❌'}</small>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Launch", key=f"launch_{app_id}"):
                        st.success(f"Launching {app['name']}...")
                with col2:
                    if st.button("Info", key=f"info_{app_id}"):
                        st.session_state.selected_app = app_id
                        st.session_state.radio = "📱 My Applications"
                        st.rerun()
    else:
        st.info("You don't have access to any applications yet. Request access below.")
        if st.button("Request Access Now"):
            st.session_state.radio = "🔐 Request Access"
            st.rerun()
    
    # Enhanced recent activity with insights
    st.subheader("My Recent Activity & Insights")
    
    user_logs = [log for log in platform.access_logs if log["user_id"] == user["user_id"]]
    recent_logs = sorted(user_logs, key=lambda x: x["timestamp"], reverse=True)[:5]
    
    if recent_logs:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Recent Actions:**")
            for log in recent_logs:
                success_icon = "✅" if log["success"] else "❌"
                time_ago = (datetime.now() - log["timestamp"]).total_seconds() / 3600
                if time_ago < 1:
                    time_text = "Just now"
                elif time_ago < 24:
                    time_text = f"{int(time_ago)}h ago"
                else:
                    time_text = f"{int(time_ago/24)}d ago"
                
                st.write(f"{success_icon} **{log['app_name']}** - {log['action']} - *{time_text}*")
        
        with col2:
            st.write("**Activity Insights:**")
            successful_logins = len([log for log in user_logs if log["action"] == "login" and log["success"]])
            failed_attempts = len([log for log in user_logs if log["action"] == "login" and not log["success"]])
            
            st.write(f"Successful Logins: {successful_logins}")
            st.write(f"Failed Attempts: {failed_attempts}")
            
            if failed_attempts > 5:
                st.warning("Multiple failed login attempts detected")
    else:
        st.info("No recent activity found")

# ... (Other user functions would follow similar enhanced patterns)

def show_my_profile(platform):
    """Display user profile management"""
    user = st.session_state.user
    
    st.header("My Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        st.write(f"**Name:** {user['first_name']} {user['last_name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Department:** {user['department']}")
        st.write(f"**Job Title:** {user['job_title']}")
        st.write(f"**Employee ID:** {user['employee_id']}")
        st.write(f"**Location:** {user['location']}")
        st.write(f"**Manager:** {user['manager']}")
    
    with col2:
        st.subheader("Account Information")
        st.write(f"**Username:** {user['user_id']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Status:** {user['status'].title()}")
        st.write(f"**Account Created:** {user['created_date'].strftime('%Y-%m-%d')}")
        st.write(f"**Last Login:** {user['last_login'].strftime('%Y-%m-%d %H:%M') if user['last_login'] else 'Never'}")
        st.write(f"**Last Password Change:** {user['last_password_change'].strftime('%Y-%m-%d')}")
        st.write(f"**MFA Enabled:** {'✅ Yes' if user['mfa_enabled'] else '❌ No'}")
    
    # Security settings
    st.subheader("Security Settings")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Enable MFA"):
            platform.users[user["user_id"]]["mfa_enabled"] = True
            st.success("MFA has been enabled for your account")
            st.rerun()
    
    with col2:
        if st.button("Change Password"):
            st.info("Password change functionality would be implemented here")
    
    with col3:
        if st.button("Download My Data"):
            st.success("Data export initiated. You will receive an email with your data.")
    
    # Application access summary
    st.subheader("Application Access Summary")
    if user["assigned_apps"]:
        access_data = []
        for app_id in user["assigned_apps"]:
            app = platform.applications[app_id]
            access_data.append({
                "Application": app["name"],
                "Category": app["category"],
                "Risk Level": app["risk_level"],
                "SSO": "Yes" if app["sso_enabled"] else "No",
                "MFA Required": "Yes" if app["mfa_required"] else "No",
                "Last Used": "Recently"  # This would be calculated from logs in real implementation
            })
        
        access_df = pd.DataFrame(access_data)
        st.dataframe(access_df, use_container_width=True)
    else:
        st.info("You don't have access to any applications yet.")

def show_security_center(platform):
    """Display security center for admin"""
    st.header("Security Center")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Security score
        total_users = len(platform.users)
        mfa_users = len([u for u in platform.users.values() if u["mfa_enabled"]])
        mfa_percentage = (mfa_users / total_users) * 100
        
        st.metric("MFA Adoption", f"{mfa_percentage:.1f}%")
        st.progress(mfa_percentage / 100)
    
    with col2:
        # Risk assessment
        high_risk_apps = len([app for app in platform.applications.values() if app["risk_level"] == "high"])
        st.metric("High Risk Applications", high_risk_apps)
    
    with col3:
        # Compliance status
        compliant_apps = len([app for app in platform.applications.values() if "SOC2" in app["compliance"]])
        st.metric("SOC2 Compliant Apps", f"{compliant_apps}/{len(platform.applications)}")
    
    # Security alerts
    st.subheader("Security Alerts")
    
    # Generate some sample alerts
    alerts = [
        {"type": "Multiple Failed Logins", "user": "user001", "severity": "High", "timestamp": datetime.now() - timedelta(hours=2)},
        {"type": "Unusual Access Pattern", "user": "user003", "severity": "Medium", "timestamp": datetime.now() - timedelta(hours=5)},
        {"type": "Password Policy Violation", "user": "user002", "severity": "Low", "timestamp": datetime.now() - timedelta(days=1)}
    ]
    
    for alert in alerts:
        severity_color = "🔴" if alert["severity"] == "High" else "🟡" if alert["severity"] == "Medium" else "🟢"
        st.write(f"{severity_color} **{alert['type']}** - {alert['user']} - {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    
    # Security recommendations
    st.subheader("Security Recommendations")
    recommendations = [
        "Enable MFA for all users with high-risk application access",
        "Review and update access controls for departed employees",
        "Conduct quarterly access reviews for privileged accounts",
        "Implement password expiration policy (90 days)"
    ]
    
    for rec in recommendations:
        st.write(f"• {rec}")

def show_security_settings(platform):
    """Display security settings for users"""
    user = st.session_state.user
    
    st.header("Security Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Multi-Factor Authentication")
        st.write(f"Current Status: {'✅ Enabled' if user['mfa_enabled'] else '❌ Disabled'}")
        
        if user["mfa_enabled"]:
            if st.button("Disable MFA"):
                platform.users[user["user_id"]]["mfa_enabled"] = False
                st.success("MFA has been disabled for your account")
                st.rerun()
        else:
            if st.button("Enable MFA"):
                platform.users[user["user_id"]]["mfa_enabled"] = True
                st.success("MFA has been enabled for your account")
                st.rerun()
        
        st.info("MFA adds an extra layer of security to your account by requiring additional verification.")
    
    with col2:
        st.subheader("Password Management")
        days_since_change = (datetime.now() - user["last_password_change"]).days
        st.write(f"Last changed: {days_since_change} days ago")
        
        if st.button("Change Password"):
            with st.form("password_change"):
                current_pwd = st.text_input("Current Password", type="password")
                new_pwd = st.text_input("New Password", type="password")
                confirm_pwd = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    if new_pwd == confirm_pwd:
                        st.success("Password has been updated successfully")
                    else:
                        st.error("New passwords do not match")
    
    # Session management
    st.subheader("Active Sessions")
    user_sessions = [log for log in platform.access_logs if log["user_id"] == user["user_id"] and log["action"] == "login" and log["success"]]
    recent_sessions = sorted(user_sessions, key=lambda x: x["timestamp"], reverse=True)[:3]
    
    for session in recent_sessions:
        st.write(f"• {session['timestamp'].strftime('%Y-%m-%d %H:%M')} - {session['location']} - {session['device']}")
    
    if st.button("Sign Out All Other Sessions"):
        st.success("All other sessions have been signed out")

def show_system_settings(platform):
    """Display system settings for admin"""
    st.header("System Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["General", "Security", "Notifications", "Backup"])
    
    with tab1:
        st.subheader("General Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            session_timeout = st.slider("Session Timeout (minutes)", 15, 480, 60)
            st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
        
        with col2:
            st.checkbox("Enable Automatic User Provisioning", value=True)
            st.checkbox("Enable Self-Service Password Reset", value=True)
        
        if st.button("Save General Settings"):
            st.success("General settings have been saved")
    
    with tab2:
        st.subheader("Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Require MFA for All Users", value=False)
            st.checkbox("Enforce Strong Password Policy", value=True)
            st.selectbox("Password Expiration", [30, 60, 90, 180], index=2)
        
        with col2:
            st.checkbox("Enable GeoIP Restrictions", value=False)
            st.checkbox("Log All User Activities", value=True)
            st.selectbox("Default Risk Level for New Apps", ["Low", "Medium", "High"], index=1)
        
        if st.button("Save Security Settings"):
            st.success("Security settings have been saved")
    
    with tab3:
        st.subheader("Notification Settings")
        
        st.checkbox("Email Notifications for Access Requests", value=True)
        st.checkbox("Slack Notifications for Security Alerts", value=True)
        st.checkbox("SMS Notifications for Critical Issues", value=False)
        
        if st.button("Save Notification Settings"):
            st.success("Notification settings have been saved")
    
    with tab4:
        st.subheader("Backup & Recovery")
        
        st.write("Last Backup: 2024-01-15 02:00 AM")
        st.write("Backup Size: 45.2 MB")
        st.write("Next Scheduled Backup: 2024-01-16 02:00 AM")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Backup Now"):
                with st.spinner("Creating backup..."):
                    time.sleep(2)
                st.success("Backup completed successfully")
        
        with col2:
            if st.button("Download Latest Backup"):
                st.success("Backup download initiated")

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
