#!/usr/bin/env python-sirius
"""."""

from epics import PV
from siriuspy.namesys import SiriusPVName


class BPM:
    """."""

    def __init__(self, name):
        """."""
        self._name = SiriusPVName(name)
        self._spanta = PV(self._name.substitute(propty='SP_AArrayData'))
        self._spantb = PV(self._name.substitute(propty='SP_BArrayData'))
        self._spantc = PV(self._name.substitute(propty='SP_CArrayData'))
        self._spantd = PV(self._name.substitute(propty='SP_DArrayData'))
        self._spposx = PV(self._name.substitute(propty='SPPosX-Mon'))
        self._spposy = PV(self._name.substitute(propty='SPPosY-Mon'))
        self._spsum = PV(self._name.substitute(propty='SPSum-Mon'))

    @property
    def connected(self):
        """."""
        conn = self._spanta.connected
        conn &= self._spantb.connected
        conn &= self._spantc.connected
        conn &= self._spantd.connected
        conn &= self._spposx.connected
        conn &= self._spposy.connected
        conn &= self._spsum.connected
        return conn

    @property
    def sp_anta(self):
        """."""
        return self._spanta.get()

    @property
    def sp_antb(self):
        """."""
        return self._spantb.get()

    @property
    def sp_antc(self):
        """."""
        return self._spantc.get()

    @property
    def sp_antd(self):
        """."""
        return self._spantd.get()

    @property
    def spposx(self):
        """."""
        return self._spposx.get()

    @property
    def spposy(self):
        """."""
        return self._spposy.get()

    @property
    def spsum(self):
        """."""
        return self._spsum.get()
