import unittest

from fluentflow import Flows


class TestFlowConcurrentModification(unittest.TestCase):

    def test_concurrent_count(self):

        data = list(range(10))
        stream = Flows.create(data)
        self.assertEqual(10, stream.count())

        data.extend(range(10))
        self.assertEqual(20, stream.count())

    def test_concurrent_slice(self):

        data = list(range(10))
        stream = Flows.create(data).slice(step=2)
        self.assertEqual(5, stream.count())

        data.extend(range(10))
        self.assertEqual(10, stream.count())

    def test_concurrent_contains(self):

        data = set(range(10))
        stream = Flows.create(data)
        self.assertTrue(stream.contains(3))

        data.remove(3)
        self.assertFalse(stream.contains(3))

    def test_concurrent_distinct(self):

        data = set(range(10))
        stream = Flows.create(data).distinct()
        self.assertTrue(stream.contains(3))

        data.remove(3)
        self.assertFalse(stream.contains(3))

