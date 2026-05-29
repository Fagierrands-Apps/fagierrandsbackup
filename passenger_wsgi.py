import os
import sys

# Fix OpenBLAS thread limit to prevent resource exhaustion
os.environ['OPENBLAS_NUM_THREADS'] = '4'

# Point to the fagierrandsbackup folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fagierrandsbackup'))

from fagierrandsbackup.wsgi import application
