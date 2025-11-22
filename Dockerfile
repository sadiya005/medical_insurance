# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy all folders
COPY fastapi ./fastapi
COPY streamlit ./streamlit
COPY model ./model

# Expose both ports
EXPOSE 8000
EXPOSE 8501

# Run both FastAPI and Streamlit inside same container
CMD ["bash", "-c", "cd fastapi && uvicorn main:app --host 0.0.0.0 --port 8000 & cd streamlit && streamlit run main.py --server.port=8501 --server.address=0.0.0.0"]
