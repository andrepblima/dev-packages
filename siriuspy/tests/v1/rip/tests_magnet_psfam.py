#!/usr/bin/env python-sirius

"""Test of the MagnetPowerSupply class."""

import unittest
import time
import numpy
from siriuspy.magnet.model import MagnetPowerSupply


class MagnetPowerSupplyFamilyTest(unittest.TestCase):
    """Test MagnetPowerSupply class.

    Test setting the strength.
    Test setting the strength repeatedly.
    Test changing the dipole current.
    TODO:
        Test changing the dipole strength.
        Test setting the current.
    """

    def setUp(self):
        pass

    def mysetUp(self):
        """Execute before every test."""
        self.ma = MagnetPowerSupply(
           "SI-Fam:MA-QDA", use_vaca=True)

        self.ma.opmode_sel = 0
        self.ma.pwrstate_sel = 1

    def tearDown(self):
        """Execute after every test."""
        self.ma.disconnect()

    def test_set_strength_sp(self):
        """Test setting strength set point."""
        self.mysetUp()
        self.ma.strength_sp = -0.40
        self.ma.process_puts(wait=0.2)
        time.sleep(1.2)
        self.assertEqual(-0.4, self.ma.strength_sp)
        self.assertEqual(-0.4, self.ma.strength_rb)
        self.assertEqual(-0.4, self.ma.strengthref_mon)
        self.assertEqual(-0.4, self.ma.strength_mon)

    def test_loop_set_strength(self):
        """Test setting strength set point repeatedly."""
        self.mysetUp()
        currents = numpy.linspace(0, 120.0, 100)
        strengths = [self.ma._strength_obj.conv_current_2_strength(
            current, current_dipole=self.ma._dipole.get("Current-SP"))
            for current in currents]
        for strength in strengths:
            time.sleep(0.01)
            self.ma.strength_sp = strength

        time.sleep(3)
        self.assertAlmostEqual(strengths[-1], self.ma.strength_sp)
        self.assertAlmostEqual(strengths[-1], self.ma.strengthref_mon)
        self.assertAlmostEqual(strengths[-1], self.ma.strength_mon)
        self.assertAlmostEqual(strengths[-1], self.ma.strength_rb)
        self.assertAlmostEqual(currents[-1], self.ma.current_sp)

    def test_change_dipole_current(self):
        """Change dipole current and assert magnet strength is set properly."""
        self.mysetUp()
        time.sleep(0.2)

        expected_strength = self.ma._strength_obj.conv_current_2_strength(
            self.ma.current_sp, current_dipole=400)
        self.ma._dipole.put("Current-SP", 400)
        time.sleep(0.2)

        self.assertEqual(400, self.ma._dipole.get("Current-SP"))
        self.assertEqual(expected_strength, self.ma.strength_sp)
        self.assertEqual(expected_strength, self.ma.strength_rb)
        self.assertEqual(expected_strength, self.ma.strengthref_mon)
        self.assertEqual(expected_strength, self.ma.strength_mon)

    # def test_change_dipole_strength(self):
    #     """Change dipole energy and assert magnet strength is set properly."""
    #     self.mysetUp()
    #     time.sleep(0.2)
    #
    #     self.dipole.strength_sp = 2.0
    #     time.sleep(0.2)
    #
    #     expected_strength = self.ma.conv_current_2_strength(
    #         self.ma.current_sp, current_dipole=self.dipole.get("Current-SP"))
    #     self.assertEqual(2.0, self.dipole.strength_sp)
    #     self.assertEqual(expected_strength, self.ma.strength_sp)
    #     self.assertEqual(expected_strength, self.ma.strength_rb)
    #     self.assertEqual(expected_strength, self.ma.strengthref_mon)
    #     self.assertEqual(expected_strength, self.ma.strength_mon)


if __name__ == "__main__":
    unittest.main()