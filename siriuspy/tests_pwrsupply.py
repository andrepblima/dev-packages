#!/usr/bin/env python3

import unittest
from siriuspy.pwrsupply import PowerSupply, PowerSupplyMA

class PowerSupplyTest(unittest.TestCase):
    def assert_currents(self, sp, rb, ref, mon):
        self.assertEqual(self.ps.current_sp, sp)
        self.assertEqual(self.ps.current_rb, rb)
        self.assertEqual(self.ps.currentref_mon, ref)
        self.assertEqual(self.ps.current_mon, mon)

class PowerSupplyOnSlowRefTest(PowerSupplyTest):

    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')
        self.initial_labels = self.ps.wfmlabels_mon

        self.ps.opmode_sel = 0
        self.ps.pwrstate_sel = 1

    def test_set_current(self):
        ''' Test set current_sp  on SlowRef'''
        self.ps.current_sp = 3.14
        self.assert_currents(3.14, 3.14, 3.14, 3.14)

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on SlowRef '''
        self.assertEqual(self.ps.opmode_sts, 0)
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 0)

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on SlowRef '''
        self.ps.current_sp = 3.14
        self.ps.reset = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on SlowRef '''
        self.assertEqual(self.ps.opmode_sts, 0)
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 0)

    def test_current_on_abort(self):
        self.ps.current_sp = 3.14
        self.ps.abort = 1
        self.assert_currents(3.14, 3.14, 3.14, 3.14)

class PowerSupplyOnSlowRefSyncTest(PowerSupplyTest):

    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')
        self.initial_labels = self.ps.wfmlabels_mon

        self.ps.opmode_sel = 1
        self.ps.pwrstate_sel = 1

    def test_set_current(self):
        ''' Test set current_sp  on SlowRefSync '''
        self.ps.current_sp = 3.14
        self.assert_currents(3.14, 3.14, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(3.14, 3.14, 3.14, 3.14)

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on SlowRefSync '''
        self.assertEqual(self.ps.opmode_sts, 1)
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 0)

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on SlowRefSync '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.reset = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on SlowRefSync '''
        self.assertEqual(self.ps.opmode_sts, 1)
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 0)

    def test_current_on_abort(self):
        ''' Test current change when abort is emitted on SlowRefSync '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.abort = 1
        self.assert_currents(3.14, 3.14, 3.14, 3.14)

    def test_current_on_abort2(self):
        ''' Test current change when abort is emitted on SlowRefSync '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.current_sp = 1.45
        self.ps.abort = 1
        self.assert_currents(1.45, 3.14, 3.14, 3.14)

