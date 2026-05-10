# Nerdfit Model Equation Visualizations

This directory contains multiple visualization approaches for the Nerdfit behavioral dynamics equations, with improved color coding, typography, and layout.

## Available Visualizations

### 1. **Original LaTeX** (`model-equations.tex`)
- Basic color-coded equations in LaTeX
- Multi-page PDF with one equation per page
- Minimal styling

### 2. **Enhanced LaTeX** (`model-equations-enhanced.tex`) ⭐ RECOMMENDED for static
- Significantly improved visual hierarchy
- Card-based layout with shadows and rounded corners
- Better spacing and organization
- Phenomenon tags for quick reference
- Highlighted important equations (motivation, complexity)
- Single-page comprehensive view

### 3. **Manim Animation** (`manim_equations.py`) ⭐ RECOMMENDED for presentations
- Animated equation building
- Shows dependencies and flow
- Multiple scenes:
  - `ColorKeyScene`: Introduction to color coding
  - `BehavioralTriggerScene`: Step-by-step trigger equation
  - `MotivationScene`: Motivation components
  - `FullDynamicsScene`: Complete system overview
- Perfect for talks and presentations

### 4. **Matplotlib/Python** (`matplotlib_equations.py`)
- Rich typography with LaTeX rendering
- Programmatic control over layout
- High-resolution PNG and PDF output
- Individual equation cards available
- Best for fine-tuned adjustments

## Installation

### LaTeX (for options 1 & 2)
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Or use Docker (no installation needed)
docker pull texlive/texlive:latest
```

### Manim (for option 3)
```bash
# Install manim
pip install manim

# Or with conda
conda install -c conda-forge manim

# Verify installation
manim --version
```

### Matplotlib (for option 4)
```bash
# Install matplotlib with LaTeX support
pip install matplotlib numpy

# You'll also need LaTeX installed (see above)
```

## Usage

### Enhanced LaTeX (Recommended Static)
```bash
cd writing/model-equations

# Compile with pdflatex
pdflatex model-equations-enhanced.tex

# Or use the build script
./compile-figures.sh

# Or with Docker (no local LaTeX install needed)
docker run --rm -v "$PWD:/work" -w /work texlive/texlive:latest \
  pdflatex model-equations-enhanced.tex

# Output: model-equations-enhanced.pdf
```

### Manim Animations
```bash
cd writing/model-equations

# Render all scenes in low quality (fast preview)
manim -pql manim_equations.py ColorKeyScene
manim -pql manim_equations.py BehavioralTriggerScene
manim -pql manim_equations.py MotivationScene
manim -pql manim_equations.py FullDynamicsScene

# Render high quality for presentations
manim -pqh manim_equations.py FullDynamicsScene

# Render 4K for publications
manim -pqk manim_equations.py FullDynamicsScene

# Output: media/videos/manim_equations/[quality]/[SceneName].mp4
```

### Matplotlib Visualization
```bash
cd writing/model-equations

# Run the script
python matplotlib_equations.py

# Output:
#   - nerdfit_equations_matplotlib.png (high-res PNG)
#   - nerdfit_equations_matplotlib.pdf (vector PDF)
#   - equation_card_*.png (individual cards)
```

## Quick Start: Build Everything
```bash
cd writing/model-equations
./build-all.sh
```

## Comparison

| Feature | Original LaTeX | Enhanced LaTeX | Manim | Matplotlib |
|---------|---------------|----------------|-------|------------|
| **Visual Quality** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Static Output** | ✅ | ✅ | ❌ | ✅ |
| **Animation** | ❌ | ❌ | ✅ | ❌ |
| **Easy to Modify** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **File Size** | Small | Medium | Large | Medium |
| **Best For** | Quick reference | Papers/docs | Presentations | Fine-tuned figures |

## Customization

### Changing Colors
All visualizations use the same color palette defined at the top of each file:
- `st` (#1B2631): State variables
- `hb` (#1B7F6A): Habit & automaticity
- `mv` (#C45C26): Motivation & reward
- `ef` (#5C4D8A): Effort / opportunity cost
- etc.

Edit the color definitions in the respective files to change the palette.

### Adding/Removing Equations
- **LaTeX**: Edit the tikzpicture blocks
- **Manim**: Create new Scene classes or modify existing ones
- **Matplotlib**: Add items to the `create_full_visualization()` function

## Troubleshooting

### LaTeX: "File not found" errors
- Install missing packages: `sudo tlmgr install <package-name>`
- Or use the full texlive distribution

### Manim: Import errors
- Ensure you have `manim` not `manimgl`
- Check version: `manim --version` (should be 0.17+)

### Matplotlib: LaTeX not rendering
- Verify LaTeX is installed: `which pdflatex`
- Check matplotlib config: `plt.rcParams['text.usetex']` should be `True`
- Install dvipng: `sudo apt-get install dvipng` (Linux) or `brew install dvipng` (macOS)

## Examples

### Create a presentation slide deck
```bash
# 1. Render Manim scenes
manim -pqh manim_equations.py FullDynamicsScene

# 2. Extract frames from video
ffmpeg -i media/videos/manim_equations/1080p60/FullDynamicsScene.mp4 \
  -vf "select='eq(n,0)+eq(n,120)+eq(n,240)'" \
  -vsync vfr frame_%03d.png

# 3. Or use the enhanced LaTeX PDF directly in your slides
```

### Create a figure for a paper
```bash
# Option 1: Enhanced LaTeX (vector, publication-ready)
pdflatex model-equations-enhanced.tex
# Include in LaTeX document: \includegraphics{model-equations-enhanced.pdf}

# Option 2: Matplotlib (more control)
python matplotlib_equations.py
# Use nerdfit_equations_matplotlib.pdf
```

## License

These visualizations are part of the Nerdfit project. See main repository for license information.
