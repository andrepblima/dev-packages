"""UDC class."""

import time as _time
import numpy as _np

from . import prucparms as _prucparms
from .csdev import UDC_MAX_NR_DEV as _UDC_MAX_NR_DEV
from .psbsmp import PSBSMPFactory as _PSBSMPFactory


class UDC:
    """UDC."""

    _prucparms = {
        'FBP': _prucparms.PRUCParmsFBP,
        'FBP_DCLink': _prucparms.PRUCParmsFBP_DCLink,
        'FAC_2S_DCDC': _prucparms.PRUCParmsFAC_2S_DCDC,
        'FAC_2P4S_DCDC': _prucparms.PRUCParmsFAC_2P4S_DCDC,
        'FAC_DCDC': _prucparms.PRUCParmsFAC_DCDC,
        'FAC_2S_ACDC': _prucparms.PRUCParmsFAC_2S_ACDC,
        'FAC_2P4S_ACDC': _prucparms.PRUCParmsFAC_2P4S_ACDC,
        'FAP': _prucparms.PRUCParmsFAP,
        'FAP_4P': _prucparms.PRUCParmsFAP_4P,
        'FAP_2P2S': _prucparms.PRUCParmsFAP_2P2S,
    }

    _soft_def = _np.zeros(_UDC_MAX_NR_DEV)


    def __init__(self, pru, psmodel, device_ids):
        """Init."""
        self._pru = pru
        self._devs_ids = device_ids
        self._psmodel = psmodel
        self._devs_bsmp = self._create_bsmp_connectors()
        self._dev_first, self._dev_second = \
            self._get_devs_first_second()
        self._is_fbp = self._psmodel == 'FBP'

    def _get_devs_first_second(self):
        ids = sorted(self._devs_ids)
        dev_first = self._devs_bsmp[ids[0]]
        dev_second = self._devs_bsmp[ids[4]] if len(ids) > 4 else None
        return dev_first, dev_second

    @property
    def pru(self):
        """Return PRU used for communication with UDC."""
        return self._pru

    @property
    def psmodel(self):
        """Return power supply model associated with UDC."""
        return self._psmodel

    @property
    def device_ids(self):
        """."""
        return self._devs_ids

    @property
    def prucparms(self):
        """Return PRU Controller parameters object."""
        prucparms_class = UDC._prucparms[self._psmodel]
        return prucparms_class()

    @property
    def CONST_BSMP(self):
        """Return PSBSMP constants."""
        return self._dev_first.CONST_BSMP

    @property
    def CONST_PSBSMP(self):
        """Return PSBSMP constants."""
        return self.prucparms.CONST_PSBSMP

    def reset(self, **kwargs):
        """Reset UDC."""
        # turn off all power supplies (NOTE: or F_RESET_UDC does not work)
        for dev in self._devs_bsmp.values():
            ack, data = dev.execute_function(
                func_id=self.CONST_PSBSMP.F_TURN_OFF)
            if ack != self.CONST_BSMP.ACK_OK:
                dev_id = dev.channel.address
                print(('UDC.reset: could not turn off '
                       'device id:{} !').format(dev_id))
                return ack, data

        # reset UDC proper.
        self._dev_first.execute_function(
            func_id=self.CONST_PSBSMP.F_RESET_UDC, **kwargs, read_flag=False)

        return ack, data

    def bufsample_disable(self):
        """Disable DSP from writting to bufsample curve."""
        for dev in self._devs_bsmp.values():
            ack, data = dev.wfmref_mon_bufsample_disable()
            if ack != self.CONST_BSMP.ACK_OK:
                return ack, data
        # a single sleep for all devices
        sleep_time = self._dev_first._sleep_disable_bufsample = 0.5  # [s]
        _time.sleep(sleep_time)
        return ack, data

    def bufsample_enable(self):
        """Enable DSP from writting to bufsample curve."""
        for dev in self._devs_bsmp.values():
            ack, data = dev.wfmref_mon_bufsample_enable()
            if ack != self.CONST_BSMP.ACK_OK:
                return ack, data
        return ack, data

    def parse_firmware_version(self, version):
        """Process firmware version from BSMP device."""
        # uses first BSMP device
        dev = self._devs_bsmp[next(iter(self._devs_bsmp))]  # first dev
        return dev.parse_firmware_version(version)

    def reset_groups_of_variables(self, groups):
        """Reset groups of variables."""
        for dev in self._devs_bsmp.values():
            dev.reset_groups_of_variables(groups=groups)

    def __getitem__(self, index):
        """Return BSMP."""
        return self._devs_bsmp[index]

    # --- SOFBCurrent methods

    def sofb_current_rb_get(self):
        """Return SOFBCurrent-RB."""
        if self._is_fbp:
            dev1, dev2 = self._dev_first, self._dev_second
            val1 = dev1.sofb_ps_setpoint
            val2 = dev2.sofb_ps_setpoint if dev2 else UDC._soft_def
            return _np.concatenate((val1, val2))
        return None

    def sofb_current_refmon_get(self):
        """Return SOFBCurrentRef-Mon."""
        if self._is_fbp:
            dev1, dev2 = self._dev_first, self._dev_second
            val1 = dev1.sofb_ps_reference
            val2 = dev2.sofb_ps_reference if dev2 else UDC._soft_def
            return _np.concatenate((val1, val2))
        return None

    def sofb_current_mon_get(self):
        """Return SOFBCurrent-Mon."""
        if self._is_fbp:
            dev1, dev2 = self._dev_first, self._dev_second
            val1 = dev1.sofb_ps_iload
            val2 = dev2.sofb_ps_iload if dev2 else UDC._soft_def
            return _np.concatenate((val1, val2))
        return None

    def sofb_current_set(self, value):
        """Set SOFB Current."""
        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'UDC.sofb_current_set (beg)', 1e3*(_time.time() % 1)))

        if self._is_fbp:
            # set value
            self._dev_first.sofb_ps_setpoint_set(value[:4])
            if self._dev_second:
                self._dev_first.sofb_ps_setpoint_set(value[4:])

        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'UDC.sofb_current_set (end)', 1e3*(_time.time() % 1)))

    def sofb_update(self):
        """Update sofb."""
        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'UDC.sofb_update (beg)', 1e3*(_time.time() % 1)))

        if self._is_fbp:
            self._dev_first.sofb_update()
            if self._dev_second:
                self._dev_second.sofb_update()

        # print('{:<30s} : {:>9.3f} ms'.format(
        #     'UDC.sofb_update (end)', 1e3*(_time.time() % 1)))

    # --- private methods

    def _create_bsmp_connectors(self):
        devices = dict()
        for dev_id in self._devs_ids:
            devices[dev_id] = _PSBSMPFactory.create(
                self._psmodel, dev_id, self._pru)
        return devices
