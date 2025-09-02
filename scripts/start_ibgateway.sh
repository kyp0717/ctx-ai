#!/bin/bash

# IBGateway Startup Script with Credential Management
# This script starts IB Gateway using stored credentials

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONFIG_DIR="$HOME/.ibxpy"
CREDENTIALS_FILE="$CONFIG_DIR/credentials.conf"
GATEWAY_LOG_DIR="$HOME/.ibxpy/logs"
GATEWAY_PID_FILE="$CONFIG_DIR/ibgateway.pid"

# Default settings
DEFAULT_TRADING_MODE="paper"  # paper or live
DEFAULT_PORT_PAPER="7497"
DEFAULT_PORT_LIVE="7496"

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

# Function to create config directory and files
setup_config() {
    if [[ ! -d "$CONFIG_DIR" ]]; then
        print_info "Creating configuration directory: $CONFIG_DIR"
        mkdir -p "$CONFIG_DIR"
        chmod 700 "$CONFIG_DIR"  # Secure permissions
    fi
    
    if [[ ! -d "$GATEWAY_LOG_DIR" ]]; then
        mkdir -p "$GATEWAY_LOG_DIR"
    fi
    
    if [[ ! -f "$CREDENTIALS_FILE" ]]; then
        print_info "Creating credentials template file"
        cat > "$CREDENTIALS_FILE" << 'EOF'
# IBGateway Credentials Configuration
# IMPORTANT: Keep this file secure with proper permissions (chmod 600)

# Trading Mode: paper or live
TRADING_MODE=paper

# IB Account Credentials
IB_USERNAME=
IB_PASSWORD=

# Optional: Second Factor Authentication (if enabled)
# Leave empty if not using 2FA
IB_2FA_METHOD=  # Options: IBKEY, SMS, VOICE
IB_2FA_DEVICE=  # Device name for IBKEY

# API Configuration
API_PORT_PAPER=7497
API_PORT_LIVE=7496
API_READONLY=false
API_MASTER_CLIENT_ID=

# Java Settings (Optional)
JAVA_HEAP_SIZE=1024m  # Memory allocation for IB Gateway

# Gateway Installation Path
# Automatically detected, but can be overridden
GATEWAY_PATH=

# Auto-restart on disconnect
AUTO_RESTART=true
RESTART_DELAY=10  # seconds

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
KEEP_LOGS_DAYS=30
EOF
        chmod 600 "$CREDENTIALS_FILE"  # Secure permissions
        
        print_warning "Please edit $CREDENTIALS_FILE with your IB credentials"
        print_info "File has been created with secure permissions (600)"
        return 1
    fi
    
    return 0
}

# Function to load credentials
load_credentials() {
    if [[ ! -f "$CREDENTIALS_FILE" ]]; then
        print_error "Credentials file not found: $CREDENTIALS_FILE"
        print_info "Run this script once to create the template"
        exit 1
    fi
    
    # Source the credentials file
    source "$CREDENTIALS_FILE"
    
    # Validate required fields
    if [[ -z "$IB_USERNAME" ]] || [[ -z "$IB_PASSWORD" ]]; then
        print_error "IB_USERNAME and IB_PASSWORD must be set in $CREDENTIALS_FILE"
        exit 1
    fi
    
    # Set defaults if not specified
    TRADING_MODE=${TRADING_MODE:-$DEFAULT_TRADING_MODE}
    API_PORT_PAPER=${API_PORT_PAPER:-$DEFAULT_PORT_PAPER}
    API_PORT_LIVE=${API_PORT_LIVE:-$DEFAULT_PORT_LIVE}
    JAVA_HEAP_SIZE=${JAVA_HEAP_SIZE:-1024m}
    AUTO_RESTART=${AUTO_RESTART:-true}
    RESTART_DELAY=${RESTART_DELAY:-10}
    LOG_LEVEL=${LOG_LEVEL:-INFO}
    
    # Set port based on trading mode
    if [[ "$TRADING_MODE" == "live" ]]; then
        API_PORT=$API_PORT_LIVE
        print_warning "LIVE TRADING MODE SELECTED - Be careful!"
    else
        API_PORT=$API_PORT_PAPER
        print_info "Paper trading mode selected (port $API_PORT)"
    fi
}

