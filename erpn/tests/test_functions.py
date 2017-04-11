#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

import unittest
import math
import erpn.functions as f


class FunctionTest(unittest.TestCase):
    """ Template class for all the individual function tests """
    def compare_input_result(self, initial_stack, result_stack,
                             undo_length=1, arrow_location=0,
                             delta=None):
        stack = initial_stack.copy()
        undo_stack = []
        self.function.run(stack, undo_stack, arrow_location)
        if delta is None:
            self.assertEqual(stack, result_stack)
        else:
            # We are looking for "close enough", but we can't check the whole stack this way
            self.assertEqual(len(stack), len(result_stack))
            for x,y in zip(stack, result_stack):
                self.assertAlmostEqual(x,y,delta=delta)
        self.assertEqual(len(undo_stack), undo_length)
        for _ in range(undo_length):
            undo_stack.pop().apply(stack)
        self.assertEqual(stack, initial_stack)


class AdditionTest(FunctionTest):
    function = f.addition

    def test_addition(self):
        self.compare_input_result(initial_stack=[1.0, 1.0, 1.0],
                                  result_stack=[1.0, 2.0])

    def test_addition_single_item(self):
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[1.0])

    def test_addition_no_item(self):
        self.compare_input_result(initial_stack=[],
                                  result_stack=[0.0])

    def test_addition_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 1.0],
                                  result_stack=[100.0, 10.0, 101.0],
                                  arrow_location=2, undo_length=2)


class Switch2Test(FunctionTest):
    function = f.switch2

    def test_switch2(self):
        self.compare_input_result(initial_stack=[1.0, 2.0, 3.0],
                                  result_stack=[1.0, 3.0, 2.0])


class DeleteTest(FunctionTest):
    function = f.Delete()

    def test_delete(self):
        self.compare_input_result(initial_stack=[1.0, 2.0, 3.0],
                                  result_stack=[1.0, 2.0])

    def test_delete_arrow(self):
        self.compare_input_result(initial_stack=[1.0, 2.0, 3.0, 4.0],
                                  result_stack=[1.0, 3.0, 4.0],
                                  arrow_location=2)


class SubtractTest(FunctionTest):
    function = f.subtract

    def test_subtract(self):
        self.compare_input_result(initial_stack=[2.0, 3.0],
                                  result_stack=[-1.0])

    def test_subtraction_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 1.0],
                                  result_stack=[100.0, 10.0, -99.0],
                                  arrow_location=2, undo_length=2)


class MultiplyTest(FunctionTest):
    function = f.multiply

    def test_multiply(self):
        self.compare_input_result(initial_stack=[-2.0, 3.0],
                                  result_stack=[-6.0])

    def test_multiply_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 13.0],
                                  result_stack=[100.0, 10.0, 1300.0],
                                  arrow_location=2, undo_length=2)

    def test_multiply_one_argument(self):
        self.compare_input_result(initial_stack=[3.0],
                                  result_stack=[3.0])

    def test_multiply_no_argument(self):
        self.compare_input_result(initial_stack=[],
                                  result_stack=[1.0])


class DivideTest(FunctionTest):
    function = f.divide

    def test_divide(self):
        self.compare_input_result(initial_stack=[3.0, 2.0],
                                  result_stack=[1.5])

    def test_divide_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 13.0],
                                  result_stack=[100.0, 10.0, 0.13],
                                  arrow_location=2, undo_length=2)


class ExponentTest(FunctionTest):
    function = f.exponent

    def test_exponent(self):
        self.compare_input_result(initial_stack=[3.0, 2.0],
                                  result_stack=[9.0])

    def test_exponent_fractional(self):
        self.compare_input_result(initial_stack=[4.0, 0.5],
                                  result_stack=[2.0])

    def test_exponent_negative(self):
        self.compare_input_result(initial_stack=[5.0, -1.0],
                                  result_stack=[0.2])

    def test_exponent_arrow(self):
        self.compare_input_result(initial_stack=[3.0, 10.0, 2.0],
                                  result_stack=[3.0, 10.0, 8.0],
                                  arrow_location=2, undo_length=2)


class SquareTest(FunctionTest):
    function = f.square

    def test_square(self):
        self.compare_input_result(initial_stack=[5.0],
                                  result_stack=[25.0])

    def test_square_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 13.0],
                                  result_stack=[100.0, 10.0, 13.0, 10000.0],
                                  arrow_location=2, undo_length=2)


class SquareRootTest(FunctionTest):
    function = f.sqrt

    def test_square(self):
        self.compare_input_result(initial_stack=[25.0],
                                  result_stack=[5.0])

    def test_square_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 10.0, 13.0],
                                  result_stack=[100.0, 10.0, 13.0, 10.0],
                                  arrow_location=2, undo_length=2)


class AddItemTest(FunctionTest):
    function = f.AddItem(4.0, description="Push 4.0")

    def test_addItem(self):
        self.compare_input_result(initial_stack=[],
                                  result_stack=[4.0])


