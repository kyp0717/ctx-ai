#!/bin/bash

# Interactive Brokers Gateway Installation Helper Script
# This script assists with downloading and installing IB Gateway

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_info "Detected OS: $OS"
}

# Function to check Java installation
check_java() {
    print_info "Checking Java installation..."
    
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
        print_success "Java found: version $JAVA_VERSION"
        
        # Check if Java version is 8 or higher
        MAJOR_VERSION=$(echo $JAVA_VERSION | cut -d'.' -f1)
        if [[ $MAJOR_VERSION -lt 8 ]] && [[ $MAJOR_VERSION != "1" ]]; then
            print_warning "Java 8 or higher is recommended for IB Gateway"
        fi
    else
        print_error "Java is not installed!"
        print_info "Please install Java 8 or higher before proceeding."
        
        if [[ "$OS" == "linux" ]]; then
            print_info "For Ubuntu/Debian: sudo apt-get install openjdk-11-jre"
            print_info "For RHEL/CentOS: sudo yum install java-11-openjdk"
        elif [[ "$OS" == "macos" ]]; then
            print_info "Download from: https://www.oracle.com/java/technologies/downloads/"
        fi
        exit 1
    fi
}

# Function to download IB Gateway
download_ibgateway() {
    print_info "Downloading IB Gateway..."
    
    DOWNLOAD_DIR="$HOME/Downloads"
    mkdir -p "$DOWNLOAD_DIR"
    
    if [[ "$OS" == "linux" ]]; then
        # Direct download URL for Linux (this URL may change, user should verify)
        DOWNLOAD_URL="https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-linux-x64.sh"
        INSTALLER_FILE="$DOWNLOAD_DIR/ibgateway-latest-standalone-linux-x64.sh"
        
        if [[ -f "$INSTALLER_FILE" ]]; then
            print_warning "Installer already exists at $INSTALLER_FILE"
            read -p "Do you want to download again? (y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return 0
            fi
        fi
        
        print_info "Downloading from Interactive Brokers..."
        if command -v wget &> /dev/null; then
            wget -O "$INSTALLER_FILE" "$DOWNLOAD_URL"
        elif command -v curl &> /dev/null; then
            curl -L -o "$INSTALLER_FILE" "$DOWNLOAD_URL"
        else
            print_error "Neither wget nor curl is installed. Please install one of them."
            exit 1
        fi
        
        if [[ -f "$INSTALLER_FILE" ]]; then
            chmod +x "$INSTALLER_FILE"
            print_success "IB Gateway installer downloaded to: $INSTALLER_FILE"
        else
            print_error "Failed to download IB Gateway installer"
            print_info "Please download manually from: https://www.interactivebrokers.com/en/index.php?f=16457"
            exit 1
        fi
        
    else
        print_info "Please download IB Gateway manually for your OS from:"
        print_info "https://www.interactivebrokers.com/en/index.php?f=16457"
        print_info "After downloading, run this script again to continue with installation."
        exit 0
    fi
}

# Function to install IB Gateway
install_ibgateway() {
    print_info "Installing IB Gateway..."
    
    if [[ "$OS" == "linux" ]]; then
        INSTALLER_FILE="$HOME/Downloads/ibgateway-latest-standalone-linux-x64.sh"
        
        if [[ ! -f "$INSTALLER_FILE" ]]; then
            print_error "Installer not found at: $INSTALLER_FILE"
            print_info "Please run the download step first."
            exit 1
        fi
        
        print_info "Running IB Gateway installer..."
        print_info "Please follow the installation wizard."
        print_info "Default installation path: ~/Jts/"
        
        # Run the installer
        "$INSTALLER_FILE"
        
        # Check if installation was successful
        if [[ -d "$HOME/Jts" ]]; then
            print_success "IB Gateway installed successfully!"
            
            # Find the actual installation directory
            GATEWAY_DIR=$(find "$HOME/Jts" -name "ibgateway" -type d | head -n 1)
            if [[ -n "$GATEWAY_DIR" ]]; then
                print_info "IB Gateway location: $GATEWAY_DIR"
            fi
        else
            print_warning "Could not verify IB Gateway installation."
            print_info "Please check if it was installed to a custom location."
        fi
        
    else
        print_info "Please run the downloaded installer for your OS."
    fi
}

