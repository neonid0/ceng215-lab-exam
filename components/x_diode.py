from interfaces import NonLinearComponent


class XDiode(NonLinearComponent):
    """
    Concrete implementation of the X-Diode specifications.
    Encapsulates the device physics.
    """

    def get_current(self, v_d: float) -> float:
        """Returns current in Amperes given voltage drop v_d."""
        i_ma = 0.0

        if v_d < 0:
            i_ma = 0.1 * v_d
        elif 0 <= v_d <= 3:
            i_ma = (2 / 3) * v_d
        else:  # v_d > 3
            i_ma = (v_d - 3) ** 2 + 2

        return i_ma * 1e-3  # Convert to Amps