class PowerTenTest(FunctionTest):
    function = f.power_10

    def test_power10(self):
        self.compare_input_result(initial_stack=[2.0],
                                  result_stack=[100.0])

    def test_power10_arrow(self):
        self.compare_input_result(initial_stack=[3.0, 4.0],
                                  result_stack=[3.0, 4.0, 1000.0],
                                  arrow_location=1, undo_length=2)


class PowerETest(FunctionTest):
    function = f.power_e

    def test_power_e(self):
        self.compare_input_result(initial_stack=[2.0],
                                  result_stack=[7.389056098930650227230427460575007813180315570551847324087])

    def test_power_e_arrow(self):
        self.compare_input_result(initial_stack=[1.0, 4.0],
                                  result_stack=[1.0, 4.0, math.e],
                                  arrow_location=1, undo_length=2)


class LnTest(FunctionTest):
    function = f.ln

    def test_ln_1(self):
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[0.0])

    def test_ln_e(self):
        self.compare_input_result(initial_stack=[math.e],
                                  result_stack=[1.0])

    def test_ln_e_inv(self):
        self.compare_input_result(initial_stack=[1/math.e],
                                  result_stack=[-1.0])

    def test_ln_arrow(self):
        self.compare_input_result(initial_stack=[1.0, 4.0],
                                  result_stack=[1.0, 4.0, 0.0],
                                  arrow_location=1, undo_length=2)


class LogTest(FunctionTest):
    """ Test Log base 10 """

    function = f.log10

    def test_log_1(self):
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[0.0])

    def test_log_10(self):
        self.compare_input_result(initial_stack=[10],
                                  result_stack=[1.0])

    def test_log_0_1(self):
        self.compare_input_result(initial_stack=[0.1],
                                  result_stack=[-1.0])

    def test_log_arrow(self):
        self.compare_input_result(initial_stack=[1.0, 4.0],
                                  result_stack=[1.0, 4.0, 0.0],
                                  arrow_location=1, undo_length=2)


class MultiplicativeInverseTest(FunctionTest):
    function = f.mult_inverse

    def test_multiplicative_inverse(self):
        self.compare_input_result(initial_stack=[0.1],
                                  result_stack=[10.0])
        self.compare_input_result(initial_stack=[10.0],
                                  result_stack=[0.1])
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[1.0])

    def test_multiplicative_inverse_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 4.0],
                                  result_stack=[100.0, 4.0, 0.01],
                                  arrow_location=1, undo_length=2)


class AdditiveInverseTest(FunctionTest):
    function = f.add_inverse

    def test_additive_inverse(self):
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[-1.0])
        self.compare_input_result(initial_stack=[-1.0],
                                  result_stack=[1.0])
        self.compare_input_result(initial_stack=[0.0],
                                  result_stack=[0.0])

    def test_additive_inverse_arrow(self):
        self.compare_input_result(initial_stack=[100.0, 4.0],
                                  result_stack=[100.0, 4.0, -100.0],
                                  arrow_location=1, undo_length=2)


class ModulusTest(FunctionTest):
    function = f.modulo

    def test_modulo(self):
        self.compare_input_result(initial_stack=[15.0, 7.0],
                                  result_stack=[1.0])

    def test_modulo_arrow(self):
        self.compare_input_result(initial_stack=[5.0, 23.0],
                                  result_stack=[5.0, 3.0],
                                  arrow_location=1, undo_length=2)

    def test_modulo_fraction(self):
        self.compare_input_result(initial_stack=[4.0, 2.5],
                                  result_stack=[1.5])

    def test_modulo_negative(self):
        self.compare_input_result(initial_stack=[-15.0, 7.0],
                                  result_stack=[6.0])
        self.compare_input_result(initial_stack=[23.0, -5.0],
                                  result_stack=[-2.0])
        self.compare_input_result(initial_stack=[-15.0, -7.0],
                                  result_stack=[-1.0])

    def test_modulo_negative_fraction(self):
        self.compare_input_result(initial_stack=[-1.0, 2.5],
                                  result_stack=[1.5])
        self.compare_input_result(initial_stack=[4.0, -2.5],
                                  result_stack=[-1.0])
        self.compare_input_result(initial_stack=[-4.0, -2.5],
                                  result_stack=[-1.5])


class GcdTest(FunctionTest):
    function = f.gcd

    def test_gcd(self):
        self.compare_input_result(initial_stack=[4.0, 12.0],
                                  result_stack=[4.0])
        self.compare_input_result(initial_stack=[-3.0, 12.0],
                                  result_stack=[3.0])

    def test_gcd_arrow(self):
        self.compare_input_result(initial_stack=[10.0, 4.0, 25.0],
                                  result_stack=[10.0, 4.0, 5.0],
                                  arrow_location=2, undo_length=2)


