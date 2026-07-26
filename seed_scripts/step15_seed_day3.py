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
    'sunrays': 372, 'classic': 332, 'clasic': 332, 'adult': 586,
    'wakiarie': 551, 'mtindo': 609, 'superfine': 518, 'troys': 462,
    'alfa': 423, 'baddies': 632, 'bddies': 632, 'fantastic': 633,
    'glory': 489, 'jazi': 583, 'meplux': 341, 'meplaux': 341, 'kiatu': 341,
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
scheduled_date = "2026-07-03"

# [client, phone, pickup, dropoff, value, distance, rider]
rows = [
    ('meplux  - kiatu emporium', '733273632', 'mepalux  - kiatu emporium', 'umoja fanis  limited', '2500ksh', '9.3km', 'johnson wawire'),
    ('meplaux  -kiatu emporium', '733273632', 'mepalux  - kiatu emporium', 'waruku', '1500ksh', '12.0km', 'cyrus ambani'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', 'tsc  kussco -upperhill', '2500ksh', '3.6km', 'willy masinde'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', 'nairobi west    opp  naivas', '1500ksh', '4.4km', 'johnson wawire'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', '5th avenue parklands', '3500ksh', '3.8km', 'shadrack atito'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', 'genuine kunga', '4500ksh', '7.2km', 'shadrack atito'),
    ('adult room   -star mall', '106205106', 'adult room  -starmall', 'kasarni  - sunton', '2500ksh', '15.9km', 'cyrus ambani'),
    ('wakiarie  business', '742537182', 'wakiarie   business', 'eastleigh  - shnghai mall', '3000ksh', '4.9km', 'willy masinde'),
    ('wakiarie  business', '742537182', 'wakiarie   business', 'kenya cinema', '1500ksh', '1.4km', 'willy masinde'),
    ('baddies empire', '714156104', 'baddies  empire  - dynamic mall', '108 riverside drive   appartments', '4500ksh', '6.8km', 'willy masinde'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', 'westlands   , church rd', '2500ksh', '2.7km', 'johnson wawire'),
    ('sunrays -flora house', '700797110', 'sunrays   flora house', 'beba beba   shopping mall', '2500ksh', '850m', 'johnson wawire'),
    ('mtindo wear-  kitengela', '710130388', 'supermetro', 'pick up mtaani', '1500ksh', '750m', 'shadrack atito'),
    ('mtindo wear-  kitengela', '710130388', 'gogo mall', 'hazina trade center', '1500ksh', '3.1km', 'shadrack atito'),
    ('mtindo wear-  kitengela', '710130388', 'gogo mall', 'raha parcel -tea room', '1500ksh', '1.0km', 'shadrack atito'),
    ('mtindo wear-  kitengela', '710130388', 'gogo mall', 'supermetro- kikuyu', '1500ksh', '1.2km', 'shadrack atito'),
    ('mtindo wear-  kitengela', '710130388', 'gogo mall', 'buruburu', '1500ksh', '7.0km', 'shadrack atito'),
    ('mtindo wear-  burburu', '710130388', 'mtindo wear    buruburu junction', 'super metro  - kintengala route', '2500ksh', '2.7km', 'jesse victor'),
    ('glory kitchenware -almond park', '113235433', 'glory kitchenware  - almond park', 'the cycads , mimosa  kamiti rd', '1500ksh', '18.3km', 'cyrus ambani'),
    ('fantastic fit', '745681950', 'bus station', 'jacaranda  garden   , kamiti rd', '2500ksh', '15.5km', 'jesse victor'),
    ('classic    cosmetics', '700797110', 'classic cosmetics', 'kasarni', '10000ksh', '12.1km', 'jesse victor'),
    ('superfine beddings -shop 42', '717679016', 'super fine beddings   -shop 42', 'pipeline', '2500ksh', '13.5km', 'willy masinde'),
    ('superfine beddings -shop 42', '717679016', 'superfine beddings', 'kileleshwa', '2500ksh', '7.6km', 'willy masinde'),
    ('superfine beddings -shop 42', '717679016', 'superfinne beddings', 'kayole- mihango stage', '2500ksh', '23.0km', 'willy masinde'),
    ('classic    cosmetics', '700797110', 'classic cosmetics', 'simba coach', '10000ksh', '5.8km', 'daniel nyakundi'),
    ('jazi sportwear', '748747848', 'jazi sportwear', 'the hedge kamakis', '1500ksh', '26.2km', 'johnson wawire'),
    ('alfa fashions', '', 'rng plaza', 'trintas   school in lavington', '2000ksh', '9.8km', 'johnson wawire'),
    ('bddies empire', '714156104', 'baddies  empire  - dynamic mall', 'golden heights mirema', '2400ksh', '13.0km', 'johnson wawire'),
    ('baddies empire', '714156104', 'baddies  empire  - dynamic mall', 'cieko rd', '2400ksh', '4.5km', 'shadrack atito'),
    ('troys closets', '704476804', 'hakati business centre', 'alsopps -magunas supermarket', '1500ksh', '10.5km', 'daniel nyakundi'),
    ('classic    cosmetics', '', 'dyce', 'classic cosmetics', '', '0km', 'daniel nyakundi'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 03.07.2026")
