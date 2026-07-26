# HOW TO SEED ORDER DATA INTO THE DATABASE
# ==========================================
# DB: distinc3_fagierrands | User: distinc3_distinc3
# All scripts live in: seed_scripts/
# Run scripts from the project root on the server

# ── KNOWN CLIENT IDs (as of July 2026) ────────────────────────────────────
# sunrays=372, classic=332, fitbox=338, adult=586, belizi=423
# mtindo(hakati/kitengela)=609, mtindo(ngara/cianda)=657
# queens choice=595, wakiarie=551, avana=521, superfine=518
# jazi/jazy=583, purple=408, yyvonne/yvvonne=631
# unique=513, micheal/michael=604, health=472
# gloria/almond=489, athiambo=634, andrew=607, troys=462, sekani=385, kiatu=341
# chelsea=452, alfafashions=649, yellowpages=650, yvonnejitihada=651
# kwabrown=652, nkirobi=653, reestyle=654, alinaridge=655, nooreen=656
# mtindongara=657, queensrng=658, nancylisters=659, kwamwalimu=660
# odero=662, climeshdesigns=663, munaflowers=664, homeoftrainer=665
# villablooms=666, nolanskids=668, linayarn=669, joybusiness=670
# genuinekunga=671, baddiesempire=632, mercyscott=673, vallaries=674
# niapetalsnew=675, willyriverside=676, trainersbysway=677
# rebune=678, tangecollect=679, kimathihouse=680, oderovictor=681
# nashique=682, miyannegifts=683, fashionfix=684

# ── KNOWN RIDER IDs ────────────────────────────────────────────────────────
# shadrack=477, cyrus=375, johnson=374, willy=403, jesse=109, daniel=310
# tony sangura=661, kelvin ndungu=667

# ── PROCESS FOR EACH NEW DATE ─────────────────────────────────────────────
# 1. Look at the data for the date
# 2. Identify any client/rider names not in the known IDs above
# 3. Create a clients script: stepXX_seed_DATEHERE_clients.py
#    - Check if exists: SELECT id, username FROM accounts_user WHERE username='...';
#    - Seed if missing using INSERT with ON CONFLICT (username) DO NOTHING
#    - Also insert profile: INSERT INTO accounts_profile ... SELECT ... WHERE username=...
#      AND id NOT IN (SELECT user_id FROM accounts_profile)
#    - Print final IDs at the end
# 4. Run the clients script, note the IDs
# 5. Create orders script: stepXX_seed_DATEHERE.py
#    - Use the clients/riders maps with all known IDs
#    - rows = list of (client, phone, pickup, dropoff, value, dist, rider)
#    - Price formula: 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
#    - INSERT into orders_order with status='completed', order_type_id=2
# 6. Run the orders script

# ── TEMPLATE: clients script ───────────────────────────────────────────────
"""
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
    ("username", "First", "Last", "email@fagierrands.com", "phone"),
]

for username, first, last, email, phone in new_clients:
    print(f">>> Checking {username}...")
    psql(f"SELECT id, username FROM accounts_user WHERE username='{username}';")
    psql(f\"\"\"
        INSERT INTO accounts_user
            (password, last_login, is_superuser, username, first_name, last_name,
             email, is_staff, is_active, date_joined, user_type, phone_number,
             is_verified, email_verified, created_at, updated_at, is_online)
        VALUES ('!disabled', NULL, false, '{username}', '{first}', '{last}',
             '{email}', false, true, '{now}', 'client', '{phone}',
             true, true, '{now}', '{now}', false)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username;
    \"\"\")
    psql(f"INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='{username}' AND id NOT IN (SELECT user_id FROM accounts_profile);")

print("\\n>>> Final IDs:")
psql("SELECT id, username FROM accounts_user WHERE username IN ('username1','username2') ORDER BY id;")
"""

# ── TEMPLATE: orders script ────────────────────────────────────────────────
"""
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
        s = str(km_str).lower().strip()
        if 'km' in s: km = float(s.replace('km','').strip())
        elif 'm' in s: km = float(s.replace('m','').strip()) / 1000
        else: km = float(s)
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_km(s):
    try:
        s = str(s).lower().strip()
        if 'km' in s: return float(s.replace('km','').strip())
        if 'm' in s: return round(float(s.replace('m','').strip()) / 1000, 3)
        return float(s)
    except:
        return 0

def parse_value(v):
    try:
        return float(''.join(c for c in str(v) if c.isdigit() or c == '.'))
    except:
        return 0

clients = {
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'adult': 586,
    # ... add all known clients + new ones for this date
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661, 'kelvin': 667,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "YYYY-MM-DD"

rows = [
    # (client, phone, pickup, dropoff, value, dist, rider)
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, value, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}'({client_id}) rider='{rider}'({rider_id})")
        skipped += 1
        continue
    price = calc_price(dist)
    km = parse_km(dist)
    est_val = parse_value(value)
    p = pickup.strip().replace("'", "''")
    d = dropoff.strip().replace("'", "''")
    psql(f\"\"\"
        INSERT INTO orders_order (
            title, description, pickup_address, delivery_address,
            contact_number, scheduled_date, price, status,
            created_at, updated_at, completed_at,
            client_id, assistant_id, order_type_id,
            distance, price_finalized, estimated_value
        ) VALUES (
            'Pickup & Delivery Order', '{p} to {d}',
            '{p}', '{d}', '{phone}', '{scheduled_date}',
            {price}, 'completed', '{now}', '{now}', '{now}',
            {client_id}, {rider_id}, 2,
            {km}, true, {est_val}
        ) RETURNING id, client_id, assistant_id, price;
    \"\"\")
    success += 1

print(f"\\nDone: {success} inserted, {skipped} skipped for {scheduled_date}")
"""
