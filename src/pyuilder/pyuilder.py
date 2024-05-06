"""Library that provides functionality for the builder design pattern in Python."""

from __future__ import annotations
import inspect
import typing as _t


### Typing

_B = _t.TypeVar("_B", bound="Builder")
_T = _t.TypeVar("_T")


_SetterAction = _t.Union[_t.Callable[[_t.Any, _T], _t.Any], str, None]


### Setter


class Setter(_t.Generic[_B, _T]):
    def __init__(self, builder: _B, name: str) -> None:
        self.builder = builder
        self.name = name

    def __call__(self, value: _T, action: _SetterAction[_T] = None, /) -> _B:
        """Set the value to use for this field once `build` is called.

        Action allows modifying how the field gets set. This can let you do an
        assortment of different things such as something similar to Lombok's `Singular`
        from Java. If action is a string, it is assumed to be a name of a method on the
        existing value for that field. If action is a callable, it is called with the
        existing value as the first argument and the provided value as the second value.
        
        Examples:
            ```
            obj = MyCls.builder()\\
                .field([])\\
                .field(1, "append")\\
                .field(2, list.append)\\
                .build()
            assert obj.field == [1, 2]  # passes!
            ```

        Args:
            value (_T): The value to set field to
            action (Any, optional): Allows modification to how field is set

        Returns:
            Builder: The builder instance this was called on
        """
        if action is None:
            self.builder._data[self.name] = value
        elif callable(action):
            action(self.builder._data[self.name], value)
        elif isinstance(action, str):
            getattr(self.builder._data[self.name], action)(value)
        return self.builder


### Builder


class Builder(_t.Generic[_T]):
    """Class for adding builders to other classes"""

    typ: _t.Type[_T]

    def __init__(self, **kwargs: _t.Any) -> None:
        """Create a new builder instance for building the class

        Args:
            **kwargs (Any): Can set any number of fields here at construction
        """
        self._data: _t.Dict[str, _t.Any] = {**kwargs}
        self._init_param_kinds = [
            inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
            inspect._ParameterKind.KEYWORD_ONLY,
        ]

    def __getattr__(self, __name: str) -> Setter[_t.Self, _t.Any]:
        return Setter(self, __name)

    def _break_args(
        self, typ: _t.Type[_T]
    ) -> _t.Tuple[_t.Dict[str, _t.Any], _t.Dict[str, _t.Any]]:
        kwargs: _t.Dict[str, _t.Any] = {}
        sig = inspect.signature(typ)
        for p in sig.parameters.values():
            if p.name in self._data and p.kind in self._init_param_kinds:
                kwargs[p.name] = self._data[p.name]
        attrs = {k: v for k, v in self._data.items() if k not in kwargs}
        return kwargs, attrs

    def build(self) -> _T:
        """Complete the builder and create an instance of the class.

        Returns:
            _T: The created class
        """
        kwargs, attrs = self._break_args(self.typ)
        inst = self.typ(**kwargs)
        for name, value in attrs.items():
            setattr(inst, name, value)
        return inst


### Builder Generation


class Buildable:
    if _t.TYPE_CHECKING:

        class builder(Builder[_t.Self]): ...  # type: ignore

    @classmethod
    def builder(cls, **kwargs: _t.Any) -> Builder[_t.Self]:
        """Create a new builder instance for building the class

        Args:
            **kwargs (Any): Can set any number of fields here at construction
        """
        b = Builder(**kwargs)
        b.typ = cls
        return b

    def __init_subclass__(cls, **_: _t.Any) -> None:
        for value in cls.__dict__.values():
            if isinstance(value, type) and issubclass(value, Builder):
                value.typ = cls  # type: ignore


__all__ = ["Buildable", "Builder", "Setter"]
