import re
from constants import COMMON_PORTS

def valid_ip(ip):
    """
    Validate if the input is a valid IPv4 address using regex.
    Returns True if valid, False otherwise.
    """
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not re.match(ip_pattern, ip):
        return False
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        for part in parts:
            num = int(part)
            if not (0 <= num <= 255):
                return False
        return True
    except ValueError:
        return False

def valid_hostname(hostname):
    """
    Validate if the input is a valid hostname using regex.
    Returns True if valid, False otherwise.
    """
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
        return False

    hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'

    if len(hostname) > 253:
        return False
    if hostname.startswith('-') or hostname.endswith('-'):
        return False
    if '..' in hostname:
        return False
        
    return re.match(hostname_pattern, hostname) is not None

def valid_port(port_str):
    """
    Validate if the input is a valid port number (1-65535).
    Returns True if valid, False otherwise.
    """
    try:
        port = int(port_str)
        return 1 <= port <= 65535
    except ValueError:
        return False

def get_service_name(port):
    """
    Return the common service name for a port, or 'Unknown' if not found.
    """
    return COMMON_PORTS.get(port, "Unknown")