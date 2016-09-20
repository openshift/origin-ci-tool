from .load import initialize_paths, load_config, add_host_to_inventory, remove_host_from_inventory

# these module-level "private" variables will hold our
# in-memory cache of information regarding configuration
_config_home = ''
_config_path = ''
_vagrant_home = ''
_inventory_path = ''
_config = dict()

initialize_paths()
load_config()
