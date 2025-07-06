@echo off
echo 🚀 Starting Techline Custom Agent Services
echo.

echo 📡 Starting FastAPI server on port 8000...
start "FastAPI Server" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak > nul

echo 🎨 Starting Streamlit GUI on port 8501...
start "Streamlit GUI" cmd /k "streamlit run streamlit_app.py --server.port 8501"

echo.
echo ✅ Services started!
echo 📡 API: http://localhost:8000
echo 🎨 GUI: http://localhost:8501
echo.
echo Press any key to continue...
pause > nul
