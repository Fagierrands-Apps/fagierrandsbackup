import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

print("=== accounts_user COLUMNS ===")
psql("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='accounts_user' ORDER BY ordinal_position;")

print("=== accounts_profile COLUMNS ===")
psql("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='accounts_profile' ORDER BY ordinal_position;")

print("=== SAMPLE USER ROW ===")
psql("SELECT * FROM accounts_user LIMIT 1;")
