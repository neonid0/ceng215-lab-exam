"""
Generic Circuit Plotter

Provides flexible plotting utilities for all circuit simulation scenarios.
Supports single plots, comparison plots, error analysis, and multi-panel layouts.
"""

from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import matplotlib.pyplot as plt
import numpy as np


class GenericPlotter:
    """
    Generic plotter for circuit simulation results.

    Features:
    - Dark/light mode
    - Single and multi-panel plots
    - Error analysis
    - Comparison plots
    - Frequency response
    - Phase portraits
    - Energy plots
    """

    def __init__(
        self, dark_mode: bool = True, figure_size: Tuple[float, float] = (10, 6)
    ):
        """
        Initialize generic plotter.

        Args:
            dark_mode: Use dark background (default True)
            figure_size: Default figure size in inches
        """
        self.dark_mode = dark_mode
        self.figure_size = figure_size

        # Set style
        if dark_mode:
            plt.style.use('dark_background')
            self.colors = {
                'primary': 'cyan',
                'secondary': 'lime',
                'tertiary': 'orange',
                'quaternary': 'magenta',
                'input': 'blue',
                'output': 'red',
                'reference': 'green',
                'error': 'red',
            }
        else:
            plt.style.use('default')
            self.colors = {
                'primary': 'blue',
                'secondary': 'green',
                'tertiary': 'red',
                'quaternary': 'purple',
                'input': 'blue',
                'output': 'red',
                'reference': 'green',
                'error': 'red',
            }

    def plot_signals(
        self,
        t: np.ndarray,
        signals: Dict[str, np.ndarray],
        title: str = "Circuit Response",
        xlabel: str = "Time (s)",
        ylabel: str = "Voltage (V)",
        grid: bool = True,
        legend: bool = True,
        save_path: Optional[str] = None,
    ):
        """
        Plot multiple signals on same axes.

        Args:
            t: Time array
            signals: Dictionary of {label: data} pairs
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            grid: Show grid
            legend: Show legend
            save_path: Path to save figure

        Example:
            plotter.plot_signals(
                t,
                {'Input': vs, 'Output': vo, 'Reference': vref},
                title="RC Circuit Response"
            )
        """
        fig, ax = plt.subplots(figsize=self.figure_size)

        # Plot each signal
        line_styles = ['-', '--', ':', '-.']
        for idx, (label, data) in enumerate(signals.items()):
            style = line_styles[idx % len(line_styles)]
            ax.plot(t, data, style, linewidth=2, label=label)

        # Add zero line
        ax.axhline(
            0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )

        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14)

        if grid:
            ax.grid(True, alpha=0.3, linestyle='--')
        if legend:
            ax.legend(fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.show()

    def plot_with_error(
        self,
        t: np.ndarray,
        numerical: np.ndarray,
        analytical: np.ndarray,
        input_signal: Optional[np.ndarray] = None,
        title: str = "Numerical vs Analytical",
        ylabel: str = "Voltage (V)",
        save_path: Optional[str] = None,
    ):
        """
        Plot numerical solution, analytical solution, and error.

        Args:
            t: Time array
            numerical: Numerical solution
            analytical: Analytical reference
            input_signal: Optional input signal to plot
            title: Main title
            ylabel: Y-axis label for signals
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Left: Signals
        if input_signal is not None:
            ax1.plot(t, input_signal, 'b--', alpha=0.5, linewidth=2, label='Input')
        ax1.plot(t, numerical, 'r-', linewidth=2, label='Numerical')
        ax1.plot(t, analytical, 'g:', linewidth=2, label='Analytical')
        ax1.axhline(
            0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )
        ax1.set_xlabel('Time (s)', fontsize=11)
        ax1.set_ylabel(ylabel, fontsize=11)
        ax1.set_title(f'{title}: Signals', fontsize=12)
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Right: Error
        error = np.abs(numerical - analytical)
        ax2.semilogy(t, error + 1e-15, self.colors['error'], linewidth=2)
        ax2.set_xlabel('Time (s)', fontsize=11)
        ax2.set_ylabel('Absolute Error', fontsize=11)
        ax2.set_title(f'{title}: Error', fontsize=12)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.show()

    def plot_multi_panel(
        self,
        panels: List[Dict],
        layout: Tuple[int, int] = (2, 2),
        main_title: Optional[str] = None,
        figure_size: Optional[Tuple[float, float]] = None,
        save_path: Optional[str] = None,
    ):
        """
        Create multi-panel plot with flexible configuration.

        Args:
            panels: List of panel configurations, each a dict with:
                - 't': time array (optional)
                - 'signals': dict of {label: data}
                - 'title': panel title
                - 'xlabel': x-axis label
                - 'ylabel': y-axis label
                - 'type': 'line', 'semilogy', 'loglog', 'semilogx' (default 'line')
            layout: (rows, cols) tuple
            main_title: Overall figure title
            figure_size: Figure size (uses default if None)
            save_path: Path to save figure

        Example:
            panels = [
                {'signals': {'vC': vC}, 'title': 'Capacitor Voltage', 'ylabel': 'V'},
                {'signals': {'iL': iL}, 'title': 'Inductor Current', 'ylabel': 'A'},
            ]
            plotter.plot_multi_panel(panels, layout=(2, 1))
        """
        if figure_size is None:
            figure_size = (self.figure_size[0] * 1.2, self.figure_size[1] * 1.2)

        fig = plt.figure(figsize=figure_size)

        if main_title:
            fig.suptitle(main_title, fontsize=16)

        rows, cols = layout

        for idx, panel in enumerate(panels[: rows * cols]):
            ax = plt.subplot(rows, cols, idx + 1)

            # Get panel config
            signals = panel.get('signals', {})
            t = panel.get('t', None)
            title = panel.get('title', '')
            xlabel = panel.get('xlabel', 'Time (s)')
            ylabel = panel.get('ylabel', 'Value')
            plot_type = panel.get('type', 'line')

            # Plot signals
            line_styles = ['-', '--', ':', '-.']
            for sig_idx, (label, data) in enumerate(signals.items()):
                style = line_styles[sig_idx % len(line_styles)]

                if t is not None:
                    x_data = t
                else:
                    x_data = np.arange(len(data))

                # Choose plot type
                if plot_type == 'semilogy':
                    ax.semilogy(x_data, data, style, linewidth=2, label=label)
                elif plot_type == 'loglog':
                    ax.loglog(x_data, data, style, linewidth=2, label=label)
                elif plot_type == 'semilogx':
                    ax.semilogx(x_data, data, style, linewidth=2, label=label)
                else:  # line
                    ax.plot(x_data, data, style, linewidth=2, label=label)

            # Formatting
            if plot_type == 'line':
                ax.axhline(
                    0,
                    color='white' if self.dark_mode else 'black',
                    linestyle='-',
                    linewidth=0.5,
                    alpha=0.3,
                )

            ax.set_xlabel(xlabel, fontsize=10)
            ax.set_ylabel(ylabel, fontsize=10)
            ax.set_title(title, fontsize=11)
            ax.grid(True, alpha=0.3)

            if len(signals) > 1 or panel.get('legend', True):
                ax.legend(fontsize=8)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.show()

    def plot_phase_portrait(
        self,
        x: np.ndarray,
        y: np.ndarray,
        title: str = "Phase Portrait",
        xlabel: str = "x",
        ylabel: str = "y",
        mark_start_end: bool = True,
        save_path: Optional[str] = None,
    ):
        """
        Plot phase portrait (trajectory in state space).

        Args:
            x: First state variable
            y: Second state variable
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            mark_start_end: Mark start and end points
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figure_size)

        ax.plot(x, y, self.colors['primary'], linewidth=2, label='Trajectory')

        if mark_start_end:
            ax.plot(x[0], y[0], 'go', markersize=10, label='Start')
            ax.plot(x[-1], y[-1], 'ro', markersize=10, label='End')

        ax.axhline(
            0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )
        ax.axvline(
            0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )

        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.show()

    def plot_frequency_response(
        self,
        frequencies: np.ndarray,
        magnitude_db: np.ndarray,
        title: str = "Frequency Response",
        mark_frequency: Optional[float] = None,
        cutoff_frequency: Optional[float] = None,
        save_path: Optional[str] = None,
    ):
        """
        Plot frequency response (Bode magnitude plot).

        Args:
            frequencies: Frequency array (rad/s or Hz)
            magnitude_db: Magnitude in dB
            title: Plot title
            mark_frequency: Optional frequency to mark
            cutoff_frequency: Optional cutoff frequency to mark
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figure_size)

        ax.semilogx(frequencies, magnitude_db, self.colors['primary'], linewidth=2)

        if cutoff_frequency:
            ax.axvline(
                cutoff_frequency,
                color='r',
                linestyle='--',
                label=f'Cutoff: {cutoff_frequency:.2f} rad/s',
            )

        if mark_frequency:
            ax.axvline(
                mark_frequency,
                color='g',
                linestyle=':',
                linewidth=2,
                label=f'ω = {mark_frequency} rad/s',
            )

        ax.axhline(-3, color='k', linestyle=':', alpha=0.3, label='-3 dB')

        ax.set_xlabel('Frequency (rad/s)', fontsize=12)
        ax.set_ylabel('Magnitude (dB)', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.grid(True, alpha=0.3, which='both')
        ax.legend(fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.show()

    def close_all(self):
        """Close all open figures."""
        plt.close('all')
