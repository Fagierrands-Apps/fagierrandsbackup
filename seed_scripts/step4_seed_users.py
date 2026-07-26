import subprocess, json, os
from datetime import datetime

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)
    return r.stdout

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

new_users = [
    {
        "username": "sienzplaza",
        "first_name": "Sienz",
        "last_name": "Plaza",
        "email": "sienzplaza@fagierrands.com",
        "phone_number": "",
        "user_type": "client",
    },
]

CACHE_FILE = "user_cache.json"
cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {"clients": {}, "riders": {}}

for u in new_users:
    print(f"\n>>> Inserting {u['username']}...")
    result = psql(f"""
        INSERT INTO accounts_user
            (password, last_login, is_superuser, username, first_name, last_name,
             email, is_staff, is_active, date_joined, user_type, phone_number,
             is_verified, email_verified, created_at, updated_at, is_online)
        VALUES
            ('!disabled', NULL, false, '{u['username']}', '{u['first_name']}', '{u['last_name']}',
             '{u['email']}', false, true, '{now}', '{u['user_type']}', '{u['phone_number']}',
             true, true, '{now}', '{now}', false)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username;
    """)

    # Extract ID from result and save to cache
    for line in result.splitlines():
        parts = line.strip().split('|')
        if len(parts) == 2:
            try:
                uid = int(parts[0].strip())
                uname = parts[1].strip()
                cache["clients"][u['first_name'].lower()] = {"id": uid, "username": uname}
                print(f"Cached: {u['first_name']} => ID {uid}")
            except ValueError:
                pass

    # Also create profile
    psql(f"""
        INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points)
        SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='{u['username']}';
    """)

json.dump(cache, open(CACHE_FILE, "w"), indent=2)
print("\nDone. Cache updated.")
