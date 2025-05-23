# Base image from AWS Lambda for Python 3.9 (x86_64)
FROM public.ecr.aws/lambda/python:3.9-x86_64

# Working directory in container
WORKDIR /var/task

# Copy requirements.txt into container
COPY requirements.txt .

# Install Python dependencies in Lambda directory
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy Lambda code
COPY handler.py .

# Set Lambda handler
CMD ["handler.lambda_handler"]
