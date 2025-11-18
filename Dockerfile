# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy your script and any required files
COPY unit_converter.py .

# Install dependencies (if your script uses any external packages)
# For example, if you use 'pint' for unit conversion:
RUN pip install --no-cache-dir pint

# Default command: runs the script with arguments
# You can override these when running 'docker run'
ENTRYPOINT ["python", "unit_converter.py"]

# Optional: provide default arguments (these can be replaced at runtime)
CMD ["--value", "10", "--from_unit", "cm", "--to_unit", "m"]
