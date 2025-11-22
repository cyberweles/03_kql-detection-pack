# SSH brute-force – big log analysis (sample_syslog_ssh_big.log)

File: `00_logs/sample_syslog_ssh_big.log`
Lines: 480
Context: synthetic lab log for practicing SSH brute-force detection and triage.

---

## 1. Basic stats

* Total lines: **480**
* Failed SSH logins (`Failed password`): **320**
* Successful SSH logins (`Accepted password`): **80**
* Sudo-related events (`sudo:`): **80**

**Quick impression:**

* ~2/3 of the file is pure attack noise.
* There is still a noticeable amount of normal admin activity (Accepted + sudo).

---

## 2. Top attacking IPs (failed SSH)

From:

```bash
grep "Failed password" sample_syslog_ssh_big.log | awk '{print $11}' | sort | uniq -c | sort -nr | head
```

**Result (aggregated):**

* `203.0.113.45` → **200** failed attempts
* `185.13.44.200` → **43** failed attempts
* `198.51.100.23` → **39** failed attempts
* `37.120.150.90` → **38** failed attempts

**Interpretation:**

* `203.0.113.45` is the main brute-force source (about **62%** of all failed logins).
* The other three IPs are additional noisy scanners (low-intensity bot activity).
* This is typical *internet background noise*: multiple bots trying common SSH passwords.

---

## 3. Successful logins – who really got in?

From:

```bash
grep "Accepted password" sample_syslog_ssh_big.log | awk '{print $11}' | sort | uniq -c | sort -nr | head
```

**Result (aggregated):**

* `10.0.0.15` → **37** successful logins
* `192.168.1.77` → **28** successful logins
* `192.168.1.50` → **15** successful logins

All of these are private IP ranges (`10.x.x.x` / `192.168.x.x`).

**Interpretation:**

* All successful SSH logins come from internal / private addresses.
* There are **no** successful logins from external attacker IPs.
* This strongly suggests normal admin/user activity from inside the network.

---

## 4. Timeline – do attacks overlap with successful logins?

**Sample lines:**

```text
Accepted:
Nov 22 12:00–12:29 ... from 10.0.0.15 / 192.168.1.50 / 192.168.1.77

Failed:
Nov 22 12:42–12:49 ... from 203.0.113.45
Nov 22 13:05:17 ... from 185.13.44.200
```

**Key point:**

* Legitimate logins happen around **12:00–12:29**.
* The brute-force and scanners appear later, from ~**12:42** onwards.
* There is no **“failed → accepted → sudo”** pattern from the same external IP.

**Conclusion:**

* No sign that attackers guessed any valid password.
* No suspicious successful login following a burst of failed attempts.

---

## 5. Usernames targeted by the main bot

From:

```bash
grep "Failed password" sample_syslog_ssh_big.log | awk '{print $9,$11}' | sort | uniq -c | sort -nr | head
```

**Selected result for `203.0.113.45`:**

* `deploy` → 42 attempts
* `backup` → 37 attempts
* `ubuntu` → 35 attempts
* `appuser` → 33 attempts
* `admin` → 28 attempts
* `root` → 25 attempts

**Interpretation:**

* The attacker cycles through a typical default username list.
* No sign of a targeted account (no real names, no company-specific users).
* This fits a **generic SSH brute-force bot**, not a focused APT-style attack.

Other attacker IPs (`198.51.100.23`, `185.13.44.200`, `37.120.150.90`) show similar low-volume patterns with `ubuntu`, `backup`, `root`, etc. → more background noise.

---

## 6. Sudo activity

We see around **80** sudo-related log entries and all of them are associated with hosts and users that belong to the internal network.

**Interpretation:**

* `sudo` is used by internal users after successful SSH logins from private IPs.
* There is no evidence of `sudo` being triggered from compromised external sessions.
* No obvious sign of privilege escalation after a successful attack.

---

## 7. Final assessment

* **Attack type:** external SSH brute-force + generic scanning
* **Main attacker:** `203.0.113.45` (high-volume brute-force)
* **Additional noise:** `185.13.44.200`, `198.51.100.23`, `37.120.150.90`
* **Successful logins:** only from internal IPs (`10.0.0.15`, `192.168.1.77`, `192.168.1.50`)
* **Evidence of compromise:** none observed
* **Lateral movement:** none observed
* **Risk level:** **Low** (no successful external login, but constant internet noise)

---

## 8. Recommendations

* Keep SSH exposed only where necessary.
* Prefer **key-based authentication** instead of passwords.
* Consider additional protections:

  * Fail2Ban / similar tools,
  * limiting SSH access by IP,
  * using VPN or a jump host pattern for admin access.
* Add or tune SIEM detections for:

  * repeated `Failed password` from the same IP,
  * unusual failed login volumes per host,
  * sudden spikes in failed SSH attempts.

---

**Summary:**
This log is a good example of how a server looks under normal admin use plus ongoing background SSH brute-force from the internet. No compromise here – just noise and a clear case for hardening.
