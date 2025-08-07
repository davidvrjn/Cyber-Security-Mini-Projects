"""
Core scanning functionality for the port scanner.
"""
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from constants import DEFAULT_TIMEOUT, DEFAULT_THREADS

def connect(target, port, timeout=DEFAULT_TIMEOUT):
    """
    Attempt to connect to a specific port on the target.
    Returns True if port is open, False if closed.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = False

    try:
        sock.connect((target, port))
        result = True
    except (socket.timeout, ConnectionRefusedError, OSError):
        result = False
    finally:
        sock.close()

    return result

def scan_port(target, port, results, lock, timeout=DEFAULT_TIMEOUT):
    """
    Scan a single port and store result in shared results list.
    """
    if connect(target, port, timeout):
        with lock:
            results.append(port)

def perform_scan(target, ports_to_scan, max_workers=DEFAULT_THREADS):
    """
    Perform the actual port scan with threading and progress tracking.
    Returns list of open ports.
    """
    print(f"Beginning scan on {target}")
    print("Scanning in progress...")
    
    results = []
    lock = threading.Lock()
    total_ports = len(ports_to_scan)
    completed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for port in ports_to_scan:
            future = executor.submit(scan_port, target, port, results, lock)
            futures.append(future)
        
        for future in futures:
            future.result()
            completed += 1
            progress = (completed / total_ports) * 100
            print(f"\rProgress: {completed}/{total_ports} ports ({progress:.1f}%)", end="", flush=True)
    
    return sorted(results)