# Function to create desktop shortcut (Linux only)
create_shortcut() {
    if [[ "$OS" != "linux" ]]; then
        return 0
    fi
    
    print_info "Creating desktop shortcut..."
    
    DESKTOP_FILE="$HOME/.local/share/applications/ibgateway.desktop"
    GATEWAY_EXEC=$(find "$HOME/Jts" -name "ibgateway" -type f -executable 2>/dev/null | head -n 1)
    
    if [[ -z "$GATEWAY_EXEC" ]]; then
        print_warning "Could not find IB Gateway executable"
        return 1
    fi
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=IB Gateway
Comment=Interactive Brokers Gateway
Exec=$GATEWAY_EXEC
Icon=$HOME/Jts/ibgateway/icon.png
Terminal=false
Categories=Finance;Trading;
EOF
    
    chmod +x "$DESKTOP_FILE"
    print_success "Desktop shortcut created"
}

# Function to configure IB Gateway
configure_ibgateway() {
    print_info "IB Gateway Configuration Instructions:"
    echo
    print_info "1. Launch IB Gateway"
    print_info "2. Login with your IB credentials"
    print_info "3. Go to Configure → Settings → API → Settings"
    print_info "4. Enable 'Enable ActiveX and Socket Clients'"
    print_info "5. Configure Socket port:"
    print_info "   - Paper Trading: 7497 (default)"
    print_info "   - Live Trading: 7496 (default)"
    print_info "6. Add '127.0.0.1' to trusted IP addresses"
    print_info "7. (Optional) Enable 'Read-Only API' for safety"
    echo
    print_info "For detailed configuration, see: ctx-ai/ibgateway_install_guide.md"
}

# Function to test connection
test_connection() {
    print_info "Testing IB Gateway connection..."
    
    # Check if Python and ibapi are available
    if command -v python3 &> /dev/null; then
        python3 -c "import ibapi" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            print_info "Testing connection to IB Gateway on port 7497..."
            
            # Create a simple test script
            cat > /tmp/test_ibgateway.py << 'EOF'
import socket
import sys

def test_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

if test_port("127.0.0.1", 7497):
    print("SUCCESS: IB Gateway is running on port 7497")
    sys.exit(0)
elif test_port("127.0.0.1", 7496):
    print("SUCCESS: IB Gateway is running on port 7496")
    sys.exit(0)
else:
    print("WARNING: IB Gateway does not appear to be running")
    print("Please start IB Gateway and ensure API is enabled")
    sys.exit(1)
EOF
            
            python3 /tmp/test_ibgateway.py
            rm -f /tmp/test_ibgateway.py
        else
            print_warning "ibapi package not installed. Skipping connection test."
            print_info "Install ibapi using: ./install_ibapi.sh"
        fi
    else
        print_warning "Python not found. Skipping connection test."
    fi
}

# Main menu
show_menu() {
    echo
    echo "========================================="
    echo "   IB Gateway Installation Helper"
    echo "========================================="
    echo "1. Check system requirements"
    echo "2. Download IB Gateway"
    echo "3. Install IB Gateway"
    echo "4. Configure IB Gateway (show instructions)"
    echo "5. Test connection"
    echo "6. Complete installation (all steps)"
    echo "0. Exit"
    echo "========================================="
    echo
}

# Main script execution
main() {
    detect_os
    
    while true; do
        show_menu
        read -p "Enter your choice [0-6]: " choice
        
        case $choice in
            1)
                check_java
                ;;
            2)
                download_ibgateway
                ;;
            3)
                install_ibgateway
                create_shortcut
                ;;
            4)
                configure_ibgateway
                ;;
            5)
                test_connection
                ;;
            6)
                print_info "Running complete installation..."
                check_java
                download_ibgateway
                install_ibgateway
                create_shortcut
                configure_ibgateway
                test_connection
                print_success "Installation process complete!"
                ;;
            0)
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Run main function
main