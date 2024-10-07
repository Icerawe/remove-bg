# remove-bg

create requirement.txt from uv
uv pip freeze > requirements.txt

test
uv run pytest test.py

build
docker build --platform linux/amd64 -t plandee-remove-bg .

run local
docker run --env-file .env -p 9000:8080 plandee-remove-bg

test local
curl -X POST -H "Content-Type: application/json" \
  -d '{"body": {"url": "https://plandee-image-transform.s3.ap-southeast-1.amazonaws.com/test/remove-bg.jpg"}}' \
  http://localhost:9000/2015-03-31/functions/function/invocations