class FactorialTest(FunctionTest):
    function = f.factorial

    def test_factorial(self):
        self.compare_input_result(initial_stack=[4.0],
                                  result_stack=[24.0])
        self.compare_input_result(initial_stack=[0.0],
                                  result_stack=[1.0])

    def test_factorial_arrow(self):
        self.compare_input_result(initial_stack=[10.0, 4.0, 25.0],
                                  result_stack=[10.0, 4.0, 25.0, 3628800.0],
                                  arrow_location=2, undo_length=2)


class FloorTest(FunctionTest):
    function = f.floor

    def test_floor(self):
        self.compare_input_result(initial_stack=[1.9],
                                  result_stack=[1.0])
        self.compare_input_result(initial_stack=[-1.1],
                                  result_stack=[-2.0])
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[1.0])

    def test_floor_arrow(self):
        self.compare_input_result(initial_stack=[10.4, 4.0, 25.0],
                                  result_stack=[10.4, 4.0, 25.0, 10.0],
                                  arrow_location=2, undo_length=2)


class CeilTest(FunctionTest):
    function = f.ceil

    def test_ceil(self):
        self.compare_input_result(initial_stack=[1.9],
                                  result_stack=[2.0])
        self.compare_input_result(initial_stack=[-1.1],
                                  result_stack=[-1.0])
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[1.0])

    def test_ceil_arrow(self):
        self.compare_input_result(initial_stack=[10.4, 4.0, 25.0],
                                  result_stack=[10.4, 4.0, 25.0, 11.0],
                                  arrow_location=2, undo_length=2)


class SinTest(FunctionTest):
    function = f.sin

    def test_sin(self):
        # Because I want to test so many identities, I put them in a list
        for x, res in [(0.0, 0.0), (math.pi, 0.0), (math.pi/2, 1.0),
                       (math.pi/4, math.sqrt(2)/2), (math.pi*1.5, -1.0),
                       (math.pi*2.5, 1.0), (-math.pi/2, -1.0)]:
            self.compare_input_result(initial_stack=[x],
                                      result_stack=[res], delta=1e-15)

    def test_sin_arrow(self):
        self.compare_input_result(initial_stack=[math.pi/2, 4.0, 25.0],
                                  result_stack=[math.pi/2, 4.0, 25.0, 1.0],
                                  arrow_location=2, undo_length=2, delta=1e-15)


class ArcsinTest(FunctionTest):
    function = f.arcsin

    def test_arcsin(self):
        self.compare_input_result(initial_stack=[1.0],
                                  result_stack=[math.pi/2])

    def test_arcsin_arrow(self):
        self.compare_input_result(initial_stack=[1.0, 5.0, 23.0],
                                  result_stack=[1.0, 5.0, 23.0, math.pi/2],
                                  arrow_location=2, undo_length=2)


class CosTest(FunctionTest):
    function = f.cos

    def test_cos(self):
        for x, res in [(0.0, 1.0), (math.pi, -1.0), (math.pi/2, 0.0),
                       (math.pi/4, math.sqrt(2)/2), (math.pi*1.5, 0.0),
                       (math.pi*2.5, 0.0), (-math.pi, -1.0)]:
            self.compare_input_result(initial_stack=[x],
                                      result_stack=[res], delta=1e-15)

    def test_cos_arrow(self):
        self.compare_input_result(initial_stack=[math.pi/2, 4.0, 25.0],
                                  result_stack=[math.pi/2, 4.0, 25.0, 0.0],
                                  arrow_location=2, undo_length=2, delta=1e-15)


class ArccosTest(FunctionTest):
    function = f.arccos

    def test_arccos(self):
        self.compare_input_result(initial_stack=[0.0],
                                  result_stack=[math.pi/2])

    def test_arccos_arrow(self):
        self.compare_input_result(initial_stack=[0.0, 5.0, 23.0],
                                  result_stack=[0.0, 5.0, 23.0, math.pi/2],
                                  arrow_location=2, undo_length=2)


class TanTest(FunctionTest):
    function = f.tan

    def test_tan(self):
        for x, res in [(0.0, 0.0), (math.pi*1.25, 1.0), (math.pi*-0.75, 1.0),
                       (math.pi*0.75, -1), (math.pi/3, math.sqrt(3))]:
            self.compare_input_result(initial_stack=[x],
                                      result_stack=[res], delta=1e-15)

    def test_tan_arrow(self):
        self.compare_input_result(initial_stack=[math.pi/4, 4.0, 25.0],
                                  result_stack=[math.pi/4, 4.0, 25.0, 1.0],
                                  arrow_location=2, undo_length=2, delta=1e-15)


class ArctanTest(FunctionTest):
    function = f.arctan

    def test_arctan(self):
        for x, res in [(1.0, math.pi/4), (0.0, 0.0)]:
            self.compare_input_result(initial_stack=[x],
                                      result_stack=[res], delta=1e-15)

    def test_arctan_arrow(self):
        self.compare_input_result(initial_stack=[-1.0, 4.0, 25.0],
                                  result_stack=[-1.0, 4.0, 25.0, -math.pi/4],
                                  arrow_location=2, undo_length=2, delta=1e-15)


if __name__ == '__main__':
    unittest.main()
