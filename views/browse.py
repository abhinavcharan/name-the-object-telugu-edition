import streamlit as st
from app.ui import get_browse_data, display_browse_card

def render_browse():
    st.markdown(f"# 🖼️ Browse Images")

    browse_data = get_browse_data()
    if not browse_data:
        st.info("No images to browse yet. Upload some images or start identifying objects!")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔍 Start Identifying"):
                st.session_state.current_page = "identify"; st.rerun()
        with c2:
            if st.button("📤 Upload Image"):
                st.session_state.current_page = "upload"; st.rerun()
        st.stop()

    st.markdown("""<div class="filter-section"><h4>🔍 Filter Images</h4></div>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        all_regions = sorted(set([item.get('region', 'Unknown') for item in browse_data]))
        selected_regions = st.multiselect("📍 Filter by Region", options=all_regions, default=all_regions, key="region_filter")
    with c2:
        all_types = sorted(set([item.get('object_type', 'Uncategorized') for item in browse_data]))
        selected_types = st.multiselect("🏷️ Filter by Type", options=all_types, default=all_types, key="type_filter")
    with c3:
        source_options = ['identification', 'upload', 'camera']
        selected_sources = st.multiselect("📸 Filter by Source", options=source_options, default=source_options, key="source_filter")
    with c4:
        search_term = st.text_input("🔍 Search Telugu Word", placeholder="తెలుగు పదం వెతకండి...", key="search_filter")

    filtered = browse_data
    if selected_regions:
        filtered = [i for i in filtered if i.get('region') in selected_regions]
    if selected_types:
        filtered = [i for i in filtered if i.get('object_type') in selected_types]
    if selected_sources:
        filtered = [i for i in filtered if i.get('source') in selected_sources]
    if search_term:
        filtered = [i for i in filtered if search_term.lower() in i.get('telugu_word', '').lower()]

    sort_option = st.selectbox("🔄 Sort by", ["Latest First", "Oldest First", "A-Z (Telugu)", "Z-A (Telugu)", "Region", "Type"], key="sort_option")
    if sort_option == "Latest First":
        filtered = sorted(filtered, key=lambda x: x.get('timestamp', ''), reverse=True)
    elif sort_option == "Oldest First":
        filtered = sorted(filtered, key=lambda x: x.get('timestamp', ''))
    elif sort_option == "A-Z (Telugu)":
        filtered = sorted(filtered, key=lambda x: x.get('telugu_word', ''))
    elif sort_option == "Z-A (Telugu)":
        filtered = sorted(filtered, key=lambda x: x.get('telugu_word', ''), reverse=True)
    elif sort_option == "Region":
        filtered = sorted(filtered, key=lambda x: x.get('region', ''))
    elif sort_option == "Type":
        filtered = sorted(filtered, key=lambda x: x.get('object_type', ''))

    st.markdown(f"<div style='text-align: center; margin: 20px 0;'><h3>Found {len(filtered)} images</h3></div>", unsafe_allow_html=True)

    if filtered:
        items_per_page = 10
        total_pages = (len(filtered) - 1) // items_per_page + 1
        if 'browse_page' not in st.session_state:
            st.session_state.browse_page = 1

        if total_pages > 1:
            a, b, c, d, e = st.columns([1, 1, 2, 1, 1])
            with a:
                if st.button("⬅️ Previous", disabled=st.session_state.browse_page <= 1):
                    st.session_state.browse_page -= 1; st.rerun()
            with b:
                if st.button("⏮️ First", disabled=st.session_state.browse_page <= 1):
                    st.session_state.browse_page = 1; st.rerun()
            with c:
                st.markdown(f"<div style='text-align: center; padding: 5px;'>Page {st.session_state.browse_page} of {total_pages}</div>", unsafe_allow_html=True)
            with d:
                if st.button("⏭️ Last", disabled=st.session_state.browse_page >= total_pages):
                    st.session_state.browse_page = total_pages; st.rerun()
            with e:
                if st.button("Next ➡️", disabled=st.session_state.browse_page >= total_pages):
                    st.session_state.browse_page += 1; st.rerun()

        start_idx = (st.session_state.browse_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = filtered[start_idx:end_idx]
        for item in page_items:
            with st.container():
                display_browse_card(item)
                st.markdown("---")
        st.markdown("### 📊 Current View Statistics")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Regions", len(set([i.get('region') for i in filtered])))
        with c2:
            st.metric("Object Types", len(set([i.get('object_type') for i in filtered])))
        with c3:
            st.metric("Contributors", len(set([i.get('username') for i in filtered])))
    else:
        st.info("No images match your filters. Try adjusting the filter criteria.")