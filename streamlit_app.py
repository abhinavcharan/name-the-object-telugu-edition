# streamlit_app.py
import streamlit as st
import os
from datetime import datetime
from PIL import Image

from app.i18n import get_text, toggle_language
from app.styles import inject_styles, render_language_toggle
from app.auth import load_users, register_user, login_user
from app.storage import ensure_dirs, load_submissions, save_submissions, load_uploads, save_uploads
from app.images import load_images_from_folder
from app.ai import torch_available, transformers_available, load_ai_models, generate_image_caption
from app.ui import display_browse_card, set_page

from views.home import render_home
from views.identify import render_identify
from views.upload import render_upload
from views.explore import render_explore
from views.browse import render_browse

# Configure page
st.set_page_config(
    page_title="తెలుగు లెన్స్ | Name The Object: Telugu Edition",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure directories
ensure_dirs()

# Initialize language
if 'language' not in st.session_state:
    st.session_state.language = 'telugu'

# Inject styles and language toggle
inject_styles()
render_language_toggle()

# Hidden language toggle trigger
if st.button("Toggle Language", key="hidden_toggle", help="Language toggle", type="secondary"):
    toggle_language()
    st.rerun()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

if 'submissions' not in st.session_state:
    st.session_state.submissions = load_submissions()

if 'uploads' not in st.session_state:
    st.session_state.uploads = load_uploads()

if 'blip_model' not in st.session_state:
    st.session_state.blip_model = None
    st.session_state.blip_processor = None

if 'ai_model_loaded' not in st.session_state:
    st.session_state.ai_model_loaded = False

if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0

if 'image_files' not in st.session_state:
    st.session_state.image_files = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

if not st.session_state.image_files:
    st.session_state.image_files = load_images_from_folder()

# Dependency banner
if not torch_available or not transformers_available:
    st.markdown(f"""
    <div class="warning-message">
        <h4>⚠️ AI Model Dependencies Missing</h4>
        <p>Some AI features may not work due to missing dependencies:</p>
        <ul>
            <li>PyTorch: {"✅ Available" if torch_available else "❌ Missing"}</li>
            <li>Transformers: {"✅ Available" if transformers_available else "❌ Missing"}</li>
        </ul>
        <p>To enable AI features, add these to your requirements.txt:</p>
        <code>
        torch<br>
        transformers<br>
        </code>
        <p>The app will continue to work without AI features.</p>
    </div>
    """, unsafe_allow_html=True)

# Authentication UI
if not st.session_state.authenticated:
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_title')}</h1>
        <h3>{get_text('app_subtitle')}</h3>
        <p>{get_text('tagline')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs([f"🔐 {get_text('login')}", f"📝 {get_text('register')}"])

        with tab1:
            st.markdown(f"### 👋 {get_text('welcome_back')}")
            username = st.text_input(get_text('username'), key="login_username")
            password = st.text_input(get_text('password'), type="password", key="login_password")
            if st.button(f"🚀 {get_text('login_btn')}", key="login_btn"):
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning(get_text('fill_all_fields'))

        with tab2:
            st.markdown(f"### 🌟 {get_text('join_community')}")
            new_username = st.text_input(get_text('username'), key="reg_username")
            new_password = st.text_input(get_text('password'), type="password", key="reg_password")
            region_placeholder = "ఉదా: గుంటూరు, వరంగల్, హైదరాబాద్..." if st.session_state.language == 'telugu' else "e.g., Guntur, Warangal, Hyderabad..."
            user_region = st.text_input(get_text('region'), placeholder=region_placeholder, key="reg_region")
            if st.button(f"✨ {get_text('register_btn')}", key="register_btn"):
                if new_username and new_password and user_region:
                    success, message = register_user(new_username, new_password, user_region)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning(get_text('fill_all_fields'))

        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Main app
users = load_users()
user_info = users.get(st.session_state.username, {})

# Sidebar
st.sidebar.markdown(f"## 🧭 {get_text('navigation')}")
st.sidebar.markdown(f"**👋 {get_text('hello')}, {st.session_state.username}!**")
st.sidebar.markdown(f"📍 **Region:** {user_info.get('region', 'Unknown')}")

if st.sidebar.button(f"🏠 {get_text('home')}", key="nav_home"):
    set_page("home")
if st.sidebar.button(f"🔍 {get_text('identify')}", key="nav_identify"):
    set_page("identify")
if st.sidebar.button(f"📤 {get_text('upload')}", key="nav_upload"):
    set_page("upload")
if st.sidebar.button(f"🌍 {get_text('explore')}", key="nav_explore"):
    set_page("explore")
if st.sidebar.button(f"🖼️ {get_text('browse')}", key="nav_browse"):
    set_page("browse")
if st.sidebar.button(f"🚪 {get_text('logout')}", key="logout_btn"):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

st.sidebar.markdown("---")
user_submissions = len([s for s in st.session_state.submissions if s.get('username') == st.session_state.username])
user_uploads = len([u for u in st.session_state.uploads if u.get('username') == st.session_state.username])
st.sidebar.markdown(f"""
<div class="stats-card">
    <h4>📊 {get_text('your_stats')}</h4>
    <p>🔍 {get_text('identifications')}: {user_submissions}</p>
    <p>📤 {get_text('uploads')}: {user_uploads}</p>
</div>
""", unsafe_allow_html=True)

# Route to views
page = st.session_state.current_page
if page == "home":
    render_home()
elif page == "identify":
    render_identify(users, user_info)
elif page == "upload":
    render_upload(user_info)
elif page == "explore":
    render_explore(users)
elif page == "browse":
    render_browse()
else:
    render_home()

# Bottom credits
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 20px;">
    <p>🏛️ తెలుగు లెన్స్ - Preserving Telugu Heritage Through Technology</p>
    <p>Made with ❤️ for the Telugu community | Current Language: {'తెలుగు' if st.session_state.language == 'telugu' else 'English'}</p>
    <p>Total Images: {len(st.session_state.image_files)} | Total Contributions: {len(st.session_state.submissions) + len(st.session_state.uploads)}</p>
</div>
""", unsafe_allow_html=True)

# Debug info
if st.sidebar.checkbox("🔧 Debug Info", value=False):
    with st.sidebar.expander("Debug Information"):
        st.write("Current Page:", st.session_state.current_page)
        st.write("Language:", st.session_state.language)
        st.write("User:", st.session_state.username)
        st.write("Image Files Count:", len(st.session_state.image_files))
        st.write("Submissions Count:", len(st.session_state.submissions))
        st.write("Uploads Count:", len(st.session_state.uploads))
        st.write("AI Model Loaded:", st.session_state.ai_model_loaded)
        st.write("PyTorch Available:", torch_available)
        st.write("Transformers Available:", transformers_available)

# Auto-refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if (datetime.now() - st.session_state.last_refresh).seconds > 60:
    st.session_state.submissions = load_submissions()
    st.session_state.uploads = load_uploads()
    st.session_state.image_files = load_images_from_folder()
    st.session_state.last_refresh = datetime.now()