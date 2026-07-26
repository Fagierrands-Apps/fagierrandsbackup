import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

# Only search clients not already known from July work
new_searches = {
    'andrew philadelphia': 'andrew',
    'aoko bags': 'aoko',
    'awe-freaque': 'awe',
    'chelsea flowers': 'chelsea',
    'muna flowers': 'muna',
    'dyaminc queens choice': 'dyaminc',
    'edna kelvins': 'edna',
    'epic human hair': 'epic',
    'essylan jeweleries': 'essylan',
    'fashio fix': 'fashio',
    'gathu': 'gathu',
    'gitau flowers': 'gitau',
    'hakati business': 'hakati',
    'harriet': 'harriet',
    'health classique': 'health',
    'irene bestlady': 'irene',
    'joe new client': 'joe',
    'joy business': 'joy',
    'kevo new client': 'kevo',
    'luxe bags': 'luxe',
    'maggie': 'maggie',
    'michael tom mboya': 'michael',
    'nancy lister carwash': 'nancy',
    'nextgen': 'nextgen',
    'phyliss flowers': 'phyliss',
    'purple heart': 'purple',
    'queen africa thrift': 'queen africa',
    'queenschoice': 'queenschoice',
    'rng plaza queens collection': 'rng',
    'unique collection': 'unique',
    'wanjira ncba': 'wanjira',
}

for name, kw in new_searches.items():
    print(f"\n>> {name}")
    psql(f"SELECT id, username, first_name, last_name FROM accounts_user WHERE LOWER(username) LIKE '%{kw}%' OR LOWER(first_name) LIKE '%{kw}%' OR LOWER(last_name) LIKE '%{kw}%';")
