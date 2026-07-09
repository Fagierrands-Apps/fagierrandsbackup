#!/bin/bash
# db_backup.sh - Daily Postgres dump → Supabase Storage + email report

# Load credentials
ENV_FILE="$(dirname "$0")/backup.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: backup.env not found at $ENV_FILE"
    exit 1
fi
source "$ENV_FILE"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y%m%d_%H%M%S')
DUMP_FILE="/tmp/fagierrands_backup_$DATE.sql.gz"
LOG=""
STATUS="SUCCESS"
START_TIME=$(date +%s)
ERRORS=""

log() {
    LOG="$LOG\n$1"
    echo "$1"
}

# Step 1: Dump and compress source DB
log "[$TIMESTAMP] Starting pg_dump from $SOURCE_DB_HOST/$SOURCE_DB_NAME..."
export PGPASSWORD="$SOURCE_DB_PASSWORD"
pg_dump \
    -h "$SOURCE_DB_HOST" \
    -p "$SOURCE_DB_PORT" \
    -U "$SOURCE_DB_USER" \
    -d "$SOURCE_DB_NAME" \
    -F p | gzip > "$DUMP_FILE" 2>&1

if [ $? -ne 0 ] || [ ! -s "$DUMP_FILE" ]; then
    STATUS="FAILED"
    ERRORS="pg_dump failed - could not dump source database"
    log "ERROR: $ERRORS"
else
    DUMP_SIZE=$(du -sh "$DUMP_FILE" | cut -f1)
    log "pg_dump: SUCCESS (compressed size: $DUMP_SIZE)"
fi

# Step 2: Upload to Supabase Storage via HTTPS
if [ "$STATUS" = "SUCCESS" ]; then
    log "Uploading to Supabase Storage..."
    FILENAME="fagierrands_backup_$DATE.sql.gz"

    HTTP_STATUS=$(curl -s -o /tmp/upload_response.txt -w "%{http_code}" \
        -X POST \
        "${SUPABASE_PROJECT_URL}/storage/v1/object/db-backups/${FILENAME}" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
        -H "Content-Type: application/octet-stream" \
        --data-binary @"$DUMP_FILE")

    UPLOAD_RESPONSE=$(cat /tmp/upload_response.txt)

    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "201" ]; then
        log "Supabase Storage upload: SUCCESS (HTTP $HTTP_STATUS)"
        log "File: $FILENAME"
    else
        STATUS="FAILED"
        ERRORS="Upload to Supabase Storage failed (HTTP $HTTP_STATUS): $UPLOAD_RESPONSE"
        log "ERROR: $ERRORS"
    fi
fi

# Step 3: Collect DB stats
DB_SIZE=$(psql \
    -h "$SOURCE_DB_HOST" -p "$SOURCE_DB_PORT" \
    -U "$SOURCE_DB_USER" -d "$SOURCE_DB_NAME" \
    -t -c "SELECT pg_size_pretty(pg_database_size('$SOURCE_DB_NAME'));" 2>/dev/null | xargs)

TABLE_COUNT=$(psql \
    -h "$SOURCE_DB_HOST" -p "$SOURCE_DB_PORT" \
    -U "$SOURCE_DB_USER" -d "$SOURCE_DB_NAME" \
    -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | xargs)

log "DB size: ${DB_SIZE:-N/A} | Tables: ${TABLE_COUNT:-N/A}"

# Step 4: Delete old backups (keep last 7)
log "Cleaning up old backups (keeping last 7)..."
OLD_FILES=$(curl -s \
    "${SUPABASE_PROJECT_URL}/storage/v1/object/list/db-backups" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"limit": 100, "sortBy": {"column": "created_at", "order": "asc"}}' \
    | python3 -c "
import sys, json
files = json.load(sys.stdin)
if isinstance(files, list) and len(files) > 7:
    for f in files[:-7]:
        print(f['name'])
" 2>/dev/null)

for OLD_FILE in $OLD_FILES; do
    curl -s -X DELETE \
        "${SUPABASE_PROJECT_URL}/storage/v1/object/db-backups/$OLD_FILE" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" > /dev/null
    log "Deleted old backup: $OLD_FILE"
done

# Step 5: Cleanup temp file
rm -f "$DUMP_FILE" /tmp/upload_response.txt

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Step 6: Send email via Python SMTP
python3 - <<EOF
import smtplib
from email.mime.text import MIMEText

body = """
================================================
 FAGISERVER DATABASE BACKUP REPORT
================================================
STATUS   : $STATUS
Timestamp: $TIMESTAMP
Duration : ${DURATION}s
DB Name  : $SOURCE_DB_NAME
DB Size  : ${DB_SIZE:-N/A}
Tables   : ${TABLE_COUNT:-N/A}
Dump Size: ${DUMP_SIZE:-N/A}
Storage  : Supabase / db-backups bucket

--- LOG ---
$(echo -e "$LOG")

--- ERRORS ---
${ERRORS:-None}

================================================
Restore command (if needed):
  gunzip backup.sql.gz
  psql -U your_user -d your_db -f backup.sql
================================================
"""

msg = MIMEText(body)
msg['Subject'] = '[DB Backup] Daily Report - $TIMESTAMP - $STATUS'
msg['From'] = '$GMAIL_USER'
msg['To'] = '$NOTIFY_EMAIL'

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('$GMAIL_USER', '$GMAIL_APP_PASSWORD')
    smtp.send_message(msg)

print("Email sent successfully")
EOF

echo "Backup complete. Status: $STATUS"
