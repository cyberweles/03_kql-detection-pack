# 03_kql-detection-pack

## Goal

Create one solid KQL detection for SSH brute-force in Azure Sentinel and understand:
- how logs → detection → alert work,
- where thresholds and tuning come in.

## Detection: ssh_bruteforce_by_ip

- Table: `Syslog`
- Pattern: multiple `Failed password` messages from the same IP in 5 minutes.
- Why (CTI - Cyber Threat Intelligence):
  - typical botnet / automated scanning,
  - often first step before password spraying or targeted brute-force.

## How to use in Sentinel

1. Go to **Microsoft Sentinel → Analytics → Create → Scheduled query rule**.
2. Paste `ssh_bruteforce_by_ip.kql` into the query.
3. Set:
   - Run every: 5 or 15 minutes
   - Lookup period: 1 hour
4. Map:
   - `SrcIp` → IP entity
   - `User` → Account entity
5. Enable and watch for alerts (then document them in `02_results/ssh_bruteforce_notes.md`).
