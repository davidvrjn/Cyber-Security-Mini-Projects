"""
Constants used throughout the port scanner application.
"""

#Common ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH", 
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis"
}

#Scanner config
DEFAULT_TIMEOUT = 0.8
DEFAULT_THREADS = 50
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 100
DEFAULT_TARGET = "127.0.0.1"

#App info
APP_NAME = "Python Port Scanner"
APP_VERSION = "1.1"