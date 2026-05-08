import os

from llm.image_classifier import classify_wedding_image
from organizer.photo_organizer import move_to_category


INPUT_FOLDER = "input_photos"


def extract_category(response_text):

    response = response_text.lower()

    categories = [
        "bride",
        "groom",
        "couple",
        "ceremony",
        "family",
        "crowd",
        "decoration",
        "food",
        "stage"
    ]

    for category in categories:
        if category in response:
            return category

    return "others"


def process_images():

    images = os.listdir(INPUT_FOLDER)

    for image in images:

        image_path = os.path.join(INPUT_FOLDER, image)

        print(f"\nProcessing: {image}")

        result = classify_wedding_image(image_path)

        print("LLM Response:", result)

        category = extract_category(result)

        final_path = move_to_category(image_path, category)

        print("Moved To:", final_path)


if __name__ == "__main__":
    process_images()
    



    