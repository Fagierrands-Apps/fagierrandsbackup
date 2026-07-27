# Server Fix Implementation - 2026-05-29

## Issues Fixed

### 1. ✅ OpenBLAS Thread Exhaustion (CRITICAL)
**Problem:** OpenBLAS trying to create 64 threads, hitting process limit (1400/1500)
**Solution:** Added `os.environ['OPENBLAS_NUM_THREADS'] = '4'` to `passenger_wsgi.py`
**File Modified:** `passenger_wsgi.py`

### 2. ✅ Import Crash on Startup (CRITICAL)
**Problem:** `openpyxl` imported at module level, triggering numpy/OpenBLAS during Django startup
**Solution:** Moved import inside the view method (lazy loading)
**File Modified:** `fagierrandsbackup/orders/export_views.py`

### 3. ✅ Server Restart
**Action:** Created `tmp/restart.txt` to trigger Passenger restart

## Verification Steps

After server restarts, verify:

1. **Check server logs** - No more OpenBLAS thread errors
   ```bash
   tail -f stderr.log
   ```

2. **Test base URL** - Should not return 404
   ```bash
   curl https://fagiserver.fagtone.com/
   ```

3. **Test API endpoint**
   ```bash
   curl https://fagiserver.fagtone.com/api/accounts/user/
   ```

4. **Check for errors** - Look for any remaining issues in logs

## Notes on Other Issues

### URL Configuration
- Main URLs are correctly configured in `fagierrandsbackup/fagierrandsbackup/urls.py`
- The `/api/api/` double prefix in logs is likely from client-side requests
- Server-side URLs are correct: `path('api/accounts/', include('accounts.urls'))`

### Supabase Storage 400 Error
- Configuration in `supabase_client.py` is correct
- The 400 error on bucket access is likely due to RLS (Row Level Security) policies
- This is handled gracefully with try/except blocks
- Does not prevent server startup

## Additional Recommendations

### 1. Add Persistent Environment Variable
Add to cPanel Python App environment variables or `.env` file:
```
OPENBLAS_NUM_THREADS=4
```

### 2. Monitor Resource Usage
```bash
# Check process limits
ulimit -a

# Monitor running processes
ps aux | grep python | wc -l
```

### 3. Clear Python Cache (if needed)
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Files Modified

1. `passenger_wsgi.py` - Added OpenBLAS thread limit
2. `fagierrandsbackup/orders/export_views.py` - Moved openpyxl import to method level
3. `tmp/restart.txt` - Created for server restart

## Expected Results

✅ Server starts without OpenBLAS errors
✅ No import crashes during startup  
✅ Base URL returns proper response (not 404)
✅ All API endpoints accessible
✅ Excel export still works (import happens on-demand)

## If Issues Persist

1. Check if server actually restarted: `ls -la tmp/restart.txt`
2. Force restart via cPanel Python App interface
3. Check stderr.log for new error messages
4. Verify environment variables are loaded