class PowerSupplyOnFastRefTest(PowerSupplyTest):
    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA', enum_keys=True)
        self.initial_labels = self.ps.wfmlabels_mon

        self.ps.opmode_sel = 'FastRef'
        self.ps.pwrstate_sel = 'On'

    def test_set_current(self):
        ''' Test set current_sp  on FastRef '''
        self.ps.current_sp = 3.14
        self.assert_currents(3.14, 3.14, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(3.14, 3.14, 0.0, 0.0)

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on FastRef '''
        self.assertEqual(self.ps.opmode_sts, 'FastRef')
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on FastRef '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.reset = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on FastRef '''
        self.assertEqual(self.ps.opmode_sts, 'FastRef')
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_current_on_abort(self):
        ''' Test current change when abort is emitted on FastRef '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.abort = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)

    def test_current_on_abort2(self):
        ''' Test current change when abort is emitted on FastRef '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps.current_sp = 1.45
        self.ps.abort = 1
        self.assert_currents(1.45, 0.0, 0.0, 0.0)

class PowerSupplyOnRmpWfmTest(PowerSupplyTest):
    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA', enum_keys=True)

        self.ps.wfmload_sel = 'Waveform2'
        self.ps.wfmdata_sp = list(range(2000))
        self.ps.opmode_sel = 'RmpWfm'
        self.ps.pwrstate_sel = 'On'

    def test_wfmindex(self):
        self.assertEqual(self.ps.wfmindex_mon, 0)
        self.assert_currents(0.0, 0.0, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(0.0, 0.0, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(0.0, 0.0, 1.0, 1.0)

    def test_wfm_loaded(self):
        self.assertEqual(self.ps.wfmload_sts, 'Waveform2')

    def test_wfm_values_loaded(self):
        for i in range(2000):
            self.assertEqual(self.ps.wfmdata_rb[i], float(i))

    def test_wfm_loop(self):
        self.ps.current_sp = 3.14
        for i in range(2000):
            self.ps._controller.trigger_signal()
            if i > self.ps.splims['HIGH']:
                val = self.ps.splims['HIGH']
            else:
                val = i
            self.assert_currents(3.14, 3.14, val, val)

    def test_set_current(self):
        ''' Test set current_sp  on RmpWfm '''
        self.ps.current_sp = 3.14
        self.assert_currents(3.14, 3.14, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.assert_currents(3.14, 3.14, 1.0, 1.0)

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on RmpWfm '''
        self.assertEqual(self.ps.opmode_sts, 'RmpWfm')
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on RmpWfm '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps.reset = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on RmpWfm '''
        self.assertEqual(self.ps.opmode_sts, 'RmpWfm')
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 'RmpWfm')

    def test_opmode_on_abort_after_scan(self):
        ''' Test abort emitted when on RmpWfm '''
        self.assertEqual(self.ps.opmode_sts, 'RmpWfm')
        self.ps.abort = 1
        for i in range(2000):
            self.ps._controller.trigger_signal()
        self.assertEqual(self.ps.wfmindex_mon, 0)
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_current_on_abort(self):
        ''' Test current change when abort is emitted on RmpWfm '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps.abort = 1
        self.assert_currents(3.14, 3.14, 2.0, 2.0)
        self.assertEqual(self.ps.wfmindex_mon, 3)

    def test_current_on_abort_after_scam(self):
        ''' Test current change on abort after scan ends on RmpWfm '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps.abort = 1
        for i in range(1997):
            self.ps._controller.trigger_signal()
        if i > self.ps.splims['HIGH']:
            cur = self.ps.splims['HIGH']
        else:
            cur = i
        self.assert_currents(3.14, cur, cur, cur)
        self.assertEqual(self.ps.wfmindex_mon, 0)

    def test_wfmdata_changes_during_scan(self):
        for i in range(5):
            self.ps._controller.trigger_signal()
        self.ps.wfmdata_sp = [2000 - x for x in range(2000)]
        for i in range(5, 2000):
            self.ps._controller.trigger_signal()
            cur = i if i < self.ps.splims['HIGH'] else self.ps.splims['HIGH']
            self.assert_currents(0.0, 0.0, cur, cur)
        for i in range(2000):
            self.ps._controller.trigger_signal()
            cur = (2000 - i) if (2000 - i) < self.ps.splims['HIGH'] else self.ps.splims['HIGH']
            self.assert_currents(0.0, 0.0, cur, cur)

class PowerSupplyOnMigWfmTest(PowerSupplyTest):
    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA', enum_keys=True)

        self.ps.wfmload_sel = 'Waveform2'
        self.ps.wfmdata_sp = list(range(2000))
        self.ps.opmode_sel = 'MigWfm'
        self.ps.pwrstate_sel = 'On'

    def test_wfmindex(self):
        self.assertEqual(self.ps.wfmindex_mon, 0)
        self.assert_currents(0.0, 0.0, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(0.0, 0.0, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.assert_currents(0.0, 0.0, 1.0, 1.0)

    def test_wfm_loaded(self):
        self.assertEqual(self.ps.wfmload_sts, 'Waveform2')

    def test_wfm_values_loaded(self):
        for i in range(2000):
            self.assertEqual(self.ps.wfmdata_rb[i], float(i))

    def test_wfm_loop(self):
        self.ps.current_sp = 3.14
        for i in range(1999):
            self.ps._controller.trigger_signal()
            val = i if i < self.ps.splims['HIGH'] else self.ps.splims['HIGH']
            self.assert_currents(3.14, 3.14, val, val)
        self.ps._controller.trigger_signal()
        val = self.ps.splims['HIGH']
        self.assert_currents(3.14, val, val, val)
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_set_current(self):
        ''' Test set current_sp  on MigWfm '''
        self.ps.current_sp = 3.14
        self.assert_currents(3.14, 3.14, 0.0, 0.0)
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.assert_currents(3.14, 3.14, 1.0, 1.0)

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on MigWfm '''
        self.assertEqual(self.ps.opmode_sts, 'MigWfm')
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on MigWfm '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps.reset = 1
        self.assert_currents(3.14, 0.0, 0.0, 0.0)
        self.assertEqual(self.ps.wfmindex_mon, 0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on MigWfm '''
        self.assertEqual(self.ps.opmode_sts, 'MigWfm')
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_current_on_abort(self):
        ''' Test current change when abort is emitted on MigWfm '''
        self.ps.current_sp = 3.14
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps._controller.trigger_signal()
        self.ps.abort = 1
        self.assert_currents(3.14, 2.0, 2.0, 2.0)
        self.assertEqual(self.ps.wfmindex_mon, 0)

class PowerSupplyOnCycleTest(PowerSupplyTest):
    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA', enum_keys=True)

        self.ps.wfmload_sel = 'Waveform2'
        self.ps.wfmdata_sp = list(range(2000))
        self.ps.opmode_sel = 'Cycle'
        self.ps.pwrstate_sel = 'On'

        self.ps._controller.trigger_signal()

    def test_wfm_loaded(self):
        self.assertEqual(self.ps.wfmload_sts, 'Waveform2')

    def test_wfm_values_loaded(self):
        for i in range(2000):
            self.assertEqual(self.ps.wfmdata_rb[i], float(i))

    def test_opmode_on_reset(self):
        ''' Test opmode change on reset when on MigWfm '''
        self.assertEqual(self.ps.opmode_sts, 'Cycle')
        self.ps.reset = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

    def test_currents_on_reset(self):
        ''' Test currents change on reset when on MigWfm '''
        self.ps.reset = 1
        self.assert_currents(0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.ps.wfmindex_mon, 0)

    def test_opmode_on_abort(self):
        ''' Test abort emitted when on MigWfm '''
        self.assertEqual(self.ps.opmode_sts, 'Cycle')
        self.ps.abort = 1
        self.assertEqual(self.ps.opmode_sts, 'SlowRef')

class PowerSupplyGeneralTest(PowerSupplyTest):

    def setUp(self):
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')
        self.ps_enum = PowerSupply(psname='SI-Fam:PS-QDA', enum_keys=True)

        self.default_labels = self.ps.wfmlabels_mon
        self.default_labels_e = self.ps.wfmlabels_mon

    def test_initialization(self):
        self.assertEqual(self.ps.psname, 'SI-Fam:PS-QDA')
        self.assertEqual(self.ps._enum_keys, False)
        self.assertEqual(self.ps.callback, None)

    def test_initial_ctrlmode(self):
        self.assertEqual(self.ps.ctrlmode_mon, 0)
        self.assertEqual(self.ps_enum.ctrlmode_mon, 'Remote')

    def test_initial_opmode(self):
        self.assertEqual(self.ps.opmode_sel, 0)
        self.assertEqual(self.ps.opmode_sts, 0)

        self.assertEqual(self.ps_enum.opmode_sel, 'SlowRef')
        self.assertEqual(self.ps_enum.opmode_sts, 'SlowRef')

    def test_set_opmode_with_int(self):
        self.ps.opmode_sel = 1
        self.ps_enum.opmode_sel = 1

        self.assertEqual(self.ps.opmode_sel, 1)
        self.assertEqual(self.ps.opmode_sts, 1)

        self.assertEqual(self.ps_enum.opmode_sel, 'SlowRefSync')
        self.assertEqual(self.ps_enum.opmode_sts, 'SlowRefSync')

    def test_set_opmode_with_str(self):
        self.ps.opmode_sel = 'FastRef'
        self.ps_enum.opmode_sel = 'FastRef'

        self.assertEqual(self.ps.opmode_sel, 2)
        self.assertEqual(self.ps.opmode_sts, 2)

        self.assertEqual(self.ps_enum.opmode_sel, 'FastRef')
        self.assertEqual(self.ps_enum.opmode_sts, 'FastRef')

    def test_set_opmode_on_local(self):
        self.ps._ctrlmode_mon = 1 #Local mode
        self.ps.opmode_sel = 2
        self.assertEqual(self.ps.opmode_sel, 0)

    def test_reset_counter(self):
        self.assertEqual(self.ps.reset, 0)
        self.ps.reset = 2
        self.assertEqual(self.ps.reset, 1)

    def test_abort_counter(self):
        self.assertEqual(self.ps.abort, 0)
        self.ps.abort = 2
        self.assertEqual(self.ps.abort, 1)

    def test_initial_label(self):
        self.assertEqual(self.ps.wfmlabel_rb, self.default_labels[0])
        self.assertEqual(self.ps.wfmlabel_sp, self.default_labels[0])

        self.assertEqual(self.ps_enum.wfmlabel_rb, self.default_labels_e[0])
        self.assertEqual(self.ps_enum.wfmlabel_sp, self.default_labels_e[0])

    def test_set_wfmlabel(self):
        self.ps.wfmlabel_sp = 'MinhaWfm'
        self.assertEqual(self.ps.wfmlabel_rb, 'MinhaWfm')
        self.assertEqual(self.ps.wfmlabel_sp, 'MinhaWfm')
        self.ps_enum.wfmlabel_sp = 'MinhaWfm'
        self.assertEqual(self.ps_enum.wfmlabel_rb, 'MinhaWfm')
        self.assertEqual(self.ps_enum.wfmlabel_sp, 'MinhaWfm')

    def test_set_wfmlabel_on_local(self):
        self.ps._ctrlmode_mon = 1 #Local mode
        self.ps.wfmlabel_sp = 'MinhaWfm'
        self.assertEqual(self.ps.wfmlabel_rb, self.default_labels[0])
        self.assertEqual(self.ps.wfmlabel_sp, self.default_labels[0])
        self.ps_enum._ctrlmode_mon = 1 #Local mode
        self.ps_enum.wfmlabel_sp = 'MinhaWfm'
        self.assertEqual(self.ps_enum.wfmlabel_rb, self.default_labels_e[0])
        self.assertEqual(self.ps_enum.wfmlabel_sp, self.default_labels_e[0])

    def test_initial_wfmload(self):
        self.assertEqual(self.ps.wfmload_sts, 0)
        self.assertEqual(self.ps.wfmload_sel, 0)
        self.assertEqual(self.ps_enum.wfmload_sts, self.default_labels_e[0])
        self.assertEqual(self.ps_enum.wfmload_sel, self.default_labels_e[0])

    def test_set_wfmload(self):
        self.ps.wfmload_sel = 2
        self.assertEqual(self.ps.wfmload_sts, 2)
        self.assertEqual(self.ps.wfmload_sel, 2)
        self.assertEqual(self.ps.wfmlabel_rb, self.default_labels[2])
        self.ps.wfmload_sel = 0
        self.assertEqual(self.ps.wfmload_sts, 0)
        self.assertEqual(self.ps.wfmload_sel, 0)
        target_label = self.default_labels_e[5]
        self.ps_enum.wfmload_sel = target_label
        self.assertEqual(self.ps_enum.wfmload_sts, target_label)
        self.assertEqual(self.ps_enum.wfmload_sel, target_label)
        self.assertEqual(self.ps_enum.wfmlabel_rb, target_label)

    def test_set_wfmload_notint_error(self):
        ''' Test if a ValueError exception is risen when enum_keys=False and
            trying to set index without an int
        '''
        with self.assertRaises(ValueError):
            self.ps.wfmload_sel = self.default_labels_e[4]

    def test_set_wfmload_notstr_error(self):
        ''' Test if a ValueError exception is risen when enum_keys=True and
            trying to set index without a string
        '''
        with self.assertRaises(ValueError):
            self.ps_enum.wfmload_sel = 4

    def test_set_wfmload_label_not_found_error(self):
        ''' Test if a KeyError exception is risen when enum_keys=True and
            trying to set index with a waveform that is not defined
        '''
        with self.assertRaises(KeyError):
            self.ps_enum.wfmload_sel = 'randomstring'

    def test_wfmsave_counter(self):
        self.assertEqual(self.ps.wfmsave_cmd, 0)
        self.ps.wfmsave_cmd = 5
        self.assertEqual(self.ps.wfmsave_cmd, 1)

    def test_set_wfmdata(self):
        self.ps.wfmdata_sp = list(range(2000))

        for i, value in enumerate(self.ps.wfmdata_rb):
            self.assertEqual(i, value)

    def test_wfmsave_label(self):
        idx_changed = 2
        old_label_name = self.default_labels[2]
        new_label_name = 'TestWfm'

        self.ps.wfmload_sel = idx_changed
        self.ps.wfmlabel_sp = new_label_name
        self.ps.wfmsave_cmd = 1
        del self.ps
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')

        labels = self.ps.wfmlabels_mon
        self.assertEqual(labels[idx_changed], new_label_name)

        self.ps.wfmload_sel = idx_changed
        self.ps.wfmlabel_sp = old_label_name
        self.ps.wfmsave_cmd = 1
        del self.ps
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')

        self.assertEqual(self.default_labels[idx_changed], old_label_name)

    def test_wfmsave_data(self):
        idx_changed = 2
        self.ps.wfmload_sel = idx_changed
        old_data = self.ps.wfmdata_rb
        new_data = list(range(2000))

        self.ps.wfmdata_sp = new_data
        self.ps.wfmsave_cmd = 1
        del self.ps
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')

        self.ps.wfmload_sel = idx_changed
        self.assertEqual(True, (self.ps.wfmdata_rb == new_data).all())

        self.ps.wfmdata_sp = old_data
        self.ps.wfmsave_cmd = 1
        del self.ps
        self.ps = PowerSupply(psname='SI-Fam:PS-QDA')

        self.ps.wfmload_sel = idx_changed
        self.assertEqual(True, (self.ps.wfmdata_rb == old_data).all())

    def test_initial_label_wfmindex(self):
        self.assertEqual(self.ps.wfmindex_mon, 0)
        self.assertEqual(self.ps_enum.wfmindex_mon, 0)

class PowerSupplyMATest(unittest.TestCase):

    def setUp(self):

        self.ma_set = [
            dict(
                input='SI-Fam:MA-B1B2', #ma name
                output= {
                    'magfunc':'dipole',
                    'strth_class':'_StrthMADip',
                    'controller':['SI-Fam:PS-B1B2-1', 'SI-Fam:PS-B1B2-2']
                }
            ),
            dict(
                input='SI-Fam:MA-QDA', #ma name
                output= {
                    'magfunc':'quadrupole',
                    'strth_class':'_StrthMAFam',
                    'controller':['SI-Fam:PS-QDA']
                }
            ),
            dict(
                input='SI-Fam:MA-SDB0', #ma name
                output= {
                    'magfunc':'sextupole',
                    'strth_class':'_StrthMAFam',
                    'controller':['SI-Fam:PS-SDB0']
                }
            ),
            dict(
                input='SI-01M2:MA-QFA',
                output= {
                    'magfunc':'quadrupole',
                    'strth_class':'_StrthMATrim',
                    'controller':['SI-01M2:PS-QFA']
                }
            )
        ]
        '''dict(
                input='SI-16C2:MA-QS',
                output= {
                    'magfunc':'quadrupole-skew',
                    'strth_class':'_StrthMA',
                    'controller':['SI-16C2:PS-QS']
                }
            ),
            dict(
                input='SI-01C2:MA-CV-2',
                output= {
                    'magfunc':'corrector-vertical',
                    'strth_class':'_StrthMA',
                    'controller':['SI-01C2:PS-CV-2']
                }
            )
        ]'''

        self.ioc_list = list()
        for ma in self.ma_set:
            self.ioc_list.append(PowerSupplyMA(ma['input'], True, 'VAG-'))

    def test_strth_class(self):
        for i, ma in enumerate(self.ma_set):
            classname = self.ioc_list[i]._strthobj.__class__.__name__
            self.assertEqual(classname, ma['output']['strth_class'])

    def test_controller(self):
        for i, ma in enumerate(self.ma_set):
            self.assertEqual(self.ioc_list[i]._psname, ma['output']['controller'])

    def test_magfunc(self):
        for i, ma in enumerate(self.ma_set):
            self.assertEqual(self.ioc_list[i].magfunc, ma['output']['magfunc'])

    def test_get_strength(self):
        for i, ma in enumerate(self.ma_set):
            self.assertEqual(type(self.ioc_list[i].strength_sp), float)

    def test_set_strength(self):
        for i, ma in enumerate(self.ma_set):
            init_strth = self.ioc_list[i].strength_sp
            self.ioc_list[i].strength_sp = init_strth + 1.0
            self.assertEqual(self.ioc_list[i].strength_sp, (init_strth + 1.0))



if __name__ == '__main__':
    unittest.main()
