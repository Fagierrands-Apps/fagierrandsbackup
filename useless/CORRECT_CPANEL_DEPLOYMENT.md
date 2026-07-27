# 📦 CORRECT cPanel Deployment Instructions

## ✅ Package Ready
File: `fagierrandsbackup-cpanel-deploy-correct.zip` (385 KB - MUCH SMALLER!)

**Location:** `/home/jarvis/Documents/GitHub/fagierrandsbackup/fagierrandsbackup-cpanel-deploy-correct.zip`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 DEPLOYMENT STEPS

### Step 1: Backup Current System
1. In cPanel File Manager, navigate to: `errandserver.fagitone.com/fagierrandsbackup/`
2. Right-click → Compress → Create backup
3. Download backup locally

### Step 2: Delete Old Files (Keep venv!)
In `errandserver.fagitone.com/fagierrandsbackup/`:
1. Select ALL files/folders EXCEPT:
   - `venv/` (keep this!)
   - `logs/` (keep this!)
   - `tmp/` (keep this!)
2. Delete selected items

### Step 3: Upload New Package
1. Stay in `errandserver.fagitone.com/fagierrandsbackup/`
2. Upload `fagierrandsbackup-cpanel-deploy-correct.zip`
3. Extract it HERE (in the fagierrandsbackup folder)
4. Files will be extracted directly into fagierrandsbackup folder

### Step 4: Setup via cPanel Console
```bash
# Navigate to directory
cd errandserver.fagitone.com/fagierrandsbackup

# Activate existing venv (or create new one if deleted)
. venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install/update dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart application
touch tmp/restart.txt

# Check status
tail -50 stderr.log
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📂 Directory Structure

**Before extraction:**
```
errandserver.fagitone.com/
└── fagierrandsbackup/
    ├── venv/                              # KEEP THIS
    ├── logs/                              # KEEP THIS
    ├── tmp/                               # KEEP THIS
    ├── (old files to delete)
    └── fagierrandsbackup-cpanel-deploy-correct.zip  # UPLOAD HERE
```

**After extraction:**
```
errandserver.fagitone.com/
└── fagierrandsbackup/
    ├── venv/                              # Kept from before
    ├── logs/                              # Kept from before
    ├── tmp/                               # Kept from before
    ├── accounts/                          # Extracted
    ├── orders/                            # Extracted
    ├── fagierrandsbackup/                 # Extracted (Django settings)
    ├── manage.py                          # Extracted
    ├── passenger_wsgi.py                  # Extracted
    ├── requirements.txt                   # Extracted
    └── ... (all other files)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚠️ CRITICAL NOTES

### Keep These Folders:
- `venv/` - Your Python virtual environment
- `logs/` - Historical logs
- `tmp/` - Passenger temp files

### Extract Location:
Extract the zip INSIDE `errandserver.fagitone.com/fagierrandsbackup/`
NOT in `errandserver.fagitone.com/`

### After Extraction:
The files should be directly in the fagierrandsbackup folder, like:
- `errandserver.fagitone.com/fagierrandsbackup/manage.py` ✅
- NOT `errandserver.fagitone.com/fagierrandsbackup/fagierrandsbackup/manage.py` ❌

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ READY TO DEPLOY

The correct zip file is ready at:
`/home/jarvis/Documents/GitHub/fagierrandsbackup/fagierrandsbackup-cpanel-deploy-correct.zip`

Transfer this file to your local machine and upload to cPanel! 🚀
