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

def calc_price(km_str):
    try:
        s = km_str.lower().strip()
        if not s or s in ('okm','0km'): return 200
        km = float(s.replace('km','').strip()) if 'km' in s else float(s.replace('m','').strip()) / 1000
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_value(v):
    try:
        return float(''.join(c for c in v if c.isdigit() or c == '.'))
    except:
        return 0

def parse_km(s):
    try:
        s = s.lower().strip()
        if not s or s in ('okm','0km'): return 0
        return float(s.replace('km','').strip()) if 'km' in s else round(float(s.replace('m','').strip()) / 1000, 3)
    except:
        return 0

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

# Check/seed unique fashions
print(">>> Checking unique fashions...")
psql("SELECT id, username FROM accounts_user WHERE LOWER(username) LIKE '%uniquefashion%' OR LOWER(first_name) LIKE '%unique%' AND LOWER(last_name) LIKE '%fashion%';")
psql(f"""
    INSERT INTO accounts_user
        (password, last_login, is_superuser, username, first_name, last_name,
         email, is_staff, is_active, date_joined, user_type, phone_number,
         is_verified, email_verified, created_at, updated_at, is_online)
    VALUES ('!disabled', NULL, false, 'uniquefashions', 'Unique', 'Fashions',
         'uniquefashions@fagierrands.com', false, true, '{now}', 'client', '',
         true, true, '{now}', '{now}', false)
    ON CONFLICT (username) DO NOTHING
    RETURNING id, username;
""")
psql("INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='uniquefashions';")
psql("SELECT id FROM accounts_user WHERE username='uniquefashions';")
