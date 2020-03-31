"""State Simulator."""

import re as _re

from ..search import PSSearch as _PSSearch
from ..pwrsupply.csdev import get_ps_propty_database as _get_database
from ..pwrsupply.csdev import Const as _Const

from .simulator import Simulator as _Simulator


# NOTE: This is a toymodel PowerSupply simulator, just to test the
# Simulator infrastructure. Other PVs such as PwrState-* and
# OpMode-* should be added!

class SimPSTypeModel(_Simulator):
    """Power supply current simulator."""

    _absolute_fluctuation = 0.001  # [A]

    # regexp used to determine setpoint PVs
    _setpoint_regexp = _setpoint_regexp = _re.compile('^.*-(SP|Sel|Cmd)$')

    # these are PS properties whose correlations this simulator takes
    # into account.
    _properties = (
        'PwrState-Sel', 'PwrState-Sts',
        'OpMode-Sel', 'OpMode-Sts',
        'Current-SP', 'Current-RB',
        'CurrentRef-Mon', 'Current-Mon',
        'SOFBCurrent-SP', 'SOFBCurrent-RB',
        'SOFBCurrentRef-Mon', 'SOFBCurrent-Mon',
        )

    _absolute_fluctuation = 0.010  # [A]

    def __init__(self, pstype, psmodel):
        """Initialize simulator.

        Static methd can be used to pass arguments.
        Ex.:
            typemodel = SimPSTypeModel.conv_psname2typemodel('BO-Fam:PS-QF')
            simps = SimPSTypeModel(*typemodel)
        """
        self._pstype = pstype
        self._psmodel = psmodel

        # call base class constructor
        super().__init__()

        # list with all setpoint PVs in use (incremented in callback execution)
        self._setpoint_pvs = list()

    @property
    def pstype(self):
        """Return pstype."""
        return self._pstype

    @property
    def psmodel(self):
        """Return psmodel."""
        return self._psmodel

    def get_pwrstate(self, pvname):
        """Return PowerState associated with a given pvname."""
        pvn = pvname.substitute(propty='PwrState-Sts')
        if pvn not in self:
            # If PwrState-Sts not simulated, assume it to be On.
            return _Const.PwrStateSts.On
        return self.pv_value_get(pvn)

    @staticmethod
    def conv_psname2typemodel(psname):
        """Return pstype and psmodel associated with psname."""
        pstype = _PSSearch.conv_psname_2_pstype(psname)
        psmodel = _PSSearch.conv_psname_2_psmodel(psname)
        return pstype, psmodel

    # --- base class abstract methods ---

    def init_pvname_dbase(self):
        """."""
        regexp_dbase = dict()
        dbpvs = _get_database(self._psmodel, self._pstype)
        for propty in self._properties:
            if propty in dbpvs:
                dbase = dbpvs[propty]
                regexp = '.*:' + propty
                regexp_dbase[regexp] = dbase
        return regexp_dbase

    def callback_pv_get(self, pvname, **kwargs):
        """Execute callback function prior to SimPV readout."""

    def callback_pv_put(self, pvname, value, **kwargs):
        """Execute callback setpoint to synchronize SimPVs."""
        # if not -SP pv, does not accept write by returning False
        if not SimPSTypeModel._setpoint_regexp.match(pvname):
            return False

        # synchronize other PVs
        status = self.callback_update(pvname=pvname, value=value, **kwargs)

        # NOTE: return status signaling wheter setpoint
        # was accepted and applied (True)
        return status

    def callback_pv_add(self, pvname):
        """."""
        # if of setpoint type, add pvname to list.
        if SimPSTypeModel._setpoint_regexp.match(pvname):
            self._setpoint_pvs.append(pvname)

    def callback_update(self, **kwargs):
        """Execute callback to update/synchronize simulator."""
        # get setpoints to be propagated in simulaltion
        if 'pvname' in kwargs:
            # this option is to optimize update callback invoked
            # from callback_set
            pvname = kwargs['pvname']
            setpoints = dict()
            setpoints[pvname] = kwargs['value']
        else:
            setpoints = dict()
            for sp_pvname in self._setpoint_pvs:
                setpoints[sp_pvname] = self.pv_value_get(sp_pvname)

        # synchronize Current PVs
        for sp_pvname, sp_value in setpoints.items():
            if '-SP' in sp_pvname:
                status = self._update_sp(sp_pvname, sp_value)
            elif '-Sel' in sp_pvname:
                status = self._update_sel(sp_pvname, sp_value)

        # return status
        return status

    # --- private methods ---

    def _update_sp(self, pvname, value):
        # -RB
        pvn = pvname.replace('-SP', '-RB')
        if pvn in self:
            self.pv_value_put(pvn, value)

        setpoint = value
        if self.get_pwrstate(pvname) != _Const.PwrStateSts.On:
            # if power supply is off, do not propagate further
            setpoint = 0 * setpoint

        # Ref-Mon
        pvn = pvname.replace('-SP', 'Ref-Mon')
        if pvn in self:
            self.pv_value_put(pvn, setpoint)

        # -Mon
        pvn = pvname.replace('-SP', '-Mon')
        if pvn in self:
            setpoint = super().Utils.add_fluctuations(
                setpoint,
                absolute=SimPSTypeModel._absolute_fluctuation)
            self.pv_value_put(pvn, setpoint)

        return True

    def _update_sel(self, pvname, value):
        pvn = pvname.replace('-Sel', '-Sts')
        if pvn in self:
            self.pv_value_put(pvn, value)

        return True