# fluentflow

A Python 3 library that provides a fluent interface for data transformations and aggregations over iterable objects.


## Quickstart/Example

```py
from fluentflow import Flows

# Dummy data, pretend this is a warehouse's inventory
def get_inventory():
    yield {'Quantity': 123, 'Name': 'Lightbulbs', 'Section': 'Electronics'}
    yield {'Quantity': 456, 'Name': 'Nails', 'Section': 'Hardware'}
    yield {'Quantity': 789, 'Name': 'Keyboards', 'Section': 'Electronics'}

# Get the total inventory in the warehouse (all items)
print(Flows.calling(get_inventory)
    .map(lambda x: x['Quantity'])
    .digest(sum)
)

# Get the total distinct item sections
print(Flows.calling(get_inventory)
    .map(lambda x: x['Section'])
    .distinct()
    .count()
)
```


## Installation

A `pyproject.toml` file is included in this repository. You should be able to clone this repository, cd into it, and then run the following command:

```py
pip install .
```

There are no additional dependencies, all you need is Python 3.


## Creating flows

Static factory methods are available in the `Flows` class.

```py
# Create an empty flow (contains no elements):
Flows.empty()

# Create a flow from a list of arguments
Flows.of(1, 2, 3)

# Create a flow from an iterable
# Note: Do not pass generators to this function. Consider instead using Flows.calling (see below)
Flows.create([1, 2, 3])

# Create a flow from a function that returns an iterable or a generator.
def generator_func():
    yield 1
    yield 2
    yield 3
Flows.calling(generator_func)
```


## Operations

Operations may be **modifying** or **terminal**. A modifying operation transforms the data in the flow. They may be chained together to form more complicated operations. A terminal operation ends the chain of operations and returns an aggregated result.

### Modifying Operations

- filter
- flatmap
- limit
- map
- reverse
- skip
- slice

### Terminal Operations

- any
- all
- count
- get (get_or)
- digest
- first (first_or)
- last (last_or)
- reduce
- to_list
- to_set
- to_tuple

