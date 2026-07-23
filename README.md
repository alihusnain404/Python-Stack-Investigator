Python Stack Investigator - Author ALI HUSNAIN
🕵️‍♂️ Enterprise AI Multi-Stack Incident Investigator & Automated Self-Healing Platform
Python Stack Investigator is an advanced, AI-driven log analysis and infrastructure diagnostic workbench. It processes complex runtime traces across multiple programming languages, integrates live Docker container telemetry, calculates aggregated system health impact, and automatically generates self-healing code remediation patches.

"Detect, Diagnose, and Self-Heal — Automated Incident Investigation at Scale."

⚠️ DISCLAIMER
This software is intended for educational purposes, DevOps diagnostic research, and authorized security & infrastructure debugging only. Developers are not responsible for any production disruption caused by automated patch deployment without human review.

🚀 Key Features
🧩 Dynamic Multi-Language Error Detection
Broad Stack Support: Detects signatures for Python, JavaScript, Java, Go, C++, PHP, and custom runtime anomalies.

Dynamic Database Ingestion: Reads runtime error signatures from an external JSON database (error_database.json) with zero app restart required.

Multi-Pipeline Correlation: Analyzes cascading errors simultaneously within a single log stream.

🐳 Live Docker Telemetry Harvest
Container Telemetry Integration: Interacts directly with Docker Engine API via Python SDK to harvest real-time log outputs.

Automated Container Scanning: Scans active containers for anomalous error signatures and extracts raw stack traces automatically.

📊 Real-time Health State & Diagnostics
System Health Impact Gauge: Evaluates incident severity and computes a live infrastructure health score via Plotly visualizations.

Incident Metadata Tracking: Automatically generates Incident IDs, Severity matrix (CRITICAL / HIGH), and detects language origins.

🛠️ Self-Healing Remediation Workbench
Side-by-Side Code Diff: Displays broken implementations alongside AI-suggested fixed patches.

Actionable AI Recommendations: Delivers context-aware root cause analysis and architectural mitigation steps.

📂 Project Directory Structure
Plaintext
├── stack.py                 # Core Streamlit Application & Pipeline Backend
├── error_database.json      # Dynamic JSON Knowledge Base for Error Signatures
├── requirements.txt         # Python Dependencies
├── Icon/
│   ├── Banner.png           # Repository Header Banner
│   └── Banner2.png          # App Telemetry Dashboard Screenshot
└── docker demo 1/           # Docker Test Environment & Demo Container Scripts
📦 Installation Guide
System Requirements
Python 3.8+

Docker Desktop (Optional: Required only for live Docker log harvesting)

1. Clone Repository & Setup Environment
Bash
# Clone the repository
git clone https://github.com/alihusnain404/python-stack-investigator

# Navigate into project directory
cd python-stack-investigator

# Create virtual environment (Recommended)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
2. Install Dependencies
Bash
pip install -r requirements.txt
(Or install manually):

Bash
pip install streamlit docker plotly
⚡ Usage & Running the App
Launch the dashboard via Streamlit:

Bash
streamlit run stack.py
Testing Live Docker Harvesting
Ensure Docker Desktop is running.

Navigate to the docker demo 1/ directory and spin up test scripts/containers.

In the Streamlit app, click FETCH LIVE DOCKER LOGS to harvest runtime logs directly into the sandbox.

Click DEPLOY PIPELINE SCANNER to view multi-incident diagnostics and self-healing patches.

🔄 Upgrading / Expanding the Error Database
A major advantage of this project is its Dynamic Knowledge Base. You can easily add new error signatures, multi-language support, and patches by modifying error_database.json without stopping or restarting the Streamlit server.

How to Add a New Error Signature
Open error_database.json.

Add a new key matching the exact error string/exception signature present in raw logs.

Define its language, buggy_code, patched_code, and remedy.

JSON Syntax Example:
JSON
{
  "NullPointerException": {
    "language": "Java",
    "buggy_code": "String text = null;\nint length = text.length();",
    "patched_code": "String text = null;\nint length = (text != null) ? text.length() : 0;",
    "remedy": "Initialize object references or add non-null assertions before invoking methods."
  },
  "IndexError: list index out of range": {
    "language": "Python",
    "buggy_code": "data = [1, 2, 3]\nvalue = data[5]",
    "patched_code": "data = [1, 2, 3]\nvalue = data[5] if len(data) > 5 else None",
    "remedy": "Ensure array bounds check or handle exception using a try-except block."
  }
}
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Fork the Project

Create your Feature Branch (git checkout -b feature/NewErrorSignature)

Commit your Changes (git commit -m 'Add Go panic signature to database')

Push to the Branch (git push origin feature/NewErrorSignature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

MADE WITH ❤️ BY AUTHOR ALI HUSNAIN
