import streamlit as st
from PIL import Image

def set_page(page_name: str) -> None:
    st.session_state.current_page = page_name

def display_browse_card(item):
    col1, col2 = st.columns([1, 2])
    with col1:
        image_path = f"images/{item['image_name']}"
        try:
            image = Image.open(image_path)
            st.image(image, use_container_width=True)
        except Exception:
            st.markdown("🖼️ *Image not available*")
    with col2:
        import pandas as pd
        try:
            formatted_time = pd.to_datetime(item['timestamp']).strftime('%Y-%m-%d %H:%M') if item['timestamp'] else 'Unknown time'
        except Exception:
            formatted_time = 'Unknown time'
        st.markdown(f"""
        <div class="browse-card">
            <h3 style="color: #667eea; margin-top: 0; font-size: 1.4rem;">{item['telugu_word']}</h3>
            <div style="margin: 8px 0;">
                <span class="regional-badge">📍 {item['region']}</span>
                <span class="type-badge">🏷️ {item['object_type']}</span>
            </div>
            <p style="margin: 8px 0;"><strong>👤 Contributed by:</strong> {item['username']}</p>
            <p style="margin: 8px 0;"><strong>📸 Source:</strong> {item.get('source','').title()}</p>
            {f"<p style='margin: 8px 0;'><strong>📝 Description:</strong> {item.get('description', 'No description available')}</p>" if item.get('description') else ""}
            <p style="font-size: 0.85rem; color: #666; margin: 8px 0;">
                <strong>🕒 Added:</strong> {formatted_time}
            </p>
        </div>
        """, unsafe_allow_html=True)

def get_browse_data():
    import uuid
    data = []
    for submission in st.session_state.submissions:
        if submission.get('image_name') and submission.get('telugu_word'):
            data.append({
                'type': 'identification',
                'image_name': submission.get('image_name'),
                'telugu_word': submission.get('telugu_word'),
                'object_type': submission.get('object_type', 'Uncategorized'),
                'region': submission.get('region', 'Unknown'),
                'username': submission.get('username', 'Anonymous'),
                'timestamp': submission.get('timestamp', ''),
                'source': 'identification',
                'id': submission.get('id', str(uuid.uuid4()))
            })
    for upload in st.session_state.uploads:
        if upload.get('filename') and upload.get('telugu_name'):
            data.append({
                'type': 'upload',
                'image_name': upload.get('filename'),
                'telugu_word': upload.get('telugu_name'),
                'object_type': upload.get('category', 'Uncategorized'),
                'region': upload.get('region', 'Unknown'),
                'username': upload.get('username', 'Anonymous'),
                'timestamp': upload.get('timestamp', ''),
                'description': upload.get('description', ''),
                'display_name': upload.get('image_name', upload.get('filename')),
                'source': upload.get('source', 'upload'),
                'id': upload.get('id', str(uuid.uuid4()))
            })
    return data