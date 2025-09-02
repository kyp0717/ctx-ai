# Interactive Brokers Gateway Installation Guide

## Overview
IB Gateway is a lightweight alternative to TWS (Trader Workstation) designed specifically for API connections. It provides the same API functionality as TWS but without the GUI trading interface, making it ideal for automated trading systems.

## System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Java**: Java Runtime Environment (JRE) 8 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Network**: Stable internet connection

## Download and Installation

### Step 1: Download IB Gateway

1. Visit the Interactive Brokers Software page:
   https://www.interactivebrokers.com/en/index.php?f=16457

2. Select "IB Gateway" from the software options

3. Choose your operating system:
   - **Windows**: Download the .exe installer
   - **macOS**: Download the .dmg installer  
   - **Linux**: Download the standalone .sh installer

### Step 2: Install IB Gateway

#### For Linux:
```bash
# Make the installer executable
chmod +x ibgateway-latest-standalone-linux-x64.sh

# Run the installer
./ibgateway-latest-standalone-linux-x64.sh

# Follow the installation wizard
# Default installation path: ~/Jts/
```

#### For macOS:
1. Open the downloaded .dmg file
2. Drag IB Gateway to Applications folder
3. Launch from Applications

#### For Windows:
1. Run the downloaded .exe installer
2. Follow the installation wizard
3. Default installation path: C:\Jts\

### Step 3: Configure IB Gateway

1. **Launch IB Gateway**
   ```bash
   # Linux (from installation directory)
   ~/Jts/ibgateway/[version]/ibgateway
   
   # Or use the desktop shortcut created during installation
   ```

2. **Login Configuration**:
   - Choose between Live Trading and Paper Trading
   - Enter your IB username and password
   - Select API mode (not Trading mode)

3. **API Settings Configuration**:
   - Click on "Configure" → "Settings" → "API" → "Settings"
   - Enable "Enable ActiveX and Socket Clients"
   - Configure Socket port:
     - Paper Trading: 7497 (default)
     - Live Trading: 7496 (default)
   - Add trusted IP addresses:
     - Add "127.0.0.1" for localhost connections
     - Add specific IPs if connecting from remote machines
   - Optional: Enable "Read-Only API" for safety during development

4. **Additional Settings**:
   - **Master API Client ID**: Leave blank or set to specific ID
   - **Timeout for Inactive API**: Set to 0 to disable timeout
   - **Create API message log file**: Enable for debugging

## Running IB Gateway

### Manual Start:
```bash
# Linux
~/Jts/ibgateway/[version]/ibgateway

# macOS
open -a "IB Gateway"

# Windows
# Use desktop shortcut or Start menu
```

### Headless/Server Mode:
For running on servers without GUI:
```bash
# Linux headless mode
xvfb-run -a ~/Jts/ibgateway/[version]/ibgateway -mode=paper
```

## Connection Ports

| Mode | Default Port | Description |
|------|-------------|-------------|
| Paper Trading | 7497 | For testing and development |
| Live Trading | 7496 | For production trading |
| FIX CTCI | 4001 | FIX protocol connections |

## Verification

### Test Connection:
```python
# Quick connection test
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        
    def error(self, reqId, errorCode, errorString):
        print(f"Error: {reqId} - {errorCode} - {errorString}")
        
    def nextValidId(self, orderId):
        print(f"Connected! Next Valid Order ID: {orderId}")
        self.disconnect()

def run_test():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=0)  # Paper trading port
    app.run()

if __name__ == "__main__":
    run_test()
```

## Auto-Start Configuration

### Linux (systemd):
Create a service file `/etc/systemd/system/ibgateway.service`:
```ini
[Unit]
Description=Interactive Brokers Gateway
After=network.target

[Service]
Type=simple
User=your_username
ExecStart=/home/your_username/Jts/ibgateway/[version]/ibgateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ibgateway
sudo systemctl start ibgateway
```

## Troubleshooting

### Common Issues:

1. **Java Not Found**:
   ```bash
   # Install Java 8 or higher
   sudo apt-get install openjdk-11-jre  # Ubuntu/Debian
   ```

2. **Connection Refused**:
   - Verify IB Gateway is running
   - Check API is enabled in settings
   - Confirm correct port (7497 for paper, 7496 for live)
   - Check firewall settings

3. **Authentication Failed**:
   - Verify username/password
   - Check if 2FA is required
   - Ensure account has API permissions

4. **Gateway Crashes**:
   - Increase Java heap size in ibgateway.vmoptions
   - Check system resources (RAM, CPU)

## Security Best Practices

1. **Use Read-Only API** during development
2. **Restrict IP addresses** to trusted sources only
3. **Use paper trading account** for testing
4. **Enable API message logging** for audit trail
5. **Set appropriate timeout** for inactive connections
6. **Use unique Client IDs** for different applications
7. **Never expose API ports** to public internet

## Differences: IB Gateway vs TWS

| Feature | IB Gateway | TWS |
|---------|-----------|-----|
| GUI Interface | Minimal | Full trading interface |
| Resource Usage | Low (~200MB RAM) | High (~1GB+ RAM) |
| API Support | Full | Full |
| Charts/Research | No | Yes |
| Manual Trading | No | Yes |
| Best For | Automated systems | Manual + automated |

## Next Steps

After installing IB Gateway:
1. Test connection with the verification script above
2. Configure your trading application to connect
3. Start with paper trading account
4. Implement proper error handling
5. Set up monitoring and alerts