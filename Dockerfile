# Use the official Microsoft Playwright image with Python 3.11/3.12 on Ubuntu Jammy
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# 1. Set the working directory inside the container
WORKDIR /app

# 2. Copy requirements first (to leverage Docker caching)
COPY requirement.txt .

# 3. Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# 4. Copy the rest of your framework code
COPY . .

# 5. Ensure Playwright browsers are installed (Chromium)
RUN playwright install chromium

# 6. Default command: Run all tests in parallel
# We don't use --headed here because Docker containers are headless by default
CMD ["pytest", "-n", "auto"]