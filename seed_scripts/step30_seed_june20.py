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

clients = {
    'sekani': 385, 'queenschoice': 595, 'queens': 595,
    'wakiar': 551, 'michael': 604, 'micheal': 604,
    'sunrays': 372, 'sunray': 372,
    'yyvonne': 631, 'yyvone': 631,
    'nairobi flower': 608,
    'harriet': 593,
    'awe': 474,
    'nextgen': 643,
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

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-06-20"

rows = [
    ('sekani  - northside apppartments', '118260620', 'northside apartments', 'Kenya pipeline estate', '2000ksh', '4.8km', 'cyrus ambani'),
    ('queenschoice', '768887510', 'BARAGA BOOKSHOOP, HAMZA ROAD', '2nk parcel drop off', '1500ksh', '6.1km', 'shadrack atito'),
    ('wakiarrie business', '742537182', 'afya centre', 'kariokor', '4000ksh', '8.2km', 'shadrack atito'),
    ('michael   tom mboya', '794775593', 'michael tom mboya', 'ongata rongai academy', '2500ksh', '24.9km', 'willy masinde'),
    ('sunrays  - flora  house', '700797110', 'sunrays-flora house', 'pangani', '1500ksh', '3.2km', 'willy masinde'),
    ('sunrays  - flora  house', '700797110', 'sunrays-flora house', 'westlands', '2500ksh', '2.7km', 'daniel nyakundi'),
    ('yyvonne  - jitihada', '794447655', 'yyvonne-jitihada', 'kasarani  -  -gorofani', '7500ksh', '14.7km', 'johnson wawire'),
    ('Nairobi flowers - tapman rd', '780906221', 'Nairobi flowers - tapman rd', 'ruaka', '3500ksh', '7.2km', 'johnson wawire'),
    ('harriet', '797990411', 'social hall eastleigh', 'quick mart    pioneer', '1500ksh', '4.5km', 'shadrack atito'),
    ('awe-freaque', '758570118', 'Kamukunji Business Centre, Ring Rd, Nairobi', 'kabiria', '3500ksh', '14.5km', 'shadrack atito'),
    ('nextgen', '797990411', 'nextgen', 'wana-anga court -syokimau', '4000ksh', '12.8km', 'cyrus ambani'),
    ('sunrays  - flora  house', '700797110', 'sunrays-flora house', 'genuine  kunga therapy', '2500ksh', '7.2km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 20.06.2026")
