import streamlit as st
import importlib
import sys
from pathlib import Path

# Fix for __file__ not being defined in Streamlit
data_dir = Path.cwd() / 'data'
sys.path.append(str(Path.cwd()))  # Add the current working directory

# Import utility modules
try:
    from utils.data_processing import load_data, initialize_session_state
    from utils.visualization import setup_css_styling
except ModuleNotFoundError as e:
    st.error(f"Module import error: {e}")

# Page configuration
st.set_page_config(
    page_title="Farm-to-Table Ecosystem",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling if available
try:
    setup_css_styling()
except Exception as e:
    st.warning(f"CSS styling could not be applied: {e}")

# Load initial data safely
try:
    initialize_session_state()
except Exception as e:
    st.error(f"Data initialization failed: {e}")

# Sidebar navigation
with st.sidebar:
    try:
        from utils.sidebar import create_sidebar
        page = create_sidebar()
    except ModuleNotFoundError as e:
        st.error(f"Sidebar import error: {e}")
        page = "Dashboard"  # Default fallback page

# Import and render the selected page dynamically
page_modules = {
    "Dashboard": "pages.dashboard",
    "Producers": "pages.producers",
    "Products": "pages.products",
    "Market Analysis": "pages.market_analysis",
    "Sustainability": "pages.sustainability",
    "Community": "pages.community"
}

if page in page_modules:
    try:
        module = importlib.import_module(page_modules[page])
        getattr(module, f'render_{page.lower().replace(" ", "_")}')()
    except (ModuleNotFoundError, AttributeError) as e:
        st.error(f"Error loading {page} page: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p class="footer-text">
            Built with <span style="color:#e25555;">❤️</span> to support local food systems • 
            <span class="footer-highlight">Farm-to-Table Ecosystem</span> • 
            Data last updated: February 24, 2025
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
