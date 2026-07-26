import subprocess, json, os

CACHE_FILE = "user_cache.json"
cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {"clients": {}, "riders": {}}

def psql(query):
    r = subprocess.run(
        ["psql", "-U", "distinc3_distinc3", "-d", "distinc3_fagierrands", "-c", query],
        capture_output=True, text=True,
        env={"PGPASSWORD": "Pa7swrd1990@", "PATH": "/usr/bin:/bin"}
    )
    return r.stdout

def search_user(name):
    # Try exact then partial match on username, first_name, last_name
    words = [w for w in name.lower().replace('-', ' ').split() if len(w) > 3]
    conditions = " OR ".join([
        f"LOWER(username) LIKE '%%{w}%%' OR LOWER(first_name) LIKE '%%{w}%%' OR LOWER(last_name) LIKE '%%{w}%%'"
        for w in words
    ])
    query = f"SELECT id, username, first_name, last_name FROM accounts_user WHERE {conditions} ORDER BY username;"
    return psql(query)

clients = ['adult   room-starmall   shop a21', 'adult room  -star mall  shop   a21',
           'avana soles  -karakor  market', 'belizi fashions', 'classic   cosmetics  - moyale mall',
           'fadhili  -', 'fitbox - kamukunji  police station', 'liz kwame', 'mtindo   wear',
           'sekni  flowers - northside appartments', 'siens  palza', 'sunrays   cosmetics  -flora house',
           'superfine  beddings - shop 42', 'troys closset  -hakati  business centre', 'wakiarie-business']

riders = ['cyrus ambani', 'daniel nyakundi', 'jesse victor', 'johnson wawire',
          'shadrack atito', 'willy masinde', 'willis masinde']

print("=" * 60)
print("SEARCHING CLIENTS")
print("=" * 60)
for name in clients:
    if name in cache["clients"]:
        print(f"\n[CACHED] {name} => {cache['clients'][name]}")
        continue
    print(f"\n>> {name}")
    print(search_user(name))

print("=" * 60)
print("SEARCHING RIDERS")
print("=" * 60)
for name in riders:
    if name in cache["riders"]:
        print(f"\n[CACHED] {name} => {cache['riders'][name]}")
        continue
    print(f"\n>> {name}")
    print(search_user(name))

# Save cache
json.dump(cache, open(CACHE_FILE, "w"), indent=2)
print("\nCache saved to", CACHE_FILE)
