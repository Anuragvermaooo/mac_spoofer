import streamlit as st
import subprocess
import re
import random

# Helper: Get current MAC
def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ifconfig", interface]).decode()
        mac_address = re.search(r"ether ([\w:]+)", output)
        return mac_address.group(1) if mac_address else "Not found"
    except:
        return "Error"

# Helper: Generate Random MAC
def generate_random_mac():
    mac = [0x00, 0x16, 0x3e] + [random.randint(0x00, 0xff) for _ in range(3)]
    return ':'.join(map(lambda x: f"{x:02x}", mac))

# Streamlit App
st.set_page_config(page_title="MAC Address Spoofer", layout="centered")
st.title("🔧 MAC Address Spoofer (Web App)")

st.markdown("Spoof your MAC address from the browser (Linux only)")

# Interface Input
interface = st.text_input("🖧 Network Interface (e.g., eth0, wlan0)", value="eth0")

# Random MAC Button
if st.button("🎲 Generate Random MAC"):
    st.session_state.random_mac = generate_random_mac()

# MAC Input
mac_input_default = st.session_state.get("random_mac", "00:11:22:33:44:55")
new_mac = st.text_input("🔀 New MAC Address", value=mac_input_default)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Change MAC"):
        if not interface or not new_mac:
            st.error("Please provide both interface and MAC address.")
        else:
            try:
                subprocess.call(["sudo", "ifconfig", interface, "down"])
                subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
                subprocess.call(["sudo", "ifconfig", interface, "up"])
                st.success(f"MAC changed to `{new_mac}` on `{interface}`")
            except Exception as e:
                st.error(f"Failed to change MAC: {e}")

with col2:
    if st.button("🔍 Show Current MAC"):
        mac = get_current_mac(interface)
        st.info(f"**Current MAC Address** for `{interface}`: `{mac}`")
