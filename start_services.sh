#!/bin/bash

echo "🚀 Starting Techline Custom Agent Services"
echo

echo "📡 Starting FastAPI server on port 8000..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

echo "⏳ Waiting for API to start..."
sleep 5

echo "🎨 Starting Streamlit GUI on port 8501..."
streamlit run streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

echo
echo "✅ Services started!"
echo "📡 API: http://localhost:8000"
echo "🎨 GUI: http://localhost:8501"
echo
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo
    echo "🛑 Stopping services..."
    kill $API_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    echo "✅ Services stopped."
    exit 0
}

# Set trap to cleanup on interrupt
trap cleanup INT

# Wait for user interrupt
while true; do
    sleep 1
done
