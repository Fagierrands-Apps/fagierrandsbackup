#!/bin/bash

echo "=== Safe Backend Cleanup - Wave 2 ==="
echo "Only removing test/debug files and documentation"
echo ""

# Count files before
BEFORE=$(find . -type f | wc -l)

# Remove test files
echo "Removing test files..."
find . -type f \( -name "test_*.py" -o -name "debug_*.py" -o -name "*_test.py" \) ! -path "*/venv/*" -delete

# Remove documentation in reports folder
echo "Removing reports folder..."
rm -rf reports/

# Remove test directories
echo "Removing tests folder..."
rm -rf tests/

# Remove accounts/tests folder
echo "Removing accounts/tests..."
rm -rf accounts/tests/

# Remove JSON test files (keep fixtures)
echo "Removing Postman collections..."
rm -f *.postman_collection.json
rm -f Simple_KSh5_Payment_Test.json
rm -f Postman_Environment.json
rm -f vercel*.json
rm -rf jsons/

# Remove SQL setup files
echo "Removing SQL files..."
rm -f *.sql

# Remove CSV/Excel seed files
echo "Removing data files..."
rm -f *.csv *.xlsx
rm -rf exports/

# Remove archive folder
echo "Removing archive..."
rm -rf archive/

# Remove temporary files
echo "Removing temp files..."
rm -f xxx.txt
rm -f deployment_test*.txt

# Remove Python cache
echo "Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Count files after
AFTER=$(find . -type f | wc -l)
REMOVED=$((BEFORE - AFTER))

echo ""
echo "=== Cleanup Complete ==="
echo "Files before: $BEFORE"
echo "Files after: $AFTER"
echo "Files removed: $REMOVED"
