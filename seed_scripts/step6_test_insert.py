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

def calc_price(km):
    if km <= 7.5:
        return 200
    return round(200 + (km - 7.5) * 23)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
scheduled_date = "2026-07-01"
distance = 8.5
price = calc_price(distance)

psql(f"""
    INSERT INTO orders_order (
        title, description, pickup_address, delivery_address,
        contact_number, scheduled_date, price, status,
        created_at, updated_at, completed_at,
        client_id, handler_id, order_type_id,
        distance, price_finalized, estimated_value
    ) VALUES (
        'Pickup & Delivery Order',
        'sunrays cosmetics -flora house to industrial area - gilgil rd',
        'sunrays cosmetics -flora house',
        'industrial area - gilgil rd',
        '704476804',
        '{scheduled_date}',
        {price},
        'completed',
        '{now}', '{now}', '{now}',
        372, 477, 2,
        {distance}, true, 2500
    ) RETURNING id, title, status, client_id, handler_id;
""")
