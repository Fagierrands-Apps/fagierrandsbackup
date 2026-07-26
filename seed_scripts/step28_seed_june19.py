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
    'sekani': 385, 'nairobi flower': 608,
    'gloria': 489, 'glory': 489,
    'purple': 408, 'belizi': 423,
    'jitihada': 631, 'yyvonne': 631, 'yyvone': 631,
    'mtindo': 609, 'edna': 606,
    'jazzy': 583, 'jazy': 583, 'jazi': 583,
    'joy': 462, 'classic': 332,
    'alfa': 423, 'gathu': 640,
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
scheduled_date = "2026-06-19"

rows = [
    ('sekani  - northside apppartments', '118260620', 'northside apartments', 'nairobi chapel -ngong road', '2500ksh', '10.9km', 'johnson wawire'),
    ('Nairobi flower center', '791418630', 'sianda house', 'eastliegh', '6000ksh', '6.0km', 'willy masinde'),
    ('gloria kitchenware', '113235433', 'gloria kitchenware', 'kitsuru   estate', '5000ksh', '15.4km', 'jesse victor'),
    ('purple heart - nextgen mall', '700276582', 'purpleheart  - nextgen', 'mayeast  -langata  south', '3000ksh', '15.1km', 'cyrus ambani'),
    ('purple heart - nextgen mall', '700276582', 'mayeast 17b langata   south', 'ivory heights  appartments    -naivasha rd', '3000ksh', '17.8km', 'cyrus ambani'),
    ('belizi fashions', '704111224', 'belizi fashions   -star court', 'palm flats   appartments', '3500ksh', '21.5km', 'willy masinde'),
    ('jitihada  -  yyvone', '794447655', 'jitihada  -yyvonne', 'south c -superloaf', '6450ksh', '7.3km', 'willy masinde'),
    ('mtindo  wear - hakati', '729620888', 'mtindo wera  - hakati', 'pick up mtaani', '5000ksh', '1.1km', 'cyrus ambani'),
    ('mtindo  wear - hakati', '729620888', 'pick up mtaani', 'bus car - charles rubia', '1500ksh', '1.5km', 'cyrus ambani'),
    ('mtindo  wear - hakati', '729620888', 'pick up mtaani', 'great rift   shuttles', '1500ksh', '2.2km', 'cyrus ambani'),
    ('belizi fashions', '704476804', 'bazaar', 'lavender heights', '1000ksh', '12.3km', 'jesse victor'),
    ('edna  kelvins   -philadephia', '718820994', 'edna  kelvins -philadephia', 'riara    road', '1500ksh', '8.2km', 'cyrus ambani'),
    ('jazzy   - capital centre', '748747848', 'jazzy  -capitla centre', 'city stadium    -ack maridadi', '2500ksh', '7.0km', 'willy masinde'),
    ('joy business', '718840856', 'east matt opp khoja stage', 'st mathews  mukui', '5000ksh', '22.3km', 'johnson wawire'),
    ('classic   cosmetics-moyale mall', '722995300', 'dyce beauty store', 'classic cosmetics-moyale mall', '15000ksh', '4.1km', 'daniel nyakundi'),
    ('alfa collections -rng plaza', '713306041', 'rng plaza  - f 27', 'asmara restaurant', '2500ksh', '5.7km', 'johnson wawire'),
    ('yyvone  -jitihada', '794447655', 'yyvonne -jitihada', 'endevile phase 2', '7500ksh', '14.1km', 'jesse victor'),
    ('gathu-new client', '742049907', 'keekorok', 'kihunguro  ruiru', '3500ksh', '23.7km', 'jesse victor'),
    ('classic   cosmetics-moyale mall', '722995300', 'dyce beauty store', 'classic cosmetics-moyale mall', '10000ksh', '4.1km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 19.06.2026")
