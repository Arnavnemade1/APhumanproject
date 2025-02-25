import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def setup_css_styling():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Card styling */
    .card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: white;
    }
    
    /* Metric styling */
    .metric-container {
        text-align: center;
        padding: 1rem;
        background-color: #f1f8e9;
        border-radius: 8px;
        border-left: 5px solid #7cb342;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2e7d32;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #616161;
    }
    
    /* Table styling */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background-color: #e8f5e9;
        color: #2e7d32;
        font-weight: bold;
        text-align: left;
        padding: 12px;
    }
    
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .dataframe tr:hover {
        background-color: #f5f5f5;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 20px;
        padding-top: 10px;
        border-top: 1px solid #e0e0e0;
    }
    
    .footer-text {
        color: #757575;
        font-size: 0.8em;
    }
    
    .footer-highlight {
        font-weight: bold;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None, delta_description="from previous period"):
    """Create a styled metric card"""
    with st.container():
        st.markdown(f"""
        <div class="card">
            <div class="metric-container">
                <div class="metric-label">{title}</div>
                <div class="metric-value">{value}</div>
                {f'<div style="color: {"green" if delta > 0 else "red"}; font-size: 0.9rem;">{delta:+.1f}% {delta_description}</div>' if delta is not None else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_sales_chart(sales_data, products_data=None, by='month', chart_type='bar'):
    """Create a sales chart by month or product"""
    if by == 'month':
        # Aggregate sales by month
        monthly_sales = sales_data.groupby('month')['revenue'].sum().reset_index()
        
        # Define month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Convert 'month' to categorical with the specified order
        monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
        
        # Sort by the categorical month
        monthly_sales = monthly_sales.sort_values('month')
        
        if chart_type == 'bar':
            fig = px.bar(
                monthly_sales, 
                x='month', 
                y='revenue',
                title='Monthly Sales Revenue',
                labels={'revenue': 'Revenue ($)', 'month': 'Month'},
                color_discrete_sequence=['#2e7d32']
            )
        else:  # line chart
            fig = px.line(
                monthly_sales, 
                x='month', 
                y='revenue',
                title='Monthly Sales Trend',
                labels={'revenue': 'Revenue ($)', 'month': 'Month'},
                markers=True,
                color_discrete_sequence=['#2e7d32']
            )
            
    elif by == 'product' and products_data is not None:
        # Merge sales data with products to get product names
        merged_data = sales_data.merge(products_data, left_on='product_id', right_on='id')
        
        # Aggregate sales by product
        product_sales = merged_data.groupby('name')['revenue'].sum().reset_index()
        
        # Sort by revenue
        product_sales = product_sales.sort_values('revenue', ascending=False)
        
        fig = px.bar(
            product_sales, 
            x='name', 
            y='revenue',
            title='Sales Revenue by Product',
            labels={'revenue': 'Revenue ($)', 'name': 'Product'},
            color_discrete_sequence=['#2e7d32']
        )
        fig.update_layout(xaxis_tickangle=-45)
        
    else:
        st.error("Invalid chart parameters or missing product data")
        return None
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, l=10, r=10, b=10),
    )
    
    return fig

def create_producer_map(producers_data):
    """Create a simple map showing producer locations (placeholder)"""
    # In a real app, you would use actual geocoded locations
    # For this example, we'll create random coordinates
    import numpy as np
    np.random.seed(42)
    
    # Create random coordinates around a central location
    central_lat, central_lon = 37.7749, -122.4194  # San Francisco coordinates
    
    # Add random coordinates to the producers DataFrame
    map_data = producers_data.copy()
    map_data['lat'] = central_lat + np.random.uniform(-0.5, 0.5, size=len(map_data))
    map_data['lon'] = central_lon + np.random.uniform(-0.5, 0.5, size=len(map_data))
    
    # Use Streamlit's built-in map function
    return map_data[['lat', 'lon', 'name', 'products']]

def create_sustainability_chart(producers_data, products_data):
    """Create a chart showing sustainability metrics"""
    # Calculate percentage of sustainable producers
    sustainable_count = producers_data['sustainable'].sum()
    total_producers = len(producers_data)
    sustainable_percentage = (sustainable_count / total_producers) * 100
    
    # Create a simple donut chart
    fig = go.Figure(go.Pie(
        labels=['Sustainable', 'Conventional'],
        values=[sustainable_count, total_producers - sustainable_count],
        hole=.4,
        marker_colors=['#388e3c', '#bdbdbd']
    ))
    
    fig.update_layout(
        title_text='Producer Sustainability',
        annotations=[dict(text=f"{sustainable_percentage:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return fig
