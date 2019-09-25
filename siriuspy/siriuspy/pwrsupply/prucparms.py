"""Model abstract factory."""

from siriuspy.pwrsupply.bsmp import PSBSMPFactory as _PSBSMPFactory
from siriuspy.pwrsupply.pru import Const as _PRUConst
from siriuspy.pwrsupply.psmodel import PSModelFactory as _PSModelFactory


class _PRUCParms:
    """PRUC parameters.

    Namespace to group useful parameters used by PRUController.
    """

    # group ids
    ALL = 0
    READONLY = 1
    WRITEABLE = 2
    ALLRELEVANT = 3
    SYNCOFF = 4
    MIRROR = 5

    SLOWREF = SYNCOFF
    MIGWFM = MIRROR
    CYCLE = SYNCOFF
    RMPWFM = MIRROR

    PRU = _PRUConst


class PRUCParmsFBP(_PRUCParms):
    """FBP-specific PRUC parameters."""

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FBP')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FBP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_TEMP_SWITCHES,
        ConstBSMP.V_DUTY_CYCLE,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FBP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_TEMP_SWITCHES,)
    groups[_PRUCParms.MIRROR] = (
        # --- mirror variables ---
        ConstBSMP.V_PS_STATUS_1,
        ConstBSMP.V_PS_STATUS_2,
        ConstBSMP.V_PS_STATUS_3,
        ConstBSMP.V_PS_STATUS_4,
        ConstBSMP.V_PS_SETPOINT_1,
        ConstBSMP.V_PS_SETPOINT_2,
        ConstBSMP.V_PS_SETPOINT_3,
        ConstBSMP.V_PS_SETPOINT_4,
        ConstBSMP.V_PS_REFERENCE_1,
        ConstBSMP.V_PS_REFERENCE_2,
        ConstBSMP.V_PS_REFERENCE_3,
        ConstBSMP.V_PS_REFERENCE_4,
        ConstBSMP.V_PS_SOFT_INTERLOCKS_1,
        ConstBSMP.V_PS_SOFT_INTERLOCKS_2,
        ConstBSMP.V_PS_SOFT_INTERLOCKS_3,
        ConstBSMP.V_PS_SOFT_INTERLOCKS_4,
        ConstBSMP.V_PS_HARD_INTERLOCKS_1,
        ConstBSMP.V_PS_HARD_INTERLOCKS_2,
        ConstBSMP.V_PS_HARD_INTERLOCKS_3,
        ConstBSMP.V_PS_HARD_INTERLOCKS_4,
        ConstBSMP.V_I_LOAD_1,
        ConstBSMP.V_I_LOAD_2,
        ConstBSMP.V_I_LOAD_3,
        ConstBSMP.V_I_LOAD_4,)


