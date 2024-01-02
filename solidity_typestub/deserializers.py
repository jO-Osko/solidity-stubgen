from typing import Mapping, Sequence

from attr import frozen
from hexbytes import HexBytes
from typing_extensions import TypeAlias

JSON_ro: TypeAlias = (
    Mapping[str, "JSON_ro"] | Sequence["JSON_ro"] | str | int | float | bool | None
)


@frozen
class SolidityTypeDecoder:
    def process(self, value: JSON_ro) -> "JSON_ro":
        raise NotImplementedError()


@frozen
class ValueType(SolidityTypeDecoder):
    def python_type(self) -> type:
        raise NotImplementedError()

    def process(self, value: JSON_ro) -> JSON_ro:
        return self.python_type()(value)


@frozen
class AddressTypeDecoder(ValueType):
    def python_type(self) -> type:
        return str


@frozen
class BytesTypeDecoder(ValueType):
    def python_type(self) -> type:
        return bytes

    def process(self, value: JSON_ro) -> JSON_ro:
        if isinstance(value, str):
            assert value.startswith("0x")
            return HexBytes(value)
        else:
            raise NotImplementedError()


@frozen
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


@frozen
class ArrayTypeDecoder(SolidityTypeDecoder):
    inner: SolidityTypeDecoder

    def process(self, value: JSON_ro) -> "JSON_ro":
        return [self.inner.process(v) for v in value]


@frozen
class StructTypeDecoder(SolidityTypeDecoder):
    fields: dict[str, SolidityTypeDecoder]

    def process(self, value: JSON_ro) -> "JSON_ro":
        return {k: self.fields[k].process(v) for k, v in value.items()}
