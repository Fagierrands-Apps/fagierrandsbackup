import subprocess

result = subprocess.run(
    ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c",
     "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"],
    capture_output=True, text=True,
    env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
)
print(result.stdout)
print(result.stderr)
