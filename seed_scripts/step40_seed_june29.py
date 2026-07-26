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
    'adult': 586, 'joy': 462,
    'tracey': 196, 'baddies': 196,
    'queens': 595,
    'charles': 242, 'kunga': 242,
    'yyvonne': 631, 'yyvone': 631,
    'avana': 521, 'fitbox': 338,
    'gloria': 489, 'almond': 489,
    'alfa': 423,
    'athiambo': 634, 'classic': 332,
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
scheduled_date = "2026-06-29"

rows = [
    ('Adult room- new client', '106205106', 'starmall', 'imara daima', '2500ksh', '11.6km', 'cyrus ambani', 'completed'),
    ('Joy business', '718840856', 'jethwa mansion', 'wanginge - total petrol  station', '10000ksh', '15.5km', 'willy masinde', 'completed'),
    ('tracey  -baddies empire', '745576790', 'tracey baddies empire', 'one    padmore   plaza kilimani', '2500ksh', '9.2km', 'cyrus ambani', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'gachie', '1500ksh', '13.6km', 'johnson wawire', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'imara noble park appartments', '1500ksh', '12.7km', 'johnson wawire', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'kiamumbi', '1500ksh', '18.3km', 'johnson wawire', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'wanyee road   , alba appartment', '1500ksh', '8.9km', 'johnson wawire', 'completed'),
    ('charles  - genuine  kunga therapy', '700797110', 'sunrays cosmetics', 'genuine kunga', '4500ksh', '7.9km', 'cyrus ambani', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'buscar', '1500ksh', '1.5km', 'johnson wawire', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'tahmeed', '1500ksh', '1.3km', 'johnson wawire', 'completed'),
    ('queens choice', '768887510', 'biashara street', 'chania', '1500ksh', '1.5km', 'johnson wawire', 'completed'),
    ('yyvonne jitihada', '768887510', 'jitihada', 'oak classic   residency', '6500ksh', '5.3km', 'johnson wawire', 'completed'),
    ('avana soles  - karioakor', '702840229', 'avana soles', 'enabled   shuttle    -national archives', '2000ksh', '2.7km', 'daniel nyakundi', 'completed'),
    ('fitbox  -ke  - kamukunji', '759396635', 'fitbox  -ke  -kamukunji', 'matasia', '4500ksh', '0km', 'willy masinde', 'rescheduled'),
    ('joy  business', '718840856', 'jethwa mansion', 'pension towers  - loita  street', '10000ksh', '1.3km', 'johnson wawire', 'completed'),
    ('almond park   - gloria kitchenware', '113235433', 'almond kitchenware', 'palm valey  appartments   , lavingtone masanduku lane', '4500ksh', '23.5km', 'johnson wawire', 'completed'),
    ('alfa fashions   -rng plaza', '796736969', 'alfa fashions  - rng plaza', 'north airport  rd  -easa', '1500ksh', '14.6km', 'cyrus ambani', 'rescheduled'),
    ('athiambo   thrift  - hakati', '112012425', 'athiambo  thrift   - hakati', 'kilimni  alina habour', '1500ksh', '6.4km', 'cyrus ambani', 'completed'),
    ('classic  comsetics   -moyale mall', '700797110', 'dyce beauty shop  -   dubois beauty  stalls', 'classic cosmetics  -moyale mall', '', '4.1km', 'daniel nyakundi', 'completed'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 29.06.2026")
