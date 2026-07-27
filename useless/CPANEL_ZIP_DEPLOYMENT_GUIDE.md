# 📦 cPanel Deployment Instructions (ZIP Upload Method)

## ✅ Package Ready
File: `fagierrandsbackup-cpanel-deploy.zip` (98 MB)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 DEPLOYMENT STEPS

### Step 1: Backup Current System (IMPORTANT!)
1. Go to cPanel File Manager
2. Right-click on current `fagierrandsbackup` folder
3. Select "Compress" → Create backup zip
4. Download the backup to your local machine

### Step 2: Remove Old Version
1. In cPanel File Manager
2. Delete or rename current `fagierrandsbackup` folder to `fagierrandsbackup-old`

### Step 3: Upload New Package
1. In cPanel File Manager, navigate to: `/home/username/` (root directory)
2. Click "Upload" button
3. Upload `fagierrandsbackup-cpanel-deploy.zip`
4. Wait for upload to complete (98 MB)

### Step 4: Extract Package
1. Right-click on `fagierrandsbackup-cpanel-deploy.zip`
2. Select "Extract"
3. Extract to current directory
4. You should now see a folder named `fagierrandsbackup`

### Step 5: Setup via cPanel Console (NOT Terminal)
Open cPanel Console and run these commands one by one:

```bash
# Navigate to directory
cd fagierrandsbackup

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (use this exact command for console)
. venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p tmp
mkdir -p static

# Set permissions
chmod 755 .
chmod 644 passenger_wsgi.py
chmod 755 tmp

# Collect static files
cd fagierrandsbackup
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Go back to root
cd ..

# Restart the application
touch tmp/restart.txt

# Check if it's running
tail -20 stderr.log
```

### Step 6: Verify Environment Variables
Check cPanel → Python App → Environment Variables:
- DEBUG=False
- SECRET_KEY=...
- PG_DB_NAME=...
- PG_USER=...
- PG_PASSWORD=...
- PG_HOST=localhost
- PG_PORT=5432
- SUPABASE_URL=...
- All other variables from your .env file

### Step 7: Verify Deployment
1. In cPanel Console, check `stderr.log` for errors:
```bash
cd fagierrandsbackup
tail -100 stderr.log
```

2. Check application logs:
```bash
tail -50 fagierrandsbackup/logs/app.log
```

3. Test the API using browser or Postman:
   - Visit: https://fagierrandsbackup.fagierrands.com/api/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📂 Expected Directory Structure After Extraction

```
/home/username/
├── fagierrandsbackup/              # Main folder
│   ├── fagierrandsbackup/          # Django project
│   │   ├── manage.py
│   │   ├── fagierrandsbackup/      # Settings
│   │   ├── accounts/
│   │   ├── orders/
│   │   ├── marketplace/
│   │   └── ...
│   ├── venv/                       # Virtual environment (create after upload)
│   ├── logs/                       # Log files (create after upload)
│   ├── tmp/                        # Passenger temp (create after upload)
│   ├── static/                     # Static files
│   ├── passenger_wsgi.py          # cPanel entry point
│   ├── requirements.txt
│   └── ...
├── public/
├── static/
└── ...
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚠️ IMPORTANT NOTES

### What's Included in ZIP:
✅ All source code
✅ passenger_wsgi.py (cPanel entry point)
✅ requirements.txt
✅ All migrations
✅ Static files source
✅ Configuration files

### What's NOT Included (Will be created on server):
❌ venv/ (create fresh on server)
❌ __pycache__/ (generated automatically)
❌ .env file (use cPanel environment variables)
❌ logs/ (create directory)
❌ Database (already exists on server)

### Database:
- Uses existing cPanel PostgreSQL database
- Connection via PG_* environment variables
- All migrations will be applied automatically

### Static Files:
- Will be collected to `staticfiles/` directory
- Served by cPanel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🆘 TROUBLESHOOTING

### If upload fails:
- File too large? Upload via FTP instead
- Or split into smaller zips

### If extraction fails:
- Check disk space: `df -h`
- Check permissions on parent directory

### If app doesn't start:
1. Check stderr.log for errors
2. Verify all environment variables are set
3. Ensure venv was created successfully
4. Check permissions on all directories

### If migrations fail:
- Database connection issue - check PG_* variables
- Run manually: `python manage.py migrate --traceback`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ SUCCESS INDICATORS

After deployment, you should see:
- No errors in stderr.log
- API responds at https://fagierrandsbackup.fagierrands.com/api/
- Logs show successful requests
- All 3 frontends can connect

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎉 DEPLOYMENT COMPLETE

Once deployed successfully:
1. Monitor logs for first 30 minutes
2. Test all critical endpoints
3. Verify frontend connectivity
4. Delete old backup if everything works

**Ready to upload! The fagierrandsbackup-cpanel-deploy.zip file is ready for deployment.** 🚀
