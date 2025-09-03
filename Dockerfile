FROM public.ecr.aws/lambda/python:3.12

RUN dnf -y update && dnf -y install \
    python3 python3-pip python3-devel gcc zlib-devel libjpeg-devel curl unzip

# Copy your function code
COPY . .
# Install pip dependencies
RUN pip3 install -r requirements.txt

# Set CMD to your function handler
CMD ["lambda_function.lambda_handler"]
