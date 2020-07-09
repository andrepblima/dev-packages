#!/usr/bin/env python-sirius
"""."""

import sys as _sys
import time as _time

import numpy as _np
import matplotlib.pyplot as _plt
import matplotlib.gridspec as _mgs

import epics as _epics

from PRUserial485 import EthBrigdeClient

from siriuspy.pwrsupply.pssofb import PSSOFB


NRPTS = 5000


def benchmark_bsmp_sofb_current_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    for i, _ in enumerate(exectimes):
        time0 = _time.time()
        pssofb.bsmp_sofb_current_update()
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)
    for exectime in exectimes:
        print(exectime)

    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # read from power supplies
        pssofb.bsmp_sofb_current_update()

        # comparison
        issame = True

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_current_setpoint():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    curr_sp = 0.1 * _np.random.randn(280)
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        pssofb.bsmp_sofb_current_setpoint(curr_sp)

        # comparison
        issame = True

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_current_setpoint_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS
    curr_sp = 0.1 * _np.random.randn(280)
    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        pssofb.bsmp_sofb_current_setpoint_update(curr_sp)

        # read from power supplies
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_current_setpoint_then_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    curr_refmon = pssofb.sofb_current_refmon

    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set current values
        curr_sp = curr_refmon + 1 * 0.005 * _np.random.randn(len(curr_refmon))
        pssofb.bsmp_sofb_current_set(curr_sp)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_current_set(curr_refmon)

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_kick_setpoint():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon

    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set kick values
        kick_sp = kick_refmon + 0 * 0.01 * _np.random.randn(len(kick_refmon))
        pssofb.bsmp_sofb_kick_set(kick_sp)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_kick_setpoint_then_update():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowref()
    exectimes = [0] * NRPTS

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon.copy()

    for i, _ in enumerate(exectimes):

        # start clock
        time0 = _time.time()

        # set kick values
        kick_sp = kick_refmon + 0 * 0.01 * _np.random.randn(len(kick_refmon))
        curr_sp = pssofb.bsmp_sofb_kick_set(kick_sp)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_rb

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    for exectime in exectimes:
        print(exectime)


def benchmark_bsmp_sofb_kick_setpoint_delay(delay_before, delay_after):
    """."""
    trigger = _epics.PV('AS-RaMO:TI-EVG:OrbSIExtTrig-Cmd')
    trigger.wait_for_connection()

    pssofb = PSSOFB(EthBrigdeClient)
    pssofb.bsmp_slowrefsync()

    exectimes = [0] * 150

    pssofb.bsmp_sofb_update()
    kick_refmon = pssofb.sofb_kick_refmon

    for i, _ in enumerate(exectimes):

        # calc new kick
        kick_sp = kick_refmon + 1 * 0.01 * _np.random.randn(len(kick_refmon))

        # start clock
        time0 = _time.time()

        # set kick values
        curr_sp = pssofb.bsmp_sofb_kick_set(kick_sp)

        # sleep for a while
        _time.sleep(delay_before)

        # send trigger
        trigger.value = 1

        # stop clock
        time1 = _time.time()
        exectimes[i] = 1000*(time1 - time0)

        # make sure trigger signal gets to power supplies.
        _time.sleep(delay_after)

        # read from power supplies
        pssofb.bsmp_sofb_update()
        curr_rb = pssofb.sofb_current_refmon

        # comparison
        issame = pssofb.sofb_vector_issame(curr_sp, curr_rb)

        if not issame:
            print('SP<>RB in event {}'.format(i))

    # restore state
    pssofb.bsmp_sofb_kick_set(kick_refmon)

    for exectime in exectimes:
        print(exectime)


def bsmp_communication_test():
    """."""
    pssofb = PSSOFB(EthBrigdeClient)
    time0 = _time.time()
    pssofb.bsmp_state_update()
    time1 = _time.time()
    print(1e3*(time1 - time0))

    print('--- hard interlock ---')
    print(pssofb.sofb_interlock_hard)

    print('--- soft interlock ---')
    print(pssofb.sofb_interlock_soft)

    print('--- current_mon ---')
    print(pssofb.sofb_state_variable_get(var_id=26))

    return pssofb


def plot_result_hist(fname, title, cutoff=float('Inf')):
    """."""
    data = _np.loadtxt(fname, skiprows=80)
    data = data[data < cutoff]
    print('selected data size: {}'.format(len(data)))
    avg = data.mean()
    std = data.std()
    minv = data.min()
    maxv = data.max()

    fig = _plt.figure(figsize=(8, 10))
    gs = _mgs.GridSpec(1, 1)
    gs.update(
        left=0.12, right=0.97, top=0.95, bottom=0.10,
        hspace=0.2, wspace=0.25)

    asp = _plt.subplot(gs[0, 0])
    asp.hist(data, bins=100)

    stg = f'avg = {avg:05.1f} ms\n'
    stg += f'std = {std:05.1f} ms\n'
    stg += f'min = {minv:05.1f} ms\n'
    stg += f'max = {maxv:05.1f} ms'
    asp.text(
        0.8, 0.8, stg, horizontalalignment='center',
        fontsize='xx-small',
        verticalalignment='center', transform=asp.transAxes,
        bbox=dict(edgecolor='k', facecolor='w', alpha=1.0))
    asp.set_xlabel('time [ms]')
    asp.set_ylabel('# total apply')
    asp.set_title(title)
    _plt.show()


def plot_result_time(fname, title):
    """."""
    data = _np.loadtxt(fname, skiprows=80)
    _plt.plot(data, '.')
    _plt.xlabel('apply index')
    _plt.ylabel('Time [ms]')
    _plt.title(title)
    _plt.grid()
    _plt.show()


def plot_result_perc(fname, title):
    """."""
    data = sorted(_np.loadtxt(fname, skiprows=80))
    time = _np.linspace(min(data), max(data), 500)
    perc = [100*sum(data <= tim)/len(data) for tim in time]
    _plt.plot(time, perc)
    _plt.xlabel('Execution time [ms]')
    _plt.ylabel('Events bellow a given execution time [%]')
    _plt.title(title)
    _plt.grid()
    _plt.show()


def run():
    """."""
    # benchmark_bsmp_sofb_current_update()
    # benchmark_bsmp_sofb_current_setpoint()
    # benchmark_bsmp_sofb_current_setpoint_update()
    # benchmark_bsmp_sofb_current_setpoint_then_update()
    # benchmark_bsmp_sofb_kick_setpoint()
    benchmark_bsmp_sofb_kick_setpoint_then_update()
    # sleep_trigger_before = float(_sys.argv[1])
    # sleep_trigger_after = float(_sys.argv[2])
    # benchmark_bsmp_sofb_kick_setpoint_delay(
    #     sleep_trigger_before, sleep_trigger_after)
    # test_methods()


if __name__ == '__main__':
    run()
