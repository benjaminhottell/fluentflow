import unittest

from fluentflow import Flows


class TestFlowWithGenerator(unittest.TestCase):

    def test_calling(self):

        def get_data():
            for x in range(10):
                yield x

        self.assertEqual(10, Flows.calling(get_data).count())

    def test_calling_doesnt_exhaust(self):

        def get_data():
            for x in range(10):
                yield x

        f = Flows.calling(get_data)
        self.assertEqual(10, f.count())
        self.assertEqual(10, f.count())

    def test_distinct(self):

        def get_data():
            for x in range(10):
                yield x
            for x in range(10):
                yield x

        self.assertEqual(10, Flows.calling(get_data).distinct().count())

    def test_reverse(self):

        def get_data():
            for x in range(10):
                yield x

        self.assertEqual(9, Flows.calling(get_data).reverse().first())
        self.assertEqual(0, Flows.calling(get_data).reverse().last())

    def test_contains(self):

        def get_data():
            for x in range(10):
                yield x

        self.assertTrue(Flows.calling(get_data).contains(5))
        self.assertFalse(Flows.calling(get_data).contains(-1))

