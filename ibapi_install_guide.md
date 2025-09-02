# Interactive Brokers API (ibapi) Installation Guide

## Overview
The `ibapi` package is Interactive Brokers' official Python API that cannot be installed via pip/PyPI. It must be downloaded directly from Interactive Brokers and installed manually.

## Installation Steps

### 1. Download TWS API
1. Visit: https://www.interactivebrokers.com/en/index.php?f=5041
2. Click on "TWS API Stable" (or "TWS API Latest" for newest features)
3. Download the appropriate version for your operating system

### 2. Extract the Archive
```bash
# For Linux/Mac (assuming downloaded to ~/Downloads)
cd ~/Downloads
unzip twsapi_macunix.*.zip  # or appropriate filename

# For Windows
# Extract using Windows Explorer or command line
```

### 3. Install ibapi Package
```bash
# Navigate to your project directory
cd /home/kelp/work/ibxpy-ai

# Activate virtual environment (if not already active)
# For bash/zsh:
source .venv/bin/activate

# For nushell:
overlay use .venv/bin/activate.nu

# For fish:
source .venv/bin/activate.fish

# Install ibapi from the extracted folder
# The package is typically located at:
uv pip install ~/Downloads/twsapi/IBJts/source/pythonclient/

# Or use the provided script (recommended)
./install_ibapi.sh
```

### 4. Verify Installation
```python
# Test import
python -c "import ibapi; print('ibapi installed successfully')"
```

## Alternative: Use the Installation Script
We've provided an installation helper script:
```bash
./install_ibapi.sh
```
This script will guide you through the installation process.

## Requirements
- TWS (Trader Workstation) or IB Gateway must be installed and running
- Default connection port: 7497 (paper trading: 7497, live trading: 7496)
- API connections must be enabled in TWS/Gateway settings

## Troubleshooting

### Common Issues:
1. **ModuleNotFoundError**: Ensure you're installing in the correct virtual environment
2. **Connection refused**: Check TWS is running and API is enabled
3. **Path not found**: Verify the extraction path matches installation command

### TWS Configuration:
1. Open TWS
2. File → Global Configuration → API → Settings
3. Enable "Enable ActiveX and Socket Clients"
4. Add "127.0.0.1" to trusted IPs
5. Set Socket port (default 7497 for paper trading)
