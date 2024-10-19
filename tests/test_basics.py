import unittest

from fluentflow import Flows, EmptyFlowError


class TestFlowCreation(unittest.TestCase):

    def test_redundant_creation(self):
        self.assertEqual(3, Flows.create(Flows.create([1,2,3])).count())


class TestEmptyFlow(unittest.TestCase):

    def test_calling_last_or_on_empty(self):
        thing = object()
        self.assertEqual(thing, Flows.empty().last_or(thing))

    def test_reverse_empty(self):
        self.assertEqual(0, Flows.empty().reverse().count())

    def test_map_empty(self):
        self.assertEqual([], Flows.empty().map(lambda a: [a,a,a]).to_list())

    def test_flatmap_empty(self):
        self.assertEqual([], Flows.empty().flatmap(lambda a: [a,a,a]).to_list())


class TestCount(unittest.TestCase):

    def test_count_empty(self):
        self.assertEqual(0, Flows.empty().count())

    def test_count_range(self):
        self.assertEqual(10, Flows.create(range(10)).count())


class TestLimit(unittest.TestCase):

    def test_limit_empty(self):
        self.assertEqual(0, Flows.empty().limit(10).count())

    def test_limit_less_than_count(self):
        self.assertEqual(10, Flows.create(range(100)).limit(10).count())

    def test_limit_greater_than_count(self):
        self.assertEqual(9, Flows.create(range(9)).limit(99).count())

    def test_limit_zero(self):
        self.assertEqual(0, Flows.create(range(10)).limit(0).count())


class TestSkip(unittest.TestCase):

    def test_skip_less_than_count(self):
        self.assertEqual(90, Flows.create(range(100)).skip(10).count())

    def test_skip_greater_than_count(self):
        self.assertEqual(0, Flows.create(range(9)).skip(99).count())

    def test_skip_zero(self):
        self.assertEqual(10, Flows.create(range(10)).skip(0).count())


class TestSlice(unittest.TestCase):

    def test_slice_to_nothing(self):
        data = list(range(10))
        self.assertEqual(
            data[5:2],
            Flows.create(data).slice(start=5, stop=2).to_list()
        )

    def test_slice_with_no_effect(self):
        data = list(range(10))
        self.assertEqual(
            data[::],
            Flows.create(data).slice().to_list()
        )

    def test_slice_with_no_effect_step_1(self):
        data = list(range(10))
        self.assertEqual(
            data[::1],
            Flows.create(data).slice(step=1).to_list()
        )

    def test_slice_negative_step(self):
        data = list(range(10))
        self.assertEqual(
            data[::-1],
            Flows.create(data).slice(step=-1).to_list()
        )


class TestReverse(unittest.TestCase):

    def test_reverse_one_element(self):
        self.assertEqual(1, Flows.create([1]).reverse().count())
        self.assertEqual(1, Flows.create([1]).reverse().first())
        self.assertEqual(1, Flows.create([1]).reverse().last())

    def test_reverse_two_elements(self):
        self.assertEqual(2, Flows.create([1, 2]).reverse().count())
        self.assertEqual(2, Flows.create([1, 2]).reverse().first())
        self.assertEqual(1, Flows.create([1, 2]).reverse().last())


class TestAccess(unittest.TestCase):

    def test_calling_get_on_empty_throws(self):
        self.assertRaises(IndexError, lambda: Flows.empty().get(1))

    def test_calling_first_on_empty_throws(self):
        self.assertRaises(IndexError, lambda: Flows.empty().first())

    def test_calling_last_on_empty_throws(self):
        self.assertRaises(IndexError, lambda: Flows.empty().last())

    def test_calling_first_or_on_empty(self):
        thing = object()
        self.assertEqual(thing, Flows.empty().first_or(thing))

    def test_get(self):
        self.assertEqual(0, Flows.create(range(3)).get(0))
        self.assertEqual(1, Flows.create(range(3)).get(1))
        self.assertEqual(2, Flows.create(range(3)).get(2))

    def test_first(self):
        self.assertEqual(0, Flows.create(range(3)).first())

    def test_last(self):
        self.assertEqual(2, Flows.create(range(3)).last())

    def test_get_or(self):
        default = object()
        self.assertEqual(default, Flows.create(range(3)).get_or(10, default))


