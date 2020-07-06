"""Insertion Device Control System epics database functions."""

from mathphys.functions import get_namedtuple as _get_namedtuple


class ETypes:
    """Enumerate types."""

    DSBL_ENBL = ('Dsbl', 'Enbl')
    DSBLD_ENBLD = ('Dsbld', 'Enbld')
    OFF_ON = ('Off', 'On')
    CLOSE_OPEN = ('Closed', 'Open')
    DISCONN_CONN = ('Disconnected', 'Connected')
    FIXED_INCR = ('Incr', 'Fixed')
    NORM_INV = ('Normal', 'Inverse')
    UNLINK_LINK = ('Unlink', 'Link')


_et = ETypes  # syntactic sugar


# --- Const class ---


class Const:
    """Const class defining power supply constants."""

    DsblEnbl = _get_namedtuple('DsblEnbl', _et.DSBL_ENBL)
    OffOn = _get_namedtuple('OffOn', _et.OFF_ON)
    CloseOpen = _get_namedtuple('CloseOpen', _et.CLOSE_OPEN)
    DisconnConn = _get_namedtuple('DisconnConn', _et.DISCONN_CONN)

    @staticmethod
    def register(name, field_names, values=None):
        """Register namedtuple."""
        return _get_namedtuple(name, field_names, values)


def get_id_apu_propty_database():
    """Return APU ID database."""
    dbase = {
        'FFWDClosedLoop-Sel': {
            'type': 'enum', 'enums': self.ClosedLoop._fields, 'value': 0},
        'FFWDClosedLoop-Sts': {
            'type': 'enum', 'enums': self.ClosedLoop._fields, 'value': 0},
        'FFWDClosedLoopFreq-SP': {
            'type': 'float', 'value': 1, 'unit': 'Hz', 'prec': 3,
            'lolim': 1e-3, 'hilim': 20},
        'FFWDClosedLoopFreq-RB': {
            'type': 'float', 'value': 1, 'prec': 2, 'unit': 'Hz'},
        }
    return dbase
