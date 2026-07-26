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

clients = {
    'sunrays': 372, 'sunnrays': 372, 'classic': 332, 'adult': 586,
    'wakiarie': 551, 'mtindo': 609, 'belizi': 423, 'avana': 521,
    'athiambo': 634, 'sam': 635,
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
scheduled_date = "2026-07-04"

rows = [
    ('wakiarie business', '742537182', 'afya centre', 'guru nank  - ngara', '2500ksh', '1.7km', 'johnson wawire'),
    ('wakiarie business', '742537182', 'afya centre', 'lumumba driive', '3500ksh', '12.5km', 'johnson wawire'),
    ('sunnrays  -flora house', '700797110', 'sunrays -flora house', 'school ane -westlands', '4500ksh', '5.3km', 'willy masinde'),
    ('avana soles  - karikor', '702840229', 'avana soles -kariakor', 'nicco movers  - juja route', '2500ksh', '2.6km', 'jesse  victor'),
    ('adult   room', '106205106', 'star mall', 'utawala  -shooters', '2000ksh', '21.8km', 'cyrus ambani'),
    ('adult   room', '106205106', 'star mall', 'good hope court  utawala mihango', '2000ksh', '26.2km', 'cyrus ambani'),
    ('athiambo thrift-hakati', '', 'athiambo thrift  -hakati', 'raila estate -langata', '1500ksh', '11.2km', 'shadrack atito'),
    ('belizi  fashions', '718454949', 'infill b  , kanguru rd', 'church  court   , garden estate', '250ksh', '11.8km', 'willy masinde'),
    ('mtindo wear', '710130388', 'supermetro', 'gogo mall - pick up mtaani', '1500ksh', '750m', 'daniel nyakundi'),
    ('mtindo wear', '710130388', 'supermetro', 'wanyee rd', '1500ksh', '9.8km', 'daniel nyakundi'),
    ('sunrays -flora house', '700797110', 'sunrays -flora house', 'state house rd crescent rd  opp veina   court', '2500ksh', '2.8km', 'jesse  victor'),
    ('sunrays -flora house', '700797110', 'sunrays -flora house', 'lana plaza  - lavingtone', '2500ksh', '6.4km', 'shadrack atito'),
    ('sam  - branding', '726953055', 'kcb  river road  branch', 'nextgen mall', '10000ksh', '8.1km', 'shadrack atito'),
    ('belizi fashions', '718454949', 'rware busness   centre', 'nextgen mall', '5000ksh', '8.1km', 'shadrack atito'),
    ('classic cosmetics', '700797110', 'dubois beauty stalls', 'classic cosmetics  - moyale mall', '15000ksh', '4.1km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 04.07.2026")
