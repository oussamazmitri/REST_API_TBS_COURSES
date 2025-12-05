FROM python:3.13.7

# Expose Flask port
EXPOSE 5000

# Set working directory
WORKDIR /app

# Copy only requirements first (for Docker caching)
COPY requirements.txt .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Command to start Flask
CMD ["flask", "run", "--host", "0.0.0.0"]