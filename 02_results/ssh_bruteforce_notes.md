# SSH brute-force - short summary

**Source IP:** 203.0.113.45 (external)
**Target host:** linux-web-01
**Event:** failed SSH login attempts
**Count:** 12 attempts within a few minutes
**Users targeted:** root, admin, deploy, ubuntu

Checked for successful logins:

- Only one valid login found: from 192.168.1.50 (internal network) - looks normal.
- No successful login from 203.0.113.45 or 198.51.100.23.

Second IP (198.51.100.23) made a few failed attempts as well - looks like normal internet scanning.

**Conclusions:**
Typical automated SSH brute-force from the internet.
No signs of a successful compromise.

**Notes:**
Worth considering SSH hardening (keys only, limited source IPs), but nothing urgent.
Just keep an eye on it.