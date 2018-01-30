"""Define Power Supply classes."""

import re as _re
from threading import Thread as _Thread
import time as _time
from epics import PV as _PV
from siriuspy.epics.computed_pv import ComputedPV as _ComputedPV
from siriuspy.pwrsupply.data import PSData as _PSData
from siriuspy.magnet.data import MAData as _MAData
from siriuspy.magnet import util as _mutil
from siriuspy.namesys import SiriusPVName as _SiriusPVName
from siriuspy.envars import vaca_prefix as _VACA_PREFIX
from siriuspy.factory import NormalizerFactory as _NormalizerFactory
from siriuspy.pwrsupply import sync as _sync


class _PSCommInterface:
    """Communication inerface class for power supplies."""

    def read(self, field):
        """Return field value."""
        raise NotImplementedError

    def write(self, field, value):
        """Write value to a field."""
        raise NotImplementedError

    def add_callback(self, func):
        """Add callback function."""
        raise NotImplementedError


class PowerSupply(_PSCommInterface):
    """PowerSupply class with ps logic."""

    _SCAN_INTERVAL = 0.1  # [s]
    _is_setpoint = _re.compile('.*-(SP|Sel|Cmd)$')

    # power supply objet, not controller's, is responsible to provide state
    # of the following fields:
    _db_const_fields = ('IntlkSoftLabels-Cte',
                        'IntlkHardLabels-Cte')

    def __init__(self, psname, controller):
        """Init method."""
        self._psdata = _PSData(psname=psname)
        self._controller = controller
        self._updating = True
        self._base_db = self._get_base_db()
        self._setpoints = self._build_setpoints()
        self._callback = None
        self._thread_scan = _Thread(target=self._scan_fields)
        self._thread_scan.setDaemon(True)
        self._thread_scan.start()

    @property
    def psdata(self):
        """Return PSData object."""
        return self._psdata

    @property
    def updating(self):
        """Return updating state."""
        return self._updating

    @updating.setter
    def updating(self, value):
        """Set updating state."""
        self._updating = value

    # --- public PSComm interface API ---

    def read(self, field):
        """Read field value."""
        # Check CtrlMode?
        if PowerSupply._is_setpoint.match(field):
            # why not use _base_db to store setpoints?
            return self._setpoints[field]['value']
        if field in PowerSupply._db_const_fields:
                return self._base_db[field]['value']
        else:
            return self._controller.read(field)

    def write(self, field, value):
        """Write value to field."""
        func = self._setpoints[field]['func']
        return func(value)

    def add_callback(self, func):
        """Add callback to be issued when a PV is updated."""
        self._callback = func

    def get_database(self, prefix=""):
        """Fill base DB with values and limits read from PVs.

        Optionally add a prefix to the dict keys.
        """
        db = self._fill_database()

        if prefix:
            prefixed_db = {}
            for key, value in db.items():
                prefixed_db[prefix + ":" + key] = value
            return prefixed_db
        else:
            return db

    # -- private methods ---

    def _build_setpoints(self):
        sp = dict()
        for field in self._get_fields():
            if not PowerSupply._is_setpoint.match(field):
                continue
            sp[field] = dict()
            self._set_field_setpoint(sp[field], field)
        return sp

    def _set_field_setpoint(self, keyvalue, field):
        # should we use databse as setpoint state?!
        db = self._base_db
        if field == 'PwrState-Sel':
            keyvalue['func'] = self._set_pwrstate
            keyvalue['value'] = db['PwrState-Sel']['value']
        elif field == 'OpMode-Sel':
            keyvalue['func'] = self._set_opmode
            keyvalue['value'] = db['OpMode-Sel']['value']
        elif field == 'Current-SP':
            keyvalue['func'] = self._set_current
            keyvalue['value'] = db['Current-SP']['value']
        elif field == 'WfmLoad-Sel':
            keyvalue['func'] = self._set_wfmload
            keyvalue['value'] = db['WfmLoad-Sel']['value']
        elif field == 'WfmLabel-SP':
            keyvalue['func'] = self._set_wfmlabel
            keyvalue['value'] = db['WfmLabel-SP']['value']
        elif field == 'WfmData-SP':
            keyvalue['func'] = self._set_wfmdata
            keyvalue['value'] = [v for v in db['WfmData-SP']['value']]
        elif field == 'Abort-Cmd':
            keyvalue['func'] = self._abort
            keyvalue['value'] = db['Abort-Cmd']['value']
        elif field == 'Reset-Cmd':
            keyvalue['func'] = self._reset
            keyvalue['value'] = db['Reset-Cmd']['value']

    def _set_pwrstate(self, value):
        self._setpoints['PwrState-Sel']['value'] = value
        return self._controller.write('PwrState-Sel', value)

    def _set_opmode(self, value):
        self._setpoints['OpMode-Sel']['value'] = value
        return self._controller.write('OpMode-Sel', value)

    def _set_current(self, value):
        self._setpoints['Current-SP']['value'] = value
        return self._controller.write('Current-SP', value)

    def _set_wfmload(self, value):
        self._wfmload_sel = value
        self._setpoints['WfmLoad-Sel']['value'] = value
        return self._controller.write('WfmLoad-Sel', value)

    def _set_wfmlabel(self, value):
        self._wfmlabel_sp = value
        self._setpoints['WfmLabel-SP']['value'] = value
        return self._controller.write('WfmLabel-SP', value)

    def _set_wfmdata(self, value):
        self._wfmdata_sp = value
        self._setpoints['WfmData-SP']['value'] = value
        return self._controller.write('WfmData-SP', value)

    def _abort(self, value):
        # op_mode = self.read('OpMode-Sts')
        self._setpoints['Abort-Cmd']['value'] += 1
        self.write('OpMode-Sel', 0)  # Set to SlowRef
        self.write('Current-SP', 0.0)

    def _reset(self, value):
        self._setpoints['Reset-Cmd']['value'] += 1
        self.write('Current-SP', 0.0)
        self.write('OpMode-Sel', 0)
        # Reset interlocks

    def _get_base_db(self):
        return self._psdata.propty_database

    def _get_fields(self):
        return self._base_db.keys()

    def _fill_database(self):
        db = dict()
        db.update(self._base_db)
        for field in db:
            value = self.read(field)
            if value is not None:
                db[field]["value"] = value

        return db

    def _scan_fields(self):
        """Scan fields."""
        while True:
            if self._updating:
                for field in self._base_db:
                    if field in PowerSupply._db_const_fields:
                        continue
                    value = self.read(field)
                    # if _base_db is a updated copy of ps state, users (IOC)
                    # of powersupply could access it directly, without the
                    # the need of callback registration!
                    if self._callback:
                        self._callback(
                            pvname=self._psdata.psname + ':' + field,
                            value=value)
            _time.sleep(PowerSupply._SCAN_INTERVAL)


