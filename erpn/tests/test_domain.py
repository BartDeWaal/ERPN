#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

import unittest
from erpn.domain import Reals, Integers
import erpn.domain as domain


class TestDomain(unittest.TestCase):
    def test_base_object(self):
        self.assertTrue(8.1 in Reals)
        self.assertTrue(8 in Reals)
        self.assertFalse("text" in Reals)
        self.assertTrue(1 not in (Reals - {1}))

    def test_comparisons(self):
        self.assertTrue(0 in (Reals < 1))
        self.assertFalse(0 in (Reals < 0))

        self.assertTrue(0 in (Reals <= 1))
        self.assertTrue(0 in (Reals <= 0))
        self.assertFalse(1 in (Reals <= 0))

        self.assertTrue(1 in (Reals > 0))
        self.assertFalse(0 in (Reals > 0))

        self.assertFalse(0 in (Reals >= 1))
        self.assertTrue(0 in (Reals >= 0))
        self.assertTrue(1 in (Reals >= 0))

    def test_special_floats(self):
        self.assertFalse(float("1e9999") in Reals)  # out of float range
        self.assertFalse(float("inf") in Reals)
        self.assertFalse(float("-inf") in Reals)
        self.assertFalse(float("NaN") in Reals)

    def test_set_domain(self):
        dom = domain.SingleValue(1) + domain.SingleValue(2)
        self.assertTrue(1 in dom)
        self.assertTrue(1.0 in dom)
        self.assertTrue(2 in dom)
        self.assertFalse(3 in dom)
        self.assertFalse(3.0 in dom)
        dom = domain.SetDomain([1, 2, 6, 7, -1])
        self.assertTrue(1 in dom)
        self.assertTrue(1.0 in dom)
        self.assertTrue(2 in dom)
        self.assertFalse(3 in dom)
        self.assertFalse(3.0 in dom)

    def test_minus(self):
        self.assertTrue(1 in (Reals - {2}))
        self.assertFalse(1 in (Reals - {1}))

    def test_integers_set(self):
        self.assertTrue(1 in Integers)
        self.assertTrue(1.0 in Integers)
        self.assertFalse(1.5 in Integers)

        self.assertTrue(1.0 in (Integers > 0))
        self.assertFalse(-1.0 in (Integers > 0))
        self.assertFalse(0.0 in (Integers > 0))

        self.assertTrue(1.0 in (Integers >= 0))
        self.assertFalse(-1.0 in (Integers >= 0))
        self.assertTrue(0.0 in (Integers >= 0))

    def test_unions(self):
        self.assertTrue(1 in (domain.SingleValue(1) + (Reals < 0)))
        self.assertTrue(-1 in (domain.SingleValue(1) + (Reals < 0)))
        self.assertFalse(0 in (domain.SingleValue(1) + (Reals < 0)))
        self.assertFalse(-0.0 in (domain.SingleValue(1) + (Reals < 0)))
        self.assertTrue(1 in ((Reals < 0) + domain.SingleValue(1)))
        self.assertTrue(-1 in ((Reals < 0) + domain.SingleValue(1)))
        self.assertFalse(0 in ((Reals < 0) + domain.SingleValue(1)))

        self.assertFalse(0 in ((Reals < 0) + (Reals > 0)))


if __name__ == '__main__':
    unittest.main()
