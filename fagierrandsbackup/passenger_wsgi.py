import os
import sys

os.environ['OPENBLAS_NUM_THREADS'] = '4'

sys.path.insert(0, os.path.dirname(__file__))

from fagierrandsbackup.wsgi import application
