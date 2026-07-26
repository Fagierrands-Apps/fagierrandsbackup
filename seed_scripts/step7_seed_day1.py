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
        km = float(km_str.lower().replace('km','').replace('m','').strip())
        if 'm' in km_str.lower() and 'km' not in km_str.lower():
            km = km / 1000
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_value(val_str):
    try:
        return float(''.join(c for c in val_str if c.isdigit() or c == '.'))
    except:
        return 0

# Client name -> DB user ID
clients = {
    'sunrays': 372,
    'classic': 332,
    'fitbox': 338,
    'sekni': 385,
    'sekani': 385,
    'wakiarie': 551,
    'mtindo': 609,
    'belizi': 423,
    'adult': 586,
    'avana': 521,
    'troys': 462,
    'superfine': 518,
    'liz kwame': 156,
    'fadhili': 623,
    'siens': 624,
    'sienz': 624,
}

# Rider name -> DB user ID
riders = {
    'shadrack': 477,
    'shadarack': 477,
    'cyrus': 375,
    'johnson': 374,
    'willy': 403,
    'willis': 403,
    'jesse': 109,
    'daniel': 310,
}

def get_client_id(name):
    name = name.lower().strip()
    for key, uid in clients.items():
        if key in name:
            return uid
    return None

def get_rider_id(name):
    name = name.lower().strip()
    for key, uid in riders.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-01"

rows = [
    ['', 'kevo', 'completed', 'sunrays   cosmetics  -flora house', '700797110', 'sunrays   cosmetics   -flora house  ', 'stima plaza -ngara', '2500ksh', '700797110', '2.1km', 'cyrus ambani', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'fitbox - kamukunji  police station', '759396635', 'firbox   - kamukunji   police station', 'the hub -karen', '2500ksh', '759396635', '15.7km', 'johnson wawire', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'sekni  flowers - northside appartments', '118260620', 'sekani  flowers   - northside  appartments', 'langata', '3500ksh', '118260620', '17.0km', 'shadrack atito', 'flowers', 'paid', ''],
    ['', 'kevo', 'completed', 'sunrays   cosmetics  -flora house', '700797110', 'sunrays   cosmetics   -flora house', 'royal canaan nairobi hotel', '2500ksh', '700797110', '5.9km', 'cyrus ambani', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'classic   cosmetics  - moyale mall', '700797110', 'dyc   beauty shop  - dubois', 'classic  cosmetics  - moyale mall', '15000ksh', '700797110', '5.7km', 'daniel nyakundi', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'wakiarie-business', '742537182', 'afya centre -wakiarie', 'ngara', '2500ksh', '742537182', '1.7km', 'willy masinde', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'mtindo   wear', '710130388', 'caxton  -kenyatta avenue', 'gogo mall', '3000ksh', '710130388', '1.2km', 'johnson wawire', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'mtindo   wear', '710130388', 'gogo mall', 'chania  genesis', '1500ksh', '710130388', '800m', 'johnson wawire', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'mtindo   wear', '710130388', 'gogo mall', 'pramukh', '1500ksh', '710130388', '550m', 'johnson wawire', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'mtindo   wear', '710130388', 'gogo mall', 'westlands', '1500ksh', '710130388', '5.9km', 'johnson wawire', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'belizi fashions', '704112224', 'star court   - syaokimau', 'imenti house', '3500ksh', '704112224', '18.1km', 'jesse victor', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'classic   cosmetics  - moyale mall', '700797110', 'classic   cosmetics  - moyale mall', 'buscar  - charles rubia rd', '15000ksh', '700797110', '4.6km', 'daniel nyakundi', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'adult room  -star mall  shop   a21', '106205106', 'adult room  -starmall  -a21', 'kasarani carwash', '2000ksh', '106205106', '12.1km', 'willy masinde', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'avana soles  -karakor  market', '702840229', 'avana soles - -karakor market', 'boma inn swtch   tv', '1500ksh', '702840229', '8.4km', 'shadarack  atito', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'troys closset  -hakati  business centre', '704476804', 'hakati business   centre', 'neptune residency', '1500ksh', '704476804', '8.0km', 'cyrus ambani', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'troys closset  -hakati  business centre', '704476804', 'hakati business   centre', 'al-mukaram   estate', '2000ksh', '704476804', '7.1km', 'cyrus ambani', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'sunrays   cosmetics  -flora house', '704476804', 'sunrays   cosmetics   -flora house', 'space appartments', '2000ksh', '704476804', '5.6km', 'willy masinde', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'superfine  beddings - shop 42', '717679016', 'superfine beddings  - shop 42', 'kawangware', '3500ksh', '717679016', '10.9km', 'jesse victor', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'liz kwame', '725795537', 'accra towers', 'nextgen mall', '2300ksh', '725795537', '7.7km', 'shadrack atito', 'parcel', 'paid', ''],
    ['', 'kevo', 'completed', 'sunrays   cosmetics  -flora house', '704476804', 'sunrays   cosmetics   -flora house', 'kileleshwa   wind court', '1500ksh', '704476804', '6.4km', 'willis  masinde', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'fadhili  -', '741862407', 'dynamic mall', 'lavender heights', '2500ksh', '741862407', '12.6km', 'jesse victor', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'siens  palza', '700039972', 'sienz plaza', 'githurai 45', '1500ksh', '700039972', '16.1km', 'shadrack   atito', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'adult   room-starmall   shop a21', '106205106', 'adult room  -starmall  -a21', 'buruburu  bamboo court  84b', '2000ksh', '106205106', '17.4km', 'cyrus ambani', 'parcel', 'paid', ''],
    ['', 'ricarda', 'completed', 'classic   cosmetics  - moyale mall', '700797110', 'classic   cosmetics  - moyale mall', 'great rift  - shuttle', '3000ksh', '700797110', '4.8km', 'daniel nyakundi', 'parcel', 'paid', ''],
]

success, failed = 0, 0
for row in rows:
    client_id = get_client_id(row[3])
    rider_id = get_rider_id(row[10])
    if not client_id or not rider_id:
        print(f"SKIP - no match: client='{row[3]}' rider='{row[10]}'")
        failed += 1
        continue

    price = calc_price(row[9])
    est_value = parse_value(row[7])
    pickup = row[5].strip().replace("'", "''")
    dropoff = row[6].strip().replace("'", "''")
    phone = str(row[4]).strip()
    desc = f"{pickup} to {dropoff}"

    psql(f"""
        INSERT INTO orders_order (
            title, description, pickup_address, delivery_address,
            contact_number, scheduled_date, price, status,
            created_at, updated_at, completed_at,
            client_id, handler_id, order_type_id,
            distance, price_finalized, estimated_value
        ) VALUES (
            'Pickup & Delivery Order',
            '{desc}',
            '{pickup}',
            '{dropoff}',
            '{phone}',
            '{scheduled_date}',
            {price},
            'completed',
            '{now}', '{now}', '{now}',
            {client_id}, {rider_id}, 2,
            {float(row[9].lower().replace('km','').replace('m','').strip()) if 'km' in row[9].lower() else float(row[9].lower().replace('m','').strip())/1000 if 'm' in row[9].lower() else 0},
            true, {est_value}
        ) RETURNING id;
    """)
    success += 1

print(f"\nDone: {success} inserted, {failed} skipped.")
