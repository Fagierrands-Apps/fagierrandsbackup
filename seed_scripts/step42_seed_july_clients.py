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

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S+03")

new_clients = [
    ("chelsea",         "Chelsea",          "",             "chelsea@fagierrands.com",          "714142519"),
    ("nooreen",         "Noreen",           "",             "nooreen@fagierrands.com",           "721999686"),
    ("yvonnejitihada",  "Yvonne",           "Jitihada",     "yvonnejitihada@fagierrands.com",    "727111000"),
    ("yellowpages",     "Yellow",           "Pages",        "yellowpages@fagierrands.com",       "706829859"),
    ("alfafashions",    "Alfa",             "Fashions",     "alfafashions@fagierrands.com",      "796736969"),
    ("kwabrown",        "Kwa",              "Brown",        "kwabrown@fagierrands.com",          "706226766"),
    ("nkirobi",         "Nkirobi",          "",             "nkirobi@fagierrands.com",           "720348793"),
    ("reestyle",        "Ree",              "Style",        "reestyle@fagierrands.com",          "799564394"),
    ("alinaridge",      "Alina",            "Ridge",        "alinaridge@fagierrands.com",        "791246003"),
    ("climeshdesigns",  "Climesh",          "Designs",      "climeshdesigns@fagierrands.com",    "700039972"),
    ("munaflowers",     "Muna",             "Flowers",      "munaflowers@fagierrands.com",       "724906221"),
    ("nolanskids",      "Nolans",           "Kids",         "nolanskids@fagierrands.com",        "717544455"),
    ("linayarn",        "Lina",             "Yarn",         "linayarn@fagierrands.com",          "713542093"),
    ("nancylisters",    "Nancy",            "Listers",      "nancylisters@fagierrands.com",      "721429708"),
    ("kwamwalimu",      "Kwa",              "Mwalimu",      "kwamwalimu@fagierrands.com",        "757609903"),
    ("villablooms",     "Villa",            "Blooms",       "villablooms@fagierrands.com",       "116682365"),
    ("homeoftrainer",   "Home",             "Of Trainer",   "homeoftrainer@fagierrands.com",     "254240068370"),
    ("baddiesempire",   "Baddies",          "Empire",       "baddiesempire@fagierrands.com",     "759535915"),
    ("rebune",          "Rebune",           "International","rebune@fagierrands.com",            "711670387"),
    ("tangecollection", "Tange",            "Collection",   "tangecollection@fagierrands.com",   "714348056"),
    ("kimathihouse",    "Kimathi",          "House",        "kimathihouse@fagierrands.com",      "798286199"),
    ("nashique",        "Nashique",         "",             "nashique@fagierrands.com",          "798086199"),
    ("miyannegifts",    "Miyanne",          "Gifts",        "miyannegifts@fagierrands.com",      "729228868"),
    ("fashionfix",      "Fashion",          "Fix",          "fashionfix@fagierrands.com",        "769777641"),
    ("trainersbysway",  "Trainers",         "By Sway",      "trainersbysway@fagierrands.com",    "1140068370"),
    ("vallaries",       "Vallaries",        "Collection",   "vallaries@fagierrands.com",         "708203462"),
    ("halimafashions",  "Halima",           "Fashions",     "halimafashions@fagierrands.com",    "795118132"),
    ("niapetals",       "Nia",              "Petals",       "niapetals@fagierrands.com",         "713777513"),
    ("oderovictor",     "Odero",            "Victor",       "oderovictor@fagierrands.com",       "712445305"),
    ("willyriverside",  "Willy",            "Riverside",    "willyriverside@fagierrands.com",    "708632359"),
    ("mercyscott",      "Mercy",            "Scott",        "mercyscott@fagierrands.com",        "721736140"),
    ("joybusiness",     "Joy",              "Business",     "joybusiness@fagierrands.com",       "718840856"),
    ("queensrng",       "Queens",           "Rng",          "queensrng@fagierrands.com",         "710617679"),
    ("tonysangura",     "Tony",             "Sangura",      "tonysangura@fagierrands.com",       ""),
    ("kelvindungu",     "Kelvin",           "Ndungu",       "kelvindungu@fagierrands.com",       ""),
]

for username, first, last, email, phone in new_clients:
    print(f">>> Seeding {username}...")
    psql(f"""
        INSERT INTO accounts_user
            (password, last_login, is_superuser, username, first_name, last_name,
             email, is_staff, is_active, date_joined, user_type, phone_number,
             is_verified, email_verified, created_at, updated_at, is_online)
        VALUES ('!disabled', NULL, false, '{username}', '{first}', '{last}',
             '{email}', false, true, '{now}', 'client', '{phone}',
             true, true, '{now}', '{now}', false)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username;
    """)
    psql(f"INSERT INTO accounts_profile (bio, address, user_id, wallet_balance, wallet_points) SELECT '', '', id, 0, 0 FROM accounts_user WHERE username='{username}';")

# Print all IDs
usernames = [u[0] for u in new_clients]
ulist = "','".join(usernames)
print("\n>>> Final IDs:")
psql(f"SELECT id, username FROM accounts_user WHERE username IN ('{ulist}') ORDER BY id;")