# Function to find IB Gateway installation
find_gateway() {
    if [[ -n "$GATEWAY_PATH" ]] && [[ -f "$GATEWAY_PATH" ]]; then
        print_info "Using configured Gateway path: $GATEWAY_PATH"
        return 0
    fi
    
    # Search common installation locations
    local search_paths=(
        "$HOME/Jts/ibgateway/*/ibgateway"
        "$HOME/Applications/IB Gateway.app/Contents/MacOS/ibgateway"
        "/Applications/IB Gateway.app/Contents/MacOS/ibgateway"
        "$HOME/IBGateway/ibgateway"
    )
    
    for pattern in "${search_paths[@]}"; do
        for path in $pattern; do
            if [[ -f "$path" ]]; then
                GATEWAY_PATH="$path"
                print_info "Found IB Gateway at: $GATEWAY_PATH"
                return 0
            fi
        done
    done
    
    print_error "Could not find IB Gateway installation"
    print_info "Please install IB Gateway or set GATEWAY_PATH in $CREDENTIALS_FILE"
    exit 1
}

# Function to check if gateway is already running
check_running() {
    if [[ -f "$GATEWAY_PID_FILE" ]]; then
        local pid=$(cat "$GATEWAY_PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            print_warning "IB Gateway is already running (PID: $pid)"
            return 0
        else
            # Clean up stale PID file
            rm -f "$GATEWAY_PID_FILE"
        fi
    fi
    
    # Also check if port is in use
    if netstat -tln 2>/dev/null | grep -q ":$API_PORT "; then
        print_warning "Port $API_PORT is already in use (IB Gateway may be running)"
        return 0
    fi
    
    return 1
}

# Function to create IBC configuration
create_ibc_config() {
    local ibc_config="$CONFIG_DIR/ibc_config.ini"
    
    cat > "$ibc_config" << EOF
# IBC Configuration for automated IB Gateway startup
# Generated by start_ibgateway.sh

# Login credentials
IbLoginId=$IB_USERNAME
IbPassword=$IB_PASSWORD
TradingMode=$TRADING_MODE

# 2FA Settings
SecondFactorAuthentication=$IB_2FA_METHOD
SecondFactorDevice=$IB_2FA_DEVICE

# Gateway settings
Gateway=true
MinimizeMainWindow=true
ExistingSessionDetectedAction=primaryoverride

# API Settings
OverrideTwsApiPort=$API_PORT
ReadOnlyApi=$API_READONLY
MasterClientID=$API_MASTER_CLIENT_ID
AcceptIncomingConnectionAction=accept

# Logging
LogToConsole=yes
LogLevel=$LOG_LEVEL

# Auto-restart
AutoRestartTime=
ClosedownAt=

# Diagnostics
DismissPasswordExpiryWarning=yes
DismissNSEComplianceNotice=yes
EOF
    
    chmod 600 "$ibc_config"
}

# Function to start IB Gateway
start_gateway() {
    print_info "Starting IB Gateway..."
    
    # Create log file with timestamp
    local log_file="$GATEWAY_LOG_DIR/ibgateway_$(date +%Y%m%d_%H%M%S).log"
    
    # Set Java options
    export JAVA_OPTS="-Xmx${JAVA_HEAP_SIZE} -XX:+UseG1GC"
    
    # Start IB Gateway in background
    if [[ "$TRADING_MODE" == "paper" ]]; then
        mode_flag="--mode=paper"
    else
        mode_flag="--mode=live"
    fi
    
    # Check if we should use IBC for automation
    local ibc_path="$HOME/ibc"
    if [[ -d "$ibc_path" ]]; then
        print_info "Using IBC for automated login"
        create_ibc_config
        # Start with IBC
        "$ibc_path/scripts/ibcstart.sh" \
            "$GATEWAY_PATH" \
            --ibc-ini="$CONFIG_DIR/ibc_config.ini" \
            --user="$IB_USERNAME" \
            --pw="$IB_PASSWORD" \
            --mode="$TRADING_MODE" \
            > "$log_file" 2>&1 &
    else
        # Start without IBC (manual login required)
        print_warning "IBC not found - manual login will be required"
        "$GATEWAY_PATH" $mode_flag > "$log_file" 2>&1 &
    fi
    
    local pid=$!
    echo $pid > "$GATEWAY_PID_FILE"
    
    print_info "IB Gateway starting (PID: $pid)"
    print_info "Log file: $log_file"
    
    # Wait for gateway to be ready
    print_info "Waiting for IB Gateway to be ready..."
    local max_wait=30
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        if netstat -tln 2>/dev/null | grep -q ":$API_PORT "; then
            print_success "IB Gateway is ready on port $API_PORT"
            return 0
        fi
        sleep 1
        waited=$((waited + 1))
        echo -n "."
    done
    
    echo
    print_warning "IB Gateway may not be fully ready yet"
    print_info "Check the log file for details: $log_file"
}

# Function to stop IB Gateway
stop_gateway() {
    if [[ -f "$GATEWAY_PID_FILE" ]]; then
        local pid=$(cat "$GATEWAY_PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            print_info "Stopping IB Gateway (PID: $pid)..."
            kill "$pid"
            sleep 2
            
            # Force kill if still running
            if ps -p "$pid" > /dev/null 2>&1; then
                print_warning "Force stopping IB Gateway..."
                kill -9 "$pid"
            fi
            
            rm -f "$GATEWAY_PID_FILE"
            print_success "IB Gateway stopped"
        else
            print_info "IB Gateway is not running"
            rm -f "$GATEWAY_PID_FILE"
        fi
    else
        print_info "IB Gateway is not running"
    fi
}

# Function to restart IB Gateway
restart_gateway() {
    stop_gateway
    sleep 2
    start_gateway
}

# Function to show status
show_status() {
    if [[ -f "$GATEWAY_PID_FILE" ]]; then
        local pid=$(cat "$GATEWAY_PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            print_success "IB Gateway is running (PID: $pid)"
            
            # Check port
            if netstat -tln 2>/dev/null | grep -q ":$API_PORT "; then
                print_success "API is available on port $API_PORT"
            else
                print_warning "API port $API_PORT is not listening"
            fi
            
            # Show memory usage
            local mem=$(ps -o rss= -p "$pid" | awk '{print int($1/1024) "MB"}')
            print_info "Memory usage: $mem"
            
            return 0
        fi
    fi
    
    print_info "IB Gateway is not running"
    return 1
}

# Function to monitor and auto-restart
monitor_gateway() {
    print_info "Starting IB Gateway monitor..."
    print_info "Press Ctrl+C to stop monitoring"
    
    while true; do
        if ! show_status > /dev/null 2>&1; then
            if [[ "$AUTO_RESTART" == "true" ]]; then
                print_warning "IB Gateway is not running. Restarting in $RESTART_DELAY seconds..."
                sleep "$RESTART_DELAY"
                start_gateway
            else
                print_error "IB Gateway is not running. Auto-restart is disabled."
                exit 1
            fi
        fi
        sleep 30  # Check every 30 seconds
    done
}

# Function to show logs
show_logs() {
    local latest_log=$(ls -t "$GATEWAY_LOG_DIR"/ibgateway_*.log 2>/dev/null | head -n 1)
    
    if [[ -n "$latest_log" ]]; then
        print_info "Showing latest log: $latest_log"
        tail -f "$latest_log"
    else
        print_warning "No log files found"
    fi
}

# Function to clean old logs
clean_logs() {
    if [[ -n "$KEEP_LOGS_DAYS" ]] && [[ "$KEEP_LOGS_DAYS" -gt 0 ]]; then
        print_info "Cleaning logs older than $KEEP_LOGS_DAYS days..."
        find "$GATEWAY_LOG_DIR" -name "ibgateway_*.log" -mtime +$KEEP_LOGS_DAYS -delete
        print_success "Old logs cleaned"
    fi
}

# Main script
main() {
    case "${1:-}" in
        start)
            setup_config && load_credentials
            find_gateway
            if check_running; then
                print_info "Use 'restart' to restart IB Gateway"
                exit 0
            fi
            start_gateway
            clean_logs
            ;;
        stop)
            stop_gateway
            ;;
        restart)
            setup_config && load_credentials
            find_gateway
            restart_gateway
            clean_logs
            ;;
        status)
            setup_config && load_credentials
            show_status
            ;;
        monitor)
            setup_config && load_credentials
            find_gateway
            monitor_gateway
            ;;
        logs)
            show_logs
            ;;
        setup)
            setup_config
            if [[ $? -eq 1 ]]; then
                print_info "Edit the credentials file and run: $0 start"
            fi
            ;;
        *)
            echo "IB Gateway Startup Script"
            echo
            echo "Usage: $0 {start|stop|restart|status|monitor|logs|setup}"
            echo
            echo "Commands:"
            echo "  start    - Start IB Gateway with stored credentials"
            echo "  stop     - Stop running IB Gateway"
            echo "  restart  - Restart IB Gateway"
            echo "  status   - Show current status"
            echo "  monitor  - Monitor and auto-restart if needed"
            echo "  logs     - Show latest log file"
            echo "  setup    - Create configuration files"
            echo
            echo "First time setup:"
            echo "  1. Run: $0 setup"
            echo "  2. Edit: $CREDENTIALS_FILE"
            echo "  3. Run: $0 start"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"