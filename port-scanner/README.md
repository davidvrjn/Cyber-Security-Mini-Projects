# Python Port Scanner

A fast, multi-threaded port scanner built in Python.

## Features

- **Multi-threaded scanning** for improved performance
- **Input validation** with regex for IP addresses and hostnames
- **Service detection** for common ports
- **Progress tracking** with real-time updates
- **Quick scan mode** for common ports
- **Clean, modular code structure**

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Installation

1. Clone this repository:

2. Run the scanner:
```bash
python3 main.py
```

## Usage

### Interactive Mode
Run the scanner and follow the prompts:
```bash
python3 main.py
```

### Examples

**Scan localhost (default):**
- Target: `127.0.0.1` (press Enter for default)
- Ports: `1-100` (press Enter for default)

**Quick scan of common ports:**
- Choose "y" when prompted for quick scan
- Scans 15 most common ports (SSH, HTTP, HTTPS, MySQL, etc.)

**Custom scan:**
- Target: `scanme.nmap.org`
- Ports: `20-443`

## Sample Output

```
==================================================
        Python Port Scanner v1.0
==================================================
Enter target IPv4 or hostname (default: 127.0.0.1): 
Target validated: 127.0.0.1
Quick scan of common ports? (y/n, default: n): y
Scanning 15 common ports...
Beginning scan on 127.0.0.1
Scanning in progress...
Progress: 15/15 ports (100.0%)

Scan Results for 127.0.0.1
----------------------------------------
Open ports:
  Port 22: OPEN (SSH)
  Port 80: OPEN (HTTP)
  Port 3306: OPEN (MySQL)
----------------------------------------
Scan complete! Found 3 open port(s).
```

## Project Structure

```
port-scanner/
├── main.py          # Main entry point and user interface
├── scanner.py       # Core scanning logic with threading
├── utils.py         # Input validation and utility functions
├── constants.py     # Configuration and port definitions
└── README.md        # This file
```

## Technical Details

- **Threading**: Uses `ThreadPoolExecutor` with 50 worker threads
- **Timeout**: 0.8 second connection timeout for optimal speed/accuracy
- **Port Range**: Supports scanning ports 1-65535
- **Validation**: Regex-based validation for IPv4 addresses and hostnames

## Supported Services

The scanner can identify these common services:
- FTP (21), SSH (22), Telnet (23), SMTP (25)
- DNS (53), HTTP (80), POP3 (110), IMAP (143)
- HTTPS (443), IMAPS (993), POP3S (995)
- MySQL (3306), RDP (3389), PostgreSQL (5432), Redis (6379)

## Disclaimer

This tool is for educational purposes only. Only scan networks and systems you own or have explicit permission to test.

## Author
David van Rooijen
Created as part of a cybersecurity learning project.