class TestDistinct(unittest.TestCase):

    def test_distinct_list(self):
        data = [1,1,1,2,1,2,2,2,1,3,2,1,2,3,3,3]
        expected = [1,2,3]
        self.assertEqual(expected, Flows.create(data).distinct().to_list())

    def test_distinct_set(self):
        data = set([1,1,1,2,1,2,2,2,1,3,2,1,2,3,3,3])
        expected = [1,2,3]
        self.assertEqual(expected, Flows.create(data).distinct().to_list())


class TestFilter(unittest.TestCase):

    def test_filter_range(self):
        data = range(10)
        expected = [x for x in data if x <= 3]
        self.assertEqual(expected, Flows.create(data).filter(lambda a: a <= 3).to_list())

    def test_filter_set(self):
        data = {'hi', 'goodbye', 'hello'}
        expected = [x for x in data if len(x) <= 3]
        self.assertEqual(expected, Flows.create(data).filter(lambda a: len(a) <= 3).to_list())


class TestMap(unittest.TestCase):

    def test_map_plus_one(self):
        data = [1,2,3]
        self.assertEqual([2,3,4], Flows.create(data).map(lambda a: a+1).to_list())

    def test_map_square(self):
        data = [1,2,3]
        self.assertEqual([1,4,9], Flows.create(data).map(lambda a: a**2).to_list())


class TestFlatMap(unittest.TestCase):

    def test_flatten(self):
        data = [ [1], [], [2, 3] ]
        expected = [1,2,3]
        self.assertEqual(expected, Flows.create(data).flatmap(lambda a: a).to_list())

    def test_flatmap_repeat_twice(self):
        self.assertEqual([1,1,2,2,3,3], Flows.create(range(1,4)).flatmap(lambda a: (a,a)).to_list())


class TestDigest(unittest.TestCase):

    def test_sum_empty(self):
        self.assertEqual(0, Flows.empty().digest(sum))

    def test_sum_int_range(self):
        data = range(1, 50)
        self.assertEqual(sum(data), Flows.create(data).digest(sum))

    def test_sum_float_list(self):
        data = [0.1, 1.2, 20.3, -3.2]
        self.assertEqual(sum(data), Flows.create(data).digest(sum))

    def test_min(self):
        self.assertEqual(0, Flows.create(range(10)).digest(min))

    def test_max(self):
        self.assertEqual(9, Flows.create(range(10)).digest(max))

    def test_join_string(self):
        data = ['a', 'bcd', '123', 'hjkl']
        self.assertEqual(''.join(data), Flows.create(data).digest(lambda all: ''.join(all)))


class TestForEach(unittest.TestCase):

    def test_for_each(self):
        counter = 0

        def _func(x):
            nonlocal counter
            counter = counter + 1

        Flows.of(1, 2, 3).for_each(_func)

        self.assertEqual(counter, 3)

class TestTerminalCollectors(unittest.TestCase):

    def test_to_list(self):
        self.assertEqual([0,1,2], Flows.create(range(3)).to_list())

    def test_to_tuple(self):
        self.assertEqual((0,1,2), Flows.create(range(3)).to_tuple())

    def test_to_set(self):
        self.assertEqual(set((0,1,2)), Flows.create(range(3)).to_set())


class TestTerminalBooleanAggregates(unittest.TestCase):

    def test_any(self):
        data = range(10)
        self.assertTrue(Flows.create(data).any(lambda a: a == 3))
        self.assertFalse(Flows.create(data).any(lambda a: a == 100))

    def test_all(self):
        data = range(10)
        self.assertTrue(Flows.create(data).all(lambda a: a >= 0))
        self.assertFalse(Flows.create(data).all(lambda a: a < 0))


class TestReduce(unittest.TestCase):

    def test_reduce_sum_int(self):
        data = [1, 2, 3]
        self.assertEqual(sum(data), Flows.create(data).reduce(lambda a,b: a+b))

    def test_reduce_sum_float(self):
        data = [0.1, 1.2, 20.3, -3.2]
        self.assertEqual(sum(data), Flows.create(data).reduce(lambda a, b: a+b))

    def test_reduce_concat_string(self):
        data = ['a', 'bcd', '123', 'hjkl']
        self.assertEqual(''.join(data), Flows.create(data).reduce(lambda a, b: a+b))

    def test_reduce_empty_error(self):
        self.assertRaises(EmptyFlowError, lambda: Flows.empty().reduce(lambda a,b: a+b))

    def test_reduce_empty_with_initial(self):
        initial = object()
        self.assertEqual(initial, Flows.empty().reduce(lambda a,b: a+b, initial))

