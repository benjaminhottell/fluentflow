import typing as ty

import collections.abc
import itertools

ElemType = ty.TypeVar('ElemType')
ResultType = ty.TypeVar('ResultType')



#
# Custom iterators and decorators for iterators
#


class _EmptyIterable:

    def __iter__(self) -> ty.Self:
        return self

    def __next__(self) -> ty.Any:
        raise StopIteration


class _CallingIterable(ty.Generic[ElemType]):

    def __init__(self, func: ty.Callable[[], ty.Iterable[ElemType]]):
        self._func = func

    def __next__(self) -> ty.Any:  # pragma: no cover
        raise TypeError('Call __iter__ first')

    def __iter__(self) -> ty.Iterator[ElemType]:
        return iter(self._func())


class _ThroughSetIterator(ty.Generic[ElemType]):
    '''Decorates an iterator to send all of its elements through a set so that duplicate elements are discarded.'''

    def __init__(self, parent: ty.Iterator[ElemType]):
        self._already: set[ElemType] = set()
        self._parent = parent

    def __iter__(self) -> ty.Self:  # pragma: no cover
        return self

    def __next__(self) -> ElemType:
        while True:
            ret = next(self._parent)
            if ret in self._already:
                continue
            self._already.add(ret)
            return ret


class _ThroughSetIterable(ty.Generic[ElemType]):

    def __init__(self, parent: ty.Iterable[ElemType]):
        self._parent = parent

    def __next__(self) -> ty.Any:  # pragma: no cover
        raise TypeError('Call __iter__ first')

    def __iter__(self) -> ty.Iterator[ElemType]:
        return _ThroughSetIterator(iter(self._parent))


class _ReversedIterable(ty.Generic[ElemType]):

    def __init__(self, parent: ty.Iterable[ElemType]):
        self._parent = parent

    def __next__(self) -> ty.Any:  # pragma: no cover
        raise TypeError('Call __iter__ first')

    def __iter__(self) -> ty.Iterator[ElemType]:
        if isinstance(self._parent, collections.abc.Reversible):
            return reversed(self._parent)
        return iter(reversed(tuple(self._parent)))


class _FlatMapIterator(ty.Generic[ElemType, ResultType]):

    def __init__(
            self,
            parent: ty.Iterator[ElemType],
            func: ty.Callable[[ElemType], ty.Iterable[ResultType]],
        ):
        self._parent = parent
        self._func = func

        self._flattening: ty.Iterator[ResultType]|None = None

    def __iter__(self) -> ty.Self:  # pragma: no cover
        return self

    def __next__(self) -> ResultType:
        while True:

            if self._flattening is not None:
                try:
                    return next(self._flattening)
                except StopIteration:
                    self._flattening = None
                    pass

            self._flattening = iter(self._func(next(self._parent)))


class _FlatMapIterable(ty.Generic[ElemType, ResultType]):

    def __init__(
            self,
            parent: ty.Iterable[ElemType],
            func: ty.Callable[[ElemType], ty.Iterable[ResultType]],
        ):
        self._parent = parent
        self._func = func

    def __next__(self) -> ty.Any:  # pragma: no cover
        raise TypeError('Call __iter__ first')

    def __iter__(self) -> ty.Iterator[ResultType]:  # pragma: no cover
        return _FlatMapIterator(iter(self._parent), self._func)


class Iterables:

    @staticmethod
    def empty() -> ty.Iterable[ty.Any]:
        return _EmptyIterable()

    @staticmethod
    def calling(func: ty.Callable[[], ty.Iterable[ElemType]]) -> ty.Iterable[ElemType]:
        return _CallingIterable(func)

    @staticmethod
    def contains(it: ty.Iterable[ElemType], elem: ElemType) -> bool:
        if isinstance(it, collections.abc.Container):
            return elem in it

        for x in it:
            if x == elem:
                return True
        return False

    @staticmethod
    def count(it: ty.Iterable[ElemType]) -> int:
        if isinstance(it, collections.abc.Sized):
            return len(it)

        count = 0
        for x in it:
            count = count + 1
        return count

    @staticmethod
    def map(it: ty.Iterable[ElemType], func: ty.Callable[[ElemType], ResultType]) -> ty.Iterable[ResultType]:
        return map(func, it)

    @staticmethod
    def flatmap(it: ty.Iterable[ElemType], func: ty.Callable[[ElemType], ty.Iterable[ResultType]]) -> ty.Iterable[ResultType]:
        return _FlatMapIterable(it, func)

    @staticmethod
    def filter(it: ty.Iterable[ElemType], func: ty.Callable[[ElemType], bool]) -> ty.Iterable[ElemType]:
        return filter(func, it)

    @staticmethod
    def reverse(it: ty.Iterable[ElemType]) -> ty.Iterable[ElemType]:
        return _ReversedIterable(it)

    @staticmethod
    def distinct(
            it: ty.Iterable[ElemType],
            allow_short_circuit: bool = True,
        ) -> ty.Iterable[ElemType]:

        if allow_short_circuit and isinstance(it, (
                range,
                collections.abc.Set,
            )):
            return it

        return _ThroughSetIterable(it)

    @staticmethod
    def slice(
            it: ty.Iterable[ElemType],
            start: int|None = None,
            stop: int|None = None,
            step: int|None = None,
        ) -> ty.Iterable[ElemType]:

        if start is None:
            start = 0

        if step is None:
            step = 1

        if start == 0 and stop is None and step == 1:
            return it

        if stop is not None and start >= stop:
            return Iterables.empty()

        if step < 0:
            return Iterables.slice(Iterables.reverse(it), start, stop, -step)

        return itertools.islice(it, start, stop, step)

    @staticmethod
    def get(it: ty.Iterable[ElemType], index: int) -> ElemType:

        if isinstance(it, collections.abc.Sequence):
            return it[index]

        if index < 0:
            new_index = Iterables.count(it) + index
            if new_index < 0:
                raise IndexError(str(index))
            index = new_index

        for elem_index, elem in enumerate(iter(it)):
            if elem_index == index:
                return elem

        raise IndexError(str(index))


__all__ = [
    'Iterables',
]

