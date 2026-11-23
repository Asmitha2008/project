import streamlit as st
import time
from datetime import datetime

# Page Config
st.set_page_config(page_title="LIFEBEAT - PulseNova", page_icon="🫀", layout="wide")

# Custom Dark Theme Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b1220; color: #f8fafc; }
    .card { background-color: #16223a; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #38bdf8; }
    .alert-box { background-color: #7f1d1d; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #ef4444; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "contacts" not in st.session_state:
    st.session_state.contacts = [("Amma", "+91 90000 00001"), ("Appa", "+91 90000 00002")]
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{datetime.now():%H:%M:%S}] App started. Sensors ready."]
if "crash_state" not in st.session_state:
    st.session_state.crash_state = "normal"  # normal, countdown, alert_sent

def add_log(msg):
    st.session_state.logs.append(f"[{datetime.now():%H:%M:%S}] {msg}")

HOSPITALS = [
    ("Govt. Mohan Kumaramangalam Hospital, Salem", "2.1 km"),
    ("Salem Gokulam Hospital", "3.4 km"),
    ("Manipal Hospital, Salem", "4.8 km"),
]
LOCATION = (11.6643, 78.1460)

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🫀 LIFEBEAT <span style='font-size:18px; color:#94a3b8;'>| Team PulseNova</span>", unsafe_allow_html=True)
with col_h2:
    if st.session_state.crash_state == "normal":
        st.success("● Protection ON")
    else:
        st.error("● EMERGENCY DETECTED")

# 4 Steps Pipeline
c1, c2, c3, c4 = st.columns(4)
steps = [
    ("1️⃣ Sense", "Hit + sudden stop", st.session_state.crash_state != "normal"),
    ("2️⃣ Check", "Are you OK? 15s", st.session_state.crash_state == "countdown"),
    ("3️⃣ Alert", "SMS + live location", st.session_state.crash_state == "alert_sent"),
    ("4️⃣ Help", "108 + hospital", st.session_state.crash_state == "alert_sent"),
]
for col, (title, desc, active) in zip([c1, c2, c3, c4], steps):
    bg = "#ef4444" if active else "#16223a"
    col.markdown(f"<div style='background:{bg}; padding:15px; border-radius:10px; text-align:center;'><b>{title}</b><br><small>{desc}</small></div>", unsafe_allow_html=True)

st.write("")

# Main Layout
left_col, right_col = st.columns([2, 1])

with left_col:
    # CRASH ALERT / COUNTDOWN SECTION
    if st.session_state.crash_state == "countdown":
        st.markdown("""
            <div class='alert-box'>
                <h1>⚠️ Are you OK? | நீங்கள் நலமா?</h1>
                <p>Impact & sudden stop detected! Sending emergency SMS if no response.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("✅ I'M OK (Cancel Alert)", use_container_width=True, type="primary"):
            st.session_state.crash_state = "normal"
            add_log("User replied OK. Alert cancelled.")
            st.rerun()
        if col_btn2.button("🚨 SEND SOS NOW", use_container_width=True):
            st.session_state.crash_state = "alert_sent"
            add_log("Manual SOS triggered!")
            st.rerun()

        # 15 Second Live Countdown
        timer_placeholder = st.empty()
        for sec in range(15, -1, -1):
            timer_placeholder.markdown(f"<h1 style='text-align:center; font-size:70px; color:#ef4444;'>{sec}s</h1>", unsafe_allow_html=True)
            time.sleep(1)
        st.session_state.crash_state = "alert_sent"
        st.rerun()

    elif st.session_state.crash_state == "alert_sent":
        link = f"https://maps.google.com/?q={LOCATION[0]},{LOCATION[1]}"
        st.error("🚨 EMERGENCY SMS SENT TO FAMILY CONTACTS!")
        for name, num in st.session_state.contacts:
            st.write(f"📩 **Sent to {name} ({num})**: *EMERGENCY! LIFEBEAT detected an accident. Live GPS: {link}*")
        add_log("Emergency SMS + Live GPS sent to all contacts.")
        if st.button("🔄 Reset System"):
            st.session_state.crash_state = "normal"
            add_log("System reset to normal monitoring.")
            st.rerun()

    else:
        st.markdown("<div class='card'><h3>📡 Live Sensor & Crash Simulator</h3><p>Monitoring accelerometer, gyroscope & sudden deceleration...</p></div>", unsafe_allow_html=True)
        if st.button("💥 Simulate Crash (Shake / High-G Impact)", type="primary", use_container_width=True):
            st.session_state.crash_state = "countdown"
            add_log("Sensors: Strong hit + sudden speed drop detected!")
            st.rerun()

    # Emergency Actions
    st.subheader("🚑 Quick Emergency Actions")
    b1, b2 = st.columns(2)
    if b1.button("📞 Call 108 Ambulance", use_container_width=True):
        add_log("Dialing 108 Ambulance...")
        st.toast("📞 Dialing 108 Ambulance (Simulated)...", icon="🚑")
        st.warning("📞 Connecting to 108 Emergency Services with Live GPS Coordinates...")

    with b2.expander("🏥 View Nearest Hospitals (Salem)"):
        for h_name, dist in HOSPITALS:
            st.write(f"**{h_name}** — `{dist}`")

with right_col:
    # Emergency Contacts Management
    st.subheader("👨‍👩‍👧 Emergency Contacts")
    for name, phone in st.session_state.contacts:
        st.markdown(f"<div style='background:#16223a; padding:10px; border-radius:8px; margin-bottom:5px;'>👤 <b>{name}</b><br><small>{phone}</small></div>", unsafe_allow_html=True)
    
    with st.form("add_contact", clear_on_submit=True):
        new_name = st.text_input("Relative Name")
        new_phone = st.text_input("Phone Number")
        if st.form_submit_button("+ Add Relative"):
            if new_name and new_phone:
                st.session_state.contacts.append((new_name, new_phone))
                add_log(f"Contact added: {new_name}")
                st.rerun()

    # Live Activity Log
    st.subheader("📋 Live Activity Log")
    log_text = "\n".join(st.session_state.logs[::-1])
    st.text_area("Logs", log_text, height=200, disabled=True)