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
    'sekani': 385, 'yyvone': 631, 'yyvonne': 631,
    'mtindo': 609, 'sunrays': 372, 'sunray': 372,
    'kiatu': 341, 'avana': 521,
    'gloria': 489, 'glory': 489,
    'athiambo': 634, 'classic': 332,
    'nancy': 490, 'andrew': 607,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'wawrie': 374, 'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = name.lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-06-26"

rows = [
    ('sekani  - northside apppartments', '118260620', 'northside apartments', 'Covo square', '2000ksh', '6.5km', 'johnson wawrie'),
    ('yyvone  - jitihada', '794447655', 'yyvone  -jitihada', 'gachie   mugacha   shopping   centre', '7000ksh', '16.3km', 'johnson wawrie'),
    ('mtindo wear  -  kitengela', '710130388', 'pick up mtaani', 'young  garden    kilimani', '1500ksh', '7.4km', 'willy masinde'),
    ('mtindo wear  -  kitengela', '710130388', 'pick  up mtaani', 'ngara', '1500ksh', '1.5km', 'willy masinde'),
    ('mtindo wear  -  kitengela', '710130388', 'pick  up mtaani', 'kilelelshwa    nyando   rd', '1500ksh', '6.6km', 'willy masinde'),
    ('mtindo wear  -  kitengela', '710130388', 'pick up mtaani', 'langata    gardens', '2000ksh', '12.4km', 'willy masinde'),
    ('mtindo wear  -  kitengela', '710130388', 'pick up-mtaani', 'donholm green fielf  estate    phase 7', '1500ksh', '10.5km', 'willy masinde'),
    ('mtindo wear  -  kitengela', '710130388', 'pick up-mtaani', 'mhiko stage opp platinum plaza', '2000ksh', '1.4km', 'cyrus ambani'),
    ('mtindo wear  -  kitengela', '710130388', 'budget wear', 'pick up-mtaani', '1500ksh', '1km', 'willy masinde'),
    ('sunrays  cosmetics', '700797110', 'sunrays  cosmetics', 'langata   ngei   2 estate     house 14', '2000ksh', '9.5km', 'cyrus ambani'),
    ('kiatu empoarium  -mepalux', '711304514', 'kiatu  emporium   -meplaux', 'fortis upperhill   - knh   hospital', '1500ksh', '5.3km', 'cyrus ambani'),
    ('avana soles', '702840229', 'avana soles  -kariakor', 'westlands sport   road', '2500ksh', '7.3km', 'jesse victor'),
    ('sunrays  cosmetics', '700797110', 'sunrays  cosmetics', 'westalnds', '1500ksh', '2.7km', 'jesse victor'),
    ('sunrays  cosmetics', '700797110', 'sunrays  cosmetics', 'ngei estate phase', '1500ksh', '9.3km', 'cyrus ambani'),
    ('gloria kitchenware -almond park  off  - kilif close', '707414270', 'gloria kitchen ware   -almond park off  kilif close', 'mkoko   appartments  ,mkoko close', '3500ksh', '11.6km', 'johnson wawrie'),
    ('athiambo thrift  - hakati', '112012425', 'athiambo  - hakati', 'rosa appartments   opposite total filling station', '1500ksh', '6.5km', 'cyrus ambani'),
    ('classic   cosmetics  -moyale mall', '700797110', 'classic  cosmetics  - moyale mall', 'buscar  -charles rubia   house', '2500ksh', '5.4km', 'daniel nyakundi'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'soweto -kayole', '1500ksh', '12.3km', 'jesse victor'),
    ('nancy  - lister  carwash', '721429708', 'prescom computer - moi avenue', 'listers carwash', '3000ksh', '4.3km', 'johnson wawrie'),
    ('kiatu empoarium  -mepalux', '710130388', 'kiatu  emporium   -meplaux', 'ngara', '1500ksh', '1.4km', 'jesse victor'),
    ('classic   cosmetics  -moyale mall', '722995300', 'classic  cosmetics  - moyale mall', 'bebeto  coaches', '7000ksh', '6.5km', 'daniel nyakundi'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'valley arcade  ngong rd', '2500ksh', '7.3km', 'jesse victor'),
    ('andrew  -philadelphia', '700797110', 'andrew -philadelphia', 'kilimani -  komolane   off wood avenue', '2000ksh', '6.3km', 'johnson wawrie'),
    ('andrew  -philadelphia', '700797110', 'andrew -philadelphia', 'corner heights  appartments', '1500ksh', '9.5km', 'johnson wawrie'),
    ('andrew  -philadelphia', '700797110', 'andrew -philadelphia', 'lower kabete   -rosehill  residence', '1500ksh', '10.0km', 'johnson wawrie'),
    ('sunrays cosmetics-flora house', '700797110', 'sunrays    cosmetics  - flora house', 'suthern oasis    appartments', '2500ksh', '6.3km', 'johnson wawrie'),
    ('athiambo thrift  - hakati', '112012425', 'athiambo  - hakati', 'accacia   green academy', '1500ksh', '16.0km', 'cyrus ambani'),
    ('classic   cosmetics  -moyale mall', '700797110', 'classic  cosmetics  - moyale mall', 'bunromaline', '2000ksh', '5.4km', 'daniel nyakundi'),
    ('classic   cosmetics  -moyale mall', '700797110', 'classic  cosmetics  - moyale mall', 'the great rift shuttle', '6000ksh', '7.1km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 26.06.2026")
