FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# # Optional, just for docs
EXPOSE 8080

# # Run Streamlit app (use $PORT)
# # This one is for GCP
CMD streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0


# # ----->>>>>  This is LOCALTESTING ONLY <<<<<<< -----

# # Expose Streamlit's default port
# EXPOSE 8501

# # Set environment variables for Streamlit (optional, for cloud)
# ENV PORT=8501
# ENV STREAMLIT_SERVER_PORT=8501
# ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
