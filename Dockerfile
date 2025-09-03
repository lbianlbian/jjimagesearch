FROM public.ecr.aws/lambda/python:3.12

RUN dnf -y update && dnf -y install gcc zlib-devel libjpeg-devel 

# Copy your function code
COPY . .
# Install pip dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Set CMD to your function handler
CMD ["lambda_function.lambda_handler"]
