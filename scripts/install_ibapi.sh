#!/bin/bash

# Interactive Brokers API (ibapi) Installation Script
# This script helps install the ibapi package from the TWS API download

set -e  # Exit on error

echo "========================================"
echo "Interactive Brokers API Installation"
echo "========================================"
echo ""

# Define possible TWS API locations
TWS_API_PATHS=(
    "$HOME/Downloads/twsapi/IBJts/source/pythonclient"
    "$HOME/Downloads/TWS_API/source/pythonclient"
    "$HOME/Downloads/twsapi_macunix/IBJts/source/pythonclient"
    "$HOME/Downloads/twsapi_linux/IBJts/source/pythonclient"
)

# Find the TWS API installation path
INSTALL_PATH=""
for path in "${TWS_API_PATHS[@]}"; do
    if [ -d "$path" ]; then
        INSTALL_PATH="$path"
        echo "✓ Found TWS API at: $INSTALL_PATH"
        break
    fi
done

if [ -z "$INSTALL_PATH" ]; then
    echo "❌ TWS API not found in expected locations."
    echo ""
    echo "Please download TWS API from:"
    echo "https://www.interactivebrokers.com/en/index.php?f=5041"
    echo ""
    echo "Expected locations:"
    for path in "${TWS_API_PATHS[@]}"; do
        echo "  - $path"
    done
    echo ""
    echo "After downloading and extracting, run this script again."
    exit 1
fi

# Check for virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Try to activate virtual environment if it exists
    if [ -f ".venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    else
        echo "⚠️  Warning: No virtual environment detected."
        echo "It's recommended to install in a virtual environment."
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            exit 1
        fi
    fi
fi

# Install ibapi using uv if available, otherwise use pip
if command -v uv &> /dev/null; then
    echo "Installing ibapi using uv..."
    uv pip install "$INSTALL_PATH"
else
    echo "Installing ibapi using pip..."
    pip install "$INSTALL_PATH"
fi

# Verify installation
echo ""
echo "Verifying installation..."
if python -c "import ibapi; print(f'✓ ibapi version {ibapi.__version__} installed successfully')" 2>/dev/null; then
    echo ""
    echo "========================================"
    echo "Installation Complete!"
    echo "========================================"
    echo ""
    echo "You can now use the Interactive Brokers API in your Python code."
    echo "Make sure TWS or IB Gateway is running with API connections enabled."
    echo ""
else
    echo "❌ Installation verification failed."
    echo "Please check the installation manually."
    exit 1
fi