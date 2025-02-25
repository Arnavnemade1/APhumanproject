import streamlit as st

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Farm-to-Table Ecosystem",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

import importlib
import sys
from pathlib import Path

# Fix for **file** not being defined in Streamlit
current_dir = Path.cwd()
data_dir = current_dir / 'data'
sys.path.append(str(current_dir))  # Add the current working directory

# Check if directories exist
utils_dir = current_dir / 'utils'
pages_dir = current_dir / 'pages'

if not utils_dir.exists():
    st.error(f"Utils directory not found at: {utils_dir}")
    st.info("Please create a 'utils' directory with the required modules.")
    
if not pages_dir.exists():
    st.error(f"Pages directory not found at: {pages_dir}")
    st.info("Please create a 'pages' directory with the required modules.")

# Create minimal fallback functions
def fallback_initialize_session_state():
    st.session_state.setdefault('data_loaded', False)
    st.warning("Using fallback session state initialization.")

def fallback_setup_css():
    st.markdown("""
    <style>
    .footer {text-align: center; margin-top: 20px;}
    .footer-text {color: #666; font-size: 0.8em;}
    .footer-highlight {font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)
    st.warning("Using fallback CSS styling.")

# Try to import modules, use fallbacks if not available
initialize_session_state = fallback_initialize_session_state
setup_css_styling = fallback_setup_css

try:
    from utils.data_processing import initialize_session_state
    from utils.visualization import setup_css_styling
    st.success("Successfully imported utility modules.")
except ImportError as e:
    st.error(f"Module import error: {e}")

# Apply custom styling
setup_css_styling()

# Initialize session state
initialize_session_state()

# Default page content if modules aren't found
def show_default_page():
    st.title("Farm-to-Table Ecosystem")
    st.write("Welcome to the Farm-to-Table Ecosystem application!")
    
    st.warning("""
    This is a placeholder page. To see the full application:
    
    1. Create a 'utils' directory with:
       - data_processing.py (containing initialize_session_state function)
       - visualization.py (containing setup_css_styling function)
       - sidebar.py (containing create_sidebar function)
    
    2. Create a 'pages' directory with page modules:
       - dashboard.py
       - producers.py
       - products.py
       - market_analysis.py
       - sustainability.py
       - community.py
    
    Each page module should have a render_* function matching the page name.
    """)
    
    st.info("Once these modules are created, the application will work as expected.")

# Try to set up sidebar, use fallback if not available
page = "Dashboard"  # Default page
try:
    with st.sidebar:
        st.title("Navigation")
        from utils.sidebar import create_sidebar
        page = create_sidebar()
except ImportError:
    with st.sidebar:
        st.title("Navigation")
        st.warning("Sidebar module not found. Using default navigation.")
        page_options = ["Dashboard", "Producers", "Products", "Market Analysis", "Sustainability", "Community"]
        page = st.selectbox("Select a page:", page_options)

# Try to render the selected page
page_modules = {
    "Dashboard": "pages.dashboard",
    "Producers": "pages.producers",
    "Products": "pages.products",
    "Market Analysis": "pages.market_analysis",
    "Sustainability": "pages.sustainability",
    "Community": "pages.community"
}

page_rendered = False
if page in page_modules:
    try:
        module = importlib.import_module(page_modules[page])
        render_func = getattr(module, f'render_{page.lower().replace(" ", "_")}')
        render_func()
        page_rendered = True
    except (ModuleNotFoundError, AttributeError) as e:
        st.error(f"Error loading {page} page: {e}")

# Show default content if page wasn't rendered
if not page_rendered:
    show_default_page()

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
