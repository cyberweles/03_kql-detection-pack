#!/usr/bin/env python3
"""
generate_big_syslog.py

Generate a synthetic SSH/sudo syslog file for offline SOC practice.

Output:
    ../00_logs/sample_syslog_ssh_big.log   (around 500 lines)
"""

from datetime import datetime, timedelta
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LOG_DIR = SCRIPT_DIR.parent / "00_logs"
LOG_FILE = LOG_DIR / "sample_syslog_ssh_big.log"

random.seed(42)

# Base time for logs
start_time = datetime(2025, 11, 22, 12, 0, 0)

hosts = ["linux-web-01", "linux-db-01", "linux-jump-01"]
users = ["root", "admin", "ubuntu", "deploy", "appuser", "backup"]
local_ips = ["192.168.1.50", "192.168.1.77", "10.0.0.15"]
attacker_ips = [
    "203.0.113.45",   # main brute-force
    "198.51.100.23",  # noisy scanner
    "185.13.44.200",  # random VPS
    "37.120.150.90"   # another random VPS
]

def fmt_time(dt: datetime) -> str:
    # Example syslog date format: "Nov 22 12:00:12"
    return dt.strftime("%b %d %H:%M:%S")

lines = []

current_time = start_time

# 1) Normal background SSH logins from local IPs
for _ in range(80):
    host = random.choice(hosts)
    user = random.choice(["ubuntu", "appuser", "backup"])
    src_ip = random.choice(local_ips)
    current_time += timedelta(seconds=random.randint(5, 60))
    line = (
        f"{fmt_time(current_time)} {host} sshd[12345]: "
        f"Accepted password for {user} from {src_ip} port {random.randint(40000, 65000)} ssh2"
    )
    lines.append(line)

# 2) Main brute-force from 203.0.113.45
for _ in range(200):
    host = random.choice(hosts)
    user = random.choice(users)
    current_time += timedelta(seconds=random.randint(1, 5))
    line = (
        f"{fmt_time(current_time)} {host} sshd[23456]: "
        f"Failed password for {user} from 203.0.113.45 port {random.randint(40000, 65000)} ssh2"
    )
    lines.append(line)

# 3) Additional noisy scanners (other external IPs)
for _ in range(120):
    host = random.choice(hosts)
    user = random.choice(users)
    ip = random.choice(attacker_ips[1:])  # skip main attacker
    current_time += timedelta(seconds=random.randint(2, 15))
    line = (
        f"{fmt_time(current_time)} {host} sshd[34567]: "
        f"Failed password for {user} from {ip} port {random.randint(40000, 65000)} ssh2"
    )
    lines.append(line)

# 4) Some sudo activity (success + failures)
for _ in range(80):
    host = random.choice(hosts)
    user = random.choice(users)
    current_time += timedelta(seconds=random.randint(5, 60))
    # 70% success, 30% failure
    if random.random() < 0.7:
        msg = f"sudo:   {user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/usr/bin/apt update"
    else:
        msg = (
            f"sudo: pam_unix(sudo:auth): authentication failure; "
            f"logname={user} uid=1000 euid=0 tty=/dev/pts/0 ruser={user} rhost=  user={user}"
        )
    line = f"{fmt_time(current_time)} {host} sudo: {msg}"
    lines.append(line)

# Shuffle lines a bit to simulate mixed log
random.shuffle(lines)

LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Wrote {len(lines)} log lines to {LOG_FILE}")
