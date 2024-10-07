FROM public.ecr.aws/lambda/python:3.9

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the entire project directory into the Docker image
COPY . ./

# Install dependencies
RUN pip install poetry
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt -t .

# Set the CMD to your Lambda handler function
CMD [ "lambda_function.handler" ]