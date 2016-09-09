# Ansible Python API currently is not well formed for
# consumers that want to set display attributes like
# the verbosity, so we need to make sure we are the
# first to place a `display` attr in `__main__` so we
# control it later when we want to update things
import __main__
from ansible.utils.display import Display

setattr(__main__, 'display', Display())
