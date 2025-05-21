import streamlit as st
import json
import os

REPORTS_FILE = "powerbi_reports.json"

def load_reports():
    if os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reports(reports):
    with open(REPORTS_FILE, "w") as f:
        json.dump(reports, f, indent=2)

st.title("Power BI Report Embedder")

# Load existing reports
reports = load_reports()

# Sidebar: Add new report
st.sidebar.header("Add New Power BI Report")
with st.sidebar.form("add_report_form"):
    report_name = st.text_input("Report Name")
    embed_url = st.text_input("Embed URL")
    access_token = st.text_area("Access Token")
    submitted = st.form_submit_button("Add Report")
    if submitted and report_name and embed_url and access_token:
        reports[report_name] = {
            "embed_url": embed_url,
            "access_token": access_token
        }
        save_reports(reports)
        st.sidebar.success(f"Report '{report_name}' added!")

# Main: Select and view report
if reports:
    selected_report = st.selectbox("Select a report to view", list(reports.keys()))
    if selected_report:
        embed_url = reports[selected_report]["embed_url"]
        access_token = reports[selected_report]["access_token"]
        st.markdown("#### Embedded Power BI Report")
        st.components.v1.html(
    f"""
    <style>
        .responsive-container {{
            position: relative;
            width: 100%;
            padding-top: 56.25%; /* 16:9 Aspect Ratio (9/16 = 0.5625) */
        }}
        .responsive-iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
    <div class="responsive-container">
        <div id="reportContainer" class="responsive-iframe"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/powerbi-client@2.19.0/dist/powerbi.js"></script>
    <script type="text/javascript">
        var models = window['powerbi-client'].models;
        var embedConfiguration = {{
            type: 'report',
            tokenType: models.TokenType.Aad,
            accessToken: "{access_token}",
            embedUrl: "{embed_url}",
            settings: {{
                panes: {{
                    filters: {{
                        visible: false
                    }},
                    pageNavigation: {{
                        visible: false
                    }}
                }}
            }}
        }};
        var reportContainer = document.getElementById('reportContainer');
        if (window.powerbi) {{
            window.powerbi.reset(reportContainer);
            window.powerbi.embed(reportContainer, embedConfiguration);
        }}
    </script>
    """,
    height=1080,  # Let the CSS control the height
)
else:
    st.info("No reports saved yet. Add a new report from the sidebar.")

st.sidebar.markdown("---")
st.sidebar.write("All report credentials are stored locally in plain text.")