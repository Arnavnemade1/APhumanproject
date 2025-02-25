import streamlit as st

def create_sidebar():
    """Create the sidebar navigation and filters"""
    st.title("Farm-to-Table Ecosystem")
    st.image("https://via.placeholder.com/150?text=F2T", width=150)
    
    st.subheader("Navigation")
    
    # Main navigation
    page = st.radio(
        "Select a page:",
        ["Dashboard", "Producers", "Products", "Market Analysis", "Sustainability", "Community"]
    )
    
    st.markdown("---")
    
    # Filters (only shown on certain pages)
    if page in ["Products", "Producers", "Market Analysis"]:
        st.subheader("Filters")
        
        # Initialize filter settings if not already in session state
        if 'filter_settings' not in st.session_state:
            st.session_state.filter_settings = {
                'sustainable_only': False,
                'in_season_only': False,
                'max_distance': 50
            }
        
        # Sustainability filter
        st.session_state.filter_settings['sustainable_only'] = st.checkbox(
            "Sustainable producers only",
            value=st.session_state.filter_settings.get('sustainable_only', False)
        )
        
        # Season filter
        if page in ["Products", "Market Analysis"]:
            st.session_state.filter_settings['in_season_only'] = st.checkbox(
                "In-season products only",
                value=st.session_state.filter_settings.get('in_season_only', False)
            )
        
        # Distance filter
        st.session_state.filter_settings['max_distance'] = st.slider(
            "Maximum distance (miles)",
            min_value=5,
            max_value=100,
            value=st.session_state.filter_settings.get('max_distance', 50),
            step=5
        )
        
        # Apply filters button
        if st.button("Apply Filters"):
            st.success("Filters applied!")
    
    st.markdown("---")
    
    # Information section
    with st.expander("About"):
        st.write("""
        The Farm-to-Table Ecosystem application connects local farmers with consumers 
        and businesses, promoting sustainable food systems and supporting local economies.
        """)
    
    return page
