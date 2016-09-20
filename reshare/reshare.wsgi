activate_this = '/home/ubuntu/Reshare/ReshareServer/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/ReshareServer/reshare')

from application import app as application
from run import *
