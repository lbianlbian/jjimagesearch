FROM public.ecr.aws/lambda/python:3.12

RUN dnf update
RUN dnf install git -y

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install clip_cpp huggingface_hub
RUN pip install -r requirements.txt
RUN huggingface-cli download mys/ggml_CLIP-ViT-B-32-laion2B-s34B-b79K CLIP-ViT-B-32-laion2B-s34B-b79K_ggml-model-f16.gguf
RUN cp /root/.cache/huggingface/hub/models--mys--ggml_CLIP-ViT-B-32-laion2B-s34B-b79K/snapshots/*/CLIP-ViT-B-32-laion2B-s34B-b79K_ggml-model-f16.gguf ${LAMBDA_TASK_ROOT}/

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
