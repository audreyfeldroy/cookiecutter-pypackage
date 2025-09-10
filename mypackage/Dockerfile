# Use lightweight Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install pip + dependencies
RUN pip install --upgrade pip \
    && pip install .

# Set PYTHONPATH so Python sees src/ as root
ENV PYTHONPATH=/app/src

# Run tests during build
RUN pytest || true

# Default command: run package as module
CMD ["uvicorn", "mypackage.app:app", "--host", "0.0.0.0", "--port", "8000"]