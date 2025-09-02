FROM public.ecr.aws/lambda/python:3.12

COPY . .

# Set the CMD to your handler function
CMD ["lambda_function.lambda_handler"]