class PSEpics(_PSCommInterface):
    """Power supply with Epics communication."""

    valid_fields = ('Current-SP', 'Current-RB', 'CurrentRef-Mon',
                    'Current-Mon', 'PwrState-Sel', 'PwrState-Sts',
                    'OpMode-Sel', 'OpMode-Sts',
                    'Energy-SP', 'Energy-RB', 'EnergyRef-Mon', 'Energy-Mon',
                    'KL-SP', 'KL-RB', 'KLRef-Mon', 'KL-Mon',
                    'SL-SP', 'SL-RB', 'SLRef-Mon', 'SL-Mon',
                    'Kick-SP', 'Kick-RB', 'KickRef-Mon', 'Kick-Mon',
                    'Reset-Cmd', 'Abort-Cmd')

    def __init__(self, psname, fields=None, use_vaca=True):
        """Create epics PVs and expose them through public controller API."""
        # Attributes use build a full PV address
        self._psname = psname
        # self._sort_fields()
        if use_vaca:
            self._prefix = _VACA_PREFIX
        else:
            self._prefix = ''
        # Get pv db
        self._base_db = self._get_base_db()
        # Get fields, if none is passed they'll will be retrieved from the db
        if fields is None:
            self._fields = self._get_fields()
        else:
            self._fields = fields
        # Holds PVs objects
        self._pvs = dict()
        self._create_pvs()

    # --- public PSComm interface API ---

    def read(self, field):
        """Read a field value."""
        if field not in self.valid_fields:
            return None
        if self._pvs[field].connected:
            return self._pvs[field].get()
        else:
            print("Not connected")
            return None

    def write(self, field, value):
        """Write a value to a field."""
        # Check wether value is valid and return 0
        if field not in self.valid_fields:
            return None
        if self._pvs[field].connected:
            return self._pvs[field].put(value)
        else:
            print("Not connected")
            return None

    def add_callback(self, func):
        """Add callback to field."""
        if not callable(func):
            raise ValueError("Tried to set non callable as a callback")
        else:
            for pvname, pv in self._pvs.items():
                field = pvname.split(':')[-1]
                # if field in self.valid_fields:
                pv.add_callback(func)

    def get_database(self, prefix=""):
        """Fill base DB with values and limits read from PVs.

        Optionally add a prefix to the dict keys.
        """
        db = self._fill_database()

        if prefix:
            prefixed_db = {}
            for key, value in db.items():
                prefixed_db[prefix + ":" + key] = value
            return prefixed_db
        else:
            return db

    # --- private methods ---

    def _create_pvs(self):
        # No/rmally create normal PV objects
        # In case more than one source is supplied creates a SyncPV
        # In case the device is a Magnet with a normalized force being supplied
        # as one of the fields, a NormalizedPV is created
        self._sort_fields()
        for field in self._fields:
            # if field in self.valid_fields:
            self._pvs[field] = self._create_pv(field)
            # return _PV(self._prefix + self.psname + ":" + field)

    def _create_pv(self, field):
        return _PV(self._prefix + self._psname + ":" + field)

    def _get_base_db(self):
        return _PSData(self._psname).propty_database

    def _get_fields(self):
        return self._base_db.keys()

    def _fill_database(self):
        db = dict()
        db.update(self._base_db)
        for field in db:
            value = self.read(field)
            if value is not None:
                db[field]["value"] = value

        return db

    def _sort_fields(self):
        fields = []
        for field in self._fields:
            if not self._is_strength.match(field):
                fields.insert(0, field)
            else:
                fields.append(field)

        self._fields = fields


