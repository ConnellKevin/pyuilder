from __future__ import annotations
import dataclasses

from pyuilder import Buildable, Builder, Setter


### Setup


class NoExplicitBuilderBuildable(Buildable):
    def __init__(self, field1: int, field2: str) -> None:
        self.field1 = field1
        self.field2 = field2


@dataclasses.dataclass
class HasExplicitBuilderBuildable(Buildable):
    field1: int
    field2: str

    class builder(Builder["HasExplicitBuilderBuildable"]):
        field1: Setter[HasExplicitBuilderBuildable.builder, int]
        field2: Setter[HasExplicitBuilderBuildable.builder, str]


@dataclasses.dataclass
class HasListFieldBuildable(Buildable):
    field1: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ParentBuildable(Buildable):
    field1: HasExplicitBuilderBuildable

    class builder(Builder["ParentBuildable"]):
        field1: Setter[ParentBuildable.builder, HasExplicitBuilderBuildable]


### Tests


def test_no_explicit_builder() -> None:
    # fmt: off
    obj = NoExplicitBuilderBuildable.builder()\
        .field1(1)\
        .field2("test")\
        .build()
    # fmt: on
    assert obj.field1 == 1
    assert obj.field2 == "test"


def test_explicit_builder() -> None:
    # fmt: off
    obj = HasExplicitBuilderBuildable.builder()\
        .field1(1)\
        .field2("test")\
        .build()
    # fmt: on
    assert obj.field1 == 1
    assert obj.field2 == "test"


def test_dynamic_assignment() -> None:
    # fmt: off
    obj = NoExplicitBuilderBuildable.builder()\
        .field3(3.14)\
        .build()
    # fmt: on
    assert getattr(obj, "field3", None) == 3.14


def test_setter_action_str() -> None:
    # fmt: off
    obj = HasListFieldBuildable.builder()\
        .field1([])\
        .field1("test", "append")\
        .build()
    # fmt: on
    assert obj.field1 == ["test"]


def test_setter_action_callable() -> None:
    # fmt: off
    obj = HasListFieldBuildable.builder()\
        .field1([])\
        .field1("test", list.append)\
        .build()
    # fmt: on
    assert obj.field1 == ["test"]


def test_nested_builder() -> None:
    # fmt: off
    obj = ParentBuildable.builder()\
        .field1(HasExplicitBuilderBuildable.builder()\
            .field1(1)\
            .field2("test")\
            .build())\
        .build()
    # fmt: on
    assert isinstance(obj.field1, HasExplicitBuilderBuildable)
    assert obj.field1.field1 == 1
    assert obj.field1.field2 == "test"
