FROM public.ecr.aws/lambda/python:3.12

RUN dnf update
RUN dnf install git -y

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install ftfy regex tqdm
RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install -r requirements.txt

# download model first
COPY download_models.py ${LAMBDA_TASK_ROOT}
RUN python download_models.py
# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
