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

def get_status(raw):
    raw = raw.lower().strip()
    if 'progress' in raw: return 'in_progress'
    return 'completed'

clients = {
    'jazi': 583, 'jazzy': 583,
    'sunrays': 372, 'sunray': 372,
    'kevo': 575, 'new client': 575,
    'joe': 568,
    'classic': 332,
    'kiatu': 341,
    'adhiambo': 634, 'athiambo': 634,
    'essylan': 639,
    'belizi': 423,
    'yyvonne': 631, 'yyvone': 631,
    'alfa': 423,
    'chelsea': 452,
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
scheduled_date = "2026-06-22"

rows = [
    ('jazi sportwear  - capital centre', '748747848', 'jazi  sportwear - capital centre', 'five star paradise -runda', '2500ksh', '17.7km', 'shadrack atito', 'completed'),
    ('sunrays  cosmetics  - perida business centre', '700797110', 'sunrays   cosmerics  -perida business centre', 'fromat   village    -riara rd', '1500ksh', '8.5km', 'jesse  victor', 'completed'),
    ('kevo  -  new client', '782909422', 'nssf  - cimmunity road', 'samosa wrld - imara daima', '', '23km', 'johnson wawire', 'completed'),
    ('joe - new client', '748342756', 'nextgen  mall', 'wilson airport', '4000ksh', '5.7km', 'cyrus ambani', 'completed'),
    ('joe - new client', '748342756', 'wilson airport', 'nextgen mall', '4000ksh', '5.7km', 'cyrus ambani', 'completed'),
    ('classic cosmetics- moyale mall', '722995300', 'jamwass   beauty store - dubois rd', 'classic comsetics', '15000ksh', '4.6km', 'daniel nyakundi', 'completed'),
    ('classic cosmetics- moyale mall', '722995300', 'dyce beauty store', 'classic comsetics', '2000ksh', '4.6km', 'daniel nyakundi', 'completed'),
    ('kevo  -  new client', '782909422', 'nssf  - cimmunity road', 'survey-thika rd', '', '5.7km', 'shadrack atito', 'completed'),
    ('classic cosmetics- moyale mall', '722995300', 'classic  cosmetics  - moyale mall', 'simba coach', '15000ksh', '5.7km', 'daniel nyakundi', 'completed'),
    ('kiatu emporium  - meplaux', '711304514', 'kiatu emporium  - mepalux plaza', 'ngong prisim towers', '2000ksh', '3.4km', 'jesse  victor', 'completed'),
    ('adhiambos    thrift  -   hakati business', '112012425', 'athiambos  thrift   -hakati   business', 'naivasha rd', '1500ksh', '12.0km', 'johnson wawire', 'completed'),
    ('essylan jeweleries -kampla bsuiness centre', '706134011', 'essylan  jeweleries    -kampala  business centre', 'astrapark  appartments   south b', '2500ksh', '7.5km', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'star mall', '3500ksh', '200m', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'platinum plaza', '3500ksh', '160m', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'bazaar', '3500ksh', '650m', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'uganda house', '3500ksh', '700m', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'technical university of kenya', '3500ksh', '1.4km', 'cyrus ambani', 'completed'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'fig tree  trade centre', '3500ksh', '1.2km', 'cyrus ambani', 'in progress'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'parklands', '3500ksh', '3.8km', 'cyrus ambani', 'in progress'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'red ginger', '3500ksh', '3.7km', 'cyrus ambani', 'in progress'),
    ('belizi fashions', '704476804', 'iconic  business plaza', 'south b   south gate', '3500ksh', '4.7km', 'cyrus ambani', 'in progress'),
    ('yyvonne  - jitihada  house', '794447655', 'yyvonne jitihada   house', 'lavington', '6500ksh', '6.3km', 'jesse  victor', 'completed'),
    ('yyvonne  - jitihada  house', '794447655', 'lavington', 'yyvonne   jithada   house', '6500ksh', '6.3km', 'jesse  victor', 'completed'),
    ('sunrays  cosmetics  -flora house', '700797110', 'sunrays  cosmetics  - flora house', '12th street  -eastleigh', '1500ksh', '3.6km', 'cyrus ambani', 'in progress'),
    ('sunrays cosmetics- flora house', '700797110', 'sunrays cosmetics - flora house', 'crescent buisness centre    parklands', '2500ksh', '3.1km', 'willy masinde', 'completed'),
    ('alfa fashions', '796736969', 'rng plaza', 'palm garden  estate', '1500ksh', '10.0km', 'shadrack atito', 'completed'),
    ('classic cosmetics- moyale mall', '722995300', 'classic  cosmetics  - moyale mall', 'ena coach', '10000ksh', '5.0km', 'daniel nyakundi', 'completed'),
    ('chelsea   flowers-city mrket', '708830753', 'chelsea city market', 'kasarani maternity   hosiptal', '', '14.7km', 'johnson wawire', 'completed'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, value, dist, rider, status in rows:
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
    completed_at = f"'{now}'" if status == 'completed' else 'NULL'
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
            {price}, '{status}', '{now}', '{now}', {completed_at},
            {client_id}, {rider_id}, 2,
            {km}, true, {est_val}
        ) RETURNING id, client_id, assistant_id, price, status;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for 22.06.2026")
