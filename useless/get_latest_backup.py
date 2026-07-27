import json

with open('/tmp/storage_list.json') as f:
    data = json.load(f)

files = data if isinstance(data, list) else []
if not files:
    raise Exception('No backup files found in db-backups bucket')

print(files[0]['name'])
