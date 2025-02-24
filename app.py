import streamlit as st
import importlib
import sys
from pathlib import Path

# Add the project directory to the sys.path
sys.path.append(str(Path(__file__).parent))

# Import utility modules
from utils.data_processing import load_data, initialize_session_state
from utils.visualization import setup_css_styling

# Page configuration
st.set_page_config(
    page_title="Farm-to-Table Ecosystem",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
setup_css_styling()

# Load initial data
initialize_session_state()

# Sidebar navigation
with st.sidebar:
    from utils.sidebar import create_sidebar
    page = create_sidebar()

# Import and render the selected page
if page == "Dashboard":
    from pages.dashboard import render_dashboard
    render_dashboard()
elif page == "Producers":
    from pages.producers import render_producers
    render_producers()
elif page == "Products":
    from pages.products import render_products
    render_products()
elif page == "Market Analysis":
    from pages.market_analysis import render_market_analysis
    render_market_analysis()
elif page == "Sustainability":
    from pages.sustainability import render_sustainability
    render_sustainability()
elif page == "Community":
    from pages.community import render_community
    render_community()

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
