import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

# Check what user_type the riders have
print("=== RIDER USER TYPES ===")
psql("SELECT id, username, first_name, last_name, user_type FROM accounts_user WHERE id IN (477, 375, 374, 403, 109, 310);")

# Check a sample order with assistant assigned
print("=== SAMPLE ORDER WITH ASSISTANT ===")
psql("SELECT id, client_id, handler_id, assistant_id, status FROM orders_order WHERE assistant_id IS NOT NULL LIMIT 3;")
