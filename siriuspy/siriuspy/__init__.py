"""Siriuspy."""

import os as _os
with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()
del _os


__all__ = [
    'envars', 'util', 'csdev', 'clientweb', 'clientconfigdb',
    'diagnostics', 'pwrsupply', 'magnet', 'namesys', 'timesys', 'csdevice',
    'epics', 'callbacks', 'search', 'devices']
