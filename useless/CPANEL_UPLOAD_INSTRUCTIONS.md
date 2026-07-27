# 📦 cPanel Upload Deployment Instructions

## Method: ZIP Upload (No SSH Access)

Since SSH is not available, we'll use cPanel File Manager upload method.

## 🎯 PREPARATION STEPS

### 1. Create Deployment Package
The system will be zipped excluding unnecessary files:
- Exclude: venv/, __pycache__/, *.pyc, .git/, node_modules/
- Include: All source code, requirements.txt, passenger_wsgi.py

### 2. Upload to cPanel
1. Login to cPanel
2. Open File Manager
3. Navigate to the directory where you want to deploy
4. Upload the zip file
5. Extract the zip file
6. The extracted folder will be named: `fagierrandsbackup`

### 3. Post-Upload Setup (via cPanel Terminal/Console)
```bash
cd fagierrandsbackup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## ⚠️ IMPORTANT FILES TO CHECK

After extraction, verify these files exist:
- passenger_wsgi.py (in root of fagierrandsbackup)
- fagierrandsbackup/manage.py
- requirements.txt
- .env (you'll need to create this manually or set via cPanel)

## 📋 NEXT STEPS

Please share:
1. Current cPanel directory structure
2. Where should fagierrandsbackup folder be placed?
3. Any specific cPanel Python app configuration needed

This will help me prepare the perfect deployment package.
