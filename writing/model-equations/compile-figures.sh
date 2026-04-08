#!/usr/bin/env bash
# Build model-equations.pdf (multi-page: color key + one equation card per page).
set -euo pipefail
cd "$(dirname "$0")"
if command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode model-equations.tex
else
  docker run --rm -v "$PWD:/work" -w /work texlive/texlive:latest \
    pdflatex -interaction=nonstopmode model-equations.tex
fi
