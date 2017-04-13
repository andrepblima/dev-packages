import uuid as _uuid
import siriuspy.namesys as _namesys
from siriuspy.timesys import device_models as _device_models
from siriuspy.timesys import timing_devices_data as _timing_data

_EventMapping = {'Linac':0,  'InjBO':1,  'InjSI':2,  'RmpBO':3,  'RmpSI':4,
                 'DigLI':5,  'DigTB':6,  'DigBO':7,  'DigTS':8,  'DigSI':9,
                 'Orbit':10, 'Coupl':11,  'Tunes':12,}

EVG_PREFIX = 'AS-Glob:TI-EVG:'

_ALL_DEVICES = _timing_data.get_all_devices()
_pv_fun = lambda x,y: _namesys.SiriusPVName(x).dev_type.lower() == y.lower()
_get_devs = lambda x: { dev for dev in _ALL_DEVICES if _pv_fun(dev,x) }

EVGs = _get_devs('evg')
EVRs = _get_devs('evr')
EVEs = _get_devs('eve')
AFCs = _get_devs('afc')

class TimingSimulation(_device_models.CallBack):

    @classmethod
    def get_database(cls, prefix = ''):
        db = dict()
        db.update(  _device_models.EVGIOC.get_database( prefix = prefix + EVG_PREFIX )  )
        for dev in EVRs:
            db.update(  _device_models.EVRIOC.get_database( prefix = prefix + dev + ':' )  )
        for dev in EVEs:
            db.update(  _device_models.EVEIOC.get_database( prefix = prefix + dev + ':' )  )
        for dev in AFCs:
            db.update(  _device_models.AFCIOC.get_database( prefix = prefix + dev + ':' )  )
        return db

    def __init__(self,rf_frequency,callbacks=None, prefix = ''):
        super().__init__(callbacks,prefix='')
        self.uuid = _uuid.uuid4()
        self.evg = _device_models.EVGIOC(rf_frequency,
                                         callbacks={self.uuid:self._callback},
                                         prefix = prefix + EVG_PREFIX  )
        self.evrs = dict()
        for dev in EVRs:
            pref = prefix + dev + ':'
            evr = _device_models.EVRIOC( rf_frequency/_device_models.RF_FREQ_DIV,
                                         callbacks={self.uuid:self._callback},
                                         prefix = pref )
            self.evg.add_pending_devices_callback(evr.uuid, evr.receive_events)
            self.evrs[pref] = evr

        self.eves = dict()
        for dev in EVEs:
            pref = prefix + dev + ':'
            eve = _device_models.EVEIOC( rf_frequency/_device_models.RF_FREQ_DIV,
                                         callbacks={self.uuid:self._callback},
                                         prefix = pref )
            self.evg.add_pending_devices_callback(eve.uuid, eve.receive_events)
            self.eves[pref] = eve

        self.afcs = dict()
        for dev in AFCs:
            pref = prefix + dev + ':'
            afc = _device_models.AFCIOC( rf_frequency/_device_models.RF_FREQ_DIV,
                                         callbacks={self.uuid:self._callback},
                                         prefix = pref )
            self.evg.add_pending_devices_callback(afc.uuid, afc.receive_events)
            self.afcs[pref] = afc

    def _callback(self,propty,value, **kwargs):
        self._call_callbacks(propty, value, **kwargs)

    def add_injection_callback(self, uuid, callback):
        self.evg.add_injection_callback(uuid, callback)

    def remove_injection_callback(self, uuid):
        self.evg.remove_injection_callback(uuid)

    def add_single_callback(self, uuid, callback):
        self.evg.add_single_callback(uuid, callback)

    def remove_single_callback(self, uuid):
        self.evg.remove_single_callback(uuid)

    def get_propty(self, reason):
        reason = reason[len(self.prefix):]
        parts = _namesys.SiriusPVName(reason)
        if parts.dev_type == 'EVG':
            return self.evg.get_propty(reason)
        elif parts.dev_name+':' in self.evrs.keys():
            return self.evrs[parts.dev_name+':'].get_propty(reason)
        elif parts.dev_name+':' in self.eves.keys():
            return self.eves[parts.dev_name+':'].get_propty(reason)
        elif parts.dev_name+':' in self.afcs.keys():
            return self.afcs[parts.dev_name+':'].get_propty(reason)
        else:
            return None

    def set_propty(self, reason, value):
        reason = reason[len(self.prefix):]
        parts = _namesys.SiriusPVName(reason)
        if parts.dev_type == 'EVG':
            return self.evg.set_propty(reason,value)
        elif parts.dev_name+':' in self.evrs.keys():
            return self.evrs[parts.dev_name+':'].set_propty(reason,value)
        elif parts.dev_name+':' in self.eves.keys():
            return self.eves[parts.dev_name+':'].set_propty(reason,value)
        elif parts.dev_name+':' in self.afcs.keys():
            return self.afcs[parts.dev_name+':'].set_propty(reason,value)
        else:
            return False


def get_mapping_timing_devs_2_receivers(): pass
