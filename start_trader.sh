#!/bin/bash

# NIFTY AUTO TRADER - Startup Script
# Usage: ./start_trader.sh

echo "========================================="
echo "  NIFTY AUTO TRADER - STARTING..."
echo "========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found!"
    echo "Please install Python 3.9+"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"
echo ""

# Check if required packages are installed
echo "🔍 Checking dependencies..."
REQUIRED_PACKAGES="pyotp requests pandas numpy reportlab smartapi-python"
MISSING_PACKAGES=""

for package in $REQUIRED_PACKAGES; do
    if ! pip3 show "$package" &> /dev/null; then
        MISSING_PACKAGES="$MISSING_PACKAGES $package"
    fi
done

if [ ! -z "$MISSING_PACKAGES" ]; then
    echo "❌ Missing packages:$MISSING_PACKAGES"
    echo ""
    echo "Install with:"
    echo "pip3 install$MISSING_PACKAGES"
    exit 1
fi

echo "✅ All dependencies installed"
echo ""

# Check for log file
if [ -f "trader.log" ]; then
    LOG_SIZE=$(du -h trader.log | cut -f1)
    echo "📋 Log file exists (size: $LOG_SIZE)"
else
    echo "📋 New log file will be created"
fi

echo ""
echo "========================================="
echo "  STARTING NIFTY AUTO TRADER GUI"
echo "========================================="
echo ""
echo "⚠️  IMPORTANT REMINDERS:"
echo "   1. Test in PAPER mode first!"
echo "   2. LIVE mode uses REAL MONEY"
echo "   3. Keep Mac awake during trading hours"
echo "   4. Monitor Telegram for alerts"
echo ""
echo "🕐 Market Hours: 9:15 AM - 3:30 PM"
echo "📱 Telegram commands: /start /stop /status /report"
echo ""
echo "========================================="
echo ""

# Start the application
python3 main_consolidated.py

echo ""
echo "========================================="
echo "  TRADER STOPPED"
echo "========================================="
