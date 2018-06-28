"""BO ramp configuration.

Values in _template_dict are arbitrary. They are used just to compare with
corresponding values when a new configuration is tried to be inserted in the
servconf database.
"""
from copy import deepcopy as _dcopy
from siriuspy.csdevice.pwrsupply import MAX_WFMSIZE as _MAX_WFMSIZE
from siriuspy.ramp.util import DEFAULT_RAMP_DURATION as _DEFAULT_RAMP_DURATION


def get_dict():
    """Return a dict with ramp settings."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict)
    }

    return _dict


# _eje_current = 981.7835215242153  # [A] - BO dipole current @ 3 GeV
_eje_energy = 3.0  # [GeV]
_i07 = (1, 104, 2480, 2576, 2640, 2736, 3840, 3999)
_v07 = (0.01, 0.026250000000000006, 1.0339285714285713,
        1.05, 1.05, 1.0, 0.07, 0.01)
_ramp_duration = _DEFAULT_RAMP_DURATION  # [s]
_wfm_nrpoints = _MAX_WFMSIZE
_interval = _ramp_duration / (_wfm_nrpoints - 1.0)


_ramp_dipole = {
    # dipole delay [us]
    'delay': 0.0,
    # ramp duration [ms]
    'duration': _ramp_duration,
    # start instants of dipole ramp regions [ms]
    'time': [_interval * i for i in _i07],
    # current values [A]
    'energy': [_eje_energy * v for v in _v07],
    # number of points
    'wfm_nrpoints': _MAX_WFMSIZE,
}
_normalized_configs = [
    # time [ms]            normalized configuration name
    [0.0000000000000000, 'ramp-start'],
    [12.743185796449112, 'rampup-start'],
    [303.87596899224806, 'rampup-stop'],
]
_rf_parameters = {
    # global RF delay [us]
    'delay': 0.0,
}


_template_dict = {
    'ramp_dipole': _ramp_dipole,
    'normalized_configs*': _normalized_configs,
    'rf_parameters': _rf_parameters,
}