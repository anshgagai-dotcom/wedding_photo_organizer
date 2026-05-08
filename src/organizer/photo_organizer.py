import os
import shutil


def move_to_category(image_path, category):

    output_folder = f"output_photos/{category}"

    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(image_path)

    destination = os.path.join(output_folder, filename)

    shutil.copy(image_path, destination)

    return destination
    