#!/bin/bash
# Setup script for Quake3Arena development environment

set -e

echo "=========================================="
echo "Quake3Arena Development Setup"
echo "=========================================="
echo ""

# Check Python installation
echo "[1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found. Please install Python 3.11 or higher."
    exit 1
fi

# Install Python dependencies
echo ""
echo "[2/4] Installing Python dependencies..."
cd Tools/ProceduralGeneration
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Run tests
echo ""
echo "[3/4] Running unit tests..."
python3 -m pytest test_arena_generator.py -v
echo "✓ All tests passed"

# Generate assets
echo ""
echo "[4/4] Generating procedural assets..."
python3 generate_all.py
echo "✓ Assets generated"

# Back to root
cd ../..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Generated assets are in: Tools/ProceduralGeneration/"
echo ""
echo "Next steps:"
echo "  1. Open Unreal3Arena.uproject in Unreal Engine 5.7"
echo "  2. Build the project (Development Editor configuration)"
echo "  3. Enable the Quake3Arena plugin if needed"
echo "  4. Create a level and add ArenaGeometryImporter actor"
echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - Plugins/GameFeatures/Quake3Arena/README.md"
echo "  - Tools/ProceduralGeneration/README.md"
echo ""
