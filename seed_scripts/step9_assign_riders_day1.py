import subprocess

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    print(r.stdout)
    if r.stderr: print("ERR:", r.stderr)

# Day 1 orders: (pickup_address, dropoff, client_id, assistant_id)
assignments = [
    ('sunrays   cosmetics   -flora house', 'industrial area  - gilgil rd', 372, 477),   # shadrack
    ('sunrays   cosmetics   -flora house', 'stima plaza -ngara', 372, 375),              # cyrus
    ('firbox   - kamukunji   police station', 'the hub -karen', 338, 374),               # johnson
    ('sekani  flowers   - northside  appartments', 'langata', 385, 477),                 # shadrack
    ('sunrays   cosmetics   -flora house', 'royal canaan nairobi hotel', 372, 375),      # cyrus
    ('dyc   beauty shop  - dubois', 'classic  cosmetics  - moyale mall', 332, 310),      # daniel
    ('afya centre -wakiarie', 'ngara', 551, 403),                                        # willy
    ('caxton  -kenyatta avenue', 'gogo mall', 609, 374),                                 # johnson
    ('gogo mall', 'chania  genesis', 609, 374),                                          # johnson
    ('gogo mall', 'pramukh', 609, 374),                                                  # johnson
    ('gogo mall', 'westlands', 609, 374),                                                # johnson
    ('star court   - syaokimau', 'imenti house', 423, 109),                              # jesse
    ('classic   cosmetics  - moyale mall', 'buscar  - charles rubia rd', 332, 310),      # daniel
    ('adult room  -starmall  -a21', 'kasarani carwash', 586, 403),                       # willy
    ('avana soles - -karakor market', 'boma inn swtch   tv', 521, 477),                  # shadrack
    ('hakati business   centre', 'neptune residency', 462, 375),                         # cyrus
    ('hakati business   centre', 'al-mukaram   estate', 462, 375),                       # cyrus
    ('sunrays   cosmetics   -flora house', 'space appartments', 372, 403),               # willy
    ('superfine beddings  - shop 42', 'kawangware', 518, 109),                           # jesse
    ('accra towers', 'nextgen mall', 156, 477),                                          # shadrack
    ('sunrays   cosmetics   -flora house', 'kileleshwa   wind court', 372, 403),         # willy
    ('dynamic mall', 'lavender heights', 623, 109),                                      # jesse
    ('sienz plaza', 'githurai 45', 624, 477),                                            # shadrack
    ('adult room  -starmall  -a21', 'buruburu  bamboo court  84b', 586, 375),            # cyrus
    ('classic   cosmetics  - moyale mall', 'great rift  - shuttle', 332, 310),           # daniel
]

for pickup, dropoff, client_id, assistant_id in assignments:
    pickup_esc = pickup.replace("'", "''")
    dropoff_esc = dropoff.replace("'", "''")
    psql(f"""
        UPDATE orders_order
        SET assistant_id = {assistant_id}
        WHERE client_id = {client_id}
          AND pickup_address ILIKE '%{pickup_esc}%'
          AND delivery_address ILIKE '%{dropoff_esc}%'
          AND scheduled_date = '2026-07-01'
        RETURNING id, assistant_id, pickup_address, delivery_address;
    """)
