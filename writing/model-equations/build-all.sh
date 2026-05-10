#!/usr/bin/env bash
# Build all equation visualizations
set -euo pipefail

cd "$(dirname "$0")"

echo "======================================"
echo "Building Nerdfit Equation Visualizations"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check dependencies
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $1 found"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        return 1
    fi
}

echo ""
echo "Checking dependencies..."
PDFLATEX_AVAILABLE=false
MANIM_AVAILABLE=false
PYTHON_AVAILABLE=false

if check_command pdflatex; then
    PDFLATEX_AVAILABLE=true
elif check_command docker; then
    echo -e "${BLUE}ℹ${NC} Will use Docker for LaTeX compilation"
    PDFLATEX_AVAILABLE=true
fi

if check_command manim; then
    MANIM_AVAILABLE=true
fi

if check_command python3; then
    PYTHON_AVAILABLE=true
fi

echo ""

# 1. Build Enhanced LaTeX
if [ "$PDFLATEX_AVAILABLE" = true ]; then
    echo "======================================"
    echo "Building Enhanced LaTeX..."
    echo "======================================"

    if command -v pdflatex >/dev/null 2>&1; then
        pdflatex -interaction=nonstopmode model-equations-enhanced.tex
        echo -e "${GREEN}✓${NC} Created: model-equations-enhanced.pdf"
    else
        docker run --rm -v "$PWD:/work" -w /work texlive/texlive:latest \
            pdflatex -interaction=nonstopmode model-equations-enhanced.tex
        echo -e "${GREEN}✓${NC} Created: model-equations-enhanced.pdf (via Docker)"
    fi

    # Clean up auxiliary files
    rm -f *.aux *.log *.out
    echo ""
fi

# 2. Build Manim animations
if [ "$MANIM_AVAILABLE" = true ]; then
    echo "======================================"
    echo "Building Manim Animations..."
    echo "======================================"

    echo "Rendering ColorKeyScene..."
    manim -ql --disable_caching manim_equations.py ColorKeyScene

    echo "Rendering BehavioralTriggerScene..."
    manim -ql --disable_caching manim_equations.py BehavioralTriggerScene

    echo "Rendering MotivationScene..."
    manim -ql --disable_caching manim_equations.py MotivationScene

    echo "Rendering FullDynamicsScene (high quality)..."
    manim -qh --disable_caching manim_equations.py FullDynamicsScene

    echo -e "${GREEN}✓${NC} Created: media/videos/manim_equations/*/*.mp4"
    echo ""
fi

# 3. Build Matplotlib visualization
if [ "$PYTHON_AVAILABLE" = true ]; then
    echo "======================================"
    echo "Building Matplotlib Visualization..."
    echo "======================================"

    # Check if matplotlib is available
    if python3 -c "import matplotlib" 2>/dev/null; then
        python3 matplotlib_equations.py
        echo -e "${GREEN}✓${NC} Created: nerdfit_equations_matplotlib.png"
        echo -e "${GREEN}✓${NC} Created: nerdfit_equations_matplotlib.pdf"
        echo -e "${GREEN}✓${NC} Created: equation_card_*.png"
    else
        echo -e "${RED}✗${NC} matplotlib not installed. Run: pip install matplotlib numpy"
        echo "   Skipping matplotlib visualization."
    fi
    echo ""
fi

# Summary
echo "======================================"
echo "Build Complete!"
echo "======================================"
echo ""
echo "Output files:"
if [ "$PDFLATEX_AVAILABLE" = true ]; then
    echo "  📄 model-equations-enhanced.pdf"
fi
if [ "$MANIM_AVAILABLE" = true ]; then
    echo "  🎬 media/videos/manim_equations/*/*.mp4"
fi
if [ "$PYTHON_AVAILABLE" = true ] && python3 -c "import matplotlib" 2>/dev/null; then
    echo "  📊 nerdfit_equations_matplotlib.{png,pdf}"
    echo "  📊 equation_card_*.png"
fi
echo ""
echo "See README.md for usage instructions."
