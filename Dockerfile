FROM python:3.13-slim

WORKDIR /app

# Install dependencies first (for caching)
COPY pyproject.toml .
RUN pip install build

# Install dev dependencies
RUN pip install pytest pylint pytest-cov

# Copy source code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Default command
CMD ["bash"]
