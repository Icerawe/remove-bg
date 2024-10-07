from PIL import Image, UnidentifiedImageError
from datetime import date
from rembg import remove

import awswrangler as wr
import requests
import uuid
import io
import os


def resize_image(image_data: bytes, max_size: tuple = (1024, 1024)) -> bytes:
    input_buffer = io.BytesIO(image_data)
    image = Image.open(input_buffer)
    image.thumbnail(max_size)
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


def process_image(file_data: bytes) -> bytes:
    # Resize image before background removal
    resized_image_data = resize_image(file_data)

    # Remove background using rembg
    output_image_data = remove(resized_image_data)

    return output_image_data  # Return the processed image bytes


def handler(event, context):
    response = {
        "statusCode": 200,
        "body": {}
    }
    try:
        if type(event['body']['url']) == str:
            print(event)
            image_url = event['body']['url']
            response_download = requests.get(image_url)
            if response_download.status_code == 200:
                image_bytes = response_download.content
            else:
                response["statusCode"] = 400
                response["body"] = "Invalid image url"
                return response

        # Process the image synchronously
        processed_image_data = process_image(image_bytes)

        # write image local
        local_file = f'{uuid.uuid4()}.png'
        with open(local_file, 'wb') as f:
            f.write(processed_image_data)

        bucket = os.environ['BUCKET_NAME']
        path = f'remove-bg/{date.today()}/{local_file}'
        # Save image to S3
        wr.s3.upload(
            local_file=local_file, 
            path=f"s3://{bucket}/{path}"
        )
        response["body"]["url"] = f'https://{bucket}.s3.ap-southeast-1.amazonaws.com/{path}'
        os.remove(local_file)

    except UnidentifiedImageError:
        response["statusCode"] = 400
        response["body"] = "Invalid image format"
    except Exception as e:
        print(f"Error: {e}")
        response["statusCode"] = 500
        response["body"] = "Internal server error"
        response["message"] = str(e)

    return response