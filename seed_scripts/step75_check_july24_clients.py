import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

psql("""
    SELECT id, username FROM accounts_user
    WHERE username ILIKE ANY(ARRAY[
        '%queens%','%jitihada%','%kiatu%','%mepalux%','%pramukh%','%joe%'
    ])
    ORDER BY id;
""")