class MAEpics(PSEpics):
    """Magnet power supply with Epics communication."""

    _is_strength = _re.compile('(Energy|KL|SL|Kick).+$')
    _is_multi_ps = _re.compile('(SI|BO)-\w{2,4}:MA-B.*$')

    def __init__(self, maname, lock=False, **kwargs):
        """Create epics PVs and expose them through public controller API."""
        # Attributes use build a full PV address
        self._maname = _SiriusPVName(maname)
        self._madata = _MAData(maname)
        self._lock = lock
        super().__init__(
            self._maname.replace("MA", "PS").replace("PM", "PU"),
            **kwargs)

    # Virtual Methods
    def _create_pvs(self):
        self._sort_fields()
        super()._create_pvs()

    def _create_pv(self, field):
        # Build either a real or computed PV
        if MAEpics._is_strength.match(field):  # NormalizedPV
            pvname = self._prefix + self._maname + ":" + field
            str_obj = self._get_normalizer(self._maname)
            pvs = self._get_str_pv(field)
            return _ComputedPV(pvname, str_obj, *pvs)
        else:
            if len(self._psnames()) > 1:  # SyncPV
                # Sync object used to sync pvs
                sync = self._get_sync_obj(field)
                # Real PVs(names) supplied to ComputedPV
                pvs = [self._prefix + device_name + ":" + field
                       for device_name in self._psnames()]
                # Name of the ComputedPV
                pvname = self._psname + ":" + field
                # Create a virtual PV (ComputedPV)
                return _ComputedPV(pvname, sync, *pvs)
            else:
                return super()._create_pv(field)

    def _get_base_db(self):
        return self._madata.get_database(self._madata.psnames[0])

    # Class methods
    def _get_normalizer(self, device_name):
        # Return Normalizer object
        return _NormalizerFactory.factory(device_name)

    def _get_sync_obj(self, field):
        # Return SyncWrite or SyncRead object
        if "SP" in field or "Sel" in field or "Cmd" in field:
            return _sync.SyncWrite(lock=self._lock)
        else:
            return _sync.SyncRead()

    def _get_str_pv(self, field):
        ma_class = _mutil.magnet_class(self._maname)
        if 'dipole' == ma_class:
            return [self._pvs[field.replace('Energy', 'Current')], ]
        elif 'pulsed' == ma_class:
            dipole_name = _mutil.get_section_dipole_name(self._maname)
            dipole = self._prefix + dipole_name
            return [self._pvs[field.replace('Kick', 'Voltage')],
                    dipole + ":" + field.replace('Kick', 'Current')]
        elif 'trim' == ma_class:
            dipole_name = _mutil.get_section_dipole_name(self._maname)
            dipole = self._prefix + dipole_name
            fam_name = _mutil.get_magnet_family_name(self._maname)
            fam = self._prefix + fam_name
            field = field.replace('KL', 'Current')
            return [self._pvs[field],
                    dipole + ':' + field,
                    fam + ':' + field]
        else:
            dipole_name = _mutil.get_section_dipole_name(self._maname)
            dipole = self._prefix + dipole_name
            field = field.replace('KL', 'Current').replace('SL', 'Current')\
                .replace('Kick', 'Current')
            return [self._pvs[field],
                    dipole + ":" + field]

    def _psnames(self):
        ma_class = _mutil.magnet_class(self._maname)
        if 'dipole' == ma_class:
            if 'SI' == self._maname.sec:
                return ['SI-Fam:PS-B1B2-1', 'SI-Fam:PS-B1B2-2']
            elif 'BO' == self._maname.sec:
                return ['BO-Fam:PS-B-1', 'BO-Fam:PS-B-2']
        elif 'pulsed' == ma_class:
            return [self._maname.replace(':PM', ':PU')]

        return [self._maname.replace(':MA', ':PS')]
