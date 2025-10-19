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
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Zero-Trust Fintech SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

class ZeroTrustFintechSOC:
    def __init__(self):
        self.transaction_logs = []
        self.user_behavior_logs = []
        self.alerts = []
        self.roles = {}
        self.zero_trust_rules = []
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize sample data and rules"""
        # Sample roles
        self.roles = {
            "admin": {"permissions": ["all"], "risk_level": "low"},
            "trader": {"permissions": ["trade", "view_portfolio"], "risk_level": "medium"},
            "analyst": {"permissions": ["view_reports", "view_data"], "risk_level": "low"},
            "customer_support": {"permissions": ["view_customer_data", "process_refunds"], "risk_level": "high"}
        }
        
        # Zero-trust rules
        self.zero_trust_rules = [
            {"id": 1, "name": "External Login", "condition": "location != 'internal'", "action": "require_2fa"},
            {"id": 2, "name": "Large Transaction", "condition": "amount > 10000", "action": "require_approval"},
            {"id": 3, "name": "Unusual Time", "condition": "hour < 6 or hour > 22", "action": "flag_review"},
            {"id": 4, "name": "Multiple Failed Logins", "condition": "failed_logins >= 3", "action": "block_account"},
            {"id": 5, "name": "New Device", "condition": "device_change == True", "action": "require_2fa"}
        ]
        
        # Generate sample transaction logs
        self.generate_sample_transactions()
        
        # Generate sample user behavior logs
        self.generate_sample_user_behavior()
        
        # Generate initial alerts
        self.run_anomaly_detection()
    
    def generate_sample_transactions(self):
        """Generate sample transaction data"""
        users = ["user_001", "user_002", "user_003", "user_004", "user_005"]
        transaction_types = ["transfer", "payment", "withdrawal", "deposit", "trade"]
        locations = ["internal", "external", "mobile", "web"]
        
        for i in range(1000):
            user = random.choice(users)
            transaction_type = random.choice(transaction_types)
            amount = random.randint(10, 50000)
            location = random.choice(locations)
            
            # Create some anomalies
            is_anomaly = False
            if random.random() < 0.05:  # 5% anomalies
                amount = random.randint(50000, 100000)  # Unusually large amount
                is_anomaly = True
            
            timestamp = datetime.now() - timedelta(hours=random.randint(0, 720))
            
            self.transaction_logs.append({
                "id": f"tx_{i:06d}",
                "user_id": user,
                "timestamp": timestamp,
                "type": transaction_type,
                "amount": amount,
                "location": location,
                "status": "completed",
                "risk_score": random.randint(0, 100),
                "is_anomaly": is_anomaly,
                "rule_violations": []
            })
    
    def generate_sample_user_behavior(self):
        """Generate sample user behavior data"""
        users = ["user_001", "user_002", "user_003", "user_004", "user_005"]
        actions = ["login", "logout", "view_account", "make_transfer", "view_statement", "change_settings"]
        devices = ["desktop_internal", "mobile_ios", "mobile_android", "tablet"]
        locations = ["192.168.1.1", "10.0.0.1", "external_ip_1", "external_ip_2"]
        
        for i in range(2000):
            user = random.choice(users)
            action = random.choice(actions)
            device = random.choice(devices)
            location = random.choice(locations)
            
            # Create some suspicious behavior
            is_suspicious = False
            if random.random() < 0.03:  # 3% suspicious activities
                action = random.choice(["login", "make_transfer"])
                device = "new_device"
                is_suspicious = True
            
            timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10080))
            
            self.user_behavior_logs.append({
                "id": f"behav_{i:06d}",
                "user_id": user,
                "timestamp": timestamp,
                "action": action,
                "device": device,
                "location": location,
                "session_duration": random.randint(1, 3600),
                "is_suspicious": is_suspicious
            })
    
    def run_anomaly_detection(self):
        """Run anomaly detection on transactions and user behavior"""
        self.alerts = []
        
        # Analyze transactions for anomalies
        for tx in self.transaction_logs:
            risk_factors = []
            
            # Large amount detection
            if tx["amount"] > 25000:
                risk_factors.append("Large transaction amount")
                tx["rule_violations"].append("Large Transaction")
            
            # Unusual location
            if tx["location"] == "external" and tx["amount"] > 5000:
                risk_factors.append("External large transaction")
                tx["rule_violations"].append("External Login")
            
            if risk_factors:
                self.alerts.append({
                    "id": f"alert_{len(self.alerts):06d}",
                    "timestamp": tx["timestamp"],
                    "type": "Transaction Anomaly",
                    "severity": "High" if tx["amount"] > 25000 else "Medium",
                    "user_id": tx["user_id"],
                    "description": f"Anomalous transaction: {', '.join(risk_factors)}",
                    "amount": tx["amount"],
                    "status": "New"
                })
        
        # Analyze user behavior for anomalies
        for behav in self.user_behavior_logs:
            risk_factors = []
            
            # New device detection
            if behav["device"] == "new_device":
                risk_factors.append("Login from new device")
            
            # Unusual time activity
            hour = behav["timestamp"].hour
            if hour < 6 or hour > 22:
                risk_factors.append("Activity during unusual hours")
            
            if risk_factors:
                self.alerts.append({
                    "id": f"alert_{len(self.alerts):06d}",
                    "timestamp": behav["timestamp"],
                    "type": "Behavioral Anomaly",
                    "severity": "Medium",
                    "user_id": behav["user_id"],
                    "description": f"Suspicious behavior: {', '.join(risk_factors)}",
                    "amount": None,
                    "status": "New"
                })
    
    def detect_data_poisoning(self, data_batch):
        """Detect potential data poisoning attempts"""
        poisoning_signals = []
        
        # Check for statistical anomalies in the data batch
        if len(data_batch) > 10:
            amounts = [item.get('amount', 0) for item in data_batch if item.get('amount')]
            if amounts:
                mean_amount = np.mean(amounts)
                std_amount = np.std(amounts)
                
                # Flag if too many outliers
                outliers = [amt for amt in amounts if abs(amt - mean_amount) > 3 * std_amount]
                if len(outliers) > len(amounts) * 0.3:  # 30% outliers
                    poisoning_signals.append("High rate of statistical outliers")
        
        return poisoning_signals
    
    def apply_zero_trust_rule(self, transaction, user_behavior):
        """Apply zero-trust rules to a transaction"""
        violations = []
        
        for rule in self.zero_trust_rules:
            if rule["condition"] == "location != 'internal'" and transaction["location"] != "internal":
                violations.append(rule["name"])
            elif rule["condition"] == "amount > 10000" and transaction["amount"] > 10000:
                violations.append(rule["name"])
            elif rule["condition"] == "hour < 6 or hour > 22":
                hour = transaction["timestamp"].hour
                if hour < 6 or hour > 22:
                    violations.append(rule["name"])
        
        return violations

def main():
    st.title("🛡️ Zero-Trust Fintech Security Operations Center")
    st.markdown("### Advanced Behavioral Analytics & Threat Detection Platform")
    
    # Initialize session state
    if 'soc' not in st.session_state:
        st.session_state.soc = ZeroTrustFintechSOC()
    
    soc = st.session_state.soc
    
    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/96/000000/security-checked.png", width=80)
    st.sidebar.title("Security Dashboard")
    
    # Navigation
    page = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "🔍 Transaction Monitoring",
        "👤 User Behavior Analytics",
        "🚨 Threat Alerts",
        "⚙️ Policy Management",
        "🛡️ Data Poisoning Defense"
    ])
    
    if page == "📊 Dashboard":
        show_dashboard(soc)
    elif page == "🔍 Transaction Monitoring":
        show_transaction_monitoring(soc)
    elif page == "👤 User Behavior Analytics":
        show_user_behavior_analytics(soc)
    elif page == "🚨 Threat Alerts":
        show_threat_alerts(soc)
    elif page == "⚙️ Policy Management":
        show_policy_management(soc)
    elif page == "🛡️ Data Poisoning Defense":
        show_data_poisoning_defense(soc)

def show_dashboard(soc):
    """Display the main dashboard"""
    st.header("Security Overview Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_alerts = len(soc.alerts)
        st.metric("Total Alerts", total_alerts, delta=f"{len([a for a in soc.alerts if a['status'] == 'New'])} new")
    
    with col2:
        high_risk_alerts = len([a for a in soc.alerts if a['severity'] == 'High'])
        st.metric("High Risk Alerts", high_risk_alerts, delta="Priority")
    
    with col3:
        suspicious_users = len(set([a['user_id'] for a in soc.alerts]))
        st.metric("Suspicious Users", suspicious_users)
    
    with col4:
        avg_risk_score = np.mean([tx['risk_score'] for tx in soc.transaction_logs])
        st.metric("Average Risk Score", f"{avg_risk_score:.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Alert severity distribution
        severity_counts = pd.DataFrame(soc.alerts)['severity'].value_counts()
        fig1 = px.pie(values=severity_counts.values, names=severity_counts.index, 
                     title="Alert Severity Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Risk heatmap by hour
        transaction_hours = [tx['timestamp'].hour for tx in soc.transaction_logs]
        risk_scores = [tx['risk_score'] for tx in soc.transaction_logs]
        
        heatmap_data = pd.DataFrame({
            'hour': transaction_hours,
            'risk_score': risk_scores
        })
        
        hourly_risk = heatmap_data.groupby('hour')['risk_score'].mean().reset_index()
        fig2 = px.bar(hourly_risk, x='hour', y='risk_score', 
                     title="Average Risk Score by Hour")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent alerts table
    st.subheader("Recent High-Priority Alerts")
    recent_alerts = sorted(soc.alerts, key=lambda x: x['timestamp'], reverse=True)[:10]
    alerts_df = pd.DataFrame(recent_alerts)
    if not alerts_df.empty:
        st.dataframe(alerts_df[['timestamp', 'type', 'severity', 'user_id', 'description']])
    else:
        st.info("No alerts generated yet.")

def show_transaction_monitoring(soc):
    """Display transaction monitoring interface"""
    st.header("Transaction Monitoring & Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_amount = st.number_input("Min Amount", value=0)
    with col2:
        max_amount = st.number_input("Max Amount", value=50000)
    with col3:
        selected_location = st.selectbox("Location", ["All", "internal", "external", "mobile", "web"])
    
    # Filter transactions
    filtered_tx = [tx for tx in soc.transaction_logs 
                  if min_amount <= tx['amount'] <= max_amount and
                  (selected_location == "All" or tx['location'] == selected_location)]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", len(filtered_tx))
    col2.metric("Anomalous Transactions", len([tx for tx in filtered_tx if tx['is_anomaly']]))
    col3.metric("Total Amount", f"${sum(tx['amount'] for tx in filtered_tx):,}")
    col4.metric("Avg Risk Score", f"{np.mean([tx['risk_score'] for tx in filtered_tx]):.1f}")
    
    # Transaction table
    st.subheader("Transaction Logs")
    tx_df = pd.DataFrame(filtered_tx[:100])  # Show first 100
    if not tx_df.empty:
        st.dataframe(tx_df[['timestamp', 'user_id', 'type', 'amount', 'location', 'risk_score', 'is_anomaly']])
    
    # Risk visualization
    st.subheader("Transaction Risk Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution
        risk_bins = pd.cut([tx['risk_score'] for tx in filtered_tx], bins=5)
        risk_dist = risk_bins.value_counts().sort_index()
        fig1 = px.bar(x=risk_dist.index.astype(str), y=risk_dist.values,
                     title="Risk Score Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Amount vs Risk scatter
        fig2 = px.scatter(tx_df, x='amount', y='risk_score', color='is_anomaly',
                         title="Amount vs Risk Score", hover_data=['user_id'])
        st.plotly_chart(fig2, use_container_width=True)

def show_user_behavior_analytics(soc):
    """Display user behavior analytics"""
    st.header("User Behavior Analytics")
    
    # Behavior insights
    st.subheader("Behavioral Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Action distribution
        action_counts = pd.DataFrame(soc.user_behavior_logs)['action'].value_counts()
        fig1 = px.bar(x=action_counts.values, y=action_counts.index, orientation='h',
                     title="User Actions Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Suspicious activity by user
        suspicious_by_user = {}
        for behav in soc.user_behavior_logs:
            if behav['is_suspicious']:
                user = behav['user_id']
                suspicious_by_user[user] = suspicious_by_user.get(user, 0) + 1
        
        if suspicious_by_user:
            fig2 = px.bar(x=list(suspicious_by_user.values()), y=list(suspicious_by_user.keys()),
                         title="Suspicious Activities by User", orientation='h')
            st.plotly_chart(fig2, use_container_width=True)
    
    # User session analysis
    st.subheader("Session Analysis")
    session_data = []
    for behav in soc.user_behavior_logs:
        if behav['action'] == 'login':
            session_data.append({
                'user_id': behav['user_id'],
                'device': behav['device'],
                'session_duration': behav['session_duration'],
                'location': behav['location']
            })
    
    if session_data:
        session_df = pd.DataFrame(session_data)
        col1, col2 = st.columns(2)
        
        with col1:
            avg_duration_by_device = session_df.groupby('device')['session_duration'].mean()
            fig3 = px.bar(avg_duration_by_device, title="Average Session Duration by Device")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            sessions_by_hour = [behav['timestamp'].hour for behav in soc.user_behavior_logs if behav['action'] == 'login']
            hour_counts = pd.Series(sessions_by_hour).value_counts().sort_index()
            fig4 = px.line(x=hour_counts.index, y=hour_counts.values, 
                          title="Login Activity by Hour")
            st.plotly_chart(fig4, use_container_width=True)

def show_threat_alerts(soc):
    """Display threat alerts and management"""
    st.header("Threat Alerts & Incident Management")
    
    # Alert filters
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_filter = st.multiselect("Severity", ["High", "Medium", "Low"], default=["High", "Medium"])
    with col2:
        type_filter = st.multiselect("Alert Type", list(set(a['type'] for a in soc.alerts)), 
                                   default=list(set(a['type'] for a in soc.alerts)))
    with col3:
        status_filter = st.multiselect("Status", ["New", "In Progress", "Resolved"], default=["New"])
    
    # Filter alerts
    filtered_alerts = [a for a in soc.alerts 
                      if a['severity'] in severity_filter and 
                      a['type'] in type_filter and 
                      a['status'] in status_filter]
    
    # Alert management
    st.subheader(f"Alerts ({len(filtered_alerts)})")
    
    for alert in filtered_alerts:
        with st.expander(f"🚨 {alert['type']} - {alert['user_id']} - {alert['severity']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Description:** {alert['description']}")
                st.write(f"**Timestamp:** {alert['timestamp']}")
                st.write(f"**Amount:** {alert['amount'] if alert['amount'] else 'N/A'}")
            with col2:
                new_status = st.selectbox("Status", ["New", "In Progress", "Resolved"], 
                                        key=f"status_{alert['id']}",
                                        index=["New", "In Progress", "Resolved"].index(alert['status']))
                if new_status != alert['status']:
                    alert['status'] = new_status
                if st.button("Take Action", key=f"action_{alert['id']}"):
                    st.success(f"Action taken on alert {alert['id']}")
    
    # Alert statistics
    st.subheader("Alert Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Alert trend (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_alerts = [a for a in soc.alerts if a['timestamp'] > seven_days_ago]
        
        if recent_alerts:
            alert_dates = [a['timestamp'].date() for a in recent_alerts]
            date_counts = pd.Series(alert_dates).value_counts().sort_index()
            fig1 = px.line(x=date_counts.index, y=date_counts.values, 
                          title="Alerts Trend (Last 7 Days)")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Alert by type
        alert_type_counts = pd.DataFrame(soc.alerts)['type'].value_counts()
        fig2 = px.pie(values=alert_type_counts.values, names=alert_type_counts.index,
                     title="Alerts by Type")
        st.plotly_chart(fig2, use_container_width=True)

def show_policy_management(soc):
    """Display zero-trust policy management"""
    st.header("Zero-Trust Policy Management")
    
    # Current rules
    st.subheader("Active Zero-Trust Rules")
    rules_df = pd.DataFrame(soc.zero_trust_rules)
    st.dataframe(rules_df)
    
    # Rule violations analysis
    st.subheader("Rule Violations Analysis")
    
    # Count violations from transactions
    violation_counts = {}
    for tx in soc.transaction_logs:
        for violation in tx['rule_violations']:
            violation_counts[violation] = violation_counts.get(violation, 0) + 1
    
    if violation_counts:
        fig = px.bar(x=list(violation_counts.values()), y=list(violation_counts.keys()),
                    orientation='h', title="Rule Violations Count")
        st.plotly_chart(fig, use_container_width=True)
    
    # Add new rule
    st.subheader("Add New Zero-Trust Rule")
    
    with st.form("add_rule_form"):
        col1, col2 = st.columns(2)
        with col1:
            rule_name = st.text_input("Rule Name")
            condition = st.selectbox("Condition", [
                "location != 'internal'",
                "amount > 10000", 
                "hour < 6 or hour > 22",
                "failed_logins >= 3",
                "device_change == True"
            ])
        with col2:
            action = st.selectbox("Action", [
                "require_2fa",
                "require_approval", 
                "flag_review",
                "block_account",
                "notify_security"
            ])
        
        if st.form_submit_button("Add Rule"):
            new_rule = {
                "id": len(soc.zero_trust_rules) + 1,
                "name": rule_name,
                "condition": condition,
                "action": action
            }
            soc.zero_trust_rules.append(new_rule)
            st.success("Rule added successfully!")
    
    # Role management
    st.subheader("Role-Based Access Control")
    roles_df = pd.DataFrame.from_dict(soc.roles, orient='index')
    st.dataframe(roles_df)

def show_data_poisoning_defense(soc):
    """Display data poisoning detection and defense"""
    st.header("🛡️ Advanced Data Poisoning Defense")
    st.markdown("""
    This module detects attempts to poison training data or manipulate behavioral models
    by identifying statistical anomalies and suspicious patterns in data streams.
    """)
    
    # Simulate data batches for poisoning detection
    st.subheader("Data Stream Analysis")
    
    # Generate sample data batches
    data_batches = []
    for i in range(5):
        batch_size = random.randint(50, 200)
        batch = []
        for j in range(batch_size):
            # Introduce some poisoning in one batch
            if i == 2 and random.random() < 0.4:  # 40% poisoned data in batch 2
                amount = random.randint(50000, 100000)  # Abnormal amounts
            else:
                amount = random.randint(10, 5000)
            
            batch.append({
                'transaction_id': f"batch_{i}_tx_{j}",
                'amount': amount,
                'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 10080)),
                'user_id': f"user_{random.randint(1, 20)}"
            })
        data_batches.append(batch)
    
    # Analyze each batch for poisoning
    poisoning_results = []
    for i, batch in enumerate(data_batches):
        signals = soc.detect_data_poisoning(batch)
        is_poisoned = len(signals) > 0
        poisoning_results.append({
            'batch_id': i,
            'size': len(batch),
            'is_poisoned': is_poisoned,
            'signals': signals,
            'avg_amount': np.mean([item['amount'] for item in batch])
        })
    
    # Display results
    results_df = pd.DataFrame(poisoning_results)
    st.dataframe(results_df)
    
    # Poisoning detection visualization
    st.subheader("Poisoning Detection Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Batch analysis
        fig1 = px.bar(results_df, x='batch_id', y='avg_amount', color='is_poisoned',
                     title="Average Amount by Batch (Poisoning Indicator)")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Statistical distribution
        all_amounts = [item['amount'] for batch in data_batches for item in batch]
        fig2 = px.histogram(x=all_amounts, nbins=50, 
                           title="Transaction Amount Distribution")
        fig2.add_vline(x=np.mean(all_amounts), line_dash="dash", line_color="red",
                      annotation_text="Mean")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Defense recommendations
    st.subheader("Defense Recommendations")
    
    poisoned_batches = [r for r in poisoning_results if r['is_poisoned']]
    if poisoned_batches:
        st.error("🚨 Potential data poisoning detected!")
        st.write("**Recommended actions:**")
        st.write("1. Quarantine affected data batches")
        st.write("2. Review data source integrity")
        st.write("3. Retrain models with clean data")
        st.write("4. Enhance input validation rules")
        st.write("5. Implement data provenance tracking")
    else:
        st.success("✅ No data poisoning detected in current analysis")

if __name__ == "__main__":
    main()
