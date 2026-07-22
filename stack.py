import streamlit as st
import time
import json
import os
import plotly.graph_objects as go

# Try importing docker SDK safeguarding against environment mismatch
try:
    import docker
except ImportError:
    docker = None

# BACKEND CORE

class EnterpriseAIInvestigator:
    def __init__(self, json_file_path="error_database.json"):
        self.json_file_path = json_file_path
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        """Loads errors from an external JSON database file."""
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"Error loading JSON database: {str(e)}")
                return {}
        else:
            st.warning(f"⚠️ '{self.json_file_path}' not found. Initializing with an empty database.")
            return {}

    def run_multi_pipeline(self, raw_trace):
        # Dynamically reload JSON on every run to capture live updates
        self.knowledge_base = self.load_knowledge_base()
        
        detected_signatures = []
        detected_languages = set()

        for error_type, details in self.knowledge_base.items():
            if error_type in raw_trace:
                detected_signatures.append(error_type)
                lang = details.get("language", "Unknown")
                detected_languages.add(lang)
        
        if not detected_signatures:
            detected_signatures = ["RuntimeAnomaly"]
            detected_languages.add("Unknown")

        compiled_patches = {}
        total_health_impact = 100
        
        for sig in detected_signatures:
            matched_fix = self.knowledge_base.get(sig, {
                "language": "Unknown",
                "buggy_code": "Custom system reference line",
                "patched_code": "# Manual architectural review required for custom logic",
                "remedy": "Review custom variables and environment states."
            })
            compiled_patches[sig] = matched_fix
            total_health_impact -= 30 if sig != "RuntimeAnomaly" else 15

        return {
            "incident_id": f"INC-{int(time.time())}",
            "signatures": detected_signatures,
            "languages": list(detected_languages),
            "severity": "CRITICAL" if len(detected_signatures) > 1 else "HIGH",
            "patches": compiled_patches,
            "health_score": max(total_health_impact, 10)
        }

# Initialize Backend Agent
agent = EnterpriseAIInvestigator()

# DOCKER LIVE TELEMETRY INTEGRATION FUNCTION

def get_live_docker_logs():
    if not docker:
        return "Error: 'docker' package not installed. Please run 'pip install docker'."
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        
        for container in containers:
            raw_logs = container.logs().decode('utf-8')
            for error in agent.knowledge_base.keys():
                if error in raw_logs:
                    return raw_logs.strip()
        return "[-] Active Docker scan complete. No anomalous container traces detected."
    except Exception as e:
        return f"Docker Connection Error: Ensure Docker Desktop is running. Details: {str(e)}"

# FRONTEND CORE

st.set_page_config(page_title="AI Multi-Stack Investigator", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { 
        background: linear-gradient(45deg, #ff4b4b, #ff7676); 
        color: white; border: none; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 4px 15px rgba(255,75,75,0.4); }
    .metric-card {
        background-color: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .sig-tag {
        background-color: #ff4b4b22; color: #ff4b4b; border: 1px solid #ff4b4b;
        padding: 4px 10px; border-radius: 6px; font-weight: bold; margin-right: 5px; display: inline-block;
    }
    .code-box {
        background-color: #010409; border-left: 5px solid #ff4b4b;
        padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace;
    }
    .patch-box {
        background-color: #010409; border-left: 5px solid #238636;
        padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ PYTHON STACK INVESTIGATOR")
st.caption("Loaded Error Signatures from JSON Database")
st.markdown("---")

# Maintain state for logs using Streamlit Session State
if "log_content" not in st.session_state:
    st.session_state.log_content = "Paste logs here or click 'FETCH LIVE DOCKER LOGS' above."

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Log Ingestion Sandbox")
    
    if st.button("FETCH LIVE DOCKER LOGS"):
        with st.spinner("Connecting to Docker Engine API & harvesting logs..."):
            fetched_logs = get_live_docker_logs()
            st.session_state.log_content = fetched_logs
            st.toast("Docker logs harvested successfully!", icon="🐳")

    log_input = st.text_area("Complex Telemetry Log Dump", value=st.session_state.log_content, height=220)
    trigger_scan = st.button("DEPLOY PIPELINE SCANNER")

with col_right:
    st.subheader("Multi-Incident Diagnostics Panel")
    
    if trigger_scan:
        with st.spinner("Analyzing log telemetry for multi-language errors..."):
            time.sleep(1.2)
            report = agent.run_multi_pipeline(log_input)
        
        # 3 Metrics Display Area (Incident ID, Severity, Language)
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"<div class='metric-card'><b>INCIDENT ID</b><br><span style='color:#ff4b4b;font-size:18px;font-weight:bold;'>{report['incident_id']}</span></div>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"<div class='metric-card'><b>SEVERITY</b><br><span style='color:red;font-size:18px;font-weight:bold;'>{report['severity']}</span></div>", unsafe_allow_html=True)
        with m_col3:
            langs_str = ", ".join(report['languages'])
            st.markdown(f"<div class='metric-card'><b>LANGUAGE</b><br><span style='color:#2ea043;font-size:18px;font-weight:bold;'>{langs_str}</span></div>", unsafe_allow_html=True)
            
        st.write("")
        st.markdown("🔍 **Detected Error Signatures:**")
        
        sig_html = "".join([f"<span class='sig-tag'>{s}</span>" for s in report['signatures']])
        st.markdown(sig_html, unsafe_allow_html=True)
        st.write("")
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = report['health_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Aggregated Infrastructure Health State", 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#ff4b4b"},
                'steps': [
                    {'range': [0, 40], 'color': "#3a0f14"},
                    {'range': [40, 70], 'color': "#3e2b0f"},
                    {'range': [70, 100], 'color': "#112e17"}],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=180, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Awaiting multi-incident data stream.")

# MULTI-PATCH SELF-HEALING WORKBENCH WORKSPACE

st.markdown("---")
st.subheader("Dynamic Self-Healing Patch Workbench (Multi-Error Resolution)")

if trigger_scan:
    for signature, patch_info in report['patches'].items():
        lang = patch_info.get("language", "General")
        with st.expander(f"🛠️ Remediation Strategy for [{signature}] — Language: {lang}", expanded=True):
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown("**Broken Code Implementation:**")
                st.markdown(f"<div class='code-box'>{patch_info['buggy_code']}</div>", unsafe_allow_html=True)
            with p_col2:
                st.markdown("**AI Remediation Resolution Patch:**")
                st.markdown(f"<div class='patch-box'>{patch_info['patched_code']}</div>", unsafe_allow_html=True)
            st.info(f"💡 **AI Recommendation Matrix:** {patch_info['remedy']}")
else:
    st.write("Execute pipeline engine to render cascading code fixes.")
