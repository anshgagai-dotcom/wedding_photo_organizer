from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def classify_wedding_image(image_path):

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Analyze this wedding image.

Return:
1. Main Category
2. Short Tags

Possible categories:
- bride
- groom
- couple
- ceremony
- family
- crowd
- decoration
- food
- stage

Return short clean response only.
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content
    