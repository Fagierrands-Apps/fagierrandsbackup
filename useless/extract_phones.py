import os
import psycopg

conn = psycopg.connect(
    dbname=os.environ.get("PG_DB_NAME"),
    user=os.environ.get("PG_USER"),
    password=os.environ.get("PG_PASSWORD"),
    host=os.environ.get("PG_HOST"),
    port=os.environ.get("PG_PORT", "5432"),
)

cur = conn.cursor()
cur.execute("SELECT phone_number FROM accounts_user WHERE phone_number IS NOT NULL AND phone_number != '';")

for row in cur.fetchall():
    print(row[0])

cur.close()
conn.close()
