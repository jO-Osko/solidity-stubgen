import dataclasses
from typing import Mapping, Sequence

from hexbytes import HexBytes
from typing_extensions import TypeAlias

JSON_ro: TypeAlias = (
    Mapping[str, "JSON_ro"] | Sequence["JSON_ro"] | str | int | float | bool | None
)


@dataclasses.dataclass(frozen=True)
class SolidityTypeDecoder:
    def process(self, value: JSON_ro) -> "JSON_ro":
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class ValueType(SolidityTypeDecoder):
    def python_type(self) -> type:
        raise NotImplementedError()

    def process(self, value: JSON_ro) -> JSON_ro:
        return self.python_type()(value)


@dataclasses.dataclass(frozen=True)
class AddressTypeDecoder(ValueType):
    def python_type(self) -> type:
        return str


@dataclasses.dataclass(frozen=True)
class BytesTypeDecoder(ValueType):
    def python_type(self) -> type:
        return bytes

    def process(self, value: JSON_ro) -> JSON_ro:
        if isinstance(value, str):
            assert value.startswith("0x")
            return HexBytes(value)
        else:
            raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class IntTypeDecoder(ValueType):
    def python_type(self) -> type:
        return int


class BoolTypeDecoder(ValueType):
    def python_type(self) -> type:
        return bool

    def process(self, value: JSON_ro) -> JSON_ro:
        if value in ["true", "True", True, 1]:
            return True
        elif value in ["false", "False", False, 0]:
            return False
        else:
            raise ValueError(f"Invalid boolean value: {value}")


@dataclasses.dataclass(frozen=True)
class ArrayTypeDecoder(SolidityTypeDecoder):
    inner: SolidityTypeDecoder

    def process(self, value: JSON_ro) -> "JSON_ro":
        return [self.inner.process(v) for v in value]


@dataclasses.dataclass(frozen=True)
class StructTypeDecoder(SolidityTypeDecoder):
    fields: dict[str, SolidityTypeDecoder]

    def process(self, value: JSON_ro) -> "JSON_ro":
        return {k: self.fields[k].process(v) for k, v in value.items()}
