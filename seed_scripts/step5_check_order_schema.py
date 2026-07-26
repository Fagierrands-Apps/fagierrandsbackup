import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

print("=== orders_order COLUMNS ===")
psql("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='orders_order' ORDER BY ordinal_position;")

print("=== SAMPLE ORDER ROW ===")
psql("SELECT * FROM orders_order LIMIT 1;")
