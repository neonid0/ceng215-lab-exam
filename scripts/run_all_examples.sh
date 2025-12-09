#!/bin/bash
# Run All Examples - Bash Script
# Simple alternative to run_all_examples.py

echo "=========================================="
echo "  CIRCUIT SIMULATION - RUN ALL EXAMPLES  "
echo "=========================================="
echo ""

# Change to project root (script is in scripts/ folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit

echo "Project root: $PROJECT_ROOT"

# Define examples directory
EXAMPLES_DIR="examples"

# List of examples to run
examples=(
    "main_exam_prep.py"
    "main_linear_rc_step.py"
    "main_linear_rc_ramp.py"
    "main_linear_rc_sine.py"
    "main_quadratic_device.py"
    "main_rlc_circuit.py"
    "main_iv_curves.py"
)

# Counters
total=${#examples[@]}
success=0
failed=0

# Run each example
for i in "${!examples[@]}"; do
    example="${examples[$i]}"
    num=$((i + 1))

    echo "[$num/$total] Running: $example"
    echo "----------------------------------------"

    # Convert filename to module name (e.g., main_exam_prep.py -> examples.main_exam_prep)
    module_name="examples.${example%.py}"

    if uv run -m "$module_name"; then
        echo "✓ SUCCESS: $example"
        ((success++))
    else
        echo "✗ FAILED: $example"
        ((failed++))
    fi

    echo ""
done

# Print summary
echo "=========================================="
echo "  SUMMARY                                 "
echo "=========================================="
echo "Total:      $total"
echo "Successful: $success"
echo "Failed:     $failed"
echo "=========================================="

# Exit with appropriate code
if [ $failed -eq 0 ]; then
    exit 0
else
    exit 1
fi
