import os
import sys
import site
 
# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__), 'groc_env/local/lib/python2.7/site-packages'))
 
# Path of execution
sys.path.append('/var/www/groc_flask_app')
 
# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'groc_env/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))
 
# import groc as application
from groc import app as application