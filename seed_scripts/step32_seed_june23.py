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
    'nancy': 490, 'wanjira': 642,
    'gloria': 489, 'glory': 489,
    'classic': 332,
    'rng plaza': 595, 'queens   collection': 595,
    'superfine': 518, 'super fine': 518,
    'toreys': 462, 'troys': 462,
    'fashio': 579,
    'joy': 462,
    'unique': 513,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'johnsons': 374, 'willy': 403, 'jesse': 109, 'daniel': 310,
}

def get_id(name, mapping):
    name = name.lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-06-23"

rows = [
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'lavington -royal villas -masanduku lane', '1500ksh', '9.7km', 'willy masinde'),
    ('sunrays   -flora house', '700797110', 'lavington  -royal villas   -masanduku lane', 'mwajoy    educational centre', '1500ksh', '16.6km', 'willy masinde'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'university of nairobi   dental sch  opp lee funeral', '2000ksh', '2.2km', 'jesse  victor'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', '11th street    2nd avenue   masud   tower', '1500ksh', '3.7km', 'johnsons wawire'),
    ('nancy  - listers  car wash', '721429708', 'super metro   -national archives', 'listers   carwash  - kindaruma rd', '4500ksh', '4.7km', 'willy masinde'),
    ('wanjira - ncba kiambu', '798516007', 'wanjira  - ncba kiambu', 'ack  garden   annex', '', '18.2km', 'johnsons wawire'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'mudzalifa    appartments', '1500ksh', '6.8km', 'cyrus ambani'),
    ('gloria kitchenware -  almond park', '707414270', 'gloria  - kitchenware  -almond park', 'langata   health  - ngei phase 1', '3500ksh', '10km', 'shadrack atito'),
    ('classic cosmetics -moyale mall', '722995300', 'eph coach', 'classisc  cosmetics moyale mall', '8000ksh', '4.6km', 'daniel nyakundi'),
    ('rng plaza   -queens   collection', '710617679', 'rng - queens collection', 'ngong rd   - marsabit plaza', '1000ksh', '8.6km', 'willy masinde'),
    ('classic cosmetics -moyale mall', '722995300', 'classic cosmetics  - moyale mall', 'buscar  - charles rubia rd', '20000ksh', '4.7km', 'daniel nyakundi'),
    ('super fine beddings  -   shop 42', '717679016', 'superfine  beddings  -   shop 42', 'kiambu -clean shelf supermarket', '2500ksh', '16.0km', 'shadrack atito'),
    ('toreys   closet - hakati', '704476804', 'toreys  close  - hakati', 'orkwood  sprigs   - mirema drive', '2000ksh', '12.1km', 'johnsons wawire'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'westlands   -goodman plaza', '1500ksh', '4.9km', 'cyrus ambani'),
    ('fashio fix  -ke', '769777641', 'fashion fix  ke  -mlolongo', 'golden gate  -south b', '1500ksh', '16.5km', 'shadrack atito'),
    ('sunrays   -flora house', '700797110', 'sunrays  -flora house', 'smarthomes   airbnb  -kilimani', '2500ksh', '5.7km', 'cyrus ambani'),
    ('joy-business', '718840856', 'jethwa mansion', 'uthiru', '20000ksh', '16km', 'johnsons wawire'),
    ('toreys   closet - hakati', '704476804', 'toreys  close  - hakati', 'rose  avenue  gate  opp  pacific  insurance', '1500ksh', '5.2km', 'jesse  victor'),
    ('unique collection-rng plaza', '797506825', 'fedha', 'unique   collection  - rng  plaza', '1500ksh', '11.0km', 'jesse  victor'),
    ('unique collection-rng plaza', '797506825', 'unique collection  - rng  plaza', 'fedha', '1500ksh', '11.0km', 'jesse  victor'),
    ('unique collection-rng plaza', '797506825', 'unique collection  - rng  plaza', 'pipeline', '1500ksh', '12.1km', 'jesse  victor'),
    ('joy-business', '718840856', 'jethwa mansion', 'glory safaris  - rpahta  rd', '20000ksh', '5.0km', 'willy masinde'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 23.06.2026")
