import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

print(">> queens-choice")
psql("SELECT id, username, first_name, last_name, email FROM accounts_user WHERE username='queens-choice';")

print(">> new client")
psql("SELECT id, username, first_name, last_name, email FROM accounts_user WHERE LOWER(username) LIKE '%newclient%' OR email='new@client.com' OR (first_name='New' AND last_name='Client');")
