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

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

new_clients = [
    ("kwabrown",   "Kwa",    "Brown",  "kwabrown@fagierrands.com",  "706226766"),
    ("nkirobi",    "Nkirobi","",       "nkirobi@fagierrands.com",   "720348793"),
    ("reestyle",   "Ree",    "Style",  "reestyle@fagierrands.com",  "799564394"),
    ("alinaridge", "Alina",  "Ridge",  "alinaridge@fagierrands.com","791246003"),
    ("nooreen",    "Noreen", "",       "nooreen@fagierrands.com",   "721999686"),
]

for username, first, last, email, phone in new_clients:
    print(f">>> Checking {username}...")
    psql(f"SELECT id, username FROM accounts_user WHERE username='{username}';")
    psql(f"""
        INSERT INTO accounts_user
            (password, last_login, is_superuser, username, first_name, last_name,
             email, is_staff, is_active, date_joined, user_type, phone_number,
             is_verified, email_verified, created_at, updated_at, is_online)
        VALUES ('!disabled', NULL, false, '{username}', '{first}', '{last}',
             '{email}', false, true, '{now}', 'client', '{phone}',
             true, true, '{now}', '{now}', false)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username;
    """)
    psql(f"INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='{username}' AND id NOT IN (SELECT user_id FROM accounts_profile);")

print("\n>>> Final IDs:")
psql("SELECT id, username FROM accounts_user WHERE username IN ('kwabrown','nkirobi','reestyle','alinaridge','nooreen') ORDER BY id;")
