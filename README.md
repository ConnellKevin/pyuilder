<h1 align="center">Pyuilder ("pill-der")</h1>

<h2 align="center">
Bringing the Builder Design Pattern to Python
</h2>

<!-- Shields Here -->
<p align="center">
</p>

---

## Summary

- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Simple example](#customize-the-builder--add-type-annotations)
    - [Customize the Builder & Add Type Annotations](#simple-example)
    - [Customize the Way Fields Are Set](#customize-the-way-fields-are-set)
- [Change log](#change-log)
- [License](#license)

## Getting started

### Installation

```shell
pip install pyuilder
```

### Usage

#### Simple example

Getting started is as easily as inheriting from `pyuilder.Buildable`:

```py
import pyuilder


class MyBuildable(pyuilder.Buildable):
    def __init__(self, field1: int, field2: str) -> None:
        self.field1 = field1
        self.field2 = field2


MyBuildable.build().field1(1).field2("hello world").build()
```

#### Customize the Builder & Add Type Annotations

The last example was great and easy to set up but you'll quickly notice you get no intellisense or typing annotations in your IDE. If that's alright with you: great! However, if you want a little more out of pyuilder it's pretty trivial to provide as much information as you want to pyuilder's `Buildable` to get auto-complete, type-hinting, and other useful information in your IDE:

```py
from __future__ import annotations

from pyuilder import Buildable, Builder, Setter


class MyBuildable(Buildable):
    class builder(Builder["MyBuildable"]):
        field1: Setter[MyBuildable.builder, int]
        field2: Setter[MyBuildable.builder, str]

    def __init__(self, field1: int, field2: str) -> None:
        self.field1 = field1
        self.field2 = field2


MyBuildable.build()\
    .field1(1)\
    .field2("hello world")\
    .build()
```

The setup here ensures correct auto-complete, type hints, etc.:

- The `TypeVar` on `Builder` (`Builder["MyBuildable"]`) is necessary to correctly annotate the return type of `build()`: `build() -> MyBuildable`.
- The name of the builder class here (`builder`), is what you will actually will call to invoke the builder: `MyBuildable.builder()`.
  Since the `Buildable` class is annotated to have a method named `builder` I recommend sticking with the same name.
- The `Setter[...]` annotations on the fields take two `TypeVars` which provide type hinting:
  - The first `TypeVar` indicates the return type after calling a field setter: `.field1() -> MyBuildable.builder`.
    This ensures that type hints aren't lost on chained field setter calls: `field1(1).field2("hello world")`.
  - The second `TypeVar` indicates the value type the field setter accepts: `.field1(value: int).field2(value: str)`.

#### Customize the Way Fields Are Set

The other thing you might want to do is have better control how fields are set when you do something like `.builder().field(...)`. If `field` was a `list` for example you might want to be able to call `field(...)` on the builder multiple times to continuously append values to it (similar to Lombok's `@Singular` in Java). This is certainly possible with pyuilder:

```py
from __future__ import annotations

from pyuilder import Buildable, Builder, Setter


class MyBuildable(Buildable):
    class builder(Builder["MyBuildable"]):
        field: Setter[MyBuildable.builder, str | list[str]]

    def __init__(self, field: list[str]) -> None:
        self.field = field


# Examples

# Setting the field as a list explicitly
MyBuildable.build().field(["foo", "bar"]).build()

# Specifying how it should be added via str
MyBuildable.build()\
    .field([])\
    .field("foo", "append")\
    .field("bar", "append")\
    .build()

# Specifying how it should be added via callable
MyBuildable.build()\
    .field(["foo"])\
    .field("bar", list.append)\
    .build()
```

If the second parameter to a field setter is a `str` as it is in the second example it is assumed to be a name of a method on the existing value for that field. In the example above, by the second call of `field()`, the existing value for field is a `list`. The setter will find the "append" method on the existing `list` value and call it with the provided value as the first argument.

If the second parameter to a field setter is a `Callable` as it is in the third example the setter will call that method. When the setter calls it it will give the existing value as the first argument to the callable and the provided value as the second argument to the callable. In the example above, the provided `list.append` callable is called with two arguments as described above: `list.append(existing, value)` where `existing = ["foo"]` and `value = "bar"`.

## Change log

See [CHANGELOG](CHANGELOG.md).

## License

MIT.
