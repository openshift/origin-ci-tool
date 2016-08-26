# these module-level "private" variables will hold our
# in-memory cache of information regarding configuration
from config.load import initialize_paths, load_config

_config_home = ''
_config_path = ''
_inventory_path = ''
_config = dict()

initialize_paths()
load_config()