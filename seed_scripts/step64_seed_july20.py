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
        s = str(km_str).lower().strip()
        if 'km' in s: km = float(s.replace('km','').strip())
        elif 'm' in s: km = float(s.replace('m','').strip()) / 1000
        else: km = float(s)
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_km(s):
    try:
        s = str(s).lower().strip()
        if 'km' in s: return float(s.replace('km','').strip())
        if 'm' in s: return round(float(s.replace('m','').strip()) / 1000, 3)
        return float(s)
    except:
        return 0

clients = {
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'adult': 586,
    'belizi': 423, 'mtindo': 609, 'queens': 595, 'wakiarie': 551,
    'avana': 521, 'superfine': 518, 'jazi': 583, 'jazy': 583,
    'gloria': 489, 'almond': 489, 'athiambo': 634, 'kiatu': 341,
    'micheal': 604, 'michael': 604, 'sekani': 385, 'health': 472,
    'chelsea': 452, 'alfa': 649, 'unique': 513, 'andrew': 607,
    'yvonne': 651, 'noreen': 656, 'norren': 656, 'nooreen': 656,
    'joy': 670, 'muna': 664, 'miyanne': 683, 'rebune': 678,
    'halima': 692, 'rand landings': 693, 'lucy': 694,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310,
    'tony': 661, 'kelvin': 667, 'nyakundi': 310,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-20"

# (client, phone, pickup, dropoff, dist, rider)
rows = [
    ('halima dera',                 '795118132',    'fagi shop -cianda mall',                   'kileleshwa',                                                       '7.2km',  'tony sangura'),
    ('Rebune international',        '711670387',    'Shiriz electronic',                         'Rebune international',                                             '4.3km',  'shadrack atito'),
    ('Rebune international',        '711670387',    'Rebune international',                      'westlands',                                                        '7.5km',  'shadrack atito'),
    ('Rebune international',        '711670387',    'Rebune international',                      'luthuli jumia',                                                    '4.9km',  'shadrack atito'),
    ('Rebune international',        '711670387',    'eastliegh',                                 'Rebune international',                                             '6.1km',  'shadrack atito'),
    ('Adult Room Star Mall',        '106205106',    'starmall a21',                              'palm suites - kinoo',                                              '16.4km', 'willy masinde'),
    ('Sekani flowers',              '118260620',    'Northside apartments',                      'Kasarani Mwki road. Sunton Mafuta stage 8th street plot no 12',    '13.7km', 'cyrus ambani'),
    ('sunrays flora house',         '700797110',    'sunrays flora house',                       'Adorn Homes Apartment / Nyeri Road Kileleshwa',                    '7.2km',  'daniel nyakundi'),
    ('sunrays flora house',         '700797110',    'sunrays flora house',                       'TRV center, 3rd Parklands Avenue',                                 '5.0km',  'johnson wawire'),
    ('Noreen',                      '721999686',    'IPS building 7th Floor, office number 11.', 'Social hall f93 eastleigh',                                        '5.4km',  'willy masinde'),
    ('noreen',                      '721999686',    'social hall f93 eastleigh',                 'IPS building 7th Floor, office number 11.',                        '5.4km',  'willy masinde'),
    ('lucy collection',             '',             'cianda mall-fagi shop',                     'eastleigh juja b',                                                 '4.0km',  'shadrack atito'),
    ('Miyanne Gifts',               '721429708',    'City market',                               'RossCliff Apartments Kamiti Road',                                 '13.9km', 'tony sangura'),
    ('athiambos thrifts',           '',             'cianda mall -fagi shop',                    'The westery, Mpesi lane, off muthithi road, Westlands, 8th floor', '4.0km',  'daniel nyakundi'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    'starmall',                                                         '700m',   'johnson wawire'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    'mithoo business center',                                           '1.0km',  'johnson wawire'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    'supermetro parcel',                                                '600m',   'johnson wawire'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    '2nk shutlle gaborone rd (nakuru & nyanyuki parcels)',               '900m',   'johnson wawire'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    'pick up mtaani',                                                   '550m',   'johnson wawire'),
    ('mtindo wear',                 '726620888',    'cianda mall -fagi shop',                    'diani springs apartment',                                          '7.5km',  'johnson wawire'),
    ('health classic',              '722995300',    'nextgenmall',                               'Mugoya phase 2',                                                   '2.4km',  'tony sangura'),
]

success, skipped = 0, 0
for client, phone, pickup, dropoff, dist, rider in rows:
    client_id = get_id(client, clients)
    rider_id = get_id(rider, riders)
    if not client_id or not rider_id:
        print(f"SKIP: client='{client}'({client_id}) rider='{rider}'({rider_id})")
        skipped += 1
        continue
    price = calc_price(dist)
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
            {km}, true, 0
        ) RETURNING id, client_id, assistant_id, price;
    """)
    success += 1

print(f"\nDone: {success} inserted, {skipped} skipped for {scheduled_date}")
