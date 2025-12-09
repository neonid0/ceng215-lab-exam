#!/usr/bin/env python3
"""
Run All Examples Script

Executes all example scripts in the examples/ directory.
Provides a convenient way to test all circuit simulations.
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")


def print_section(text: str):
    """Print formatted section."""
    print(f"\n{BOLD}{YELLOW}{text}{RESET}")
    print(f"{YELLOW}{'-' * len(text)}{RESET}")


def run_example(script_path: Path) -> Tuple[bool, str]:
    """
    Run a single example script.

    Args:
        script_path: Path to the example script

    Returns:
        Tuple of (success, output_message)
    """
    try:
        print(f"{BLUE}▶ Running: {script_path.name}{RESET}")

        # Run the script with uv (change to project root first)
        module_name = f"examples.{script_path.stem}"
        result = subprocess.run(
            ["uv", "run", "-m", module_name],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
            cwd=Path(__file__).parent.parent,  # Run from project root
        )

        if result.returncode == 0:
            print(f"{GREEN}✓ SUCCESS: {script_path.name}{RESET}")
            return True, result.stdout
        else:
            print(f"{RED}✗ FAILED: {script_path.name}{RESET}")
            print(f"{RED}Error output:{RESET}")
            print(result.stderr)
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print(f"{RED}✗ TIMEOUT: {script_path.name} (exceeded 60 seconds){RESET}")
        return False, "Timeout"
    except Exception as e:
        print(f"{RED}✗ ERROR: {script_path.name} - {str(e)}{RESET}")
        return False, str(e)


def main():
    """Main execution function."""
    print_header("CIRCUIT SIMULATION - RUN ALL EXAMPLES")

    # Get project root (script is in scripts/ folder, so go up one level)
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"

    # Define examples to run (in order)
    examples = [
        "main_exam_prep.py",
        "main_linear_rc_step.py",
        "main_linear_rc_ramp.py",
        "main_linear_rc_sine.py",
        "main_quadratic_device.py",
        "main_rlc_circuit.py",
        "main_iv_curves.py",
    ]

    print(f"Examples directory: {examples_dir}")
    print(f"Found {len(examples)} example scripts to run")

    # Track results
    results = []

    # Run each example
    for idx, example_name in enumerate(examples, 1):
        print_section(f"Example {idx}/{len(examples)}: {example_name}")

        example_path = examples_dir / example_name

        if not example_path.exists():
            print(f"{RED}✗ NOT FOUND: {example_name}{RESET}")
            results.append((example_name, False, "File not found"))
            continue

        success, output = run_example(example_path)
        results.append((example_name, success, output))

    # Print summary
    print_header("SUMMARY")

    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful

    print(f"\n{BOLD}Total Examples: {len(results)}{RESET}")
    print(f"{GREEN}Successful: {successful}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")

    # List failed examples
    if failed > 0:
        print(f"\n{BOLD}{RED}Failed Examples:{RESET}")
        for name, success, _ in results:
            if not success:
                print(f"  {RED}✗ {name}{RESET}")

    # List successful examples
    if successful > 0:
        print(f"\n{BOLD}{GREEN}Successful Examples:{RESET}")
        for name, success, _ in results:
            if success:
                print(f"  {GREEN}✓ {name}{RESET}")

    print_header("COMPLETE")

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
