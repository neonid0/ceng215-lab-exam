"""
I-V Curve Plotter

Plots current-voltage characteristics for any circuit component.
Useful for visualizing and understanding component behavior.
"""

import sys
from pathlib import Path
from typing import (
    Optional,
    Union,
)

import matplotlib.pyplot as plt
import numpy as np

from interfaces.linear_component import LinearComponent
from interfaces.non_linear_component import NonLinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class IVCurvePlotter:
    """
    Plots I-V (current-voltage) characteristics for circuit components.

    Supports:
    - Linear components (resistor, capacitor impedance, inductor impedance)
    - Nonlinear components (diodes, quadratic devices, etc.)

    Use Cases:
    - Understand component behavior
    - Verify piecewise models (like X-diode)
    - Compare different components
    - Educational visualization
    """

    def __init__(self, dark_mode: bool = True):
        """
        Initialize I-V curve plotter.

        Args:
            dark_mode: Use dark mode styling (default True)
        """
        self.dark_mode = dark_mode

        if dark_mode:
            plt.style.use('dark_background')
            self.color_primary = 'cyan'
            self.color_secondary = 'lime'
            self.color_tertiary = 'orange'
        else:
            self.color_primary = 'blue'
            self.color_secondary = 'green'
            self.color_tertiary = 'red'

    def plot_component(
        self,
        component: Union[NonLinearComponent, LinearComponent],
        v_min: float = -5.0,
        v_max: float = 5.0,
        num_points: int = 1000,
        title: Optional[str] = None,
        show_grid: bool = True,
        save_path: Optional[str] = None,
    ):
        """
        Plot I-V characteristic for a component.

        Args:
            component: Component to characterize
            v_min: Minimum voltage in Volts
            v_max: Maximum voltage in Volts
            num_points: Number of points to plot
            title: Plot title (auto-generated if None)
            show_grid: Show grid on plot
            save_path: Path to save figure (if provided)

        Note:
            For nonlinear components, uses current(voltage) method.
            For linear components (resistors), plots V/R.
        """
        # Generate voltage range
        v = np.linspace(v_min, v_max, num_points)

        # Calculate current
        if isinstance(component, NonLinearComponent):
            i = np.array([component.get_current(vk) for vk in v])
            component_type = "Nonlinear"
        elif hasattr(component, 'current'):
            # Linear component with current method (Resistor)
            i = np.array([component.current(vk) for vk in v])
            component_type = "Linear"
        else:
            raise TypeError(f"Component must have get_current() or current() method")

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot I-V curve
        ax.plot(
            v, i * 1000, color=self.color_primary, linewidth=2, label=str(component)
        )

        # Add zero lines
        ax.axhline(
            y=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )
        ax.axvline(
            x=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )

        # Labels and title
        ax.set_xlabel('Voltage (V)', fontsize=12)
        ax.set_ylabel('Current (mA)', fontsize=12)

        if title is None:
            title = f'{component_type} Component I-V Characteristic'
        ax.set_title(title, fontsize=14)

        # Grid
        if show_grid:
            ax.grid(True, alpha=0.3, linestyle='--')

        # Legend
        ax.legend(fontsize=10)

        plt.tight_layout()

        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved I-V curve to: {save_path}")

        plt.show()

    def compare_components(
        self,
        components: list,
        labels: list,
        v_min: float = -5.0,
        v_max: float = 5.0,
        num_points: int = 1000,
        title: str = "Component I-V Comparison",
        save_path: Optional[str] = None,
    ):
        """
        Plot I-V characteristics for multiple components on same axes.

        Args:
            components: List of components to compare
            labels: List of labels for each component
            v_min: Minimum voltage in Volts
            v_max: Maximum voltage in Volts
            num_points: Number of points to plot
            title: Plot title
            save_path: Path to save figure (if provided)

        Raises:
            ValueError: If components and labels have different lengths
        """
        if len(components) != len(labels):
            raise ValueError(
                f"Components and labels must have same length: "
                f"{len(components)} != {len(labels)}"
            )

        # Generate voltage range
        v = np.linspace(v_min, v_max, num_points)

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))

        colors = [
            self.color_primary,
            self.color_secondary,
            self.color_tertiary,
            'magenta',
            'yellow',
            'pink',
        ]

        # Plot each component
        for idx, (component, label) in enumerate(zip(components, labels)):
            try:
                if isinstance(component, NonLinearComponent):
                    i = np.array([component.get_current(vk) for vk in v])
                elif hasattr(component, 'current'):
                    i = np.array([component.current(vk) for vk in v])
                else:
                    print(f"Skipping {label}: no get_current() or current() method")
                    continue

                color = colors[idx % len(colors)]
                ax.plot(v, i * 1000, color=color, linewidth=2, label=label)

            except Exception as e:
                print(f"Error plotting {label}: {e}")

        # Add zero lines
        ax.axhline(
            y=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )
        ax.axvline(
            x=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )

        # Labels and title
        ax.set_xlabel('Voltage (V)', fontsize=12)
        ax.set_ylabel('Current (mA)', fontsize=12)
        ax.set_title(title, fontsize=14)

        # Grid and legend
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)

        plt.tight_layout()

        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved comparison plot to: {save_path}")

        plt.show()

    def plot_piecewise_regions(
        self,
        component: NonLinearComponent,
        breakpoints: list,
        v_min: float = -5.0,
        v_max: float = 5.0,
        num_points: int = 1000,
        title: str = "Piecewise I-V Characteristic",
        save_path: Optional[str] = None,
    ):
        """
        Plot I-V curve with piecewise regions highlighted.

        Args:
            component: Piecewise nonlinear component
            breakpoints: List of voltage breakpoints
            v_min: Minimum voltage in Volts
            v_max: Maximum voltage in Volts
            num_points: Number of points to plot
            title: Plot title
            save_path: Path to save figure (if provided)

        Example:
            For X-diode with breakpoints at [0, 3]:
            - Region 1: v < 0
            - Region 2: 0 ≤ v ≤ 3
            - Region 3: v > 3
        """
        # Generate voltage range
        v = np.linspace(v_min, v_max, num_points)
        i = np.array([component.get_current(vk) for vk in v])

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot full curve
        ax.plot(
            v, i * 1000, color=self.color_primary, linewidth=2, label=str(component)
        )

        # Highlight breakpoints
        for bp in breakpoints:
            i_bp = component.get_current(bp)
            ax.axvline(
                x=bp,
                color=self.color_tertiary,
                linestyle='--',
                alpha=0.5,
                linewidth=1.5,
            )
            ax.plot(
                bp,
                i_bp * 1000,
                'o',
                color=self.color_tertiary,
                markersize=8,
                label=f'Breakpoint: v={bp}V',
            )

        # Add zero lines
        ax.axhline(
            y=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )
        ax.axvline(
            x=0,
            color='white' if self.dark_mode else 'black',
            linestyle='-',
            linewidth=0.5,
            alpha=0.3,
        )

        # Labels and title
        ax.set_xlabel('Voltage (V)', fontsize=12)
        ax.set_ylabel('Current (mA)', fontsize=12)
        ax.set_title(title, fontsize=14)

        # Grid and legend
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)

        plt.tight_layout()

        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved piecewise plot to: {save_path}")

        plt.show()
