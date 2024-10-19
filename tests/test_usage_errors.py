import unittest

from fluentflow import Flows


class TestLimitErrors(unittest.TestCase):

    def test_limit_negative(self):
        self.assertRaises(ValueError, lambda: Flows.empty().limit(-1))


class TestSkipErrors(unittest.TestCase):

    def test_skip_negative(self):
        self.assertRaises(ValueError, lambda: Flows.empty().skip(-1))


class TestSliceErrors(unittest.TestCase):

    def test_slice_step_zero(self):
        self.assertRaises(ValueError, lambda: Flows.empty().slice(step=0).to_list())

