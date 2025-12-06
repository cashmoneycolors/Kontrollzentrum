"""Frontend Dashboard - Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime
from core.database import SessionLocal, ModuleLog
from core.logging import logger

st.set_page_config(page_title="Kontrollzentrum Dashboard", layout="wide")
st.title("🤖 Kontrollzentrum Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Module Aktiv", "16", "+2")

with col2:
    st.metric("AI Vertrauen", "100%", "↑ 0%")

with col3:
    st.metric("Uptime", "99.9%", "↑ 0.1%")

st.divider()

tab1, tab2, tab3 = st.tabs(["Module", "Logs", "Performance"])

with tab1:
    st.subheader("Module Status")
    modules_data = {
        "Modul": ["ai_assistant", "data_analytics", "email_automation", "customer_crm"],
        "Status": ["✅ Active", "✅ Active", "✅ Active", "✅ Active"],
        "Vertrauen": ["100%", "100%", "100%", "100%"]
    }
    st.dataframe(pd.DataFrame(modules_data))

with tab2:
    st.subheader("System Logs")
    db = SessionLocal()
    logs = db.query(ModuleLog).order_by(ModuleLog.timestamp.desc()).limit(10).all()
    for log in logs:
        st.write(f"📝 {log.module_name}: {log.status} ({log.execution_time}ms)")

with tab3:
    st.subheader("Performance Metrics")
    st.line_chart({"CPU": [40, 42, 41, 43], "Memory": [256, 258, 260, 262]})

logger.info("Dashboard accessed")
