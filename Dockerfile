# FROM public.ecr.aws/lambda/python:3.12

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev gcc zlib1g-dev libjpeg-dev

# Then install your Python dependencies
COPY . .
RUN pip3 install -r requirements.txt

# Set the CMD to your handler function
CMD ["lambda_function.lambda_handler"]
