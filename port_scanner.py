import socket
from concurrent.futures import ThreadPoolExecutor

def grab_banner(sock):
    try:
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))

        if result == 0:
            banner = grab_banner(sock)
            print(f"[+] Port {port} OPEN", end="")

            if banner:
                print(f" | Banner: {banner}")
            else:
                print(" | No banner")

        sock.close()
    except:
        pass

def main():
    target = input("Enter target (IP or domain): ")

    try:
        target_ip = socket.gethostbyname(target)
    except:
        print("Invalid target")
        return

    print(f"\nScanning {target_ip} with multithreading...")
    print("-" * 50)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in range(1, 1025):
            executor.submit(scan_port, target_ip, port)

    print("\nScan complete.")

if __name__ == "__main__":
    main()