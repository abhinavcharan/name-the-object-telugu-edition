# app/styles.py
import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    .language-toggle { position: fixed; top: 20px; right: 20px; z-index: 1000; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; border-radius: 25px; padding: 8px 16px; color: white; font-family: 'Poppins', sans-serif; font-weight: 600; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.3s ease; font-size: 14px; min-width: 120px; }
    .language-toggle:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
    .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem; font-family: 'Poppins', sans-serif; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .feature-card { background: linear-gradient(145deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4ECDC4; margin: 0.5rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1); font-family: 'Poppins', sans-serif; transition: transform 0.3s ease; color: #2c3e50 !important; }
    .feature-card:hover { transform: translateY(-5px); }
    .feature-card h3 { color: #1a202c !important; font-weight: 600; margin-bottom: 10px; }
    .feature-card p { color: #4a5568 !important; line-height: 1.6; }
    .browse-card { background: linear-gradient(145deg, #ffffff, #f8f9fa); padding: 1rem; border-radius: 12px; border: 2px solid #e9ecef; margin: 0.5rem 0; box-shadow: 0 3px 10px rgba(0,0,0,0.1); font-family: 'Poppins', sans-serif; transition: all 0.3s ease; position: relative; overflow: hidden; color: #2c3e50; }
    .browse-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); border-color: #667eea; color: #1a252f; }
    .browse-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); }
    .browse-card h1,.browse-card h2,.browse-card h3,.browse-card h4,.browse-card h5,.browse-card h6 { color: #34495e; font-weight: 600; }
    .browse-card p { color: #2c3e50; line-height: 1.6; }
    .browse-card a { color: #667eea; text-decoration: none; font-weight: 500; }
    .browse-card a:hover { color: #764ba2; text-decoration: underline; }
    .dialect-input { background: linear-gradient(145deg, #fff3cd, #ffeaa7); padding: 1.5rem; border-radius: 12px; border: 3px solid #f39c12; box-shadow: 0 5px 15px rgba(243,156,18,0.3); font-family: 'Poppins', sans-serif; }
    .similarity-score { font-size: 1.3rem; font-weight: bold; padding: 1rem; border-radius: 10px; text-align: center; font-family: 'Poppins', sans-serif; box-shadow: 0 5px 15px rgba(0,0,0,0.2); margin: 1rem 0; }
    .high-similarity { background: linear-gradient(145deg, #d4edda, #c3e6cb); color: #155724; border: 2px solid #28a745; }
    .medium-similarity { background: linear-gradient(145deg, #fff3cd, #ffeaa7); color: #856404; border: 2px solid #ffc107; }
    .low-similarity { background: linear-gradient(145deg, #f8d7da, #f1aeb5); color: #721c24; border: 2px solid #dc3545; }
    .nav-button { width: 100%; margin-bottom: 0.5rem; font-family: 'Poppins', sans-serif; font-weight: 600; }
    .category-header { background: linear-gradient(90deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 8px; text-align: center; margin: 1rem 0 0.5rem 0; font-family: 'Poppins', sans-serif; font-weight: 600; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .login-container { background: linear-gradient(145deg, #ffffff, #f8f9fa); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 400px; margin: 2rem auto; font-family: 'Poppins', sans-serif; }
    .success-message { background: linear-gradient(145deg, #d4edda, #c3e6cb); color: #155724; padding: 1rem; border-radius: 8px; border-left: 5px solid #28a745; margin: 1rem 0; font-family: 'Poppins', sans-serif; }
    .telugu-support { background: linear-gradient(145deg, #e3f2fd, #bbdefb); padding: 0.5rem; border-radius: 5px; border-left: 3px solid #2196f3; margin: 0.5rem 0; font-size: 0.9rem; color: #1565c0; }
    .stats-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; text-align: center; font-family: 'Poppins', sans-serif; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .recent-activity { background: linear-gradient(145deg, #f8f9fa, #e9ecef); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #007bff; font-family: 'Poppins', sans-serif; }
    .word-comparison { background: linear-gradient(145deg, #e8f5e8, #d4edda); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #28a745; font-family: 'Poppins', sans-serif; }
    .filter-section { background: linear-gradient(145deg, #f0f0f0, #e0e0e0); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
    .search-tip { background: linear-gradient(145deg, #fff3e0, #ffcc02); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #ff9800; font-size: 0.9rem; color: #e65100; }
    .regional-badge { display: inline-block; background: linear-gradient(45deg, #4CAF50, #45a049); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin: 2px; }
    .type-badge { display: inline-block; background: linear-gradient(45deg, #2196F3, #1976D2); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin: 2px; }
    .comparison-section { background: linear-gradient(145deg, #f3e5f5, #e1bee7); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 2px solid #9c27b0; }
    .error-message { background: linear-gradient(145deg, #f8d7da, #f1aeb5); color: #721c24; padding: 1rem; border-radius: 8px; border-left: 5px solid #dc3545; margin: 1rem 0; font-family: 'Poppins', sans-serif; }
    .warning-message { background: linear-gradient(145deg, #fff3cd, #ffeaa7); color: #856404; padding: 1rem; border-radius: 8px; border-left: 5px solid #ffc107; margin: 1rem 0; font-family: 'Poppins', sans-serif; }
</style>
"""

def inject_styles() -> None:
    st.markdown(CSS, unsafe_allow_html=True)

def render_language_toggle() -> None:
    current_lang_text = "తెలుగు" if st.session_state.language == 'telugu' else "English"
    other_lang_text = "English" if st.session_state.language == 'telugu' else "తెలుగు"
    st.markdown(f"""
    <div style="text-align: right; margin-bottom: 20px;">
        <button class="language-toggle" onclick="document.querySelector('[data-testid=\\"baseButton-secondary\\"]').click();">
            🌐 Switch to {other_lang_text}
        </button>
    </div>
    """, unsafe_allow_html=True)