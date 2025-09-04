FROM public.ecr.aws/lambda/python:3.12

# Copy your function code
COPY . .
# Install pip dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Set CMD to your function handler
CMD ["lambda_function.lambda_handler"]
