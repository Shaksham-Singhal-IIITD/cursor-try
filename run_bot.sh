#!/bin/bash

# Sales Page Quick-Answer & Lead Bot Startup Script

echo "🤖 Starting Sales Page Quick-Answer & Lead Bot..."
echo "================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    pip3 install --break-system-packages -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your Python environment."
        exit 1
    fi
fi

echo "✅ Dependencies ready!"

# Create leads.json if it doesn't exist
if [ ! -f "leads.json" ]; then
    echo "📄 Creating leads.json file..."
    echo "[]" > leads.json
fi

echo "🚀 Starting Streamlit application..."
echo "🌐 The bot will be available at: http://localhost:8501"
echo "📖 Check README.md for usage instructions"
echo ""

# Run the application
python3 -m streamlit run sales_bot.py --server.port 8501 --server.headless false