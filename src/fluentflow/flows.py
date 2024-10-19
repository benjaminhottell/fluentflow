import typing as ty

from .iterables import Iterables


ElemType = ty.TypeVar('ElemType')
ResultType = ty.TypeVar('ResultType')

KeyType = ty.TypeVar('KeyType')
ValueType = ty.TypeVar('ValueType')


# Placeholder for when None as a default argument won't suffice
_missing = object()


class EmptyFlowError(ValueError):
    '''Thrown when an operation is called on an empty stream that requires the stream to contain elements (be nonempty.'''
    pass



#
# Flow interface
#


class Flow(ty.Generic[ElemType]):


    # Required methods (must override in subclass)

    def __iter__(self):  # pragma: no cover
        raise NotImplementedError()


    # Modifying operations

    def reverse(self):
        '''Reverses the flow. (Warning: This could hang the application if the flow comes from an infinite generator).'''
        return Flows.calling(lambda: Iterables.reverse(self))

    def slice(
        self,
        start: int|None = None,
        stop: int|None = None,
        step: int|None = None,
    ) -> 'Flow[ElemType]':
        return Flows.calling(lambda: Iterables.slice(self, start=start, stop=stop, step=step))

    def skip(self, count: int) -> 'Flow[ElemType]':
        '''Removes elements from the start of the flow.'''
        if count < 0:
            raise ValueError(f'Cannot skip negative elements: {count}')
        elif count == 0:
            return self
        else:
            return self.slice(start=count)

    def limit(self, count: int) -> 'Flow[ElemType]':
        '''Removes elements from the end of the flow if the flow has more elements than the given limit.'''
        if count < 0:
            raise ValueError(f'Cannot limit to a negative size: {count}')
        elif count == 0:
            return Flows.empty()
        else:
            return self.slice(stop=count)

    def distinct(self):
        return Flows.calling(lambda: Iterables.distinct(self))

    def map(self, func: ty.Callable[[ElemType], ResultType]) -> 'Flow[ResultType]':
        '''Transforms every element of the flow.'''
        return Flows.calling(lambda: Iterables.map(self, func))

    def flatmap(self, func: ty.Callable[[ElemType], ty.Iterable[ResultType]]) -> 'Flow[ResultType]':
        '''
        Maps every element from the flow into an iterable.
        Then, every element from every iterable will be an element of the new flow.
        '''
        return Flows.calling(lambda: Iterables.flatmap(self, func))

    def filter(self, func: ty.Callable[[ElemType], bool]) -> 'Flow[ElemType]':
        '''Removes elements from the flow that do not meet a given condition.'''
        return Flows.calling(lambda: Iterables.filter(self, func))


    # Terminal operations

    def get(self, index: int) -> 'ElemType':
        return Iterables.get(self, index)

    def first(self) -> ElemType:
        return self.get(0)

    def last(self) -> 'ElemType':
        return self.get(-1)

    def get_or(self, index: int, other: ResultType) -> ElemType|ResultType:
        try:
            return self.get(index)
        except IndexError:
            return other

    def first_or(self, other: ResultType) -> ElemType|ResultType:
        try:
            return self.first()
        except IndexError:
            return other

    def last_or(self, other: ResultType) -> ElemType|ResultType:
        try:
            return self.last()
        except IndexError:
            return other

    def reduce(self, func, start = _missing):

        it = iter(self)

        if start is _missing:
            try:
                ret = next(it)
            except StopIteration as e:
                raise EmptyFlowError('Flow is empty, and no initial value was given.') from e
        else:
            ret = start

        for elem in it:
            ret = func(ret, elem)

        return ret

    def count(self) -> int:
        return self.digest(Iterables.count)

    def any(self, func: ty.Callable[[ElemType], bool]) -> bool:
        '''Returns True if any element in the flow matches the given condition.'''
        for elem in self:
            if func(elem):
                return True
        return False

    def all(self, func: ty.Callable[[ElemType], bool]) -> bool:
        '''Returns True if every element in the flow matches the given condition.'''
        for elem in self:
            if not func(elem):
                return False
        return True

    def to_list(self) -> list[ElemType]:
        return list(self)

    def to_tuple(self) -> tuple[ElemType]:
        return tuple(self)

    def to_set(self) -> set[ElemType]:
        return set(self)

    def digest(self, func: ty.Callable[[ty.Iterable[ElemType]], ResultType]) -> ResultType:
        '''
        Accepts any function that accepts an iterable. Returns the result of calling that function.
        Examples: `digest(min)`, `digest(statistics.mean)`.
        '''
        return func(self)

    def for_each(self, func: ty.Callable[[ElemType], ty.Any]) -> None:
        for x in self:
            func(x)



#
# Flow implementations and decorators
#


class _IterableFlow(Flow[ElemType]):

    def __init__(self, data: ty.Iterable[ElemType]):
        self._data = data

    def __iter__(self):
        return iter(self._data)

    def digest(self, func: ty.Callable[[ty.Iterable[ElemType]], ResultType]) -> ResultType:
        return func(self._data)

    def distinct(self) -> Flow[ElemType]:
        return Flows.calling(lambda: Iterables.distinct(self._data))

    def reverse(self) -> Flow[ElemType]:
        return Flows.calling(lambda: Iterables.reverse(self._data))

    def contains(self, elem: ElemType) -> bool:
        return Iterables.contains(self._data, elem)

    def get(self, index: int) -> ElemType:
        return Iterables.get(self._data, index)


#
# Flow factory
#

class Flows:

    @staticmethod
    def empty() -> Flow[ty.Any]:
        return _IterableFlow(Iterables.empty())

    @staticmethod
    def of(*args: ElemType) -> Flow[ElemType]:
        return Flows.create(args)

    @staticmethod
    def create(it: ty.Iterable[ElemType]) -> Flow[ElemType]:
        if isinstance(it, Flow):
            return it
        return _IterableFlow(it)

    @staticmethod
    def calling(func: ty.Callable[[], ty.Iterable[ElemType]]) -> Flow[ElemType]:
        return Flows.create(Iterables.calling(func))


__all__ = [
    'Flow',
    'Flows',
    'EmptyFlowError',
]

