import subprocess
from datetime import datetime

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

print(">> charles genuine kunga")
psql("SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%charles%' OR LOWER(username) LIKE '%kunga%' OR LOWER(first_name) LIKE '%charles%';")
