# 🎯 Module 1 — Phishing Simulation & Analysis

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

> **Status:** Completed — portfolio-ready lab  
> **Scope:** Safe phishing simulation, automated triage, and initial incident-response workflow (designed and implemented as a hands-on learning project).

---

## Overview — what I built and why

This repository contains a reproducible, **benign phishing simulation** and an incident-response triage workflow I developed to practice defender techniques. The lab is intentionally non-malicious and designed to run on isolated VMs (attacker + victim) to replicate the real-world sequence:

1. Phishing delivery → 2. Payload fetch & execution → 3. Rapid triage → 4. Analyst decision (isolate / collect / escalate).

The emphasis is on repeatable evidence collection, defensible artifact handling, and mapping observed behaviors to MITRE ATT&CK techniques. I documented design choices, trade-offs, and the forensic hygiene I followed so this is interview- and portfolio-ready.

---

## Repo contents

```
module1_phishing_simulation/
├─ phishing_server.py            # Flask server hosting fake login page
├─ victim_fetch_and_run.py       # Simulates endpoint fetching payload (benign)
├─ triage_collect.py             # Automated triage: processes, network, scheduled tasks
├─ phishing_email_template.html  # Example landing page / email demo
├─ results/                      # Sanitized sample outputs (captured credentials, triage JSON)
├─ screenshots/                  # Sample screenshots referenced in this README
├─ requirements.txt              # Python deps for reproducing the lab
├─ README.md                     # <-- you are reading this
└─ LICENSE                       # MIT (recommended for portfolio)
```

> **Security note:** This project is educational. Do **not** run these scripts on production or public networks. Use host-only or internal VM networking only.

---

## Quick demo 

**Phishing page** (fake corporate login) → user submits credentials → `phishing_server.py` logs the submission into `results/captured_credentials.csv`.

**Victim triage** (`triage_collect.py`) gathers:
- process list (pid, cmdline, username)  
- active network connections (local/remote, pid)  
- scheduled tasks (top lines)  
and writes `results/triage_output.json`.

The analyst then verifies artifacts, computes hashes, and decides containment steps (isolate host, capture memory, image disk if needed).

---

## Setup & prerequisites

**Attacker VM: Linux (Ubuntu recommended) or any OS with Python 3.8+**  
**Victim VM: Windows 10/11 (recommended for realism) with Python 3.8+**  
**Network: Host-only or internal virtual network (NO INTERNET). Snapshots recommended.**

**Install dependencies (Attacker / Analysis host)**

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**requirements.txt**
```
flask
pandas
psutil
requests
python-dateutil
```

---

## How to run — step-by-step (tested)

> **Before you begin:** take VM snapshots and ensure VMs are on the same isolated network.

### 1) Start the phishing server (Attacker VM)

```bash
source venv/bin/activate
python phishing_server.py
```

- Server default: `0.0.0.0:8080`
- Browse from Victim VM: `http://<ATTACKER_IP>:8080`

### 2) Simulate victim behavior (Victim VM)

**Manual (browser):**
- Visit `http://<ATTACKER_IP>:8080`, submit dummy credentials.

**Automated (PowerShell):**
```powershell
py victim_fetch_and_run.py
```

This will download the benign payload and create `C:\temp\dropped.txt` and `C:\temp\dropped_log.txt`.

### 3) Run triage collection (Victim VM — run as admin for fuller capture)

```powershell
py triage_collect.py
# Output: C:\temp\triage\triage_output.json
```

### 4) Analyst verification & basic forensic hygiene

- Compute file hash (PowerShell):
```powershell
Get-FileHash C:\temp\triage\triage_output.json -Algorithm SHA256
```
- Transfer the artifact to your analysis host (use a secured path) and store metadata:
  - `collector`, `timestamp_utc`, `tool/version`, `sha256`, `comments`.

---

## Example outputs (sanitized)

**results/captured_credentials.csv**
```
username,password,ip
alice,Winter2025!,192.168.56.12
bob,Password123,192.168.56.15
```

**results/triage_output.json (excerpt)**
```json
{
  "timestamp":"2025-10-27T09:15:12.345678",
  "host":"WIN-VICTIM01",
  "processes":[
    {"pid":456,"name":"python.exe","cmdline":["C:\\Python39\\python.exe","victim_fetch_and_run.py"],"username":"CORP\\alice"}
  ],
  "connections":[
    {"laddr":"192.168.56.12:52345","raddr":"192.168.56.10:8080","status":"ESTABLISHED","pid":456}
  ]
}
```

---


## Attack mapping & detections — MITRE ATT&CK

| Tactic          | Technique ID  | Notes (lab mapping) |
|-----------------|---------------|---------------------|
| Initial Access  | T1566.001     | Phishing attachment / link leading to credential page |
| Credential Access| T1556        | Input capture via fake login form |
| Exfiltration    | T1041         | POSTing captured credentials to remote web endpoint |

**Detection ideas**
- SIEM: Alert on outbound HTTP POSTs to new/uncommon domains from regular user hosts.  
- Endpoint: Detect `explorer.exe` or browser process spawning unexpected child processes or unexpected file writes to `C:\\temp`.  
- Network: Correlate proxy/DNS logs for suspicious domains and block at perimeter.

---

## Forensic hygiene & decisions I practiced

During runs I enforced:
1. Snapshot VMs before tests.  
2. Run triage and compute SHA256 immediately.  
3. Store artifacts in a write-protected archive and log collection metadata.  
4. Only after imaging/collection was remediation (cleanup, snapshots revert) performed.

**Decision examples documented in the project:**
- When triage shows active C2-like callbacks: isolate host immediately.
- If only benign artifact and no network egress: consider monitoring but still collect memory if suspicious behavior occurred.

---

## What I learned & technical challenges

- **Network isolation quirks:** solved by ensuring both VMs use the same host-only adapter and static IPs.  
- **Telemetry harmonization:** Sysmon and triage JSON used different field names; I implemented normalization in the triage script to make downstream correlation reliable.  
- **Reproducibility:** added `results/README.md` and `.gitignore` to keep only sanitized samples in repo.

---

## Roadmap / Future work

- Add Sysmon + Winlogbeat forwarding into ELK and demonstrate a Sigma -> Kibana translation.  
- Extend triage to grab registry Run keys and Scheduled Task XMLs for persistence hunting.  
- Create a Streamlit dashboard for visual timeline reconstruction from `triage_output.json`.  
- Add unit tests for the triage JSON schema and CI to validate PRs.


---

## Contribution, license & contact

Contributions welcome — fork, add small, documented PRs (e.g., add a Sigma rule, expand triage fields).

**License:** MIT — see `LICENSE` file.

**Author:** Ebenezer (GitHub: `slatX`)  
Email: Omoniyiebenezer97@gmail.com  
GitHub: https://github.com/slatX

---

## Quick commit & push example

```bash
git add README.md phishing_server.py victim_fetch_and_run.py triage_collect.py requirements.txt .gitignore
git commit -m "Add Module 1 — phishing simulation lab (polished README + scripts)"
git branch -M main
git remote add origin https://github.com/slatX/phishing-simulation-lab.git
git push -u origin main
```

---

**Final note:** This README was generated as a polished, portfolio-ready document reflecting time spent understanding the topic and building the lab.
