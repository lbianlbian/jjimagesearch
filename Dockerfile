FROM public.ecr.aws/lambda/python:3.12

COPY . .

RUN apk add build-base zlib-dev jpeg-dev

RUN pip install -r requirements.txt

# Set the CMD to your handler function
CMD ["lambda_function.lambda_handler"]
