"""
Main entry point for the Python Port Scanner.
"""
import argparse
from utils import valid_ip, valid_hostname, valid_port, get_service_name
from scanner import perform_scan
from constants import COMMON_PORTS, APP_NAME, APP_VERSION, DEFAULT_START_PORT, DEFAULT_END_PORT, DEFAULT_TARGET

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='A multi-threaded port scanner.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py -t 192.168.1.1 -p 80-443
  python3 main.py --target google.com --ports 22,80,443
  python3 main.py -t scanme.nmap.org --common
  python3 main.py --target 127.0.0.1 --start 1 --end 1000
        """
    )
    
    parser.add_argument('-t', '--target', 
                       help=f'Target IP address or hostname (default: {DEFAULT_TARGET})')
    
    parser.add_argument('-p', '--ports', 
                       help='Port range (e.g., 80-443) or comma-separated ports (e.g., 22,80,443)')
    
    parser.add_argument('--start', type=int, 
                       help=f'Start port (default: {DEFAULT_START_PORT})')
    
    parser.add_argument('--end', type=int,
                       help=f'End port (default: {DEFAULT_END_PORT})')
    
    parser.add_argument('-c', '--common', action='store_true',
                       help='Scan common ports only')
    
    parser.add_argument('-v', '--version', action='version', 
                       version=f'{APP_NAME} v{APP_VERSION}')
    
    return parser.parse_args()

def parse_ports(ports_str):
    """
    Parse port string into list of ports.
    Supports formats: '80-443', '22,80,443'
    """
    ports = []
    
    if '-' in ports_str and ',' not in ports_str:
        try:
            start, end = ports_str.split('-')
            start, end = int(start), int(end)
            if start > end:
                raise ValueError("Start port cannot be greater than end port")
            ports = list(range(start, end + 1))
        except ValueError as e:
            raise ValueError(f"Invalid port range '{ports_str}': {e}")
    
    elif ',' in ports_str:
        try:
            ports = [int(p.strip()) for p in ports_str.split(',')]
        except ValueError:
            raise ValueError(f"Invalid port list '{ports_str}': ports must be integers")
    
    else:
        try:
            ports = [int(ports_str)]
        except ValueError:
            raise ValueError(f"Invalid port '{ports_str}': must be an integer")
    
    for port in ports:
        if not (1 <= port <= 65535):
            raise ValueError(f"Port {port} is out of valid range (1-65535)")
    
    return ports

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

    print("\nPort scanning options:")
    print("1. Quick scan (common ports)")
    print("2. Port range (e.g., 1-1000)")
    print("3. Specific ports (e.g., 22,80,443)")
    
    choice = input("Select option (1/2/3, default: 2): ").strip()
    
    if choice == '1':
        ports_to_scan = list(COMMON_PORTS.keys())
        print(f"Scanning {len(ports_to_scan)} common ports...")
    elif choice == '3':
        ports_input = input("Enter specific ports (comma-separated, e.g., 22,80,443): ").strip()
        if not ports_input:
            print("ERROR: No ports specified.")
            return None, None
        try:
            ports_to_scan = parse_ports(ports_input)
            print(f"Scanning {len(ports_to_scan)} specified ports...")
        except ValueError as e:
            print(f"ERROR: {e}")
            return None, None
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
        print(f"Scanning ports {start_port}-{end_port}...")

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
    args = parse_arguments()
    
    print("=" * 50)
    print(f"        {APP_NAME} v{APP_VERSION}")
    print("=" * 50)

    #Using command line arguments
    if args.target or args.ports or args.common or args.start or args.end:
        target = args.target or DEFAULT_TARGET
        
        if not (valid_ip(target) or valid_hostname(target)):
            print(f"ERROR: '{target}' is not a valid IPv4 address or hostname.")
            print("Please check your input and try again.")
            return
        
        if args.common:
            ports_to_scan = list(COMMON_PORTS.keys())
            print(f"Scanning {len(ports_to_scan)} common ports on {target}")
        elif args.ports:
            try:
                ports_to_scan = parse_ports(args.ports)
                print(f"Scanning {len(ports_to_scan)} specified ports on {target}")
            except ValueError as e:
                print(f"ERROR: {e}")
                return
        else:
            start = args.start or DEFAULT_START_PORT
            end = args.end or DEFAULT_END_PORT
            if start > end:
                print(f"ERROR: Start port ({start}) cannot be greater than end port ({end})")
                return
            ports_to_scan = list(range(start, end + 1))
            print(f"Scanning ports {start}-{end} on {target}")
            
    else:
        #Interactive mode
        target, ports_to_scan = get_user_input()
        if not target or not ports_to_scan:
            return

    results = perform_scan(target, ports_to_scan)
    display_results(target, results)

if __name__ == "__main__":
    main()