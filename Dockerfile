FROM public.ecr.aws/lambda/python:3.12

COPY . .

RUN apt-get update && \
    apt-get install -y gcc zlib1g-dev libjpeg-dev

RUN pip install -r requirements.txt

# Set the CMD to your handler function
CMD ["lambda_function.lambda_handler"]
