FROM ubuntu:22.04

# Install dependencies including Python and curl for downloading RIC
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev gcc zlib1g-dev libjpeg-dev curl unzip

# Install AWS Lambda Runtime Interface Client (RIC)
RUN curl -Lo /usr/local/bin/aws-lambda-rie \
    https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x /usr/local/bin/aws-lambda-rie

# Download the Lambda Runtime Interface Client for Lambda to invoke your handler
RUN curl -Lo /lambda-rie \
    https://github.com/aws/aws-lambda-runtime-interface-client/releases/latest/download/aws-lambda-rie-linux-amd64 && \
    chmod +x /lambda-rie

ENV PATH="/usr/local/bin:${PATH}"

# Copy your function code
COPY . .
# Install pip dependencies
RUN pip3 install -r requirements.txt

# Set entrypoint to launch the RIC (which runs the Lambda runtime)
ENTRYPOINT ["/lambda-rie"]

# Set CMD to your function handler
CMD ["lambda_function.lambda_handler"]
