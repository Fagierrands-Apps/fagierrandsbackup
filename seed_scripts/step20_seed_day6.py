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
        return float(s.replace('km','').strip()) if 'km' in s else round(float(s.replace('m','').strip()) / 1000, 3)
    except:
        return 0

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

# Seed nm clothing
print(">>> Seeding nmclothing...")
psql(f"""
    INSERT INTO accounts_user
        (password, last_login, is_superuser, username, first_name, last_name,
         email, is_staff, is_active, date_joined, user_type, phone_number,
         is_verified, email_verified, created_at, updated_at, is_online)
    VALUES ('!disabled', NULL, false, 'nmclothing', 'NM', 'Clothing',
         'nmclothing@fagierrands.com', false, true, '{now}', 'client', '',
         true, true, '{now}', '{now}', false)
    ON CONFLICT (username) DO NOTHING
    RETURNING id, username;
""")
psql("INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='nmclothing';")
psql("SELECT id FROM accounts_user WHERE username='nmclothing';")

clients = {
    'sunrays': 372, 'classic': 332, 'adult': 586, 'aldult': 586,
    'wakiarie': 551, 'superfine': 518, 'belizi': 423,
    'athiambo': 634, 'alfa': 423, 'aalfa': 423,
    'meplaux': 341, 'nm clothing': 636, 'nm': 636,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = name.lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

scheduled_date = "2026-07-06"

rows = [
    ('sunrays   cosmetcs', '700797110', 'sunrays cosmetics', 'the piano  1171    brookside    drive   13th floor   cps', '2500ksh', '5.2km', 'willy masinde'),
    ('adult room  - starmall', '106205106', 'adult room - starmall', 'kitsuru   - oak appartments', '2000ksh', '15.2km', 'johnson wawire'),
    ('sunrays   cosmetcs', '700797110', 'sunrays cosmetics', 'mbiru heights -south b', '2500ksh', '5.5km', 'shadrack atito'),
    ('meplaux   -kiatu emporium', '733273632', 'mepalux plaza', 'maximum miracle church  - dandora phase 2', '1500ksh', '13.5km', 'cyrus ambani'),
    ('aldult room -  starmall', '106205106', 'adult room - starmall', 'brookside drive   gate 22  westalnds', '2000ksh', '5.2km', 'willy masinde'),
    ('aalfa fashions    - rng plaza', '7133064041', 'alfa fashions -rng', '55b mitoni  road karen', '1500ksh', '15.7km', 'johnson wawire'),
    ('athiambo thrift  - hakati', '112012425', 'athiambo thrift-hakati', 'alina rdge appartments', '1500ksh', '6.4km', 'daniel nyakundi'),
    ('athiambo thrift  - hakati', '112012425', 'athiambo thrift-hakati', 'gatundu heights', '1500ksh', '7.0km', 'daniel nyakundi'),
    ('adult room  - starmall', '106205106', 'adult room - starmall', 'harambee  chool-buruburu', '2500ksh', '7.5km', 'willy masinde'),
    ('adult room  - starmall', '106205106', 'adult room - starmall', 'cyka -kagundo rd', '2500ksh', '14.5km', 'willy masinde'),
    ('wakiarie  business', '742537182', 'afya centre', 'supreme court biulding', '1500ksh', '1.5km', 'cyrus ambani'),
    ('nm clothing', '703712828', 'kimathi house    3rd floor', 'mololine shuttle -nakuru(latema rd)', '2000ksh', '1.1km', 'johnson wawire'),
    ('belizi fashions', '718454949', 'nextgen mall', 'star court  -syokimau', '5000ksh', '12.9km', 'shadrack atito'),
    ('classic cosmetics  -moyale mall', '700797110', 'dyce beauty shop', 'classic cosmetics', '10000ksh', '4.1km', 'daniel nyakundi'),
    ('superfine beddings', '717679016', 'superfine beddings  -shop 42', 'buruburu -pioneer  estate', '2500ksh', '10.5km', 'johnson wawire'),
    ('adult room  - starmall', '106205106', 'adult room - starmall', 'green belt heights appartments', '2500ksh', '19.3km', 'shadrack atito'),
    ('adult room  - starmall', '106205106', 'digital  shopping mall', 'ruhan  , kahawa sukari', '2500ksh', '17.6km', 'willy masinde'),
    ('adult room  - starmall', '106205106', 'digital  shopping mall', 'utawal shooters', '2500ksh', '21.0km', 'shadrack atito'),
    ('alfa fashions   -rng  plaza', '7133064041', 'alfa fashions -rng plaza', 'lavington chalbi drive    elegance villas', '1500ksh', '11.4km', 'cyrus ambani'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, value, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}' rider='{rider}'")
        skipped += 1
        continue
    price = calc_price(dist)
    est_val = parse_value(value)
    km = parse_km(dist)
    p = pickup.strip().replace("'", "''")
    d = dropoff.strip().replace("'", "''")
    psql(f"""
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
        ) RETURNING id, client_id, assistant_id, price, estimated_value;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for 06.07.2026")
