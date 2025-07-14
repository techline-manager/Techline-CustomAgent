FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional, just for docs
EXPOSE 8080

# Run Streamlit app (use $PORT)
CMD streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
