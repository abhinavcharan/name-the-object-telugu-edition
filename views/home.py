import streamlit as st
from app.i18n import get_text
from app.ai import torch_available, transformers_available

def render_home():
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_title')}</h1>
        <h3>{get_text('app_subtitle')}</h3>
        <p>{get_text('tagline')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎯 {get_text('our_mission')}</h3>
            <p>{get_text('mission_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card">
            <h3>🧠 {get_text('ai_power')}</h3>
            <p>{get_text('ai_desc')}</p>
            <p style="font-size: 0.9rem; color: #666;">
                {"✅ AI Available" if torch_available and transformers_available else "⚠️ Limited AI (Dependencies Missing)"}
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🏛️ {get_text('preserve_dialects')}</h3>
            <p>{get_text('preserve_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card">
            <h3>👥 {get_text('community_data')}</h3>
            <p>{get_text('community_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="category-header">
        <h2>{get_text('how_it_works')}</h2>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button(f"🔍 {get_text('identify_objects')}", key="home_identify"):
            st.session_state.current_page = "identify"; st.rerun()
        st.markdown(f"<p style='text-align: center;'>{get_text('identify_desc')}</p>", unsafe_allow_html=True)
    with c2:
        if st.button(f"📤 {get_text('upload_image')}", key="home_upload"):
            st.session_state.current_page = "upload"; st.rerun()
        st.markdown(f"<p style='text-align: center;'>Upload your own images to expand our collection!</p>", unsafe_allow_html=True)
    with c3:
        if st.button(f"🖼️ {get_text('browse_images')}", key="home_browse"):
            st.session_state.current_page = "browse"; st.rerun()
        st.markdown(f"<p style='text-align: center;'>{get_text('learn_from_others')}</p>", unsafe_allow_html=True)
    with c4:
        if st.button(f"🌍 {get_text('explore_data')}", key="home_explore"):
            st.session_state.current_page = "explore"; st.rerun()
        st.markdown(f"<p style='text-align: center;'>View statistics and analytics!</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🕒 Recent Community Activity")
    recent = sorted(st.session_state.submissions, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
    if recent:
        for s in recent:
            username = s.get('username', 'Unknown User')
            region = s.get('region', 'Unknown Region')
            telugu_word = s.get('telugu_word', 'Unknown Word')
            object_type = s.get('object_type', 'Unknown Type')
            st.markdown(f"""
            <div class="recent-activity">
                <strong>👤 {username}</strong> from <em>{region}</em> 
                called an object <strong>"{telugu_word}"</strong> 
                <small>(Category: {object_type})</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity. Be the first to contribute!")