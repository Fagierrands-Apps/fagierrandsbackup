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
        if not s or s in ('okm','0km',''): return 200
        if 'km' in s: km = float(s.replace('km','').strip())
        elif 'm' in s: km = float(s.replace('m','').strip()) / 1000
        else: km = float(s)
        return 200 if km <= 7.5 else round(200 + (km - 7.5) * 23)
    except:
        return 200

def parse_value(v):
    try:
        return float(''.join(c for c in str(v) if c.isdigit() or c == '.'))
    except:
        return 0

def parse_km(s):
    try:
        s = str(s).lower().strip()
        if not s or s in ('okm','0km',''): return 0
        if 'km' in s: return float(s.replace('km','').strip())
        if 'm' in s: return round(float(s.replace('m','').strip()) / 1000, 3)
        return float(s)
    except:
        return 0

# ── UPDATE THESE after running step42 ──────────────────────────────────────
TONY_ID    = 0   # replace with tony sangura's rider ID
KELVIN_ID  = 0   # replace with kelvin ndungu's rider ID
# ───────────────────────────────────────────────────────────────────────────

clients = {
    'sunrays': 372, 'classic': 332, 'fitbox': 338, 'adult': 586,
    'belizi': 423, 'mtindo': 609, 'queens choice': 595, 'queens': 595,
    'platinum': 629, 'nairobi flower': 608, 'nia petals': 628,
    'wakiarie': 551, 'avana': 521, 'superfine': 518, 'supefine': 518,
    'jazi': 583, 'jazzy': 583, 'jazy': 583, 'jazy': 583,
    'purple': 408, 'yyvonne': 631, 'yvvonne': 631, 'yvvone': 631,
    'unique': 513, 'micheal': 604, 'michael': 604,
    'health': 472, 'gloria': 489, 'almond': 489,
    'athiambo': 634, 'andrew': 607, 'troys': 462,
    # new july clients (IDs assigned after step42 runs)
    'chelsea': 0,       'nooreen': 0,   'noreen': 0,    'noreens': 0,
    'yvonne jitihada': 0, 'yvonne': 0,
    'yellow pages': 0,  'alfa': 0,      'rng': 0,
    'kwa brown': 0,     'nkirobi': 0,   'ree style': 0,
    'alina': 0,         'climesh': 0,   'muna': 0,
    'nolans': 0,        'lina yarn': 0, 'nancy': 0,
    'kwa mwalimu': 0,   'villa blooms': 0, 'home of trainer': 0,
    'baddies empire': 0,'baddies': 0,   'rebune': 0,
    'tange': 0,         'kimathi': 0,   'nashique': 0,
    'miyanne': 0,       'fashion fix': 0, 'trainers': 0,
    'vallaries': 0,     'halima': 0,    'niapetals': 0,
    'odero': 0,         'willy-riverside': 0, 'mercy': 0,
    'joy': 0,           'queens rng': 0, 'queensrng': 0,
}

riders = {
    'shadrack': 477, 'cyrus': 375, 'johnson': 374, 'johnsons': 374,
    'willy': 403, 'jesse': 109, 'daniel': 310, 'nyakundi': 310,
    'tony': TONY_ID, 'kelvin': KELVIN_ID,
}

def get_id(name, mapping):
    name = str(name).lower().strip()
    for key, uid in mapping.items():
        if key in name:
            return uid
    return None

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")
print("NOTE: Run step42 first and update TONY_ID and KELVIN_ID at the top of this file, then re-run.")
print("Rows with ID=0 will be skipped.\n")
