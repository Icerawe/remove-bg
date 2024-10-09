# remove-bg

## Setup Requirements

Create a `requirements.txt` from your environment using `uv`:

```bash
uv pip freeze > requirements.txt
```

## Running Tests

To run tests using `pytest`:

```bash
uv run pytest test.py
```

## Building the Docker Image

To build the Docker image for the `remove-bg` service:

```bash
docker build --platform linux/amd64 -t plandee-remove-bg .
```

## Running Locally

To run the Docker container locally:

```bash
docker run --env-file .env -p 9000:8080 plandee-remove-bg
```

## Testing Locally

You can test the local instance using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"body": {"url": "https://plandee-image-transform.s3.ap-southeast-1.amazonaws.com/test/remove-bg.jpg"}}' \
  http://localhost:9000/2015-03-31/functions/function/invocations
```