import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

searches = {
    'queens collection': 'queens',
    'phyliss flowers': 'philis',
    'bestlady irene': 'bestlady',
    'new client kevo': 'newclient',
    'dyaminc': 'dyaminc',
    'epic human hair': 'epic',
    'essylan jeweleries': 'essylan',
    'gathu': 'gathu',
    'hakati business': 'hakati',
    'wanjira': 'wanjira',
    'queen africa': 'africa',
}

for name, kw in searches.items():
    print(f"\n>> {name}")
    psql(f"SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%{kw}%' OR LOWER(first_name) LIKE '%{kw}%' OR LOWER(last_name) LIKE '%{kw}%';")
