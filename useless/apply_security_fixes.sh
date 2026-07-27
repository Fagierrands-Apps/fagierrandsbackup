#!/bin/bash
# Quick Security Fixes Script

echo "=== APPLYING CRITICAL SECURITY FIXES ==="
echo ""

cd /home/jarvis/Documents/GitHub/fagierrandsbackup/fagierrandsbackup

# 1. Disable DEBUG mode
echo "1. Disabling DEBUG mode..."
sed -i 's/DEBUG=True/DEBUG=False/' .env
echo "✅ DEBUG mode disabled"

# 2. Add .env to .gitignore if not already there
echo ""
echo "2. Protecting .env file..."
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo ".env" >> .gitignore
    echo "✅ .env added to .gitignore"
else
    echo "✅ .env already in .gitignore"
fi

# 3. Generate new SECRET_KEY
echo ""
echo "3. Generating new SECRET_KEY..."
NEW_SECRET=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$NEW_SECRET/" .env
echo "✅ New SECRET_KEY generated"

# 4. Add NCBA webhook secret placeholder
echo ""
echo "4. Adding NCBA webhook secret..."
if ! grep -q "NCBA_WEBHOOK_SECRET" .env; then
    echo "" >> .env
    echo "# NCBA Webhook Security" >> .env
    echo "NCBA_WEBHOOK_SECRET=your_webhook_secret_here_get_from_ncba" >> .env
    echo "✅ NCBA_WEBHOOK_SECRET added to .env (UPDATE THIS VALUE!)"
else
    echo "✅ NCBA_WEBHOOK_SECRET already exists"
fi

echo ""
echo "=== SECURITY FIXES APPLIED ==="
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. Update NCBA_WEBHOOK_SECRET in .env with actual secret from NCBA"
echo "2. If .env was previously committed to Git, run:"
echo "   git rm --cached .env"
echo "   git commit -m 'Remove .env from repository'"
echo "3. Rotate database password in cPanel"
echo "4. Test the application thoroughly"
echo ""
echo "DEBUG mode is now: $(grep '^DEBUG=' .env)"
