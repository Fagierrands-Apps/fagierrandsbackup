import subprocess
from datetime import datetime

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

# Confirm IDs
print("=== gloria kitchen & AlphaFashionCloset ===")
psql("SELECT id, username, first_name, last_name FROM accounts_user WHERE username IN ('gloria', 'AlphaFashionCloset');")

# Seed missing ones
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
for username, first, last, email in [
    ("baddiesempire", "Baddies", "Empire", "baddiesempire@fagierrands.com"),
    ("fantasticfit", "Fantastic", "Fit", "fantasticfit@fagierrands.com"),
]:
    print(f"\n>>> Seeding {username}...")
    psql(f"""
        INSERT INTO accounts_user
            (password, last_login, is_superuser, username, first_name, last_name,
             email, is_staff, is_active, date_joined, user_type, phone_number,
             is_verified, email_verified, created_at, updated_at, is_online)
        VALUES ('!disabled', NULL, false, '{username}', '{first}', '{last}',
             '{email}', false, true, '{now}', 'client', '',
             true, true, '{now}', '{now}', false)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username;
    """)
    psql(f"INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='{username}';")
