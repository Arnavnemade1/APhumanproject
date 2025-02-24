import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import base64

def setup_css_styling():
    """Set up custom CSS styling for the app"""
    # Color palette
    colors = {
        "primary": "#2E7D32",    # Forest Green
        "secondary": "#1976D2",  # Ocean Blue  
        "accent": "#FF9800",     # Harvest Orange
        "background": "#F8F9FA", # Light Cloud
        "text": "#212121",       # Deep Charcoal
        "light_text": "#757575", # Smooth Gray
        "success": "#66BB6A",    # Fresh Mint
        "warning": "#FFA726",    # Amber Alert
        "danger": "#EF5350",     # Tomato Red
    }
    
    st.markdown(f"""
    <style>
        /* Base styling */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 3rem;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {colors["primary"]};
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }}
        p {{
            font-family: 'Helvetica Neue', sans-serif;
            color: {colors["text"]};
        }}
        
        /* Cards and containers */
        .metric-card {{
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 5px solid {colors["primary"]};
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .insights-container {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        /* Tags and status indicators */
        .local-tag {{
            color: white;
            background-color: {colors["primary"]};
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .regional-tag {{
            color: white;
            background-color: {colors["secondary"]};
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            font-size: 0.75rem;
            font-weight: 500;
            border-radius: 12px;
            margin-right: 5px;
        }}
        .badge-organic {{
            background-color: #C8E6C9;
            color: #2E7D32;
        }}
        .badge-conventional {{
            background-color: #E8EAF6;
            color: #3949AB;
        }}
        .badge-regenerative {{
            background-color: #DCEDC8;
            color: #558B2F;
        }}
        
        /* Header and hero section */
        .hero-section {{
            padding: 2rem 0;
            text-align: center;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, rgba(46,125,50,0.1) 0%, rgba(25,118,210,0.1) 100%);
            border-radius: 10px;
        }}
        .hero-title {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, {colors["primary"]}, {colors["secondary"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-subtitle {{
            font-size: 1.2rem;
            color: {colors["light_text"]};
            max-width: 600px;
            margin: 0 auto;
        }}
        
        /* Navigation and sidebar */
        .sidebar .sidebar-content {{
            background-color: {colors["background"]};
        }}
        
        /* Data displays */
        .dataframe {{
            border: none !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
        }}
        .dataframe th {{
            background-color: {colors["primary"]};
            color: white;
            font-weight: 500;
            text-align: left;
            padding: 10px !important;
        }}
        .dataframe td {{
            padding: 10px !important;
            border-bottom: 1px solid #f0f0f0;
        }}
        .dataframe tr:nth-child(even) {{
            background-color: #f8f8f8;
        }}
        
        /* Season markers */
        .season-marker {{
            display: inline-block;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        .spring-marker {{ background-color: #ABEBC6; }}
        .summer-marker {{ background-color: #F8C471; }}
        .fall-marker {{ background-color: #E59866; }}
        .winter-marker {{ background-color: #85C1E9; }}
        .year-round-marker {{ background-color: #BB8FCE; }}
        
        /* Custom buttons */
        .stButton>button {{
            background-color: {colors["primary"]};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {colors["secondary"]};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        /* Footer styling */
        .footer {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            margin-top: 3rem;
            text-align: center;
        }}
        .footer-text {{
            color: {colors["light_text"]};
            font-size: 0.9rem;
        }}
        .footer-highlight {{
            color: {colors["primary"]};
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)

def create_seasonal_calendar(products):
    """Create a seasonal availability calendar for products"""
    from datetime import datetime
    import calendar
    
    now = datetime.now()
    current_month = now.month
    
    # Define which products are available in each month
    months = list(calendar.month_name)[1:]
    product_seasons = {}
    
    for _, product in products.iterrows():
        product_name = product['name']
        seasons = product['season'].split('/')
        
        available_months = []
        if 'Year-round' in seasons:
            available_months = list(range(1, 13))
        else:
            if 'Spring' in seasons:
                available_months.extend([3, 4, 5])
            if 'Summer' in seasons:
                available_months.extend([6, 7, 8])
            if 'Fall' in seasons:
                available_months.extend([9, 10, 11])
            if 'Winter' in seasons:
                available_months.extend([12, 1, 2])
        
        product_seasons[product_name] = available_months
    
    return product_seasons, current_month, months

def get_placeholder_image(width=300, height=200):
    """Generate a placeholder image for farms"""
    # Create a placeholder farm image
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Draw a simple farm scene
    # Green field
    ax.add_patch(plt.Rectangle((0, 0), 10, 4, color='#7CCC6F'))
    # Blue sky
    ax.add_patch(plt.Rectangle((0, 4), 10, 6, color='#87CEEB'))
    # Farm house
    ax.add_patch(plt.Rectangle((2, 2), 3, 2, color='#F5DEB3'))
    ax.add_patch(plt.Polygon([(2, 4), (5, 4), (3.5, 5.5)], color='#8B4513'))
    # Sun
    ax.add_patch(plt.Circle((8, 8), 1, color='#FFD700'))
    
    ax.axis('off')
    fig.tight_layout(pad=0)
    
    # Convert to image
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    
    return f"data:image/png;base64,{img_str}"

def create_map_visualization(producers, user_location=None):
    """Create an interactive map of producers"""
    import folium
    from folium.plugins import MarkerCluster, HeatMap
    from
