from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OpaqueClientIdentity:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("opaque value must be a string")


@dataclass(frozen=True, slots=True)
class OpaqueRequestIdentity:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("opaque value must be a string")


@dataclass(frozen=True, slots=True)
class IntentFingerprint:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("opaque value must be a string")


@dataclass(frozen=True, slots=True)
class EvidenceLookupKey:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("opaque value must be a string")


@dataclass(frozen=True, slots=True)
class TechnicalOperationKey:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("opaque value must be a string")


@dataclass(frozen=True, slots=True)
class OpaqueReplayMetadata:
    entries: tuple[tuple[str, str], ...] = ()
