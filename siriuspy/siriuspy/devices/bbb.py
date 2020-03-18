"""."""

import time as _time

from ..csdevice.orbitcorr import SOFBFactory
from .device import Device as _Device
from .util import get_namedtuple as _get_namedtuple


class BbB(_Device):
    """BbB Device."""

    _devices = {
        'H': 'SI-Glob:DI-BbBProc-H',
        'V': 'SI-Glob:DI-BbBProc-V',
        'L': 'SI-Glob:DI-BbBProc-L'}
    DEVICES = _get_namedtuple('Devices', *zip(*_devices.items()))

    _properties = (
        'REVISION', 'GPIO_SEL',
        'CSET0', 'CSET1',
        'CR256', 'DELAY', 'RF_FREQ', 'HARM_NUM', 'PROC_DS',
        'SRAM_GDTIME', 'SRAM_HOLDTIME', 'SRAM_REC_DS', 'SRAM_POSTTIME',
        'SRAM_EXTEN', 'SRAM_POSTSEL', 'SRAM_DUMP',
        'SRAM_RAW:SAMPLES', 'SRAM_RAW', 'SRAM_'
        'BRAM_GDTIME', 'BRAM_HOLDTIME', 'BRAM_REC_DS', 'SRAM_POSTTIME',
        'BRAM_EXTEN', 'BRAM_POSTSEL', 'BRAM_DUMP',
        'BRAM_RAW:SAMPLES', 'BRAM_RAW',
        'FBE_Z_ATT', 'FBE_Z_PHASE',
        'FBE_BE_ATT', 'FBE_BE_PHASE',
        'FBE_X_ATT', 'FBE_X_PHASE',
        'FBE_Y_ATT', 'FBE_Y_PHASE',
        'DESC:CSET0', 'DESC:CSET1')

    _default_timeout = 10  # [s]
    _off, _on = 0, 1
    _fpga_bits = 2**15

    def __init__(self, devname):
        """."""
        # check if device exists
        if devname not in BbB.DEVICES:
            raise NotImplementedError(devname)

        # call base class constructor
        super().__init__(devname, properties=BbB._properties)

    @property
    def version(self):
        return self['REVISION']

    @property
    def gpio_sel(self):
        return self['GPIO_SEL']

    @gpio_sel.setter
    def gpio_sel(self, value):
        return self['GPIO_SEL'] = int(value)

    @property
    def CSET0(self):
        return self['CSET0']

    @property
    def CSET1(self):
        return self['CSET1']

    @property
    def CR256(self):
        return self['CR256']

    @property
    def DELAY(self):
        return self['DELAY']

    @property
    def RF_FREQ(self):
        return self['RF_FREQ']

    @property
    def HARM_NUM(self):
        return self['HARM_NUM']

    @property
    def PROC_DS(self):
        return self['PROC_DS']

    @property
    def sram_growthtime(self):
        return self['SRAM_GDTIME']

    @property
    def sram_holdtime(self):
        return self['SRAM_HOLDTIME']

    @property
    def sram_downsample(self):
        return self['SRAM_REC_DS']

    @property
    def sram_posttime(self):
        return self['SRAM_POSTTIME']

    @property
    def sram_trigtype(self):
        return self['SRAM_EXTEN']

    @property
    def sram_acqtype(self):
        return self['SRAM_POSTSEL']

    @property
    def sram_dumpdata(self):
        return self['SRAM_DUMP']

    @property
    def sram_nrsamples(self):
        return self['SRAM_RAW_SAMPLES']

    @property
    def sram_rawdata(self):
        return self['SRAM_RAW']

    @property
    def bram_downsample(self):
        return self['BRAM_REC_DS']

    @bram_downsample.setter
    def bram_downsample(self, value):
        self['BRAM_REC_DS'] = int(value)

    @property
    def bram_trigtype(self):
        return self['BRAM_EXTEN']

    @bram_trigtype.setter
    def bram_trigtype(self, value):
        self['BRAM_EXTEN'] = 1 if value else 0

    @property
    def bram_acqtype(self):
        return self['BRAM_POSTSEL']

    @bram_acqtype.setter
    def bram_acqtype(self, value):
        self['BRAM_POSTSEL'] = 1 if value else 0

    @property
    def bram_acqtime(self):
        return self['BRAM_ACQTIME']

    @bram_acqtime.setter
    def bram_acqtime(self, value):
        self['BRAM_ACQTIME'] = value

    @property
    def bram_growthtime(self):
        return self['BRAM_GDTIME']

    @bram_growthtime.setter
    def bram_growthtime(self, value):
        self['BRAM_GDTIME'] = value

    @property
    def bram_holdtime(self):
        return self['BRAM_HOLDTIME']

    @bram_holdtime.setter
    def bram_holdtime(self, value):
        self['BRAM_HOLDTIME'] = value

    @property
    def bram_posttime(self):
        return self['BRAM_POSTTIME']

    @bram_posttime.setter
    def bram_posttime(self, value):
        self['BRAM_POSTTIME'] = value

    @property
    def bram_dumpdata(self):
        return self['BRAM_DUMP']

    @bram_dumpdata.setter
    def bram_dumpdata(self, value):
        self['BRAM_DUMP'] = 1

    @property
    def bram_nrsamples(self):
        return self['BRAM_RAW_SAMPLES']

    @property
    def bram_rawdata(self):
        return self['BRAM_RAW']

    @property
    def FBE_Z_ATT(self):
        return self['FBE_Z_ATT']

    @property
    def FBE_Z_PHASE(self):
        return self['FBE_Z_PHASE']

    @property
    def FBE_BE_ATT(self):
        return self['FBE_BE_ATT']

    @property
    def FBE_BE_PHASE(self):
        return self['FBE_BE_PHASE']

    @property
    def FBE_X_ATT(self):
        return self['FBE_X_ATT']

    @property
    def FBE_X_PHASE(self):
        return self['FBE_X_PHASE']

    @property
    def FBE_Y_ATT(self):
        return self['FBE_Y_ATT']

    @property
    def FBE_Y_PHASE(self):
        return self['FBE_Y_PHASE']

    @property
    def DESC:CSET0(self):
        return self['DESC:CSET0']

    @property
    def DESC:CSET(self):
        return self['DESC:CSET1]

    def cmd_reset(self):
        """."""
        self['SmoothReset-Cmd'] = SOFB._on

    def cmd_calccorr(self):
        """."""
        self['CalcDelta-Cmd'] = SOFB._on

    def cmd_applycorr(self):
        """."""
        self['ApplyDelta-Cmd'] = self.data.ApplyDelta.CH
        _time.sleep(0.3)
        self['ApplyDelta-Cmd'] = self.data.ApplyDelta.CV

    @property
    def autocorrsts(self):
        """."""
        return self['ClosedLoop-Sts']

    def cmd_turn_on_autocorr(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        self['ClosedLoop-Sel'] = SOFB._on
        self._wait(
            'ClosedLoop-Sts', SOFB._on, timeout=timeout)

    def cmd_turn_off_autocorr(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        self['ClosedLoop-Sel'] = SOFB._off
        self._wait(
            'ClosedLoop-Sts', SOFB._off, timeout=timeout)

    def wait_buffer(self, timeout=None):
        """."""
        timeout = timeout or SOFB._default_timeout
        interval = 0.050  # [s]
        ntrials = int(timeout/interval)
        _time.sleep(10*interval)
        for _ in range(ntrials):
            if self.buffer_count >= self['SmoothNrPts-SP']:
                break
            _time.sleep(interval)
        else:
            print('WARN: Timed out waiting orbit.')
