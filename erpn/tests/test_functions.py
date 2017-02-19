#!/usr/bin/env python3
# ERPN, an RPN calculator
# Copyright (C) 2017 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details

import unittest
import erpn.functions as f


class FunctionTest(unittest.TestCase):
    """ Template class for all the individual function tests """
    def compare_input_result(self, initial_stack, result_stack, undo_length=1, arrow_location=0):
        stack = initial_stack.copy()
        undo_stack = []
        self.function.run(stack, undo_stack, arrow_location)
        self.assertEqual(stack, result_stack)
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


if __name__ == '__main__':
    unittest.main()
