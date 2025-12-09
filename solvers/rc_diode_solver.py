from typing import Tuple

import numpy as np

from interfaces import NonLinearComponent


class RC_Diode_Solver:
    """
    Handles the numerical integration (Euler's Method).
    It manages the state of the circuit simulation.
    """

    def __init__(
        self, r_load: float, c_filter: float, dt: float, diode: NonLinearComponent
    ):
        self.R = r_load
        self.C = c_filter
        self.dt = dt
        self.diode = diode  # Dependency Injection

    def simulate(
        self, t_end: float, initial_voltage: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Runs the simulation loop.
        Returns: (time_array, source_voltage, output_voltage)
        """
        # Time setup
        t = np.arange(0, t_end, self.dt)
        n_steps = len(t)

        # State arrays
        Vs = 10 * np.sin(10 * t)
        Vo = np.zeros(n_steps)
        Vo[0] = initial_voltage

        # Integration Loop
        for k in range(n_steps - 1):
            v_out_curr = Vo[k]
            v_source_curr = Vs[k]

            # 1. Calculate Component States
            v_d = v_source_curr - v_out_curr
            i_diode = self.diode.get_current(v_d)
            i_resistor = v_out_curr / self.R

            # 2. Apply KCL: i_C = i_in - i_out
            i_cap = i_diode - i_resistor

            # 3. Euler Update: V_new = V_old + (dV/dt * dt)
            dvo_dt = i_cap / self.C
            Vo[k + 1] = v_out_curr + (dvo_dt * self.dt)

        return t, Vs, Vo
