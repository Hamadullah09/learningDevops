import streamlit as st
import socket
import json
import threading
import time

AGENT_STATE = {}

def fetch_agents():
    # In a real setup, you'd expose a REST endpoint from coordinator.
    # For now, we simulate reading from coordinator’s shared state.
    try:
        with open("agents_state.json", "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

def update_loop():
    while True:
        state = fetch_agents()
        AGENT_STATE.clear()
        AGENT_STATE.update(state)
        time.sleep(2)

st.title("Multi-Agent Dashboard")

placeholder = st.empty()

# Background refresh thread
threading.Thread(target=update_loop, daemon=True).start()

while True:
    with placeholder.container():
        st.subheader("Active Agents")
        if AGENT_STATE:
            for agent, info in AGENT_STATE.items():
                st.write(f"🟢 {agent}: {info}")
        else:
            st.write("No active agents detected.")
    time.sleep(2)
    st.rerun()
