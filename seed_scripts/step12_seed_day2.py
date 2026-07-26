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
        if 'km' in s:
            km = float(s.replace('km','').strip())
        elif 'm' in s:
            km = float(s.replace('m','').strip()) / 1000
        else:
            km = float(s)
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_value(v):
    try:
        return float(''.join(c for c in v if c.isdigit() or c == '.'))
    except:
        return 0

def parse_km(km_str):
    try:
        s = km_str.lower().strip()
        if 'km' in s: return float(s.replace('km','').strip())
        if 'm' in s: return round(float(s.replace('m','').strip()) / 1000, 3)
        return float(s)
    except:
        return 0

clients = {
    'sunrays': 372, 'classic': 332, 'clasic': 332, 'fitbox': 338,
    'adult': 586, 'belizi': 423, 'mtindo': 609, 'queens choice': 595,
    'platinum': 629, 'nairobi flower': 608, 'nia petals': 628,
    'micheal': 630, 'yyvonne': 631, 'kaiatu': 341, 'kiatu': 341,
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
scheduled_date = "2026-07-02"

# [client, phone, pickup, dropoff, value, distance, rider]
rows = [
    ('queens choice   -afya centre', '768887510', 'queens choice  - afya cente', 'qwetu  wilson view', '3500ksh', '6.1km', 'shadrack atito'),
    ('sunrays -flora house', '700797110', 'sunrays  - flora house', 'kenrails -towers-westalnds', '2500ksh', '4.3km', 'johnson wawire'),
    ('platinum plaza', '', 'platinum plaza', 'jitihada', '3500ksh', '600m', 'willy masinde'),
    ('fitbox  - ke', '759396635', 'fitbox  - ke', 'tanzil gardens -five star gardens', '4500ksh', '6.7km', 'jesse victor'),
    ('platinum plaza', '', 'platinum plaza', 'lucky summer', '1500ksh', '15.3km', 'willy masinde'),
    ('belizi faashions', '748399605', 'belizi fashions', 'kileleshwa    lana plaza', '3500ksh', '23.9km', 'cyrus ambani'),
    ('adult room -starmall  - shop a 21', '106205106', 'adult room -starmall shop a21', 'kiambu', '4500ksh', '14.2km', 'johnson wawire'),
    ('kaiatu emporium -meaplux plaza', '733273632', 'kiatu emporium - mepalux plaza', 'ufanis  limited', '1500ksh', '9.4km', 'shadrack atito'),
    ('sunrays -flora house', '700797110', 'sunrays  - flora house', 'garden court - langata', '10000ksh', '7.6km', 'willy masinde'),
    ('micheals  bouquette', '794775593', 'micheal bouquet', 'adlife plaza kilimani', '4500ksh', '5.2km', 'jesse victor'),
    ('yyvonne  -jitihada', '768887510', 'yyvonne jitihada', 'nextgen', '7500ksh', '7.7km', 'willy masinde'),
    ('nia petals  -cianda house   ( city mrkt)', '793956127', 'nia petals   - cianda house', 'westalnds    office park', '4500ksh', '7.3km', 'cyrus ambani'),
    ('adult room -starmall  - shop a 21', '106205106', 'adult room -starmall shop a21', 'brookside drive gate', '2500ksh', '5.3km', 'willy masinde'),
    ('nairobi flowers', '791418630', 'nairobi flowers', 'kpytech   office supplies    limited', '4500ksh', '4.5km', 'shadrack atito'),
    ('mtindo wear', '710130388', 'supermetro', 'gogo mall', '1500ksh', '750m', 'jesse victor'),
    ('clasic cosmertics - moyale mall', '700797110', 'dyce  beauty store', 'classic  cosmetics', '10000ksh', '4.1km', 'daniel nyakundi'),
    ('clasic cosmertics - moyale mall', '700797110', 'dyce  beauty store', 'classic  cosmetics', '10000ksh', '4.1km', 'daniel nyakundi'),
]

success = 0
for client, phone, pickup, dropoff, value, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}' rider='{rider}'")
        continue
    price = calc_price(dist)
    est_val = parse_value(value)
    km = parse_km(dist)
    pickup_e = pickup.strip().replace("'", "''")
    dropoff_e = dropoff.strip().replace("'", "''")
    psql(f"""
        INSERT INTO orders_order (
            title, description, pickup_address, delivery_address,
            contact_number, scheduled_date, price, status,
            created_at, updated_at, completed_at,
            client_id, assistant_id, order_type_id,
            distance, price_finalized, estimated_value
        ) VALUES (
            'Pickup & Delivery Order',
            '{pickup_e} to {dropoff_e}',
            '{pickup_e}', '{dropoff_e}',
            '{phone}', '{scheduled_date}',
            {price}, 'completed',
            '{now}', '{now}', '{now}',
            {client_id}, {rider_id}, 2,
            {km}, true, {est_val}
        ) RETURNING id, client_id, assistant_id, price, estimated_value;
    """)
    success += 1

print(f"\nDone: {success} orders inserted for 02.07.2026")
