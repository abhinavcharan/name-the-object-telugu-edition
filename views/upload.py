import uuid
from datetime import datetime
from PIL import Image
import streamlit as st

from app.i18n import get_text
from app.images import save_uploaded_image, save_camera_image, load_images_from_folder
from app.storage import save_uploads

def render_upload(user_info: dict):
    st.markdown(f"# 📤 {get_text('upload_image')}")
    st.markdown("""
    <div class="feature-card">
        <h3>📸 Upload Your Own Images</h3>
        <p>Help expand our collection by uploading images of objects with unique Telugu names!</p>
    </div>
    """, unsafe_allow_html=True)

    upload_method = st.radio("Choose how to add an image:", ["📁 Upload from device", "📸 Take photo with camera"], horizontal=True)
    uploaded_file = camera_image = None
    if upload_method == "📁 Upload from device":
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'], help="Upload clear images of objects with interesting Telugu names")
    else:
        st.markdown("### 📸 Camera Capture")
        camera_image = st.camera_input("Take a photo of an object", help="Make sure the object is clearly visible and well-lit")

    image_source = uploaded_file or camera_image
    if image_source is not None:
        image = Image.open(image_source)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            caption_text = "Uploaded Image" if uploaded_file else "Captured Photo"
            st.image(image, caption=caption_text, use_container_width=True)

        with st.form("upload_form"):
            st.markdown("### Add Details")
            image_name = st.text_input("Image Name (optional)", placeholder="e.g., Traditional Pot")
            description = st.text_area("Description (optional)", placeholder="Brief description of the object...")
            col1, col2 = st.columns(2)
            with col1:
                telugu_name = st.text_input("Telugu Name", placeholder="ఈ వస్తువు యొక్క తెలుగు పేరు...")
            with col2:
                category = st.selectbox("Category", ["Kitchen Items", "Religious Objects", "Tools", "Decorative Items", "Household Items", "Traditional Items", "Other"])
            upload_submitted = st.form_submit_button("📤 Upload Image")

            if upload_submitted:
                if uploaded_file:
                    saved_filename = save_uploaded_image(uploaded_file)
                    original_name = uploaded_file.name
                else:
                    saved_filename = save_camera_image(camera_image)
                    original_name = f"camera_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                if saved_filename:
                    new_upload = {
                        "id": str(uuid.uuid4()),
                        "username": st.session_state.username,
                        "region": user_info.get('region', 'Unknown'),
                        "filename": saved_filename,
                        "original_name": original_name,
                        "image_name": image_name or original_name,
                        "description": description,
                        "telugu_name": telugu_name,
                        "category": category,
                        "source": "upload" if uploaded_file else "camera",
                        "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.uploads.append(new_upload)
                    save_uploads(st.session_state.uploads)
                    st.markdown(f"""<div class="success-message">🎉 {get_text('object_uploaded')}</div>""", unsafe_allow_html=True)
                    st.session_state.image_files = load_images_from_folder()
                    st.balloons()
    else:
        st.info("👆 Click 'Browse files' above to select an image from your device" if upload_method == "📁 Upload from device" else "📸 Click 'Take Photo' above to capture an image using your camera")

    st.markdown("""
    <div class="feature-card">
        <h4>📝 Tips for Great Photos:</h4>
        <ul>
            <li>🔆 Ensure good lighting</li>
            <li>🎯 Focus on the main object</li>
            <li>📐 Keep the object centered</li>
            <li>🔍 Make sure text/details are readable</li>
            <li>🌟 Capture unique or traditional items</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)