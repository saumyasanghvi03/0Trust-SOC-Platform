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
from typing import Dict, List, Any, Tuple
import warnings
import requests
import jwt
import bcrypt
from cryptography.fernet import Fernet
import asyncio
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Enterprise IAM Security Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional enterprise look
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
    .alert-critical {
        background-color: #ffcccc;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ff0000;
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
</style>
""", unsafe_allow_html=True)

class EnterpriseIAMPlatform:
    def __init__(self):
        self.initialize_enterprise_data()
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def initialize_enterprise_data(self):
        """Initialize comprehensive enterprise IAM data"""
        # Enhanced role hierarchy with departments
        self.departments = ["Finance", "HR", "IT", "Operations", "Sales", "Marketing", "R&D", "Legal"]
        
        self.roles = {
            "super_admin": {
                "permissions": ["all"], 
                "risk_level": "critical",
                "department": "IT",
                "sensitive_access": True,
                "mfa_required": True
            },
            "finance_manager": {
                "permissions": ["financial_reports", "approve_payments", "view_salaries"],
                "risk_level": "high",
                "department": "Finance",
                "sensitive_access": True,
                "mfa_required": True
            },
            "hr_director": {
                "permissions": ["employee_data", "salary_info", "performance_reviews"],
                "risk_level": "high",
                "department": "HR",
                "sensitive_access": True,
                "mfa_required": True
            },
            "developer": {
                "permissions": ["code_access", "test_environments", "ci_cd"],
                "risk_level": "medium",
                "department": "R&D",
                "sensitive_access": False,
                "mfa_required": True
            },
            "sales_rep": {
                "permissions": ["crm_access", "sales_data", "customer_info"],
                "risk_level": "medium",
                "department": "Sales",
                "sensitive_access": False,
                "mfa_required": True
            }
        }
        
        # Enhanced zero-trust rules for enterprise
        self.zero_trust_rules = [
            {"id": 1, "name": "External Access", "condition": "location != 'corporate_network'", "action": "require_2fa", "priority": "high"},
            {"id": 2, "name": "After Hours Access", "condition": "hour < 6 or hour > 22", "action": "flag_review", "priority": "medium"},
            {"id": 3, "name": "Multiple Failed Logins", "condition": "failed_logins >= 3", "action": "block_temporary", "priority": "critical"},
            {"id": 4, "name": "New Device Access", "condition": "device_change == True", "action": "require_2fa", "priority": "high"},
            {"id": 5, "name": "Sensitive Data Access", "condition": "sensitive_access == True", "action": "log_and_alert", "priority": "high"},
            {"id": 6, "name": "Role Change Detection", "condition": "role_changed == True", "action": "require_approval", "priority": "high"},
            {"id": 7, "name": "Geographic Anomaly", "condition": "country_change == True", "action": "block_and_alert", "priority": "critical"}
        ]
        
        # Generate enterprise user base
        self.users = self.generate_enterprise_users()
        self.access_logs = []
        self.privileged_sessions = []
        self.iam_alerts = []
        self.access_reviews = []
        self.compliance_checks = []
        
        # Generate initial data
        self.generate_enterprise_access_logs()
        self.generate_privileged_sessions()
        self.run_iam_analytics()
        self.schedule_access_reviews()
    
    def generate_enterprise_users(self):
        """Generate realistic enterprise user base"""
        users = {}
        user_count = 500  # Medium enterprise size
        
        first_names = ["John", "Jane", "Robert", "Maria", "David", "Sarah", "Michael", "Lisa", 
                      "James", "Jennifer", "William", "Elizabeth", "Richard", "Susan", "Joseph"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                     "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
        
        departments = self.departments
        roles_list = list(self.roles.keys())
        
        for i in range(user_count):
            user_id = f"emp_{i:05d}"
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            department = random.choice(departments)
            role = random.choice(roles_list)
            
            # Ensure role matches department
            if role == "finance_manager" and department != "Finance":
                role = random.choice([r for r in roles_list if "sales" in r.lower() or "developer" in r.lower()])
            
            users[user_id] = {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "department": department,
                "role": role,
                "hire_date": datetime.now() - timedelta(days=random.randint(30, 3650)),
                "status": "active",
                "last_login": None,
                "failed_login_attempts": 0,
                "mfa_enabled": random.random() > 0.3,  # 70% MFA adoption
                "sensitive_access": self.roles[role]["sensitive_access"]
            }
        
        return users
    
    def generate_enterprise_access_logs(self):
        """Generate comprehensive access logs for enterprise monitoring"""
        applications = [
            "ERP System", "CRM Platform", "HR Portal", "Financial Database", 
            "Code Repository", "File Shares", "Email System", "Admin Console",
            "BI Dashboard", "Project Management", "Customer Database", "Internal Wiki"
        ]
        
        locations = ["corporate_network", "vpn", "home_office", "mobile_data", "public_wifi"]
        countries = ["US", "UK", "Germany", "India", "Singapore", "Australia", "Canada", "Japan"]
        
        for i in range(10000):  # Large dataset for analytics
            user_id = random.choice(list(self.users.keys()))
            user = self.users[user_id]
            
            # Generate realistic timestamp (last 90 days)
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            application = random.choice(applications)
            location = random.choice(locations)
            country = random.choice(countries)
            
            # Business hours weighting
            hour = timestamp.hour
            if 9 <= hour <= 17:  # Business hours
                activity_factor = 0.8
            else:
                activity_factor = 0.2
            
            # Generate access event
            access_event = {
                "log_id": f"access_{i:08d}",
                "user_id": user_id,
                "timestamp": timestamp,
                "application": application,
                "action": random.choice(["login", "view", "modify", "download", "upload", "delete"]),
                "resource": f"{application}_{random.randint(1, 100)}",
                "location": location,
                "country": country,
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "device_type": random.choice(["laptop", "desktop", "mobile", "tablet"]),
                "success": random.random() > 0.05,  # 95% success rate
                "risk_score": random.randint(0, 100),
                "session_duration": random.randint(60, 3600) if random.random() > 0.3 else 0
            }
            
            # Update user last login
            if access_event["action"] == "login" and access_event["success"]:
                self.users[user_id]["last_login"] = timestamp
                self.users[user_id]["failed_login_attempts"] = 0
            elif access_event["action"] == "login" and not access_event["success"]:
                self.users[user_id]["failed_login_attempts"] += 1
            
            self.access_logs.append(access_event)
    
    def generate_privileged_sessions(self):
        """Generate privileged access session data"""
        privileged_apps = ["Admin Console", "Financial Database", "HR Portal", "Network Infrastructure", "Server Management"]
        
        for i in range(500):  # Privileged sessions
            user_id = random.choice(list(self.users.keys()))
            user = self.users[user_id]
            
            if not user["sensitive_access"]:
                continue
                
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23)
            )
            
            session = {
                "session_id": f"priv_{i:06d}",
                "user_id": user_id,
                "timestamp": timestamp,
                "application": random.choice(privileged_apps),
                "privilege_level": random.choice(["admin", "super_user", "root"]),
                "actions_performed": random.randint(1, 50),
                "session_duration": random.randint(300, 7200),
                "sensitive_operations": random.randint(0, 10),
                "justification": random.choice(["routine_maintenance", "user_support", "system_update", "security_patch"]),
                "approver": f"manager_{random.randint(1, 50)}"
            }
            
            self.privileged_sessions.append(session)
    
    def run_iam_analytics(self):
        """Run comprehensive IAM analytics and threat detection"""
        self.iam_alerts = []
        
        # User behavior analytics
        user_activities = {}
        for log in self.access_logs:
            user_id = log["user_id"]
            if user_id not in user_activities:
                user_activities[user_id] = []
            user_activities[user_id].append(log)
        
        # Detect anomalies
        for user_id, activities in user_activities.items():
            user = self.users[user_id]
            alerts = self.analyze_user_behavior(user, activities)
            self.iam_alerts.extend(alerts)
        
        # Privileged access monitoring
        for session in self.privileged_sessions:
            alerts = self.analyze_privileged_access(session)
            self.iam_alerts.extend(alerts)
        
        # Compliance checks
        self.run_compliance_checks()
    
    def analyze_user_behavior(self, user, activities):
        """Analyze user behavior for anomalies"""
        alerts = []
        
        # Recent activities (last 7 days)
        recent_activities = [a for a in activities if a["timestamp"] > datetime.now() - timedelta(days=7)]
        
        if not recent_activities:
            return alerts
        
        # Failed login analysis
        failed_logins = [a for a in recent_activities if a["action"] == "login" and not a["success"]]
        if len(failed_logins) >= 5:
            alerts.append({
                "alert_id": f"alert_{len(self.iam_alerts) + len(alerts):06d}",
                "timestamp": datetime.now(),
                "type": "Multiple Failed Logins",
                "severity": "High",
                "user_id": user["user_id"],
                "description": f"User {user['first_name']} {user['last_name']} has {len(failed_logins)} failed login attempts in 7 days",
                "department": user["department"],
                "status": "New",
                "recommended_action": "Temporary account lockout and user verification"
            })
        
        # Geographic anomalies
        countries = [a["country"] for a in recent_activities if a["action"] == "login" and a["success"]]
        if len(set(countries)) > 2:  # Access from more than 2 countries
            alerts.append({
                "alert_id": f"alert_{len(self.iam_alerts) + len(alerts):06d}",
                "timestamp": datetime.now(),
                "type": "Geographic Anomaly",
                "severity": "Medium",
                "user_id": user["user_id"],
                "description": f"User accessed from {len(set(countries))} different countries in 7 days",
                "department": user["department"],
                "status": "New",
                "recommended_action": "Verify travel schedule or require additional authentication"
            })
        
        # After-hours access pattern
        after_hours_access = [a for a in recent_activities 
                            if a["action"] == "login" and a["success"] 
                            and (a["timestamp"].hour < 6 or a["timestamp"].hour > 22)]
        
        if len(after_hours_access) > len(recent_activities) * 0.3:  # 30% after hours
            alerts.append({
                "alert_id": f"alert_{len(self.iam_alerts) + len(alerts):06d}",
                "timestamp": datetime.now(),
                "type": "Unusual Access Hours",
                "severity": "Medium",
                "user_id": user["user_id"],
                "description": "Significant after-hours access pattern detected",
                "department": user["department"],
                "status": "New",
                "recommended_action": "Review work schedule and access needs"
            })
        
        return alerts
    
    def analyze_privileged_access(self, session):
        """Analyze privileged access sessions"""
        alerts = []
        user = self.users[session["user_id"]]
        
        # Long privileged sessions
        if session["session_duration"] > 3600:  # More than 1 hour
            alerts.append({
                "alert_id": f"alert_{len(self.iam_alerts) + len(alerts):06d}",
                "timestamp": datetime.now(),
                "type": "Extended Privileged Session",
                "severity": "Medium",
                "user_id": user["user_id"],
                "description": f"Privileged session lasted {session['session_duration']//60} minutes",
                "department": user["department"],
                "status": "New",
                "recommended_action": "Review session logs for unusual activity"
            })
        
        # High number of sensitive operations
        if session["sensitive_operations"] > 5:
            alerts.append({
                "alert_id": f"alert_{len(self.iam_alerts) + len(alerts):06d}",
                "timestamp": datetime.now(),
                "type": "High Sensitive Operations",
                "severity": "High",
                "user_id": user["user_id"],
                "description": f"Performed {session['sensitive_operations']} sensitive operations in one session",
                "department": user["department"],
                "status": "New",
                "recommended_action": "Immediate review and potential session termination"
            })
        
        return alerts
    
    def run_compliance_checks(self):
        """Run compliance and policy checks"""
        self.compliance_checks = []
        
        # MFA compliance check
        users_without_mfa = [user for user in self.users.values() 
                           if user["sensitive_access"] and not user["mfa_enabled"]]
        
        if users_without_mfa:
            self.compliance_checks.append({
                "check_id": "COMP_001",
                "name": "MFA for Sensitive Access",
                "status": "FAIL",
                "description": f"{len(users_without_mfa)} users with sensitive access lack MFA",
                "severity": "High",
                "remediation": "Enable MFA for all sensitive access users"
            })
        
        # Password policy check (simulated)
        self.compliance_checks.append({
            "check_id": "COMP_002",
            "name": "Password Policy Enforcement",
            "status": "PASS",
            "description": "All users comply with password complexity requirements",
            "severity": "Medium",
            "remediation": "None required"
        })
        
        # Access review compliance
        overdue_reviews = [r for r in self.access_reviews if r["status"] == "overdue"]
        if overdue_reviews:
            self.compliance_checks.append({
                "check_id": "COMP_003",
                "name": "Access Review Timeliness",
                "status": "FAIL",
                "description": f"{len(overdue_reviews)} access reviews are overdue",
                "severity": "Medium",
                "remediation": "Complete pending access reviews"
            })
    
    def schedule_access_reviews(self):
        """Schedule and manage access reviews"""
        # Generate quarterly access reviews
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        current_year = datetime.now().year
        
        for quarter in quarters:
            due_date = datetime(current_year, (quarters.index(quarter) + 1) * 3, 30)
            
            self.access_reviews.append({
                "review_id": f"REV_{quarter}_{current_year}",
                "name": f"{quarter} {current_year} Access Review",
                "due_date": due_date,
                "status": "pending" if due_date > datetime.now() else "overdue",
                "reviewers_required": 5,
                "reviewers_completed": random.randint(0, 5),
                "users_in_scope": len([u for u in self.users.values() if u["sensitive_access"]]),
                "department": "All"
            })
    
    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive user data"""
        if isinstance(data, str):
            return self.cipher_suite.encrypt(data.encode()).decode()
        return data
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt sensitive user data"""
        if isinstance(encrypted_data, str):
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        return encrypted_data

def main():
    st.markdown('<div class="main-header">🔐 Enterprise IAM Security Platform</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Identity & Access Management Monitoring & Analytics")
    
    # Initialize session state
    if 'iam_platform' not in st.session_state:
        st.session_state.iam_platform = EnterpriseIAMPlatform()
    
    platform = st.session_state.iam_platform
    
    # Enhanced sidebar with enterprise sections
    st.sidebar.image("https://img.icons8.com/color/96/000000/security-checked.png", width=80)
    st.sidebar.title("IAM Security Command Center")
    
    # Navigation
    page = st.sidebar.radio("Navigation", [
        "📊 Executive Dashboard",
        "👥 User Access Monitoring", 
        "🔐 Privileged Access Management",
        "🚨 Security Alerts & Incidents",
        "📋 Access Certification",
        "⚖️ Compliance & Audit",
        "🛡️ Zero-Trust Policy Engine",
        "📈 Analytics & Reporting"
    ])
    
    if page == "📊 Executive Dashboard":
        show_executive_dashboard(platform)
    elif page == "👥 User Access Monitoring":
        show_user_access_monitoring(platform)
    elif page == "🔐 Privileged Access Management":
        show_privileged_access_management(platform)
    elif page == "🚨 Security Alerts & Incidents":
        show_security_alerts(platform)
    elif page == "📋 Access Certification":
        show_access_certification(platform)
    elif page == "⚖️ Compliance & Audit":
        show_compliance_audit(platform)
    elif page == "🛡️ Zero-Trust Policy Engine":
        show_zero_trust_policy(platform)
    elif page == "📈 Analytics & Reporting":
        show_analytics_reporting(platform)

def show_executive_dashboard(platform):
    """Display executive dashboard with key IAM metrics"""
    st.header("Executive Security Dashboard")
    
    # Top-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(platform.users)
        active_users = len([u for u in platform.users.values() if u["status"] == "active"])
        st.metric("Total Users", total_users, f"{active_users} active")
    
    with col2:
        total_alerts = len(platform.iam_alerts)
        critical_alerts = len([a for a in platform.iam_alerts if a["severity"] == "Critical"])
        st.metric("Security Alerts", total_alerts, f"{critical_alerts} critical", delta_color="inverse")
    
    with col3:
        privileged_users = len([u for u in platform.users.values() if u["sensitive_access"]])
        st.metric("Privileged Users", privileged_users)
    
    with col4:
        mfa_coverage = len([u for u in platform.users.values() if u["mfa_enabled"]]) / len(platform.users) * 100
        st.metric("MFA Coverage", f"{mfa_coverage:.1f}%")
    
    # Second row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        failed_logins = len([log for log in platform.access_logs if log["action"] == "login" and not log["success"]])
        st.metric("Failed Logins (7d)", failed_logins)
    
    with col2:
        compliance_status = len([c for c in platform.compliance_checks if c["status"] == "PASS"])
        total_checks = len(platform.compliance_checks)
        st.metric("Compliance", f"{compliance_status}/{total_checks}", "Checks Passed")
    
    with col3:
        access_reviews_due = len([r for r in platform.access_reviews if r["status"] == "overdue"])
        st.metric("Overdue Reviews", access_reviews_due, delta_color="inverse")
    
    with col4:
        avg_risk_score = np.mean([log["risk_score"] for log in platform.access_logs])
        st.metric("Average Risk Score", f"{avg_risk_score:.1f}")
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Alert severity distribution
        if platform.iam_alerts:
            alert_df = pd.DataFrame(platform.iam_alerts)
            severity_counts = alert_df['severity'].value_counts()
            fig1 = px.pie(values=severity_counts.values, names=severity_counts.index,
                         title="Security Alert Severity Distribution")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Access pattern by hour
        access_hours = [log["timestamp"].hour for log in platform.access_logs]
        hour_counts = pd.Series(access_hours).value_counts().sort_index()
        fig2 = px.bar(x=hour_counts.index, y=hour_counts.values,
                     title="Access Patterns by Hour of Day")
        fig2.update_layout(xaxis_title="Hour of Day", yaxis_title="Access Count")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent critical alerts
    st.subheader("Recent Critical Alerts")
    critical_alerts = [a for a in platform.iam_alerts if a["severity"] in ["Critical", "High"]][:10]
    
    if critical_alerts:
        for alert in critical_alerts:
            with st.expander(f"🚨 {alert['type']} - {alert['user_id']} - {alert['severity']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Description:** {alert['description']}")
                    st.write(f"**Department:** {alert['department']}")
                    st.write(f"**Recommended Action:** {alert['recommended_action']}")
                with col2:
                    st.selectbox("Status", ["New", "Investigating", "Resolved"], 
                               key=f"status_{alert['alert_id']}", index=0)
                    if st.button("Take Action", key=f"action_{alert['alert_id']}"):
                        st.success(f"Action initiated for {alert['alert_id']}")
    else:
        st.success("No critical alerts at this time")

def show_user_access_monitoring(platform):
    """Display user access monitoring interface"""
    st.header("User Access Monitoring & Analytics")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        department_filter = st.multiselect("Department", platform.departments, default=platform.departments)
    with col2:
        role_filter = st.multiselect("Role", list(platform.roles.keys()), default=list(platform.roles.keys()))
    with col3:
        status_filter = st.multiselect("Status", ["active", "inactive"], default=["active"])
    
    # Filter users
    filtered_users = [u for u in platform.users.values() 
                     if u["department"] in department_filter and 
                     u["role"] in role_filter and 
                     u["status"] in status_filter]
    
    # User metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Filtered Users", len(filtered_users))
    col2.metric("With MFA", len([u for u in filtered_users if u["mfa_enabled"]]))
    col3.metric("Sensitive Access", len([u for u in filtered_users if u["sensitive_access"]]))
    col4.metric("Avg Days Since Login", 
               f"{np.mean([(datetime.now() - (u['last_login'] or datetime.now())).days for u in filtered_users]):.1f}")
    
    # User access table
    st.subheader("User Access Details")
    user_df = pd.DataFrame(filtered_users)
    if not user_df.empty:
        # Select columns to display
        display_columns = ["user_id", "first_name", "last_name", "department", "role", "status", "mfa_enabled", "last_login"]
        st.dataframe(user_df[display_columns])
    
    # Access pattern analysis
    st.subheader("Access Pattern Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Department-wise access distribution
        dept_access = pd.DataFrame(platform.access_logs)
        if not dept_access.empty:
            dept_access['user_dept'] = dept_access['user_id'].map(lambda x: platform.users[x]['department'])
            dept_counts = dept_access['user_dept'].value_counts()
            fig1 = px.bar(x=dept_counts.values, y=dept_counts.index, orientation='h',
                         title="Access Count by Department")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Application access heatmap
        app_access = dept_access.groupby(['user_dept', 'application']).size().reset_index(name='count')
        fig2 = px.density_heatmap(app_access, x='user_dept', y='application', z='count',
                                 title="Department vs Application Access Heatmap")
        st.plotly_chart(fig2, use_container_width=True)

def show_privileged_access_management(platform):
    """Display privileged access management interface"""
    st.header("Privileged Access Management")
    
    # PAM metrics
    col1, col2, col3, col4 = st.columns(4)
    
    privileged_sessions = platform.privileged_sessions
    col1.metric("Privileged Sessions", len(privileged_sessions))
    col2.metric("Active Privileged Users", len(set([s["user_id"] for s in privileged_sessions])))
    col3.metric("Avg Session Duration", f"{np.mean([s['session_duration'] for s in privileged_sessions])/60:.1f} min")
    col4.metric("Sensitive Operations", sum([s['sensitive_operations'] for s in privileged_sessions]))
    
    # Privileged session monitoring
    st.subheader("Privileged Session Monitoring")
    
    if privileged_sessions:
        session_df = pd.DataFrame(privileged_sessions)
        st.dataframe(session_df)
        
        # Session analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Session duration distribution
            fig1 = px.histogram(session_df, x='session_duration', nbins=20,
                              title="Privileged Session Duration Distribution")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Sensitive operations by application
            sensitive_ops = session_df.groupby('application')['sensitive_operations'].sum().reset_index()
            fig2 = px.bar(sensitive_ops, x='application', y='sensitive_operations',
                         title="Sensitive Operations by Application")
            st.plotly_chart(fig2, use_container_width=True)
    
    # Just-in-Time access requests (simulated)
    st.subheader("Just-in-Time Access Requests")
    
    # Simulate JIT access requests
    jit_requests = [
        {
            "request_id": f"JIT_{i:04d}",
            "user_id": random.choice(list(platform.users.keys())),
            "application": random.choice(["Admin Console", "Financial Database", "HR System"]),
            "privilege_level": random.choice(["admin", "super_user"]),
            "requested_duration": random.choice([2, 4, 8, 24]),
            "justification": random.choice(["Emergency maintenance", "User support", "System update"]),
            "status": random.choice(["pending", "approved", "denied"]),
            "request_time": datetime.now() - timedelta(hours=random.randint(1, 24))
        }
        for i in range(10)
    ]
    
    jit_df = pd.DataFrame(jit_requests)
    st.dataframe(jit_df)
    
    # JIT access approval workflow
    st.subheader("Access Approval Workflow")
    if st.button("Generate New Access Request"):
        st.info("New access request workflow initiated")
        # In real implementation, this would trigger an approval workflow

def show_security_alerts(platform):
    """Display security alerts and incident management"""
    st.header("Security Alerts & Incident Management")
    
    # Alert summary
    total_alerts = len(platform.iam_alerts)
    alert_df = pd.DataFrame(platform.iam_alerts)
    
    if not alert_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Alerts", total_alerts)
        col2.metric("Critical", len(alert_df[alert_df['severity'] == 'Critical']))
        col3.metric("High", len(alert_df[alert_df['severity'] == 'High']))
        col4.metric("Medium", len(alert_df[alert_df['severity'] == 'Medium']))
    
    # Alert management interface
    st.subheader("Alert Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_filter = st.multiselect("Severity", ["Critical", "High", "Medium", "Low"], 
                                       default=["Critical", "High"])
    with col2:
        status_filter = st.multiselect("Status", ["New", "Investigating", "Resolved"], default=["New"])
    with col3:
        type_filter = st.multiselect("Alert Type", 
                                   list(set(a['type'] for a in platform.iam_alerts)) if platform.iam_alerts else [],
                                   default=list(set(a['type'] for a in platform.iam_alerts)) if platform.iam_alerts else [])
    
    # Filter alerts
    filtered_alerts = [a for a in platform.iam_alerts 
                      if a['severity'] in severity_filter and 
                      a['status'] in status_filter and 
                      a['type'] in type_filter]
    
    # Display alerts
    for alert in filtered_alerts:
        alert_class = "alert-critical" if alert['severity'] == 'Critical' else \
                     "alert-high" if alert['severity'] == 'High' else "alert-medium"
        
        with st.container():
            st.markdown(f'<div class="{alert_class}">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{alert['type']}** - {alert['user_id']}")
                st.write(alert['description'])
            
            with col2:
                st.write(f"**Department:** {alert['department']}")
                st.write(f"**Recommended:** {alert['recommended_action']}")
            
            with col3:
                new_status = st.selectbox("Status", ["New", "Investigating", "Resolved"], 
                                        key=f"status_{alert['alert_id']}",
                                        index=["New", "Investigating", "Resolved"].index(alert['status']))
                if new_status != alert['status']:
                    alert['status'] = new_status
                
                if st.button("Investigate", key=f"investigate_{alert['alert_id']}"):
                    st.success(f"Investigation started for {alert['alert_id']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("---")
    
    # Alert trends
    st.subheader("Alert Trends & Analytics")
    
    if platform.iam_alerts:
        col1, col2 = st.columns(2)
        
        with col1:
            # Alert trend over time
            alert_dates = [a['timestamp'].date() for a in platform.iam_alerts]
            date_counts = pd.Series(alert_dates).value_counts().sort_index()
            fig1 = px.line(x=date_counts.index, y=date_counts.values, 
                          title="Daily Alert Trend")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Alert by department
            dept_alerts = pd.DataFrame(platform.iam_alerts)
            dept_alerts['department'] = dept_alerts['user_id'].map(lambda x: platform.users[x]['department'])
            dept_counts = dept_alerts['department'].value_counts()
            fig2 = px.bar(x=dept_counts.values, y=dept_counts.index, orientation='h',
                         title="Alerts by Department")
            st.plotly_chart(fig2, use_container_width=True)

def show_access_certification(platform):
    """Display access certification and review interface"""
    st.header("Access Certification & Reviews")
    
    # Access review status
    st.subheader("Access Review Campaigns")
    
    for review in platform.access_reviews:
        completion_rate = (review["reviewers_completed"] / review["reviewers_required"]) * 100
        
        with st.expander(f"📋 {review['name']} - {review['status'].upper()}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Due Date", review["due_date"].strftime("%Y-%m-%d"))
            col2.metric("Completion", f"{completion_rate:.1f}%")
            col3.metric("Users in Scope", review["users_in_scope"])
            
            # Progress bar
            st.progress(review["reviewers_completed"] / review["reviewers_required"])
            
            if st.button("Start Review", key=f"review_{review['review_id']}"):
                st.success(f"Access review {review['review_id']} initiated")
    
    # User access certification interface
    st.subheader("User Access Certification")
    
    # Select users for certification
    cert_users = st.multiselect("Select Users for Certification", 
                               [f"{u['user_id']} - {u['first_name']} {u['last_name']}" 
                                for u in platform.users.values() if u["sensitive_access"]])
    
    if cert_users and st.button("Generate Certification Report"):
        st.success(f"Access certification report generated for {len(cert_users)} users")
        
        # Display certification details
        for user_str in cert_users:
            user_id = user_str.split(" - ")[0]
            user = platform.users[user_id]
            
            with st.expander(f"User: {user['first_name']} {user['last_name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Current Access:**")
                    st.write(f"- Role: {user['role']}")
                    st.write(f"- Department: {user['department']}")
                    st.write(f"- MFA Enabled: {user['mfa_enabled']}")
                    st.write(f"- Last Login: {user['last_login']}")
                
                with col2:
                    st.write("**Certification Actions:**")
                    cert_status = st.selectbox("Certification Status", 
                                            ["Approved", "Revoked", "Modified", "Pending"],
                                            key=f"cert_{user_id}")
                    st.text_area("Comments", key=f"comments_{user_id}")
                    
                    if st.button("Submit Certification", key=f"submit_{user_id}"):
                        st.success(f"Access certified for {user_id}")

def show_compliance_audit(platform):
    """Display compliance and audit reporting"""
    st.header("Compliance & Audit Reporting")
    
    # Compliance status overview
    st.subheader("Compliance Status")
    
    for check in platform.compliance_checks:
        status_color = "🟢" if check["status"] == "PASS" else "🔴"
        
        with st.expander(f"{status_color} {check['name']} - {check['status']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Description:** {check['description']}")
                st.write(f"**Severity:** {check['severity']}")
                st.write(f"**Remediation:** {check['remediation']}")
            with col2:
                if check["status"] == "FAIL":
                    if st.button("Remediate", key=f"remediate_{check['check_id']}"):
                        st.success(f"Remediation initiated for {check['check_id']}")
    
    # Audit trail
    st.subheader("Access Audit Trail")
    
    # Generate comprehensive audit trail
    audit_events = []
    for log in platform.access_logs[:1000]:  # Sample for performance
        user = platform.users[log["user_id"]]
        audit_events.append({
            "timestamp": log["timestamp"],
            "user_id": log["user_id"],
            "user_name": f"{user['first_name']} {user['last_name']}",
            "department": user["department"],
            "action": log["action"],
            "application": log["application"],
            "resource": log["resource"],
            "location": log["location"],
            "success": log["success"],
            "risk_score": log["risk_score"]
        })
    
    audit_df = pd.DataFrame(audit_events)
    if not audit_df.empty:
        # Filters for audit trail
        col1, col2, col3 = st.columns(3)
        with col1:
            audit_dept = st.multiselect("Department", platform.departments, key="audit_dept")
        with col2:
            audit_action = st.multiselect("Action", list(set(audit_df['action'])), key="audit_action")
        with col3:
            min_risk = st.slider("Minimum Risk Score", 0, 100, 0)
        
        # Apply filters
        filtered_audit = audit_df
        if audit_dept:
            filtered_audit = filtered_audit[filtered_audit['department'].isin(audit_dept)]
        if audit_action:
            filtered_audit = filtered_audit[filtered_audit['action'].isin(audit_action)]
        filtered_audit = filtered_audit[filtered_audit['risk_score'] >= min_risk]
        
        st.dataframe(filtered_audit.sort_values('timestamp', ascending=False))
    
    # Compliance reporting
    st.subheader("Compliance Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Generate SOC 2 Report"):
            st.success("SOC 2 compliance report generated")
            # In real implementation, this would generate a detailed report
    
    with col2:
        if st.button("Generate SOX Report"):
            st.success("SOX compliance report generated")
    
    with col3:
        if st.button("Generate GDPR Report"):
            st.success("GDPR compliance report generated")

def show_zero_trust_policy(platform):
    """Display zero-trust policy management"""
    st.header("Zero-Trust Policy Engine")
    
    # Current policy rules
    st.subheader("Active Zero-Trust Policies")
    policy_df = pd.DataFrame(platform.zero_trust_rules)
    st.dataframe(policy_df)
    
    # Policy effectiveness analytics
    st.subheader("Policy Effectiveness")
    
    # Simulate policy violation tracking
    policy_violations = {}
    for rule in platform.zero_trust_rules:
        violation_count = random.randint(5, 50)  # Simulated data
        policy_violations[rule["name"]] = violation_count
    
    if policy_violations:
        fig = px.bar(x=list(policy_violations.values()), y=list(policy_violations.keys()),
                    orientation='h', title="Policy Violations by Rule")
        st.plotly_chart(fig, use_container_width=True)
    
    # Policy management interface
    st.subheader("Policy Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Add New Policy Rule**")
        with st.form("add_policy_form"):
            rule_name = st.text_input("Rule Name")
            condition = st.selectbox("Condition", [
                "location != 'corporate_network'",
                "failed_logins >= 3",
                "device_change == True", 
                "country_change == True",
                "sensitive_access == True",
                "hour < 6 or hour > 22",
                "role_changed == True"
            ])
            action = st.selectbox("Action", [
                "require_2fa",
                "block_temporary", 
                "flag_review",
                "require_approval",
                "log_and_alert",
                "block_and_alert"
            ])
            priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
            
            if st.form_submit_button("Add Policy Rule"):
                new_rule = {
                    "id": len(platform.zero_trust_rules) + 1,
                    "name": rule_name,
                    "condition": condition,
                    "action": action,
                    "priority": priority
                }
                platform.zero_trust_rules.append(new_rule)
                st.success("Policy rule added successfully!")
    
    with col2:
        st.write("**Policy Simulation**")
        st.info("Test policy effectiveness with simulated scenarios")
        
        scenario = st.selectbox("Test Scenario", [
            "External access attempt",
            "After-hours privileged access", 
            "Multiple failed logins",
            "Geographic anomaly",
            "Role change detection"
        ])
        
        if st.button("Run Policy Simulation"):
            st.success(f"Policy simulation completed for: {scenario}")
            # In real implementation, this would run actual policy simulations

def show_analytics_reporting(platform):
    """Display advanced analytics and reporting"""
    st.header("Advanced Analytics & Reporting")
    
    # Comprehensive analytics dashboard
    st.subheader("IAM Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk score distribution
        risk_scores = [log["risk_score"] for log in platform.access_logs]
        fig1 = px.histogram(x=risk_scores, nbins=20, title="Risk Score Distribution")
        st.plotly_chart(fig1, use_container_width=True)
        
        # User access frequency
        user_access_count = {}
        for log in platform.access_logs:
            user_id = log["user_id"]
            user_access_count[user_id] = user_access_count.get(user_id, 0) + 1
        
        top_users = sorted(user_access_count.items(), key=lambda x: x[1], reverse=True)[:10]
        fig3 = px.bar(x=[count for _, count in top_users], 
                     y=[platform.users[user_id]["first_name"] + " " + platform.users[user_id]["last_name"] 
                        for user_id, _ in top_users],
                     orientation='h', title="Top 10 Users by Access Frequency")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Access pattern by day of week
        access_days = [log["timestamp"].weekday() for log in platform.access_logs]
        day_counts = pd.Series(access_days).value_counts().sort_index()
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        fig2 = px.bar(x=[day_names[i] for i in day_counts.index], y=day_counts.values,
                     title="Access Patterns by Day of Week")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Department risk comparison
        dept_risk = {}
        for log in platform.access_logs:
            dept = platform.users[log["user_id"]]["department"]
            if dept not in dept_risk:
                dept_risk[dept] = []
            dept_risk[dept].append(log["risk_score"])
        
        avg_dept_risk = {dept: np.mean(scores) for dept, scores in dept_risk.items()}
        fig4 = px.bar(x=list(avg_dept_risk.values()), y=list(avg_dept_risk.keys()),
                     orientation='h', title="Average Risk Score by Department")
        st.plotly_chart(fig4, use_container_width=True)
    
    # Advanced reporting
    st.subheader("Advanced Reports")
    
    report_type = st.selectbox("Select Report Type", [
        "User Access Review Report",
        "Privileged Access Audit", 
        "Compliance Status Report",
        "Security Incident Report",
        "Risk Assessment Report"
    ])
    
    date_range = st.date_input("Report Date Range", [])
    
    if st.button("Generate Advanced Report"):
        st.success(f"Advanced {report_type} generated for selected period")
        
        # Display sample report (in real implementation, this would be a detailed report)
        st.subheader(f"Sample: {report_type}")
        
        if "User Access Review" in report_type:
            st.write("""
            **Key Findings:**
            - 95% of users have appropriate access levels
            - 5 users require access review due to role changes
            - 2 users have excessive permissions that need remediation
            
            **Recommendations:**
            1. Review and adjust access for identified users
            2. Implement quarterly access reviews
            3. Enhance role-based access controls
            """)
        elif "Privileged Access" in report_type:
            st.write("Privileged access audit report content...")
        elif "Compliance" in report_type:
            st.write("Compliance status report content...")

if __name__ == "__main__":
    main()
