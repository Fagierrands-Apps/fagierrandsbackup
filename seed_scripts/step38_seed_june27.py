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
    'sunrays': 372, 'sunray': 372,
    'tracey': 196, 'baddies': 196,
    'yyvonne': 631, 'yyvone': 631,
    'wakiarie': 551,
    'joy': 462,
    'jazi': 583, 'jazzy': 583,
    'sekani': 385,
    'hakati': 641, 'athiambo': 634,
    'kiatu': 341,
    'classic': 332,
    'lornak': 645,
    'mtindo': 609,
    'vanessa': 646,
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
scheduled_date = "2026-06-27"

rows = [
    ('sunrays  -flora house', '700797110', 'sunrays  - flora house', 'un   - gigiri', '1500ksh', '7.6km', 'willy masinde'),
    ('tracey  -baddies   empire', '745576790', 'diamond  plaza', 'hirson towers   -   biashara street', '2500ksh', '5.4km', 'jesse victor'),
    ('tracey  -baddies   empire', '745576790', 'diamond  plaza', 'cbd', '35000ksh', '0km', 'jesse victor'),
    ('yyvonne  - jitihada', '794447655', 'yyvonne  jitihada', 'g- cpoach  -eastleigh', '6500ksh', '3.3km', 'shadrack atito'),
    ('wakiarie  business', '742537182', 'wakiarie  business', 'nairobi water   springs', '10000ksh', '15.5km', 'cyrus ambani'),
    ('joy business', '718840856', 'glory safaris  - rpahta rd', 'gitaru market', '10000ksh', '15.9km', 'johnson wawire'),
    ('jazi sportswear', '748747848', 'capital center', 'royal complex kileleshwa', '1500ksh', '12.4km', 'cyrus ambani'),
    ('sekani', '118260620', 'northside apartments', 'focus academy -membley', '1500ksh', '21.4km', 'shadrack atito'),
    ('sunrays  -flora house', '700797110', 'sunrays  - flora house', 'shamza residency parklands', '2000ksh', '4.7km', 'johnson wawire'),
    ('hakati business -athiambo thrift', '112012425', 'hakati business', 'lamuria gardens', '1500ksh', '6.2km', 'shadrack atito'),
    ('sunrays  -flora house', '700797110', 'sunrays  -flora house', 'south c', '2500ksh', '7.4km', 'shadrack atito'),
    ('kiatu emporium', '710130388', 'mepalux plaza', 'westlands', '1500ksh', '4.5km', 'jesse victor'),
    ('classic cosmetics', '700797110', 'classic cosmetics', 'northrift  shuttle', '10000ksh', '4.9km', 'daniel nyakundi'),
    ('lornak', '728382117', 'royal palm mall', 'zealgym marurui', '2500ksh', '14.9km', 'willy masinde'),
    ('mtindo wear', '710130388', 'supermetro', 'gogo mall', '3000ksh', '750m', 'johnson wawire'),
    ('mtindo wear', '710130388', 'gogo mall', 'buscar', '1500ksh', '1.2km', 'johnson wawire'),
    ('mtindo wear', '710130388', 'gogo mall', 'nnus parcel', '1500ksh', '700m', 'johnson wawire'),
    ('yyvonne  - jitihada', '794447655', 'yyvonne  jitihada', 'komarock', '2000ksh', '13.2km', 'willy masinde'),
    ('vanessa', '718803000', 'hakati business', 'roysambu safari park', '2500ksh', '10.3km', 'jesse victor'),
    ('classic cosmetics', '700797110', 'classic cosmetics', 'glob Arusha', '15000ksh', '4.4km', 'daniel nyakundi'),
    ('sunrays  -flora house', '700797110', 'sunrays  -flora house', 'kileleshwa', '2500ksh', '5.7km', 'johnson wawire'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 27.06.2026")
