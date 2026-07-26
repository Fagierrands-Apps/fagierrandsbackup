import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

new_clients = {
    'platinum plaza': 'platinum',
    'queens choice': 'queens',
    'nairobi flowers': 'nairobi',
    'nia petals': 'nia',
    'micheals bouquette': 'micheal',
    'yyvonne jitihada': 'yyvonne',
    'kaiatu emporium meaplux': 'kiatu',
}

for name, keyword in new_clients.items():
    print(f"\n>> {name}")
    psql(f"SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%{keyword}%' OR LOWER(first_name) LIKE '%{keyword}%' OR LOWER(last_name) LIKE '%{keyword}%';")
