import streamlit as st
import requests
import sqlite3

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="centered")
st.title("🌍 AI Travel Planner")

# ========== LOGIN ==========
st.sidebar.header("User Login")
username = st.sidebar.text_input("Enter your username")
if "user" not in st.session_state:
    st.session_state.user = username

# ========== TRIP INPUT ==========
st.subheader("🧳 Trip Information")

origin = st.text_input("Origin City", placeholder="e.g. Ho Chi Minh City")
destination = st.text_input("Destination City", placeholder="e.g. Da Nang")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

interests = st.multiselect(
    "Your Interests",
    ["food", "museums", "nature", "nightlife"],
    default=["food"]
)
pace = st.selectbox("Travel Pace", ["relaxed", "normal", "tight"])

# ========== GENERATE BUTTON ==========
if st.button("✨ Generate Itinerary"):
    if not (origin and destination and username):
        st.warning("Please fill in all fields including username!")
    else:
        payload = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "interests": interests,
            "pace": pace
        }
        with st.spinner("Generating your itinerary..."):
            response = requests.post("http://localhost:5000/generate", json=payload)
            data = response.json()
        
        st.success("✅ Here’s your itinerary!")
        st.text_area("Generated Plan", data["itinerary"], height=400)

        # Save history
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS history(
            user TEXT, origin TEXT, destination TEXT, plan TEXT)""")
        c.execute("INSERT INTO history VALUES (?, ?, ?, ?)",
                  (username, origin, destination, data["itinerary"]))
        conn.commit()
        conn.close()

# ========== HISTORY ==========
if st.sidebar.button("📜 View History"):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS history(user TEXT, origin TEXT, destination TEXT, plan TEXT)")
    c.execute("SELECT * FROM history WHERE user=?", (username,))
    rows = c.fetchall()
    if not rows:
        st.sidebar.info("No previous itineraries found.")
    else:
        for row in rows:
            st.sidebar.markdown(f"**{row[1]} → {row[2]}**")
            st.sidebar.text(row[3])
    conn.close()
