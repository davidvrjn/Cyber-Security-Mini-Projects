"""
Main entry point for the Python Port Scanner.
"""
from utils import valid_ip, valid_hostname, valid_port, get_service_name
from scanner import perform_scan
from constants import COMMON_PORTS, APP_NAME, APP_VERSION, DEFAULT_START_PORT, DEFAULT_END_PORT, DEFAULT_TARGET

def get_user_input():
    """
    Get and validate user input for target and ports.
    Returns (target, ports_to_scan) or (None, None) if invalid.
    """
    target = input(f"Enter target IPv4 or hostname (default: {DEFAULT_TARGET}): ").strip()
    
    if not target:  
        target = DEFAULT_TARGET

    if not (valid_ip(target) or valid_hostname(target)):
        print(f"ERROR: {target} is not a valid IPv4 or hostname. Please try again.")
        return None, None

    print(f"Target validated: {target}")

    scan_type = input("Quick scan of common ports? (y/n, default: n): ").strip().lower()
    
    if scan_type == 'y' or scan_type == 'yes':
        ports_to_scan = list(COMMON_PORTS.keys())
        print(f"Scanning {len(ports_to_scan)} common ports...")
    else:
        start_port = input(f"Enter start port (default: {DEFAULT_START_PORT}): ") or str(DEFAULT_START_PORT)
        if not valid_port(start_port):
            print(f"ERROR: {start_port} is not a valid port. Please try again.")
            return None, None

        end_port = input(f"Enter end port (default: {DEFAULT_END_PORT}): ") or str(DEFAULT_END_PORT)
        if not valid_port(end_port):
            print(f"ERROR: {end_port} is not a valid port. Please try again.")
            return None, None
        
        start_port = int(start_port)
        end_port = int(end_port)
        
        if start_port > end_port:
            print(f"ERROR: Start port ({start_port}) cannot be greater than end port ({end_port}). Please try again.")
            return None, None

        ports_to_scan = list(range(start_port, end_port + 1))

    return target, ports_to_scan

def display_results(target, results):
    """
    Display the scan results in a formatted way.
    """
    print(f"\n\nScan Results for {target}")
    print("-" * 40)
    
    if results:
        print("Open ports:")
        for port in results:
            service = get_service_name(port)
            print(f"  Port {port}: OPEN ({service})")
    else:
        print("  No open ports found")
    
    print("-" * 40)
    print(f"Scan complete! Found {len(results)} open port(s).")

def main():
    print("=" * 50)
    print(f"        {APP_NAME} v{APP_VERSION}")
    print("=" * 50)

    target, ports_to_scan = get_user_input()
    if not target or not ports_to_scan:
        return

    results = perform_scan(target, ports_to_scan)
    display_results(target, results)

if __name__ == "__main__":
    main()