# 1. Use an official Python runtime (matching 3.11/3.12 environment)
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy the requirements file we already have
COPY requirements.txt .

# 4. Install all the specific versions from file
# --no-cache-dir keeps the Docker image small and fast
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project folders (src, data, etc.)
COPY . .

# 6. Run the master pipeline
CMD ["python", "run_pipeline.py"]