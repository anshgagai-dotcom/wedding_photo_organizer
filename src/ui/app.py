import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st

from src.llm.image_classifier import classify_wedding_image
from src.organizer.photo_organizer import move_to_category


# -------------------------------
# Streamlit Page Config
# -------------------------------

st.set_page_config(
    page_title="Wedding Photo Organizer",
    layout="wide"
)

st.title("💍 AI Wedding Photo Organizer")
st.write("Upload wedding images and organize them using LLM-based image classification.")


# -------------------------------
# Upload Section
# -------------------------------

uploaded_files = st.file_uploader(
    "Upload Wedding Photos",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

UPLOAD_FOLDER = "input_photos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# Process Uploaded Images
# -------------------------------

if uploaded_files:

    for uploaded_file in uploaded_files:

        # Save uploaded image
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display image
        st.image(save_path, caption=uploaded_file.name, width=300)

        # Analyze using LLM
        with st.spinner("Analyzing Image using LLM..."):

            result = classify_wedding_image(save_path)

            st.success("Classification Complete")

            # Show LLM response
            st.write("### LLM Response")
            st.write(result)

            # Extract category
            response = result.lower()

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

            detected_category = "others"

            for category in categories:
                if category in response:
                    detected_category = category
                    break

            # Organize image
            final_path = move_to_category(save_path, detected_category)

            st.write("### Organized To")
            st.code(final_path)
            