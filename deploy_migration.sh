#!/bin/bash

# Domain Migration Deployment Script
# This script helps deploy the domain changes

echo "============================================"
echo "Domain Migration Deployment"
echo "Old: https://errandserver.fagitone.com/"
echo "New: https://fagierrandsbackup.fagierrands.com/"
echo "============================================"
echo ""

# Check if we're in the right directory
if [ ! -f "fagierrandsbackup/fagierrandsbackup/settings.py" ]; then
    echo "Error: Must run from project root directory"
    exit 1
fi

echo "Step 1: Checking for old domain references..."
OLD_REFS=$(grep -r "errandserver.fagitone.com" . --exclude-dir=.git --exclude-dir=__pycache__ --exclude="*.pyc" --exclude="DOMAIN_MIGRATION_SUMMARY.md" --exclude="deploy_migration.sh" 2>/dev/null | grep -v ".backup" | wc -l)

if [ "$OLD_REFS" -gt 0 ]; then
    echo "Warning: Found $OLD_REFS references to old domain (excluding backups and docs)"
    grep -r "errandserver.fagitone.com" . --exclude-dir=.git --exclude-dir=__pycache__ --exclude="*.pyc" --exclude="DOMAIN_MIGRATION_SUMMARY.md" --exclude="deploy_migration.sh" 2>/dev/null | grep -v ".backup"
    echo ""
else
    echo "✓ No old domain references found in code"
fi

echo ""
echo "Step 2: Verifying new domain in settings..."
NEW_REFS=$(grep "fagierrandsbackup.fagierrands.com" fagierrandsbackup/fagierrandsbackup/settings.py | wc -l)
echo "✓ Found $NEW_REFS references to new domain in settings.py"

echo ""
echo "Step 3: Git status check..."
git status --short

echo ""
echo "============================================"
echo "Manual Steps Required:"
echo "============================================"
echo ""
echo "1. Update cPanel Environment Variables:"
echo "   - BASE_URL=https://fagierrandsbackup.fagierrands.com"
echo ""
echo "2. Update NCBA Callback URL in their dashboard:"
echo "   - https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/callback/"
echo ""
echo "3. Verify DNS and SSL certificate for new domain"
echo ""
echo "4. Git operations:"
echo "   git add ."
echo "   git commit -m 'Update server domain to fagierrandsbackup.fagierrands.com'"
echo "   git push origin main"
echo ""
echo "5. Restart application:"
echo "   touch tmp/restart.txt"
echo ""
echo "See DOMAIN_MIGRATION_SUMMARY.md for complete details"
echo "============================================"
