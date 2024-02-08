import typing
from typing import Callable
from typing import cast
from typing import List
from typing import Type
from typing import TypeVar

T = TypeVar("T")


def from_bool(x: typing.Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: typing.Any) -> str:
    assert isinstance(x, str)
    return x


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_none(x: typing.Any) -> typing.Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[typing.Any], T], x: typing.Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def is_type(t: Type[T], x: typing.Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: typing.Any) -> dict:
    assert isinstance(x, c)
    return cast(typing.Any, x).to_dict()
