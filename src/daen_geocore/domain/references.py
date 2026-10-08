from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaceRef:
    """Opaque Place reference; PlaceRef is the frozen GeoID namespace."""

    token: str

    def __post_init__(self) -> None:
        if type(self.token) is not str:
            raise TypeError("reference token must be a string")


@dataclass(frozen=True, slots=True)
class SourceAssertionRef:
    token: str

    def __post_init__(self) -> None:
        if type(self.token) is not str:
            raise TypeError("reference token must be a string")


@dataclass(frozen=True, slots=True)
class SelectionRecordRef:
    token: str

    def __post_init__(self) -> None:
        if type(self.token) is not str:
            raise TypeError("reference token must be a string")


@dataclass(frozen=True, slots=True)
class AccessPointRef:
    token: str

    def __post_init__(self) -> None:
        if type(self.token) is not str:
            raise TypeError("reference token must be a string")
