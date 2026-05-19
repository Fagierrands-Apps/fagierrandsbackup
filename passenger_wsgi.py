import os
import sys

# Point to the fagierrandsbackup folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fagierrandsbackup'))

from fagierrandsbackup.wsgi import application
