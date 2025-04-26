import tkinter as tk
from tkinter import messagebox, ttk
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

# Change MAC Address
def change_mac():
    interface = interface_entry.get().strip()
    new_mac = mac_entry.get().strip()

    if not interface or not new_mac:
        messagebox.showerror("Error", "Enter both interface and MAC address.")
        return

    try:
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        show_current_mac()
        messagebox.showinfo("Success", f"MAC changed to {new_mac} on {interface}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to change MAC: {str(e)}")

# Show Current MAC
def show_current_mac():
    interface = interface_entry.get().strip()
    if not interface:
        current_mac_var.set("Enter interface to check")
        return
    mac = get_current_mac(interface)
    current_mac_var.set(f"Current MAC: {mac}")

# Autofill random MAC
def use_random_mac():
    mac_entry.delete(0, tk.END)
    mac_entry.insert(0, generate_random_mac())

# GUI Setup
root = tk.Tk()
root.title("Professional MAC Address Spoofer")
root.geometry("460x350")
root.resizable(False, False)

# Style
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TEntry", font=("Segoe UI", 10))

# Frame
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# Interface Input
ttk.Label(main_frame, text="Network Interface (e.g., eth0, wlan0)").pack(anchor="w", pady=(0, 4))
interface_entry = ttk.Entry(main_frame, width=40)
interface_entry.pack(pady=5)

# MAC Input
ttk.Label(main_frame, text="New MAC Address (e.g., 00:11:22:33:44:55)").pack(anchor="w", pady=(10, 4))
mac_entry = ttk.Entry(main_frame, width=40)
mac_entry.pack(pady=5)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=15)

ttk.Button(button_frame, text="Change MAC", command=change_mac).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Show Current MAC", command=show_current_mac).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Generate Random MAC", command=use_random_mac).grid(row=0, column=2, padx=5)

# Current MAC Display
current_mac_var = tk.StringVar(value="Current MAC: --")
current_mac_label = ttk.Label(main_frame, textvariable=current_mac_var, foreground="blue", font=("Segoe UI", 10, "bold"))
current_mac_label.pack(pady=(20, 0))

# Start GUI loop
root.mainloop()
