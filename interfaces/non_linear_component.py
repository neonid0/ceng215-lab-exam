from abc import (
    ABC,
    abstractmethod,
)


class NonLinearComponent(ABC):
    """
    Abstract Base Class for any non-linear component.
    Why? This allows the Solver to accept ANY component (Diode, Transistor),
    not just this specific 'X-Diode'.
    """

    @abstractmethod
    def get_current(self, voltage_drop: float) -> float:
        pass
