import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="EchoMind Guide", layout="wide")
st.markdown('<meta name="apple-mobile-web-app-capable" content="yes"><meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

# Diagnostics (Improved)
try:
    import streamlit
except ImportError:
    st.error("Streamlit missing: pip install streamlit")
if "day" not in st.session_state: st.session_state.day = 1
if "checklist" not in st.session_state: st.session_state.checklist = {}
if "triggers" not in st.session_state: st.session_state.triggers = ""
if "email" not in st.session_state: st.session_state.email = ""

# 8-Day Array (Streamlined)
days = [
    {"focus": "Spot & Detach", "routine": [
        "Morning (2 min): Affirmation [](https://innertune.app)—positives aloud.",
        "Day (5 min): Journal negatives; rate; name critic; challenge humor/compassion.",
        "Evening (3 min): Gratitude; distanced talk."
    ]},
    # Placeholder—expand to full 8 days in your copy (e.g., Day 2: Add breath/music; Day 8: Review).
]

st.title("EchoMind Guide: 8-Day Booster")
st.write("Triggers:")
st.session_state.triggers = st.text_input("", st.session_state.triggers)
st.write("Email summaries (optional—skip if no setup):")
st.session_state.email = st.text_input("", st.session_state.email, type="password")

st.subheader(f"Day {st.session_state.day}: {days[st.session_state.day-1]['focus']} (For: {st.session_state.triggers})")
for step in days[st.session_state.day-1]['routine']:
    checked = st.checkbox(step, key=f"d{st.session_state.day}_{step[:10]}")
    st.session_state.checklist[step] = checked

progress = sum(st.session_state.checklist.values()) / max(1, len(days[st.session_state.day-1]['routine'])) * 100
st.progress(progress / 100)
negativity = st.slider("Negativity (1-10):", 1, 10, 5)

if st.button("Log & Next"):
    log = f"Day {st.session_state.day}: Negativity {negativity}/10 | Triggers: {st.session_state.triggers} | Checked: {sum(st.session_state.checklist.values())}/{len(days[st.session_state.day-1]['routine'])}"
    if st.session_state.email:
        try:
            msg = MIMEText(log)
            msg['Subject'] = 'Progress'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("your_gmail", "app_pass")  # Replace with your creds
            server.sendmail("your_gmail", st.session_state.email, msg.as_string())
            server.quit()
            st.write("Emailed!")
        except:
            st.write("Email skipped—setup issue.")
    st.session_state.day += 1 if st.session_state.day < 8 else st.write("Done! Weekly maintain.")
    st.session_state.checklist = {}

if st.button("Reset Progress"):
    st.session_state.day = 1
    st.session_state.checklist = {}

st.sidebar.title("Help")
st.sidebar.write("Error? Use python -m streamlit run app.py. Cloud: No local needed.")
st.sidebar.markdown("[Resources](https://psychologytoday.com)")
st.info("Check steps, click Next. Autosaves.")
