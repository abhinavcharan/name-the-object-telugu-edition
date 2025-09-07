import streamlit as st
from app.i18n import get_text

def render_explore(users: dict):
    st.markdown(f"# 🌍 {get_text('explore_data')}")

    total_submissions = len(st.session_state.submissions)
    total_uploads = len(st.session_state.uploads)
    total_users = len(users)
    unique_regions = len(set([s.get('region', 'Unknown') for s in st.session_state.submissions] + [u.get('region', 'Unknown') for u in st.session_state.uploads]))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stats-card"><h3>📊</h3><h2>{total_submissions}</h2><p>{get_text('identifications')}</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stats-card"><h3>📤</h3><h2>{total_uploads}</h2><p>{get_text('uploads')}</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stats-card"><h3>🌍</h3><h2>{unique_regions}</h2><p>{get_text('regions')}</p></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stats-card"><h3>👥</h3><h2>{total_users}</h2><p>{get_text('members')}</p></div>""", unsafe_allow_html=True)

    if total_submissions > 0 or total_uploads > 0:
        st.markdown(f"""<div class="category-header"><h3>📍 {get_text('by_region')}</h3></div>""", unsafe_allow_html=True)
        region_counts = {}
        for submission in st.session_state.submissions:
            region = submission.get('region', 'Unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        for upload in st.session_state.uploads:
            region = upload.get('region', 'Unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        if region_counts:
            max_count = max(region_counts.values())
            for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
                bar_width = (count / max_count) * 100
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>📍 {region}</strong><span>{count} contributions</span>
                    </div>
                    <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px;">
                        <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {bar_width}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""<div class="category-header"><h3>🏷️ {get_text('by_object_type')}</h3></div>""", unsafe_allow_html=True)
        type_counts = {}
        for submission in st.session_state.submissions:
            obj_type = submission.get('object_type', 'Uncategorized')
            if obj_type:
                type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        for upload in st.session_state.uploads:
            obj_type = upload.get('category', 'Uncategorized')
            if obj_type:
                type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        if type_counts:
            max_count = max(type_counts.values())
            for obj_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                bar_width = (count / max_count) * 100
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>🏷️ {obj_type}</strong><span>{count} items</span>
                    </div>
                    <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 8px;">
                        <div style="background: linear-gradient(90deg, #4ECDC4, #44A08D); height: 100%; width: {bar_width}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""<div class="category-header"><h3>🌟 {get_text('member_contributions')}</h3></div>""", unsafe_allow_html=True)
        contributor_counts = {}
        for submission in st.session_state.submissions:
            username = submission.get('username', 'Unknown')
            contributor_counts[username] = contributor_counts.get(username, 0) + 1
        for upload in st.session_state.uploads:
            username = upload.get('username', 'Unknown')
            contributor_counts[username] = contributor_counts.get(username, 0) + 1
        if contributor_counts:
            top_contributors = sorted(contributor_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for i, (username, count) in enumerate(top_contributors):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
                user_region = users.get(username, {}).get('region', 'Unknown Region')
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div><strong>{medal} {username}</strong><br><small>📍 {user_region}</small></div>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #667eea;">{count}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No data available yet. Start contributing to see analytics!")