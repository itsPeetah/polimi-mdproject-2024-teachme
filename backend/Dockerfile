FROM python:3.11-alpine

# Set up environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up backend variables for TeachMe
# ENV OPENAI_API_KEY=<YOUR_OPENAI_KEY>
# ENV MONGODB_URI=<YOUR_MONGODB_URI>

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose the port your application will run on
EXPOSE 5000

# Specify the command to run on container start
CMD ["python", "main.py"]
