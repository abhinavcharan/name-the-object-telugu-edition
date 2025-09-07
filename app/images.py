import os
import glob
import uuid
from datetime import datetime
import streamlit as st
from PIL import Image

@st.cache_data
def load_images_from_folder():
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']
    image_files = []
    for extension in image_extensions:
        image_files.extend(glob.glob(f"images/{extension}"))
    if not image_files:
        try:
            from PIL import Image, ImageDraw
            sample_objects = [
                ("sample_pot.jpg", "Traditional Pot", "#8B4513"),
                ("sample_spoon.jpg", "Wooden Spoon", "#DEB887"),
                ("sample_lamp.jpg", "Oil Lamp", "#FFD700")
            ]
            for filename, text, color in sample_objects:
                img = Image.new('RGB', (300, 300), color)
                draw = ImageDraw.Draw(img)
                try:
                    draw.text((50, 150), text, fill='white', anchor='mm')
                except Exception:
                    pass
                img.save(f"images/{filename}")
            return [fn for fn, _, _ in sample_objects]
        except Exception as e:
            st.warning(f"Could not create sample images: {str(e)}")
            return []
    return sorted([os.path.basename(f) for f in image_files])

def save_uploaded_image(uploaded_file):
    try:
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{file_extension}"
        image_path = f"images/{unique_filename}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if unique_filename not in st.session_state.image_files:
            st.session_state.image_files.append(unique_filename)
        return unique_filename
    except Exception as e:
        st.error(f"Error saving image: {str(e)}")
        return None

def save_camera_image(camera_image):
    try:
        unique_filename = f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.jpg"
        image_path = f"images/{unique_filename}"
        image = Image.open(camera_image)
        image.save(image_path)
        if unique_filename not in st.session_state.image_files:
            st.session_state.image_files.append(unique_filename)
        return unique_filename
    except Exception as e:
        st.error(f"Error saving camera image: {str(e)}")
        return None