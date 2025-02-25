import pandas as pd

def initialize_session_state():
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'sustainable_only': False,
            'in_season_only': False,
            'max_distance': 50
        }
