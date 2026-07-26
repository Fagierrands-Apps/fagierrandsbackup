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

for kw, label in [('tracey', 'tracey baddies'), ('lornak', 'lornak'), ('vanessa', 'vanessa')]:
    print(f"\n>> {label}")
    psql(f"SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%{kw}%' OR LOWER(first_name) LIKE '%{kw}%';")
