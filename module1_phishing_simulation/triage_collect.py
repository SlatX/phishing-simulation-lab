#!/usr/bin/env python3
import psutil, socket, datetime, json, os, subprocess
out = {'timestamp': datetime.datetime.utcnow().isoformat(), 'host': socket.gethostname(), 'processes': [], 'connections': []}

# processes
for p in psutil.process_iter(['pid','name','cmdline','username']):
    try:
        out['processes'].append(p.info)
    except Exception:
        pass

# connections
for c in psutil.net_connections(kind='inet'):
    try:
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ''
    except:
        laddr = str(c.laddr)
    raddr = ''
    try:
        if c.raddr:
            raddr = f"{c.raddr.ip}:{c.raddr.port}"
    except:
        raddr = str(c.raddr)
    out['connections'].append({'laddr': laddr, 'raddr': raddr, 'status': c.status, 'pid': c.pid})

# scheduled tasks (best-effort)
try:
    tasks = subprocess.check_output(['schtasks','/Query','/FO','LIST'], shell=True, text=True)
    out['scheduled_tasks_top'] = tasks.splitlines()[:20]
except Exception as e:
    out['scheduled_tasks_error'] = str(e)

os.makedirs('C:\\temp\\triage', exist_ok=True)
with open('C:\\temp\\triage\\triage_output.json','w') as f:
    json.dump(out, f, indent=2)
print('Triage output written to C:\\temp\\triage\\triage_output.json')
