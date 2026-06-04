FROM python:3.10-slim

# Install system dependencies for reportlab and kaleido
RUN apt-get update && apt-get install -y \
    build-essential \
    libnss3 \
    libexpat1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces require running as a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

# Copy the requirements file from the solar_app directory
COPY --chown=user:user solar_app/requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY --chown=user:user . .

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Command to run the Streamlit application
CMD ["streamlit", "run", "solar_app/app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false"]