class PRUCParmsFBP_DCLink(_PRUCParms):
    """FBP_DCLink-specific PRUC parameters."""

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 2.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FBP_DCLink')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        # ConstBSMP.V_SIGGEN_ENABLE,
        # ConstBSMP.V_SIGGEN_TYPE,
        # ConstBSMP.V_SIGGEN_NUM_CYCLES,
        # ConstBSMP.V_SIGGEN_N,
        # ConstBSMP.V_SIGGEN_FREQ,
        # ConstBSMP.V_SIGGEN_AMPLITUDE,
        # ConstBSMP.V_SIGGEN_OFFSET,
        # ConstBSMP.V_SIGGEN_AUX_PARAM,
        # --- FBP_DCLink variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_MODULES_STATUS,
        ConstBSMP.V_V_OUT,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_OUT_3,
        ConstBSMP.V_DIG_POT_TAP,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        # ConstBSMP.V_SIGGEN_ENABLE,
        # ConstBSMP.V_SIGGEN_TYPE,
        # ConstBSMP.V_SIGGEN_NUM_CYCLES,
        # ConstBSMP.V_SIGGEN_N,
        # ConstBSMP.V_SIGGEN_FREQ,
        # ConstBSMP.V_SIGGEN_AMPLITUDE,
        # ConstBSMP.V_SIGGEN_OFFSET,
        # ConstBSMP.V_SIGGEN_AUX_PARAM,
        # --- FBP_DCLink variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_MODULES_STATUS,
        ConstBSMP.V_V_OUT,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_OUT_3,
        ConstBSMP.V_DIG_POT_TAP,)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAC_2S_DCDC(_PRUCParms):
    """FAC_2S specific PRUC parameters.

    Represent FAC_2S_DCDC psmodels.
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2S_DCDC')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC_2S_DCDC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_CAPBANK_1,
        ConstBSMP.V_V_CAPBANK_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_I_INPUT_IIB_1,
        ConstBSMP.V_I_OUTPUT_IIB_1,
        ConstBSMP.V_V_INPUT_IIB_1,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_1,
        ConstBSMP.V_TEMP_HEATSINK_IIB_1,
        ConstBSMP.V_DRIVER_ERROR_1_IIB_1,
        ConstBSMP.V_DRIVER_ERROR_2_IIB_1,
        ConstBSMP.V_I_INPUT_IIB_2,
        ConstBSMP.V_I_OUTPUT_IIB_2,
        ConstBSMP.V_V_INPUT_IIB_2,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_2,
        ConstBSMP.V_TEMP_HEATSINK_IIB_2,
        ConstBSMP.V_DRIVER_ERROR_1_IIB_2,
        ConstBSMP.V_DRIVER_ERROR_2_IIB_2,
        ConstBSMP.V_IIB_INTERLOCKS_1,
        ConstBSMP.V_IIB_INTERLOCKS_2)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC_2S_DCDC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_CAPBANK_1,
        ConstBSMP.V_V_CAPBANK_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_I_INPUT_IIB_1,
        ConstBSMP.V_I_OUTPUT_IIB_1,
        ConstBSMP.V_V_INPUT_IIB_1,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_1,
        ConstBSMP.V_TEMP_HEATSINK_IIB_1,
        ConstBSMP.V_DRIVER_ERROR_1_IIB_1,
        ConstBSMP.V_DRIVER_ERROR_2_IIB_1,
        ConstBSMP.V_I_INPUT_IIB_2,
        ConstBSMP.V_I_OUTPUT_IIB_2,
        ConstBSMP.V_V_INPUT_IIB_2,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_2,
        ConstBSMP.V_TEMP_HEATSINK_IIB_2,
        ConstBSMP.V_DRIVER_ERROR_1_IIB_2,
        ConstBSMP.V_DRIVER_ERROR_2_IIB_2,
        ConstBSMP.V_IIB_INTERLOCKS_1,
        ConstBSMP.V_IIB_INTERLOCKS_2)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAC_2P4S_DCDC(_PRUCParms):
    """FAC-specific PRUC parameters.

    Represent FAC_2P4S psmodels.
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2P4S_DCDC')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_I_ARM_1,
        ConstBSMP.V_I_ARM_2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_CAPBANK_1,
        ConstBSMP.V_V_CAPBANK_2,
        ConstBSMP.V_V_CAPBANK_3,
        ConstBSMP.V_V_CAPBANK_4,
        ConstBSMP.V_V_CAPBANK_5,
        ConstBSMP.V_V_CAPBANK_6,
        ConstBSMP.V_V_CAPBANK_7,
        ConstBSMP.V_V_CAPBANK_8,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_OUT_3,
        ConstBSMP.V_V_OUT_4,
        ConstBSMP.V_V_OUT_5,
        ConstBSMP.V_V_OUT_6,
        ConstBSMP.V_V_OUT_7,
        ConstBSMP.V_V_OUT_8,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_CYCLE_3,
        ConstBSMP.V_DUTY_CYCLE_4,
        ConstBSMP.V_DUTY_CYCLE_5,
        ConstBSMP.V_DUTY_CYCLE_6,
        ConstBSMP.V_DUTY_CYCLE_7,
        ConstBSMP.V_DUTY_CYCLE_8)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_I_ARM_1,
        ConstBSMP.V_I_ARM_2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_CAPBANK_1,
        ConstBSMP.V_V_CAPBANK_2,
        ConstBSMP.V_V_CAPBANK_3,
        ConstBSMP.V_V_CAPBANK_4,
        ConstBSMP.V_V_CAPBANK_5,
        ConstBSMP.V_V_CAPBANK_6,
        ConstBSMP.V_V_CAPBANK_7,
        ConstBSMP.V_V_CAPBANK_8,
        ConstBSMP.V_V_OUT_1,
        ConstBSMP.V_V_OUT_2,
        ConstBSMP.V_V_OUT_3,
        ConstBSMP.V_V_OUT_4,
        ConstBSMP.V_V_OUT_5,
        ConstBSMP.V_V_OUT_6,
        ConstBSMP.V_V_OUT_7,
        ConstBSMP.V_V_OUT_8,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_CYCLE_3,
        ConstBSMP.V_DUTY_CYCLE_4,
        ConstBSMP.V_DUTY_CYCLE_5,
        ConstBSMP.V_DUTY_CYCLE_6,
        ConstBSMP.V_DUTY_CYCLE_7,
        ConstBSMP.V_DUTY_CYCLE_8)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAC_DCDC(_PRUCParms):
    """FAC-specific PRUC parameters.

    Represent FAC, FAC_2S, FAC_2P4S psmodels.
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_DCDC')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_CAPBANK,
        ConstBSMP.V_TEMP_INDUCTORS,
        ConstBSMP.V_TEMP_IGBTS,
        ConstBSMP.V_DUTY_CYCLE,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_LOAD,
        ConstBSMP.V_V_CAPBANK,
        ConstBSMP.V_TEMP_INDUCTORS,
        ConstBSMP.V_TEMP_IGBTS,
        ConstBSMP.V_DUTY_CYCLE,)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAC_2S_ACDC(_PRUCParms):
    """FAC_2S_ACDC-specific PRUC parameters."""

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 2.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAC_2S_ACDC')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        # ConstBSMP.V_SIGGEN_ENABLE,
        # ConstBSMP.V_SIGGEN_TYPE,
        # ConstBSMP.V_SIGGEN_NUM_CYCLES,
        # ConstBSMP.V_SIGGEN_N,
        # ConstBSMP.V_SIGGEN_FREQ,
        # ConstBSMP.V_SIGGEN_AMPLITUDE,
        # ConstBSMP.V_SIGGEN_OFFSET,
        # ConstBSMP.V_SIGGEN_AUX_PARAM,
        # ConstBSMP.V_WFMREF_SELECTED,
        # ConstBSMP.V_WFMREF_SYNC_MODE,
        # ConstBSMP.V_WFMREF_GAIN,
        # ConstBSMP.V_WFMREF_OFFSET,
        # ConstBSMP.V_WFMREF0_START,
        # ConstBSMP.V_WFMREF0_END,
        # ConstBSMP.V_WFMREF0_IDX,
        # ConstBSMP.V_WFMREF1_START,
        # ConstBSMP.V_WFMREF1_END,
        # ConstBSMP.V_WFMREF1_IDX,
        # --- FAC_2S_ACDC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_V_CAPBANK,
        ConstBSMP.V_V_OUT_RECTIFIER,
        ConstBSMP.V_I_OUT_RECTIFIER,
        ConstBSMP.V_TEMP_HEATSINK,
        ConstBSMP.V_TEMP_INDUCTORS,
        ConstBSMP.V_DUTY_CYCLE,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        # ConstBSMP.V_SIGGEN_ENABLE,
        # ConstBSMP.V_SIGGEN_TYPE,
        # ConstBSMP.V_SIGGEN_NUM_CYCLES,
        # ConstBSMP.V_SIGGEN_N,
        # ConstBSMP.V_SIGGEN_FREQ,
        # ConstBSMP.V_SIGGEN_AMPLITUDE,
        # ConstBSMP.V_SIGGEN_OFFSET,
        # ConstBSMP.V_SIGGEN_AUX_PARAM,
        # ConstBSMP.V_WFMREF_SELECTED,
        # ConstBSMP.V_WFMREF_SYNC_MODE,
        # ConstBSMP.V_WFMREF_GAIN,
        # ConstBSMP.V_WFMREF_OFFSET,
        # ConstBSMP.V_WFMREF0_START,
        # ConstBSMP.V_WFMREF0_END,
        # ConstBSMP.V_WFMREF0_IDX,
        # ConstBSMP.V_WFMREF1_START,
        # ConstBSMP.V_WFMREF1_END,
        # ConstBSMP.V_WFMREF1_IDX,
        # --- FAC_2S_ACDC variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_V_CAPBANK,
        ConstBSMP.V_V_OUT_RECTIFIER,
        ConstBSMP.V_I_OUT_RECTIFIER,
        ConstBSMP.V_TEMP_HEATSINK,
        ConstBSMP.V_TEMP_INDUCTORS,
        ConstBSMP.V_DUTY_CYCLE,)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAC_2P4S_ACDC(PRUCParmsFAC_2S_ACDC):
    """FAC_2P4S_ACDC-specific PRUC parameters."""

    # PS model parms
    model = _PSModelFactory.create('FAC_2P4S_ACDC')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities


class PRUCParmsFAP(_PRUCParms):
    """FAC-specific PRUC parameters.

    Represent FAP
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_I_IGBT_1,
        ConstBSMP.V_I_IGBT_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_V_INPUT_IIB,
        ConstBSMP.V_V_OUTPUT_IIB,
        ConstBSMP.V_I_IGBT_1_IIB,
        ConstBSMP.V_I_IGBT_2_IIB,
        ConstBSMP.V_TEMP_IGBT_1_IIB,
        ConstBSMP.V_TEMP_IGBT_2_IIB,
        ConstBSMP.V_V_DRIVER_IIB,
        ConstBSMP.V_I_DRIVER_1_IIB,
        ConstBSMP.V_I_DRIVER_2_IIB,
        ConstBSMP.V_TEMP_INDUCTOR_IIB,
        ConstBSMP.V_TEMP_HEATSINK_IIB,
        ConstBSMP.V_IIB_INTERLOCKS,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_I_IGBT_1,
        ConstBSMP.V_I_IGBT_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_V_INPUT_IIB,
        ConstBSMP.V_V_OUTPUT_IIB,
        ConstBSMP.V_I_IGBT_1_IIB,
        ConstBSMP.V_I_IGBT_2_IIB,
        ConstBSMP.V_TEMP_IGBT_1_IIB,
        ConstBSMP.V_TEMP_IGBT_2_IIB,
        ConstBSMP.V_V_DRIVER_IIB,
        ConstBSMP.V_I_DRIVER_1_IIB,
        ConstBSMP.V_I_DRIVER_2_IIB,
        ConstBSMP.V_TEMP_INDUCTOR_IIB,
        ConstBSMP.V_TEMP_HEATSINK_IIB,
        ConstBSMP.V_IIB_INTERLOCKS,)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAP_4P(_PRUCParms):
    """FAC-specific PRUC parameters.

    Represent FAP_4P
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP_4P')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups useful for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_I_IGBT_1,
        ConstBSMP.V_I_IGBT_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_V_INPUT_IIB,
        ConstBSMP.V_V_OUTPUT_IIB,
        ConstBSMP.V_I_IGBT_1_IIB,
        ConstBSMP.V_I_IGBT_2_IIB,
        ConstBSMP.V_TEMP_IGBT_1_IIB,
        ConstBSMP.V_TEMP_IGBT_2_IIB,
        ConstBSMP.V_V_DRIVER_IIB,
        ConstBSMP.V_I_DRIVER_1_IIB,
        ConstBSMP.V_I_DRIVER_2_IIB,
        ConstBSMP.V_TEMP_INDUCTOR_IIB,
        ConstBSMP.V_TEMP_HEATSINK_IIB,
        ConstBSMP.V_IIB_INTERLOCKS,)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        # --- FAP variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_V_DCLINK,
        ConstBSMP.V_I_IGBT_1,
        ConstBSMP.V_I_IGBT_2,
        ConstBSMP.V_DUTY_CYCLE_1,
        ConstBSMP.V_DUTY_CYCLE_2,
        ConstBSMP.V_DUTY_DIFF,
        ConstBSMP.V_V_INPUT_IIB,
        ConstBSMP.V_V_OUTPUT_IIB,
        ConstBSMP.V_I_IGBT_1_IIB,
        ConstBSMP.V_I_IGBT_2_IIB,
        ConstBSMP.V_TEMP_IGBT_1_IIB,
        ConstBSMP.V_TEMP_IGBT_2_IIB,
        ConstBSMP.V_V_DRIVER_IIB,
        ConstBSMP.V_I_DRIVER_1_IIB,
        ConstBSMP.V_I_DRIVER_2_IIB,
        ConstBSMP.V_TEMP_INDUCTOR_IIB,
        ConstBSMP.V_TEMP_HEATSINK_IIB,
        ConstBSMP.V_IIB_INTERLOCKS,)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]


class PRUCParmsFAP_2P2S(_PRUCParms):
    """FAC_2P2S-specific PRUC parameters.

    Represent FAP_2P2S
    """

    FREQ_RAMP = 2.0  # [Hz]
    FREQ_SCAN = 10.0  # [Hz]

    # PS model parms
    model = _PSModelFactory.create('FAP_2P2S')
    ConstBSMP = model.bsmp_constants
    Entities = model.entities

    groups = dict()
    # reserved variable groups (not to be used)
    groups[_PRUCParms.ALL] = tuple(sorted(Entities.list_variables(0)))
    groups[_PRUCParms.READONLY] = tuple(sorted(Entities.list_variables(1)))
    groups[_PRUCParms.WRITEABLE] = tuple(sorted(Entities.list_variables(2)))
    # new variable groups usefull for PRUController.
    groups[_PRUCParms.ALLRELEVANT] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAP_2P2S variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_I_ARM_1,
        ConstBSMP.V_I_ARM_2,
        ConstBSMP.V_I_IGBT_1_1,
        ConstBSMP.V_I_IGBT_2_1,
        ConstBSMP.V_I_IGBT_1_2,
        ConstBSMP.V_I_IGBT_2_2,
        ConstBSMP.V_I_IGBT_1_3,
        ConstBSMP.V_I_IGBT_2_3,
        ConstBSMP.V_I_IGBT_1_4,
        ConstBSMP.V_I_IGBT_2_4,
        ConstBSMP.V_V_DCLINK_1,
        ConstBSMP.V_V_DCLINK_2,
        ConstBSMP.V_V_DCLINK_3,
        ConstBSMP.V_V_DCLINK_4,
        ConstBSMP.V_DUTY_MEAN,
        ConstBSMP.V_DUTY_ARMS_DIFF,
        ConstBSMP.V_DUTY_CYCLE_1_1,
        ConstBSMP.V_DUTY_CYCLE_2_1,
        ConstBSMP.V_DUTY_CYCLE_1_2,
        ConstBSMP.V_DUTY_CYCLE_2_2,
        ConstBSMP.V_DUTY_CYCLE_1_3,
        ConstBSMP.V_DUTY_CYCLE_2_3,
        ConstBSMP.V_DUTY_CYCLE_1_4,
        ConstBSMP.V_DUTY_CYCLE_2_4,
        ConstBSMP.V_V_INPUT_IIB_1,
        ConstBSMP.V_V_OUTPUT_IIB_1,
        ConstBSMP.V_I_IGBT_1_IIB_1,
        ConstBSMP.V_I_IGBT_2_IIB_1,
        ConstBSMP.V_TEMP_IGBT_1_IIB_1,
        ConstBSMP.V_TEMP_IGBT_2_IIB_1,
        ConstBSMP.V_V_DRIVER_IIB_1,
        ConstBSMP.V_I_DRIVER_1_IIB_1,
        ConstBSMP.V_I_DRIVER_2_IIB_1,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_1,
        ConstBSMP.V_TEMP_HEATSINK_IIB_1,
        ConstBSMP.V_V_INPUT_IIB_2,
        ConstBSMP.V_V_OUTPUT_IIB_2,
        ConstBSMP.V_I_IGBT_1_IIB_2,
        ConstBSMP.V_I_IGBT_2_IIB_2,
        ConstBSMP.V_TEMP_IGBT_1_IIB_2,
        ConstBSMP.V_TEMP_IGBT_2_IIB_2,
        ConstBSMP.V_V_DRIVER_IIB_2,
        ConstBSMP.V_I_DRIVER_1_IIB_2,
        ConstBSMP.V_I_DRIVER_2_IIB_2,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_2,
        ConstBSMP.V_TEMP_HEATSINK_IIB_2,
        ConstBSMP.V_V_INPUT_IIB_3,
        ConstBSMP.V_V_OUTPUT_IIB_3,
        ConstBSMP.V_I_IGBT_1_IIB_3,
        ConstBSMP.V_I_IGBT_2_IIB_3,
        ConstBSMP.V_TEMP_IGBT_1_IIB_3,
        ConstBSMP.V_TEMP_IGBT_2_IIB_3,
        ConstBSMP.V_V_DRIVER_IIB_3,
        ConstBSMP.V_I_DRIVER_1_IIB_3,
        ConstBSMP.V_I_DRIVER_2_IIB_3,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_3,
        ConstBSMP.V_TEMP_HEATSINK_IIB_3,
        ConstBSMP.V_V_INPUT_IIB_4,
        ConstBSMP.V_V_OUTPUT_IIB_4,
        ConstBSMP.V_I_IGBT_1_IIB_4,
        ConstBSMP.V_I_IGBT_2_IIB_4,
        ConstBSMP.V_TEMP_IGBT_1_IIB_4,
        ConstBSMP.V_TEMP_IGBT_2_IIB_4,
        ConstBSMP.V_V_DRIVER_IIB_4,
        ConstBSMP.V_I_DRIVER_1_IIB_4,
        ConstBSMP.V_I_DRIVER_2_IIB_4,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_4,
        ConstBSMP.V_TEMP_HEATSINK_IIB_4,
        ConstBSMP.V_IIB_INTERLOCKS_1,
        ConstBSMP.V_IIB_INTERLOCKS_2,
        ConstBSMP.V_IIB_INTERLOCKS_3,
        ConstBSMP.V_IIB_INTERLOCKS_4,
        ConstBSMP.V_I_MOD_1,
        ConstBSMP.V_I_MOD_2,
        ConstBSMP.V_I_MOD_3,
        ConstBSMP.V_I_MOD_4)
    groups[_PRUCParms.SYNCOFF] = (
        # --- common variables
        ConstBSMP.V_PS_STATUS,
        ConstBSMP.V_PS_SETPOINT,
        ConstBSMP.V_PS_REFERENCE,
        ConstBSMP.V_FIRMWARE_VERSION,
        ConstBSMP.V_COUNTER_SET_SLOWREF,
        ConstBSMP.V_COUNTER_SYNC_PULSE,
        ConstBSMP.V_SIGGEN_ENABLE,
        ConstBSMP.V_SIGGEN_TYPE,
        ConstBSMP.V_SIGGEN_NUM_CYCLES,
        ConstBSMP.V_SIGGEN_N,
        ConstBSMP.V_SIGGEN_FREQ,
        ConstBSMP.V_SIGGEN_AMPLITUDE,
        ConstBSMP.V_SIGGEN_OFFSET,
        ConstBSMP.V_SIGGEN_AUX_PARAM,
        ConstBSMP.V_WFMREF_SELECTED,
        ConstBSMP.V_WFMREF_SYNC_MODE,
        ConstBSMP.V_WFMREF_GAIN,
        ConstBSMP.V_WFMREF_OFFSET,
        ConstBSMP.V_WFMREF0_START,
        ConstBSMP.V_WFMREF0_END,
        ConstBSMP.V_WFMREF0_IDX,
        ConstBSMP.V_WFMREF1_START,
        ConstBSMP.V_WFMREF1_END,
        ConstBSMP.V_WFMREF1_IDX,
        # --- FAP_2P2S variables ---
        ConstBSMP.V_PS_SOFT_INTERLOCKS,
        ConstBSMP.V_PS_HARD_INTERLOCKS,
        ConstBSMP.V_I_LOAD_MEAN,
        ConstBSMP.V_I_LOAD1,
        ConstBSMP.V_I_LOAD2,
        ConstBSMP.V_I_ARM_1,
        ConstBSMP.V_I_ARM_2,
        ConstBSMP.V_I_IGBT_1_1,
        ConstBSMP.V_I_IGBT_2_1,
        ConstBSMP.V_I_IGBT_1_2,
        ConstBSMP.V_I_IGBT_2_2,
        ConstBSMP.V_I_IGBT_1_3,
        ConstBSMP.V_I_IGBT_2_3,
        ConstBSMP.V_I_IGBT_1_4,
        ConstBSMP.V_I_IGBT_2_4,
        ConstBSMP.V_V_DCLINK_1,
        ConstBSMP.V_V_DCLINK_2,
        ConstBSMP.V_V_DCLINK_3,
        ConstBSMP.V_V_DCLINK_4,
        ConstBSMP.V_DUTY_MEAN,
        ConstBSMP.V_DUTY_ARMS_DIFF,
        ConstBSMP.V_DUTY_CYCLE_1_1,
        ConstBSMP.V_DUTY_CYCLE_2_1,
        ConstBSMP.V_DUTY_CYCLE_1_2,
        ConstBSMP.V_DUTY_CYCLE_2_2,
        ConstBSMP.V_DUTY_CYCLE_1_3,
        ConstBSMP.V_DUTY_CYCLE_2_3,
        ConstBSMP.V_DUTY_CYCLE_1_4,
        ConstBSMP.V_DUTY_CYCLE_2_4,
        ConstBSMP.V_V_INPUT_IIB_1,
        ConstBSMP.V_V_OUTPUT_IIB_1,
        ConstBSMP.V_I_IGBT_1_IIB_1,
        ConstBSMP.V_I_IGBT_2_IIB_1,
        ConstBSMP.V_TEMP_IGBT_1_IIB_1,
        ConstBSMP.V_TEMP_IGBT_2_IIB_1,
        ConstBSMP.V_V_DRIVER_IIB_1,
        ConstBSMP.V_I_DRIVER_1_IIB_1,
        ConstBSMP.V_I_DRIVER_2_IIB_1,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_1,
        ConstBSMP.V_TEMP_HEATSINK_IIB_1,
        ConstBSMP.V_V_INPUT_IIB_2,
        ConstBSMP.V_V_OUTPUT_IIB_2,
        ConstBSMP.V_I_IGBT_1_IIB_2,
        ConstBSMP.V_I_IGBT_2_IIB_2,
        ConstBSMP.V_TEMP_IGBT_1_IIB_2,
        ConstBSMP.V_TEMP_IGBT_2_IIB_2,
        ConstBSMP.V_V_DRIVER_IIB_2,
        ConstBSMP.V_I_DRIVER_1_IIB_2,
        ConstBSMP.V_I_DRIVER_2_IIB_2,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_2,
        ConstBSMP.V_TEMP_HEATSINK_IIB_2,
        ConstBSMP.V_V_INPUT_IIB_3,
        ConstBSMP.V_V_OUTPUT_IIB_3,
        ConstBSMP.V_I_IGBT_1_IIB_3,
        ConstBSMP.V_I_IGBT_2_IIB_3,
        ConstBSMP.V_TEMP_IGBT_1_IIB_3,
        ConstBSMP.V_TEMP_IGBT_2_IIB_3,
        ConstBSMP.V_V_DRIVER_IIB_3,
        ConstBSMP.V_I_DRIVER_1_IIB_3,
        ConstBSMP.V_I_DRIVER_2_IIB_3,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_3,
        ConstBSMP.V_TEMP_HEATSINK_IIB_3,
        ConstBSMP.V_V_INPUT_IIB_4,
        ConstBSMP.V_V_OUTPUT_IIB_4,
        ConstBSMP.V_I_IGBT_1_IIB_4,
        ConstBSMP.V_I_IGBT_2_IIB_4,
        ConstBSMP.V_TEMP_IGBT_1_IIB_4,
        ConstBSMP.V_TEMP_IGBT_2_IIB_4,
        ConstBSMP.V_V_DRIVER_IIB_4,
        ConstBSMP.V_I_DRIVER_1_IIB_4,
        ConstBSMP.V_I_DRIVER_2_IIB_4,
        ConstBSMP.V_TEMP_INDUCTOR_IIB_4,
        ConstBSMP.V_TEMP_HEATSINK_IIB_4,
        ConstBSMP.V_IIB_INTERLOCKS_1,
        ConstBSMP.V_IIB_INTERLOCKS_2,
        ConstBSMP.V_IIB_INTERLOCKS_3,
        ConstBSMP.V_IIB_INTERLOCKS_4,
        ConstBSMP.V_I_MOD_1,
        ConstBSMP.V_I_MOD_2,
        ConstBSMP.V_I_MOD_3,
        ConstBSMP.V_I_MOD_4)
    groups[_PRUCParms.MIRROR] = groups[_PRUCParms.SYNCOFF]
