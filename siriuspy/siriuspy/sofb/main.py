"""Main Module of the program."""

from time import time as _time, sleep as _sleep
import logging as _log
from functools import partial as _part
from threading import Thread as _Thread
import numpy as _np

from ..epics import PV as _PV

from .matrix import BaseMatrix as _BaseMatrix
from .orbit import BaseOrbit as _BaseOrbit
from .correctors import BaseCorrectors as _BaseCorrectors
from .base_class import BaseClass as _BaseClass, \
    compare_kicks as _compare_kicks

INTERVAL = 1


class SOFB(_BaseClass):
    """Main Class of the IOC."""

    def __init__(
            self, acc, prefix='', callback=None, orbit=None, matrix=None,
            correctors=None):
        """Initialize Object."""
        super().__init__(acc, prefix=prefix, callback=callback)
        _log.info('Starting SOFB...')
        self._orbit = self._correctors = self._matrix = None
        self._auto_corr = self._csorb.ClosedLoop.Off
        self._auto_corr_freq = 1
        self._measuring_respmat = False
        self._ring_extension = 1
        self._corr_factor = {'ch': 1.00, 'cv': 1.00}
        self._max_kick = {'ch': 300, 'cv': 300}
        self._max_delta_kick = {'ch': 300, 'cv': 300}
        self._meas_respmat_kick = {'ch': 15, 'cv': 15}
        if self.acc == 'SI':
            self._corr_factor['rf'] = 1.00
            self._max_kick['rf'] = 1e12  # a very large value
            self._max_delta_kick['rf'] = 500
            self._meas_respmat_kick['rf'] = 80
        self._meas_respmat_wait = 1  # seconds
        self._dtheta = None
        self._ref_corr_kicks = None
        self._thread = None
        self._havebeam_pv = _PV('SI-Glob:AP-CurrInfo:StoredEBeam-Mon')

        self.orbit = orbit
        self.correctors = correctors
        self.matrix = matrix

    def get_map2write(self):
        """Get the database of the class."""
        dbase = {
            'ClosedLoop-Sel': self.set_auto_corr,
            'ClosedLoopFreq-SP': self.set_auto_corr_frequency,
            'MeasRespMat-Cmd': self.set_respmat_meas_state,
            'CalcDelta-Cmd': self.calc_correction,
            'DeltaFactorCH-SP': _part(self.set_corr_factor, 'ch'),
            'DeltaFactorCV-SP': _part(self.set_corr_factor, 'cv'),
            'MaxKickCH-SP': _part(self.set_max_kick, 'ch'),
            'MaxKickCV-SP': _part(self.set_max_kick, 'cv'),
            'MaxDeltaKickCH-SP': _part(self.set_max_delta_kick, 'ch'),
            'MaxDeltaKickCV-SP': _part(self.set_max_delta_kick, 'cv'),
            'DeltaKickCH-SP': _part(
                self.set_delta_kick, self._csorb.ApplyDelta.CH),
            'DeltaKickCV-SP': _part(
                self.set_delta_kick, self._csorb.ApplyDelta.CV),
            'MeasRespMatKickCH-SP': _part(self.set_respmat_kick, 'ch'),
            'MeasRespMatKickCV-SP': _part(self.set_respmat_kick, 'cv'),
            'MeasRespMatWait-SP': self.set_respmat_wait_time,
            'ApplyDelta-Cmd': self.apply_corr,
            }
        if self.isring:
            dbase['RingSize-SP'] = self.set_ring_extension
        if self.acc == 'SI':
            dbase['DeltaFactorRF-SP'] = _part(self.set_corr_factor, 'rf')
            dbase['MaxDeltaKickRF-SP'] = _part(self.set_max_delta_kick, 'rf')
            dbase['DeltaKickRF-SP'] = _part(
                self.set_delta_kick, self._csorb.ApplyDelta.RF),
            dbase['MeasRespMatKickRF-SP'] = _part(self.set_respmat_kick, 'rf')
        return dbase

    @property
    def orbit(self):
        """."""
        return self._orbit

    @orbit.setter
    def orbit(self, orb):
        """."""
        if isinstance(orb, _BaseOrbit):
            self._map2write.update(orb.get_map2write())
            self._orbit = orb

    @property
    def correctors(self):
        """."""
        return self._correctors

    @correctors.setter
    def correctors(self, corrs):
        """."""
        if isinstance(corrs, _BaseCorrectors):
            self._map2write.update(corrs.get_map2write())
            self._correctors = corrs

    @property
    def matrix(self):
        """."""
        return self._matrix

    @matrix.setter
    def matrix(self, mat):
        """."""
        if isinstance(mat, _BaseMatrix):
            self._map2write.update(mat.get_map2write())
            self._matrix = mat

    @property
    def havebeam(self):
        """."""
        if self.acc != 'SI':
            return True
        return self._havebeam_pv.connected and self._havebeam_pv.value

    def process(self):
        """Run continuously in the main thread."""
        time0 = _time()
        self.status
        tfin = _time()
        dtime = INTERVAL - (tfin-time0)
        if dtime > 0:
            _sleep(dtime)
        else:
            _log.debug('process took {0:f}ms.'.format((tfin-time0)*1000))

    def set_ring_extension(self, val):
        """."""
        val = 1 if val < 1 else int(val)
        val = self._csorb.MAX_RINGSZ if val > self._csorb.MAX_RINGSZ else val
        if val == self._ring_extension:
            return True
        okay = self.orbit.set_ring_extension(val)
        if not okay:
            return False
        okay &= self.matrix.set_ring_extension(val)
        if not okay:
            return False
        self._ring_extension = val
        self.run_callbacks('RingSize-RB', val)
        bpms = _np.array(self._csorb.bpm_pos)
        bpm_pos = [bpms + i*self._csorb.circum for i in range(val)]
        bpm_pos = _np.hstack(bpm_pos)
        self.run_callbacks('BPMPosS-Mon', bpm_pos)
        return True

    def apply_corr(self, code):
        """Apply calculated kicks on the correctors."""
        if self.orbit.mode == self._csorb.SOFBMode.Offline:
            msg = 'ERR: Offline, cannot apply kicks.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if self._thread and self._thread.is_alive():
            msg = 'ERR: Loop is Closed or MeasRespMat is On.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if self._dtheta is None:
            msg = 'ERR: Cannot Apply Kick. Calc Corr first.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        _Thread(
            target=self._apply_corr, kwargs={'code': code},
            daemon=True).start()
        return True

    def calc_correction(self, _):
        """Calculate correction."""
        if self._thread and self._thread.is_alive():
            msg = 'ERR: Loop is Closed or MeasRespMat is On.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        _Thread(target=self._calc_correction, daemon=True).start()
        return True

    def set_delta_kick(self, code, dkicks):
        """Calculate correction."""
        if self._thread and self._thread.is_alive():
            msg = 'ERR: Loop is Closed or MeasRespMat is On.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        _Thread(
            target=self._set_delta_kick,
            kwargs={'code': code, 'dkicks': dkicks}, daemon=True).start()
        return True

    def set_respmat_meas_state(self, value):
        """."""
        if value == self._csorb.MeasRespMatCmd.Start:
            self._start_meas_respmat()
        elif value == self._csorb.MeasRespMatCmd.Stop:
            self._stop_meas_respmat()
        elif value == self._csorb.MeasRespMatCmd.Reset:
            self._reset_meas_respmat()
        return True

    def set_auto_corr(self, value):
        """."""
        if value == self._csorb.ClosedLoop.On:
            if self._auto_corr == self._csorb.ClosedLoop.On:
                msg = 'ERR: ClosedLoop is Already On.'
                self._update_log(msg)
                _log.error(msg[5:])
                return False
            if self._thread and self._thread.is_alive():
                msg = 'ERR: Cannot Correct, Measuring RespMat.'
                self._update_log(msg)
                _log.error(msg[5:])
                return False
            if not self.havebeam:
                msg = 'ERR: Cannot Correct, We do not have stored beam!'
                self._update_log(msg)
                _log.error(msg[5:])
                return False
            msg = 'Closing the Loop.'
            self._update_log(msg)
            _log.info(msg)
            self._auto_corr = value
            self._thread = _Thread(
                target=self._do_auto_corr, daemon=True)
            self._thread.start()
        elif value == self._csorb.ClosedLoop.Off:
            msg = 'Opening the Loop.'
            self._update_log(msg)
            _log.info(msg)
            self._auto_corr = value
        return True

    def set_auto_corr_frequency(self, value):
        """."""
        bpmfreq = self._csorb.BPMsFreq
        value = bpmfreq / max(int(bpmfreq/value), 1)
        self._auto_corr_freq = value
        self.run_callbacks('ClosedLoopFreq-RB', value)
        return True

    def set_max_kick(self, plane, value):
        """."""
        self._max_kick[plane] = float(value)
        self.run_callbacks('MaxKick'+plane.upper()+'-RB', float(value))
        return True

    def set_max_delta_kick(self, plane, value):
        """."""
        self._max_delta_kick[plane] = float(value)
        self.run_callbacks('MaxDeltaKick'+plane.upper()+'-RB', float(value))
        return True

    def set_corr_factor(self, plane, value):
        """."""
        self._corr_factor[plane] = value/100
        msg = '{0:s} DeltaFactor set to {1:6.2f}'.format(plane.upper(), value)
        self._update_log(msg)
        _log.info(msg)
        self.run_callbacks('DeltaFactor'+plane.upper()+'-RB', value)
        return True

    def set_respmat_kick(self, plane, value):
        """."""
        self._meas_respmat_kick[plane] = value
        self.run_callbacks('MeasRespMatKick'+plane.upper()+'-RB', value)
        return True

    def set_respmat_wait_time(self, value):
        """."""
        self._meas_respmat_wait = value
        self.run_callbacks('MeasRespMatWait-RB', value)
        return True

    def _update_status(self):
        self._status = bool(
            self._correctors.status | self._matrix.status | self._orbit.status)
        self.run_callbacks('Status-Mon', self._status)

    def _set_delta_kick(self, code, dkicks):
        nr_ch = self._csorb.nr_ch
        nr_chcv = self._csorb.nr_chcv
        self._ref_corr_kicks = self.correctors.get_strength()
        if self._dtheta is None:
            self._dtheta = _np.zeros(self._ref_corr_kicks.size, dtype=float)
        if code == self._csorb.ApplyDelta.CH:
            self._dtheta[:nr_ch] = dkicks
            self.run_callbacks('DeltaKickCH-RB', list(dkicks))
            self.run_callbacks('DeltaKickCH-Mon', list(dkicks))
        elif code == self._csorb.ApplyDelta.CV:
            self._dtheta[nr_ch:nr_chcv] = dkicks
            self.run_callbacks('DeltaKickCV-RB', list(dkicks))
            self.run_callbacks('DeltaKickCV-Mon', list(dkicks))
        elif self.acc == 'SI' and code == self._csorb.ApplyDelta.RF:
            self._dtheta[-1] = dkicks
            self.run_callbacks('DeltaKickRF-RB', float(dkicks))
            self.run_callbacks('DeltaKickRF-Mon', float(dkicks))

    def _apply_corr(self, code):
        nr_ch = self._csorb.nr_ch
        if self._dtheta is None:
            msg = 'Err: All kicks are zero.'
            self._update_log(msg)
            _log.warning(msg[6:])
            return
        dkicks = self._dtheta.copy()
        if code == self._csorb.ApplyDelta.CH:
            dkicks[nr_ch:] = 0
        elif code == self._csorb.ApplyDelta.CV:
            dkicks[:nr_ch] = 0
            if self.acc == 'SI':
                dkicks[-1] = 0
        elif self.acc == 'SI' and code == self._csorb.ApplyDelta.RF:
            dkicks[:-1] = 0
        msg = 'Applying {0:s} kicks.'.format(
                        self._csorb.ApplyDelta._fields[code])
        self._update_log(msg)
        _log.info(msg)
        kicks = self._process_kicks(self._ref_corr_kicks, dkicks)
        if kicks is None:
            return
        ret = self.correctors.apply_kicks(kicks)
        if ret is None:
            msg = 'ERR: There is some problem with a corrector!'
            self._update_log(msg)
            _log.error(msg[:5])
        elif ret == -1:
            msg = 'WARN: Last was not applied yet'
            self._update_log(msg)
            _log.error(msg[:5])
        elif ret == 0:
            msg = 'kicks applied!'
            self._update_log(msg)
            _log.info(msg)
        else:
            msg = f'WARN: {ret:03d} kicks were not applied previously!'
            self._update_log(msg)
            _log.warning(msg[:6])

    def _stop_meas_respmat(self):
        if not self._measuring_respmat:
            msg = 'ERR: No Measurement ocurring.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        msg = 'Aborting measurement. Wait...'
        self._update_log(msg)
        _log.info(msg)
        self._measuring_respmat = False
        return True

    def _reset_meas_respmat(self):
        if self._measuring_respmat:
            msg = 'Cannot Reset, Measurement in process.'
            self._update_log(msg)
            _log.info(msg)
            return False
        msg = 'Reseting measurement status.'
        self._update_log(msg)
        _log.info(msg)
        self.run_callbacks('MeasRespMat-Mon', self._csorb.MeasRespMatMon.Idle)
        return True

    def _start_meas_respmat(self):
        if self.orbit.mode == self._csorb.SOFBMode.Offline:
            msg = 'ERR: Cannot Meas Respmat in Offline Mode'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if self._measuring_respmat:
            msg = 'ERR: Measurement already in process.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if self._thread and self._thread.is_alive():
            msg = 'ERR: Cannot Measure, Loop is Closed.'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        if not self.havebeam:
            msg = 'ERR: Cannot Measure, We do not have stored beam!'
            self._update_log(msg)
            _log.error(msg[5:])
            return False
        msg = 'Starting RespMat measurement.'
        self._update_log(msg)
        _log.info(msg)
        self._measuring_respmat = True
        self._thread = _Thread(target=self._do_meas_respmat, daemon=True)
        self._thread.start()
        return True

    def _do_meas_respmat(self):
        self.run_callbacks(
            'MeasRespMat-Mon', self._csorb.MeasRespMatMon.Measuring)
        mat = list()
        orig_kicks = self.correctors.get_strength()
        enbllist = self.matrix.corrs_enbllist
        sum_enbld = sum(enbllist)
        j = 1
        nr_corrs = len(orig_kicks)
        orbzero = _np.zeros(len(self.matrix.bpm_enbllist), dtype=float)
        for i in range(nr_corrs):
            if not self._measuring_respmat:
                self.run_callbacks(
                    'MeasRespMat-Mon', self._csorb.MeasRespMatMon.Aborted)
                msg = 'Measurement stopped.'
                self._update_log(msg)
                _log.info(msg)
                for _ in range(i, nr_corrs):
                    mat.append(orbzero)
                break
            if not self.havebeam:
                self.run_callbacks(
                    'MeasRespMat-Mon', self._csorb.MeasRespMatMon.Aborted)
                msg = 'ERR: Cannot Measure, We do not have stored beam!'
                self._update_log(msg)
                _log.info(msg)
                for _ in range(i, nr_corrs):
                    mat.append(orbzero)
                break
            if not enbllist[i]:
                mat.append(orbzero)
                continue
            msg = '{0:d}/{1:d} -> {2:s}'.format(
                j, sum_enbld, self.correctors.corrs[i].name)
            self._update_log(msg)
            _log.info(msg)
            j += 1

            if i < self._csorb.nr_ch:
                delta = self._meas_respmat_kick['ch']
            elif i < self._csorb.nr_ch + self._csorb.nr_cv:
                delta = self._meas_respmat_kick['cv']
            elif i < self._csorb.nr_corrs:
                delta = self._meas_respmat_kick['rf']

            kicks = _np.array([None, ] * nr_corrs, dtype=float)
            kicks[i] = orig_kicks[i] + delta/2
            self.correctors.apply_kicks(kicks)
            _sleep(self._meas_respmat_wait)
            orbp = self.orbit.get_orbit(reset=True)

            kicks[i] = orig_kicks[i] - delta/2
            self.correctors.apply_kicks(kicks)
            _sleep(self._meas_respmat_wait)
            orbn = self.orbit.get_orbit(reset=True)
            mat.append((orbp-orbn)/delta)

            kicks[i] = orig_kicks[i]
            self.correctors.apply_kicks(kicks)

        mat = _np.array(mat).T
        self.matrix.set_respmat(list(mat.ravel()))
        self.run_callbacks(
            'MeasRespMat-Mon', self._csorb.MeasRespMatMon.Completed)
        self._measuring_respmat = False
        msg = 'RespMat Measurement Completed!'
        self._update_log(msg)
        _log.info(msg)

    def _do_auto_corr(self):
        self.run_callbacks('ClosedLoop-Sts', 1)
        times, rets = [], []
        count = 0
        bpmsfreq = self._csorb.BPMsFreq
        while self._auto_corr == self._csorb.ClosedLoop.On:
            if not self.havebeam:
                msg = 'ERR: Cannot Correct, We do not have stored beam!'
                self._update_log(msg)
                _log.info(msg)
                break
            if count >= 100:
                _Thread(
                    target=self._print_auto_corr_info,
                    args=(times, rets), daemon=True).start()
                times, rets = [], []
                count = 0
            count += 1
            tims = []

            interval = 1/self._auto_corr_freq
            use_pssofb = self.correctors.use_pssofb
            norbs = 1
            if use_pssofb:
                norbs = max(int(bpmsfreq*interval), 1)

            tims.append(_time())
            orb = self.orbit.get_orbit(synced=True)
            for i in range(1, norbs):
                interval = 1/self._auto_corr_freq
                norbs = max(int(bpmsfreq/interval), 1)
                if i >= norbs:
                    break
                orb = self.orbit.get_orbit(synced=True)

            tims.append(_time())
            dkicks = self.matrix.calc_kicks(orb)
            tims.append(_time())

            self._ref_corr_kicks = self.correctors.get_strength()
            tims.append(_time())

            kicks = self._process_kicks(self._ref_corr_kicks, dkicks)
            tims.append(_time())
            if kicks is None:
                self._auto_corr = self._csorb.ClosedLoop.Off
                self.run_callbacks('ClosedLoop-Sel', 0)
                break

            ret = self.correctors.apply_kicks(kicks)
            rets.append(ret)
            tims.append(_time())
            tims.append(tims[1])  # to compute total time - get_orbit
            times.append(tims)
            if ret == -2:
                self._auto_corr = self._csorb.ClosedLoop.Off
                msg = 'ERR: Problem with Corrector!'
                self._update_log(msg)
                _log.error(msg[5:])
                self.run_callbacks('ClosedLoop-Sel', 0)
                break
            elif ret == -1:
                # means that correctors are not ready yet
                # skip this iteration
                continue

            dtime = tims[0] - tims[-1]
            dtime += interval
            if not use_pssofb and dtime > 0:
                _sleep(dtime)
        msg = 'Loop opened!'
        self._update_log(msg)
        _log.info(msg)
        self.run_callbacks('ClosedLoop-Sts', 0)

    def _print_auto_corr_info(self, times, rets):
        """."""
        rets = _np.array(rets)
        ok_ = _np.sum(rets == 0)
        tout = _np.sum(rets == -1)
        diff = _np.sum(rets > 0)
        _log.info('PERFORMANCE:')
        _log.info(f'  # iterations = {rets.size:03d}')
        _log.info(f'  # Ok = {ok_:03d}')
        _log.info(f'  # Timeout = {tout:03d}')
        _log.info(f'  # Diff = {diff:03d}')

        dtimes = _np.diff(times, axis=1).T * 1000
        dtimes[-1] *= -1
        max_ = dtimes.max(axis=1)
        min_ = dtimes.min(axis=1)
        avg_ = dtimes.mean(axis=1)
        std_ = dtimes.std(axis=1)
        msg = '{:s}: geto={:7.2f}, calc={:7.2f}, getk={:7.2f}, proc={:7.2f}, '
        msg += 'apply={:7.2f}, tot={:7.2f}'
        _log.info('TIME:')
        _log.info(msg.format('  MAX', *max_))
        _log.info(msg.format('  MIN', *min_))
        _log.info(msg.format('  AVG', *avg_))
        _log.info(msg.format('  STD', *std_))

    def _calc_correction(self):
        msg = 'Getting the orbit.'
        self._update_log(msg)
        _log.info(msg)
        orb = self.orbit.get_orbit()
        msg = 'Calculating kicks.'
        self._update_log(msg)
        _log.info(msg)
        self._ref_corr_kicks = self.correctors.get_strength()
        dkicks = self.matrix.calc_kicks(orb)
        if dkicks is not None:
            self._dtheta = dkicks
        msg = 'Kicks calculated!'
        self._update_log(msg)
        _log.info(msg)

    def _process_kicks(self, kicks, dkicks):
        if dkicks is None:
            return None

        # keep track of which dkicks were originally different from zero:
        newkicks = _np.full(dkicks.shape, _np.nan, dtype=float)
        apply_idcs = ~_compare_kicks(dkicks, 0)
        if not apply_idcs.any():
            return newkicks

        nr_ch = self._csorb.nr_ch
        slcs = {'ch': slice(None, nr_ch), 'cv': slice(nr_ch, None)}
        if self.acc == 'SI':
            slcs = {
                'ch': slice(None, nr_ch),
                'cv': slice(nr_ch, -1),
                'rf': slice(-1, None)}
        for pln in sorted(slcs.keys()):
            slc = slcs[pln]
            idcs_pln = apply_idcs[slc]
            if not idcs_pln.any():
                continue
            dk_slc = dkicks[slc][idcs_pln]
            k_slc = kicks[slc][idcs_pln]
            dk_slc *= self._corr_factor[pln]

            # Check if any kick is larger than the maximum allowed:
            ind = (_np.abs(k_slc) > self._max_kick[pln]).nonzero()[0]
            if ind.size:
                msg = 'ERR: Kicks above MaxKick{0:s}.'.format(pln.upper())
                self._update_log(msg)
                _log.error(msg[5:])
                return None

            # Check if any delta kick is larger the maximum allowed
            max_delta_kick = _np.max(_np.abs(dk_slc))
            factor1 = 1.0
            if max_delta_kick > self._max_delta_kick[pln]:
                factor1 = self._max_delta_kick[pln]/max_delta_kick
                dk_slc *= factor1
                percent = self._corr_factor[pln] * factor1 * 100
                msg = 'WARN: reach MaxDeltaKick{0:s}. Using {1:5.2f}%'.format(
                    pln.upper(), percent)
                self._update_log(msg)
                _log.warning(msg[6:])

            # Check if any kick + delta kick is larger than the maximum allowed
            max_kick = _np.max(_np.abs(k_slc + dk_slc))
            factor2 = 1.0
            if max_kick > self._max_kick[pln]:
                que = _np.ones((2, k_slc.size), dtype=float)
                # perform the modulus inequality:
                que[0, :] = (-self._max_kick[pln] - k_slc) / dk_slc
                que[1, :] = (self._max_kick[pln] - k_slc) / dk_slc
                # since we know that any initial kick is lesser than max_kick
                # from the previous comparison, at this point each column of Q
                # has a positive and a negative value. We must consider only
                # the positive one and take the minimum value along the columns
                # to be the multiplicative factor:
                que = _np.max(que, axis=0)
                factor2 = min(_np.min(que), 1.0)
                dk_slc *= factor2
                percent = self._corr_factor[pln] * factor1 * factor2 * 100
                msg = 'WARN: reach MaxKick{0:s}. Using {1:5.2f}%'.format(
                    pln.upper(), percent)
                self._update_log(msg)
                _log.warning(msg[6:])

            dkicks[slc][idcs_pln] = dk_slc

        newkicks[apply_idcs] = kicks[apply_idcs] + dkicks[apply_idcs]
        return newkicks
