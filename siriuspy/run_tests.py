#!/usr/bin/env python3

import unittest
import siriuspy as sp

class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.curr_min = 0; self.curr_max = 10.0; self.curr_std = 0.1
        self.c = sp.pwrsupply.ControllerSim(current_min=self.curr_min,
                                            current_max=self.curr_max,
                                            current_std=self.curr_std,
                                            random_seed=131071)

    def test_constructor(self):
        self.assertEqual(self.c.opmode, 0)
        self.assertEqual(self.c.pwrstate, 0)
        self.assertEqual(self.c.reset, 0)
        self.assertEqual(self.c.current_min, self.curr_min)
        self.assertEqual(self.c.current_max, self.curr_max)
        self.assertEqual(self.c.current_sp, 0.0)
        self.assertEqual(self.c.current_ref, 0.0)
        self.assertEqual(self.c.current_load, -0.01262415230153511)
        c1 = self.c.current_load; c2 = self.c.current_load; self.assertEqual(c1, c2)
        self.assertEqual(self.c.wfmramping, False)
        self.assertEqual(self.c.trigger_timeout, False)

    def test_pwrstate_off(self):
        self.c.current_sp = 10.0
        self.assertEqual(self.c.current_sp, 10.0)
        self.assertEqual(self.c.current_ref, 0.0)
        self.assertEqual(self.c.current_load, -0.05711411364691349)

    def test_pwrstate_on(self):
        self.c.current_sp = 10.0
        self.c.pwrstate = 1
        self.assertEqual(self.c.current_sp, 10.0)
        self.assertEqual(self.c.current_ref, 10.0)
        self.assertEqual(self.c.current_load,10.039223131824139)
        self.c.pwrstate = 0
        self.assertEqual(self.c.current_sp, 10.0)
        self.assertEqual(self.c.current_ref, 0.0)
        self.assertEqual(self.c.current_load,0.16835556870840707)

    def test_current_limits(self):
        self.c.pwrstate = 1
        self.c.current_sp = 20.0
        self.assertEqual(self.c.current_sp, 20.0)
        self.assertEqual(self.c.current_ref, self.curr_max)
        self.assertEqual(self.c.current_load, 10.039223131824139)



if __name__ == '__main__':
    unittest.main()
