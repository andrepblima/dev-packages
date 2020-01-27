#!/usr/bin/env python-sirius
"""."""

import time as _time
from epics import PV
from siriuspy.csdevice.orbitcorr import SOFBFactory


class SOFB:
    """."""

    def __init__(self, acc):
        """."""
        self.data = SOFBFactory.create(acc)
        orbtp = 'MTurn' if self.data.isring else 'SPass'
        self._trajx = PV(acc+'-Glob:AP-SOFB:'+orbtp+'OrbX-Mon')
        self._trajy = PV(acc+'-Glob:AP-SOFB:'+orbtp+'OrbY-Mon')
        self._orbx = PV(acc+'-Glob:AP-SOFB:SlowOrbX-Mon', auto_monitor=False)
        self._orby = PV(acc+'-Glob:AP-SOFB:SlowOrbY-Mon', auto_monitor=False)
        if self.data.isring:
            self._trajx_idx = PV(acc+'-Glob:AP-SOFB:'+orbtp+'Idx'+'OrbX-Mon')
            self._trajy_idx = PV(acc+'-Glob:AP-SOFB:'+orbtp+'Idx'+'OrbY-Mon')
        self._rst = PV(acc+'-Glob:AP-SOFB:SmoothReset-Cmd')
        self._npts_sp = PV(acc+'-Glob:AP-SOFB:SmoothNrPts-SP')
        self._npts_rb = PV(acc+'-Glob:AP-SOFB:BufferCount-Mon')
        self._sum = PV(acc+'-Glob:AP-SOFB:'+orbtp+'Sum-Mon')
        self._trigsample_sp = PV(acc+'-Glob:AP-SOFB:TrigNrSamplesPost-SP')
        self._trigsample_rb = PV(acc+'-Glob:AP-SOFB:TrigNrSamplesPost-RB')

    @property
    def connected(self):
        """."""
        conn = self._trajx.connected
        conn &= self._trajy.connected
        conn &= self._orbx.connected
        conn &= self._orby.connected
        conn &= self._sum.connected
        conn &= self._rst.connected
        conn &= self._npts_sp.connected
        conn &= self._npts_rb.connected
        return conn

    @property
    def trajx(self):
        """."""
        return self._trajx.get()

    @property
    def trajy(self):
        """."""
        return self._trajy.get()

    @property
    def orbx(self):
        """."""
        return self._orbx.get()

    @property
    def orby(self):
        """."""
        return self._orby.get()

    @property
    def trajx_idx(self):
        """."""
        return self._trajx_idx.get() if self.data.isring \
            else self.trajx

    @property
    def trajy_idx(self):
        """."""
        return self._trajy_idx.get() if self.data.isring \
            else self.trajy

    @property
    def sum(self):
        """."""
        return self._sum.get()

    @property
    def nr_points(self):
        """."""
        return self._npts_rb.value

    @nr_points.setter
    def nr_points(self, value):
        self._npts_sp.value = int(value)

    @property
    def trigsample(self):
        """."""
        return self._trigsample_rb.value

    @trigsample.setter
    def trigsample(self, value):
        self._trigsample_sp.value = int(value)

    def wait(self, timeout=10):
        """."""
        inter = 0.05
        n = int(timeout/inter)
        _time.sleep(4*inter)
        for _ in range(n):
            if self._npts_rb.value >= self._npts_sp.value:
                break
            _time.sleep(inter)
        else:
            print('WARN: Timed out waiting orbit.')

    def reset(self):
        """."""
        self._rst.value = 1
