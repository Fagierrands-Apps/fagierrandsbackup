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
    'classic': 332, 'clasic': 332,
    'belizi': 423,
    'sekani': 385, 'sekni': 385,
    'hakati': 641, 'toreys': 462, 'troys': 462,
    'jitihada': 631, 'yyvonne': 631,
    'muna': 488,
    'jazy': 583, 'jazi': 583,
    'gitau': 460,
    'wakiarie': 551,
    'athiambo': 634,
    'edna': 606,
    'andrew': 607,
}

riders = {
    'shadrack': 477, 'shadarack': 477, 'atitio': 477,
    'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = name.lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-06-18"

rows = [
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'south c', '2000ksh', '7.4km', 'jesse victor'),
    ('classic cosmetic - moyale mall', '722995300', 'ena couch', 'classic cosmetic', '10000ksh', '4.7km', 'daniel nyakundi'),
    ('belizi fashions', '704476804', 'cbd  - tommboya', 'westen heights', '3500ksh', '4.6km', 'willy masinde'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'genuine kunga   therapy', '3000ksh', '7.3km', 'johnson wawire'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', '80 mzizma springs   rd , lavingtone', '1500ksh', '7.8km', 'johnson wawire'),
    ('sekani flowers   -northside appartments', '118260620', 'sekni flowers  - northside   appartments', 'ole   sangale  link', '3500ksh', '6.2km', 'jesse victor'),
    ('hakati  -toreys   closet', '704476804', 'hakati-toreys closet', 'skyhorse  appartment   kilimani', '1500ksh', '5.7km', 'jesse victor'),
    ('jitihada   -yyvonne', '794447655', 'jitihada  - yyvonne', '55  muthangari drive', '6500ksh', '7.4km', 'willy masinde'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'winchester   garden  , amazing   drive', '15000ksh', '5.8km', 'shadrack atitio'),
    ('classic cosmetic - moyale mall', '722995300', 'supreme arcade', 'classic cosmetic', '', '4.6km', 'daniel nyakundi'),
    ('city market - muna flowers', '', 'city market  - muna flowers', 'cbd', '2500ksh', '0km', 'jesse victor'),
    ('classic cosmetic - moyale mall', '722995300', 'classic cosmetic  - moyale mall', 'buscar -charles rubia rd', '10000ksh', '5.3km', 'johnson wawire'),
    ('classic cosmetic - moyale mall', '722995300', 'dyce cosmetics', 'classic cosmetic', '20000ksh', '4.1km', 'daniel nyakundi'),
    ('classic cosmetic - moyale mall', '722995300', 'classic cosmetic  - moyale mall', '12th street eastleigh', '10000ksh', '2.6km', 'jesse victor'),
    ('classic cosmetic - moyale mall', '722995300', 'classic cosmetic  - moyale mall', 'moi avenue', '4000ksh', '5.5km', 'jesse victor'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'r.king african culture', '2500ksh', '9.7km', 'willy masinde'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'pagani msikiti hindi', '3000ksh', '4.4km', 'cyrus ambani'),
    ('toreys closet', '704476804', 'hakati-toreys closet', 'olenguruone avenue', '1500ksh', '7.3km', 'johnson wawire'),
    ('athiambo  - thrift -hakati business', '112012425', 'athiambo thrift  -hakati   business', 'Leshwa House 1, Othaya Rd, Nairobi', '1500ksh', '7.4km', 'johnson wawire'),
    ('athiambo  - thrift -hakati business', '112012425', 'athiambo thrift  -hakati   business', 'nnus office - naivasha', '1500ksh', '900m', 'johnson wawire'),
    ('athiambo  - thrift -hakati business', '112012425', 'athiambo thrift  -hakati   business', 'chaina cool- ukunda', '1500ksh', '1.0km', 'johnson wawire'),
    ('jazy sportwear', '748747848', 'capital centre  - jazi sportwear', 'Five star phase South C', '2500ksh', '3.0km', 'shadrack atitio'),
    ('gitau flowers-nairobi flowers', '791418630', 'nairobi flowers', 'kahawa  garrison', '3000ksh', '17.0km', 'shadrack atitio'),
    ('wakiarie business', '742537182', 'afya centre', 'westlands', '5000ksh', '4.9km', 'johnson wawire'),
    ('wakiarie business', '742537182', 'afya centre', 'westlands', '5000ksh', '4.9km', 'johnson wawire'),
    ('classic cosmetic - moyale mall', '722995300', 'dyce beauty store-dubois', 'classic cosmetic', '10000ksh', '4.2km', 'daniel nyakundi'),
    ('edna kelvins-philadelphia house', '718820994', 'edna  kelvins   -philadelphia  house', 'kk appartments   1st avenue -parklands', '1500ksh', '4.1km', 'johnson wawire'),
    ('edna kelvins-philadelphia house', '718820994', 'edna  kelvins   -philadelphia  house', 'checkper   appartemnents  -langata', '1500ksh', '8.2km', 'johnson wawire'),
    ('andrew-philadelphhia   house', '702483450', 'andrew', 'wambco apartments-south c', '1500ksh', '4.1km', 'johnson wawire'),
    ('andrew-philadelphhia   house', '702483450', 'andrew', 'shangri-la residency westlands', '1500ksh', '6.0km', 'johnson wawire'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 18.06.2026")
