
# app.py
import streamlit as st
from utils.sidebar import create_sidebar
from utils.visualization import setup_css_styling

# Apply custom CSS styling
setup_css_styling()

# Initialize session state
def initialize_session_state():
    if 'filter_settings' not in st.session_state:
        st.session_state.filter_settings = {
            'sustainable_only': False,
            'in_season_only': False,
            'max_distance': 50
        }

initialize_session_state()

# Create sidebar and navigation
page = create_sidebar()

# Load corresponding page module dynamically
try:
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
    else:
        st.error("Page not found.")
except ModuleNotFoundError as e:
    st.warning(f"Error loading {page} page: {e}")
    st.write("This is a placeholder page. Full functionality will be available when all modules are created.")
