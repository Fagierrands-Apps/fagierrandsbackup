import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

print(">> nm clothing")
psql("SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%nm%' OR LOWER(first_name) LIKE '%nm%' OR LOWER(last_name) LIKE '%clothing%';")
