import uuid
from datetime import datetime
from PIL import Image
import streamlit as st

from app.i18n import get_text
from app.storage import save_submissions
from app.ai import torch_available, transformers_available, load_ai_models, generate_image_caption

def render_identify(users: dict, user_info: dict):
    st.markdown(f"# 🔍 {get_text('identify_objects')}")

    if not st.session_state.image_files:
        st.warning("No images found! Please upload some images first.")
        if st.button("Go to Upload"):
            st.session_state.current_page = "upload"; st.rerun()
        st.stop()

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_image_index == 0):
            st.session_state.current_image_index = max(0, st.session_state.current_image_index - 1); st.rerun()
    with c2:
        st.markdown(f"<div style='text-align: center;'><p>Image {st.session_state.current_image_index + 1} of {len(st.session_state.image_files)}</p></div>", unsafe_allow_html=True)
    with c3:
        if st.button("Next ➡️", disabled=st.session_state.current_image_index >= len(st.session_state.image_files) - 1):
            st.session_state.current_image_index = min(len(st.session_state.image_files) - 1, st.session_state.current_image_index + 1); st.rerun()

    current_image_name = st.session_state.image_files[st.session_state.current_image_index]
    image_path = f"images/{current_image_name}"
    try:
        image = Image.open(image_path)
        cc1, cc2, cc3 = st.columns([1, 2, 1])
        with cc2:
            st.image(image, caption="What is this object called in your dialect?", use_container_width=True)
    except FileNotFoundError:
        st.error(f"Image not found: {current_image_name}")
        st.stop()

    existing = [s for s in st.session_state.submissions if s.get('image_name') == current_image_name]
    if existing:
        st.markdown("### 🏷️ Existing Names for This Object:")
        for entry in existing[-3:]:
            st.markdown(f"""
            <div class="word-comparison">
                <strong>{entry['telugu_word']}</strong> - 
                <em>{entry['region']}</em> by {entry['username']}
            </div>
            """, unsafe_allow_html=True)

    if torch_available and transformers_available:
        st.markdown(f"""
        <div class="category-header">
            <h3>🤖 {get_text('ai_caption')}</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🧠 Generate AI Description"):
            if load_ai_models():
                with st.spinner("🤖 AI is analyzing the image..."):
                    caption = generate_image_caption(image)
                    st.markdown(f"""
                    <div class="success-message">
                        <strong>AI Description:</strong> {caption}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-message">
            <h4>⚠️ AI Features Unavailable</h4>
            <p>AI image description is not available due to missing dependencies. The identification feature still works!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dialect-input">
        <h3>🏷️ {get_text('your_dialect_word')}</h3>
        <p>{get_text('what_call_object')}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("dialect_form"):
        telugu_word = st.text_input(
            get_text('your_dialect_word'),
            placeholder="ఉదా: గిన్నె, కలశం, దీపం..." if st.session_state.language == 'telugu' else "e.g., pot, vessel, lamp...",
            key=f"telugu_word_{st.session_state.current_image_index}"
        )
        object_type = st.text_input(
            get_text('object_type'),
            placeholder=get_text('type_placeholder'),
            key=f"object_type_{st.session_state.current_image_index}"
        )
        submitted = st.form_submit_button(f"💾 {get_text('submit')}")
        if submitted and telugu_word.strip():
            new_submission = {
                "id": str(uuid.uuid4()),
                "username": st.session_state.username,
                "region": user_info.get('region', 'Unknown'),
                "image_name": current_image_name,
                "telugu_word": telugu_word.strip(),
                "object_type": object_type.strip(),
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.submissions.append(new_submission)
            save_submissions(st.session_state.submissions)
            users[st.session_state.username]["submissions"] = users[st.session_state.username].get("submissions", 0) + 1
            from app.auth import save_users
            save_users(users)
            st.markdown(f"""<div class="success-message">🎉 {get_text('successfully_saved')}</div>""", unsafe_allow_html=True)
            if st.session_state.current_image_index < len(st.session_state.image_files) - 1:
                st.session_state.current_image_index += 1; st.rerun()