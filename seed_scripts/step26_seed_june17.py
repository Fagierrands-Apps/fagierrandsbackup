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
    if 'rescheduled' in raw: return 'rescheduled'
    return 'completed'

clients = {
    'health': 472, 'helath': 472,
    'sunrays': 372, 'sunray': 372,
    'aoko': 599,
    'glory': 489, 'gloria': 489,
    'muna': 488,
    'maggie': 605,
    'belizi': 423,
    'toreys': 462, 'troys': 462,
    'classic': 332,
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
scheduled_date = "2026-06-17"

rows = [
    ('helath classique -nextgen', '722995300', 'nextgen mall  - health classique', 'rayan coach eastleigh', '3500ksh', '7.5km', 'cyrus ambani', 'completed'),
    ('sunrays  - flora  house', '700797110', 'sunrays  -flora house', 'lusaka rd , pemba   street', '2500ksh', '3.9km', 'willy masinde', 'completed'),
    ('aoko -   thika ymca', '706432898', 'aoko   -thika ymca', 'dynamic mall', '4000ksh', '44.4km', 'johnson wawire', 'completed'),
    ('aoko -   thika ymca', '706432898', 'dyanmic mall', 'eph', '1500ksh', '700m', 'johnson wawire', 'completed'),
    ('aoko -   thika ymca', '706432898', 'eph', 'nyamakima', '1500ksh', '850m', 'johnson wawire', 'completed'),
    ('aoko -   thika ymca', '706432898', 'nyamakima', 'riverroad', '1000ksh', '800m', 'johnson wawire', 'completed'),
    ('glory kitchenware', '113235433', 'glory kitchenware', 'iguta paradise - runda', '6000ksh', '16.6km', 'shadrack atito', 'completed'),
    ('muna  flowers  - tabman rd', '724906221', 'muna  flowers  -tabman rd', 'qwetu abadare heights  usisu rd', '2000ksh', '11.3km', 'willy masinde', 'completed'),
    ('maggie', '720561713', 'superior   arcade   shop g1', 'prittlane   house   b3', '1000ksh', '9.4km', 'shadrack atito', 'completed'),
    ('maggie', '720561713', 'prittlane house   b3', 'superior arcade', '1000ksh', '9.4km', 'shadrack atito', 'completed'),
    ('maggie', '720561713', 'superior   arcade   shop g1', 'prittlane   house   b3', '1000ksh', '9.4km', 'shadrack atito', 'completed'),
    ('belizi fashions', '704476804', 'imenti house', 'lavender heights', '2500ksh', '12.0km', 'cyrus ambani', 'completed'),
    ('belizi  fashions', '704476804', 'kbs garage   -eastleigh', 'star court  -syokimau', '6000ksh', '16.2km', 'willy masinde', 'completed'),
    ('toreys  -hakati  business', '704476804', 'toreys -hakati business', 'kahawa sukari   , taveta rd', '1500ksh', '19.3km', 'johnson wawire', 'completed'),
    ('toreys  -hakati  business', '704476804', 'toreys -hakati business', '40   rosslyn   lone tree', '1500ksh', '13.3km', 'johnson wawire', 'completed'),
    ('belizi  fashions', '704476804', 'star court', 'nextgen', '4000ksh', '11.8km', 'willy masinde', 'completed'),
    ('classic cosmetics', '721420878', 'classic cosmetics', 'burma market', '3500ksh', '5.6km', 'daniel nyakundi', 'completed'),
    ('health classique', '722995300', 'nextgen mall  - health classique', 'Total Thome', '15000ksh', '19.2km', 'shadrack atito', 'completed'),
    ('health classique', '722995300', 'nextgen mall  - health classique', 'sasa mall', '10000ksh', '6.7km', 'cyrus ambani', 'completed'),
    ('chelsea flowers  - city market', '708830753', 'chelsea flowers  -city market', 'eastleigh ushikrika', '1400ksh', '5.9km', 'cyrus ambani', 'completed'),
    ('belizi  fashions', '704476804', 'star court -syokimau', 'western heights', '3500ksh', '21.1km', 'willy masinde', 'rescheduled'),
    ('classic cosmetics', '722995300', 'ena coach', 'classic cosmetics', '10000ksh', '4.7km', 'daniel nyakundi', 'rescheduled'),
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

print(f"\nDone: {success} inserted, {skipped} skipped for 17.06.2026")
