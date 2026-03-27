import socket
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import scrolledtext

# --- SCANNER LOGIC ---
def grab_banner(sock):
    try:
        return sock.recv(1024).decode().strip()
    except:
        return None

def scan_port(target, port, output_box):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))

        if result == 0:
            banner = grab_banner(sock)
            message = f"[+] Port {port} OPEN"

            if banner:
                message += f" | {banner}"
            else:
                message += " | No banner"

            output_box.insert(tk.END, message + "\n")
            output_box.see(tk.END)

        sock.close()
    except:
        pass

# --- START SCAN ---
def start_scan():
    target = entry.get()
    output_box.delete(1.0, tk.END)

    try:
        target_ip = socket.gethostbyname(target)
    except:
        output_box.insert(tk.END, "Invalid target\n")
        return

    output_box.insert(tk.END, f"Scanning {target_ip}...\n")
    output_box.insert(tk.END, "-" * 50 + "\n")

    def run_scan():
        with ThreadPoolExecutor(max_workers=50) as executor:
            for port in range(1, 1025):
                executor.submit(scan_port, target_ip, port, output_box)

        output_box.insert(tk.END, "\nScan complete.\n")

    # Run scan without freezing GUI
    root.after(100, run_scan)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Cybersecurity Port Scanner 🛡️")
root.geometry("600x400")

# Input
label = tk.Label(root, text="Enter Target (IP or Domain):")
label.pack()

entry = tk.Entry(root, width=40)
entry.pack()

# Button
scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

# Output box
output_box = scrolledtext.ScrolledText(root, width=70, height=20)
output_box.pack()

# Run app
root.mainloop()