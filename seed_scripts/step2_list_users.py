import subprocess

def psql(query):
    result = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(result.stdout)
    if result.stderr:
        print("ERR:", result.stderr)

# Check columns in accounts_user
print("=== accounts_user COLUMNS ===")
psql("SELECT column_name FROM information_schema.columns WHERE table_name='accounts_user' ORDER BY ordinal_position;")

# List all usernames/names in the system
print("=== ALL USERS ===")
psql("SELECT id, username, first_name, last_name, email FROM accounts_user ORDER BY username;")
