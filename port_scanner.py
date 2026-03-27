import socket

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    target = input("Enter target (IP or domain): ")
    
    try:
        target_ip = socket.gethostbyname(target)
    except:
        print("Invalid target.")
        return

    print(f"\nScanning target: {target_ip}")
    print("-" * 40)

    open_ports = []

    for port in range(1, 1025):
        if scan_port(target_ip, port):
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)

    print("\nScan complete.")
    print(f"Open ports: {open_ports}")

if __name__ == "__main__":
    main()