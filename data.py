import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path

@st.cache_data
def load_data():
    """
    Load data from CSV files or create sample data if files don't exist
    """
    data_dir = Path(__file__).parent.parent / 'data'
    
    # Check if data directory exists, if not create it
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    
    # Load producers data
    producers_path = data_dir / 'producers.csv'
    if producers_path.exists():
        producers = pd.read_csv(producers_path)
    else:
        # Create sample producer data
        producers = pd.DataFrame({
            'name': ['Green Acres Farm', 'Sunny Valley Dairy', 'River Farm', 'Highland Ranch', 
                    'Mountain View Farm', 'Valley Fresh Produce', 'Meadowbrook Dairy', 'Riverside Poultry'],
            'distance': [15, 25, 45, 30, 20, 35, 28, 42],
            'products': ['Vegetables', 'Dairy', 'Meat, Eggs', 'Fruits', 'Vegetables, Fruits', 
                        'Vegetables, Herbs', 'Dairy', 'Eggs'],
            'certification': ['Organic', 'Conventional', 'Regenerative', 'Organic', 'Organic', 
                            'Conventional', 'Organic', 'Conventional'],
            'lat': [40.7128, 40.7589, 40.6892, 40.7281, 40.7431, 40.7023, 40.7589, 40.6992],
            'lon': [-74.0060, -73.9851, -74.0445, -73.9467, -73.9712, -74.0182, -73.9951, -74.0345],
            'founded': [2010, 2005, 2015, 2008, 2012, 2018, 2007, 2014],
            'employees': [12, 8, 15, 10, 7, 5, 9, 6],
            'description': [
                'Specializing in organic, pesticide-free vegetables with sustainable farming practices.',
                'Family-owned dairy farm producing milk, cheese, and yogurt since 2005.',
                'Regenerative livestock farm raising grass-fed beef and free-range chickens.',
                'Orchard growing a variety of seasonal fruits with minimal chemical treatments.',
                'Diverse farm offering both vegetables and fruits using organic methods.',
                'Focused on specialty vegetables and culinary herbs for local restaurants.',
                'Small-batch dairy products from grass-fed Jersey cows.',
                'Dedicated poultry farm producing free-range eggs.'
            ],
            'website': [f'http://www.{name.lower().replace(" ", "")}.com' for name in 
                        ['Green Acres Farm', 'Sunny Valley Dairy', 'River Farm', 'Highland Ranch', 
                        'Mountain View Farm', 'Valley Fresh Produce', 'Meadowbrook Dairy', 'Riverside Poultry']]
        })
        # Save sample data
        producers.to_csv(producers_path, index=False)
    
    # Load products data
    products_path = data_dir / 'products.csv'
    if products_path.exists():
        products = pd.read_csv(products_path)
    else:
        # Create sample product data
        products = pd.DataFrame({
            'name': ['Tomatoes', 'Lettuce', 'Milk', 'Eggs', 'Apples', 'Carrots', 'Beef', 'Cheese',
                    'Potatoes', 'Broccoli', 'Strawberries', 'Herbs', 'Chicken', 'Honey', 'Mushrooms'],
            'price_per_unit': [3.99, 2.99, 4.50, 5.99, 2.99, 2.49, 12.99, 8.50, 1.99, 3.49, 4.99, 2.99, 9.99, 7.50, 5.99],
            'unit': ['lb', 'head', 'gallon', 'dozen', 'lb', 'bunch', 'lb', 'lb', 'lb', 'bunch', 'pint', 'bunch', 'lb', 'jar', 'lb'],
            'season': ['Summer', 'Spring/Fall', 'Year-round', 'Year-round', 'Fall', 'Year-round', 'Year-round', 
                    'Year-round', 'Fall', 'Spring/Fall', 'Spring/Summer', 'Spring/Summer/Fall', 'Year-round', 'Summer/Fall', 'Year-round'],
            'producer': ['Green Acres Farm', 'Sunny Valley Dairy', 'Sunny Valley Dairy', 'River Farm', 'Highland Ranch',
                        'Green Acres Farm', 'River Farm', 'Meadowbrook Dairy', 'Mountain View Farm', 'Valley Fresh Produce',
                        'Highland Ranch', 'Valley Fresh Produce', 'River Farm', 'Mountain View Farm', 'Valley Fresh Produce'],
            'organic': [True, False, False, False, True, True, False, True, True, False, True, False, False, True, False],
            'nutrition_score': [85, 90, 75, 80, 70, 85, 65, 60, 65, 95, 75, 80, 70, 65, 75]
        })
        # Save sample data
        products.to_csv(products_path, index=False)
    
    # Generate market data (always generate fresh for demo purposes)
    market_df = generate_market_data(products)
    
    # Generate customer data
    customer_df = generate_customer_data()
    
    # Generate sustainability data
    carbon_df = generate_carbon_data(producers)
    
    return producers, products, market_df, customer_df, carbon_df

def generate_market_data(products):
    """Generate synthetic market data for demonstration"""
    dates = pd.date_range(start='2023-01-01', end='2024-02-23', freq='W')
    market_data = []
    
    for product in products['name'].unique():
        base_price = products[products['name'] == product]['price_per_unit'].iloc[0]
        seasonal_factor = 0.2  # Price fluctuation based on seasonality
        
        for date in dates:
            month = date.month
            # Seasonal variation based on month
            season_effect = np.sin(month / 12 * 2 * np.pi) * seasonal_factor
            # Add trend and random noise
            trend = date.year - 2023  # Slight yearly increase
            random_effect = np.random.normal(0, 0.05)  # Random noise
            
            price = base_price * (1 + season_effect + 0.05 * trend + random_effect)
            volume = np.random.randint(50, 500)  # Random sales volume
            
            market_data.append({
                'date': date,
                'product': product,
                'price': round(price, 2),
                'volume': volume,
                'revenue': round(price * volume, 2)
            })
    
    return pd.DataFrame(market_data)

def generate_customer_data():
    """Generate synthetic customer data for demonstration"""
    customer_types = ['Individual', 'Restaurant', 'Retailer', 'Food Service']
    distance_ranges = ['0-5 miles', '5-15 miles', '15-30 miles', '30+ miles']
    
    customer_data = []
    for month in range(1, 13):
        for ctype in customer_types:
            for distance in distance_ranges:
                # More locals in summer, more distant customers in winter
                season_factor = 1 + 0.3 * np.sin((month - 6) / 12 * 2 * np.pi)
                if distance == '0-5 miles':
                    base = 100 * season_factor
                elif distance == '5-15 miles':
                    base = 80 * season_factor
                elif distance == '15-30 miles':
                    base = 60 / season_factor
                else:
                    base = 40 / season_factor
                
                # Adjust for customer type
                if ctype == 'Individual':
                    type_factor = 1.0
                elif ctype == 'Restaurant':
                    type_factor = 0.3
                elif ctype == 'Retailer':
                    type_factor = 0.2
                else:
                    type_factor = 0.15
                
                customers = int(base * type_factor * (1 + np.random.normal(0, 0.1)))
                revenue = customers * np.random.randint(20, 100)
                
                customer_data.append({
                    'month': month,
                    'customer_type': ctype,
                    'distance_range': distance,
                    'customers': customers,
                    'revenue': revenue
                })
    
    return pd.DataFrame(customer_data)

def generate_carbon_data(producers):
    """Generate synthetic carbon footprint data for demonstration"""
    carbon_data = []
    for _, producer in producers.iterrows():
        distance = producer['distance']
        products_offered = producer['products']
        certification = producer['certification']
        
        # Base footprint depends on distance
        transport_emissions = distance * 0.2  # kg CO2 per mile
        
        # Adjust for farming practices
        if certification == 'Organic':
            farming_emissions = np.random.uniform(0.5, 1.5)
        elif certification == 'Regenerative':
            farming_emissions = np.random.uniform(0.2, 0.8)
        else:
            farming_emissions = np.random.uniform(1.0, 2.0)
        
        # Adjust for product type
        if 'Meat' in products_offered:
            product_factor = np.random.uniform(1.5, 2.5)
        elif 'Dairy' in products_offered:
            product_factor = np.random.uniform(1.2, 1.8)
        else:
            product_factor = np.random.uniform(0.7, 1.3)
        
        total_emissions = transport_emissions + farming_emissions * product_factor
        carbon_sequestration = 0
        
        # Carbon sequestration for regenerative farms
        if certification == 'Regenerative':
            carbon_sequestration = np.random.uniform(0.5, 1.5)
        
        carbon_data.append({
            'producer': producer['name'],
            'transport_emissions': round(transport_emissions, 2),
            'farming_emissions': round(farming_emissions * product_factor, 2),
            'total_emissions': round(total_emissions, 2),
            'carbon_sequestration': round(carbon_sequestration, 2),
            'net_impact': round(total_emissions - carbon_sequestration, 2)
        })
    
    return pd.DataFrame(carbon_data)

def initialize_session_state():
    """Initialize session state variables"""
    # Load data
    producers, products, market_df, customer_df, carbon_df = load_data()
    
    # Set up session state
    if 'producers' not in st.session_state:
        st.session_state.producers = producers
    if 'products' not in st.session_state:
        st.session_state.products = products
    if 'market_data' not in st.session_state:
        st.session_state.market_data = market_df
    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = customer_df
    if 'carbon_data' not in st.session_state:
        st.session_state.carbon_data = carbon_df
    if 'notifications' not in st.session_state:
        st.session_state.notifications = [
            {"type": "info", "message": "Welcome to the Farm-to-Table Ecosystem Dashboard!", "date": datetime.now().strftime("%Y-%m-%d")},
            {"type": "success", "message": "New producer 'Riverside Poultry' joined our network", "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")},
            {"type": "warning", "message": "Seasonal shift: Summer crops ending soon", "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")}
        ]
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'user_location' not in st.session_state:
        st.session_state.user_location = [40.7128, -74.0060]  # Default NYC location
    if 'favorite_producers' not in st.session_state:
        st.session_state.favorite_producers = []
    if 'community_events' not in st.session_state:
        st.session_state.community_events = [
            {"title": "Farmers Market", "date": "2024-03-05", "location": "Central Park", "description": "Weekly farmers market featuring local producers"},
            {"title": "Farm Tour Day", "date": "2024-03-15", "location": "Green Acres Farm", "description": "Open farm tour with demonstrations of organic farming practices"},
            {"title": "Cooking Workshop", "date": "2024-03-22", "location": "Community Center", "description": "Learn to cook seasonal dishes with local ingredients"}
        ]

def format_currency(value):
    """Format a number as currency"""
    return f"${value:.2f}"

def get_badge_html(certification):
    """Generate HTML for certification badges"""
    if certification == 'Organic':
        return f'<span class="badge badge-organic">Organic</span>'
    elif certification == 'Regenerative':
        return f'<span class="badge badge-regenerative">Regenerative</span>'
    else:
        return f'<span class="badge badge-conventional">Conventional</span>'

def get_trend_indicator(value):
    """Generate HTML for trend indicators"""
    if value > 0:
        return f'<span style="color:#66BB6A">↑ {value:.1f}%</span>'
    elif value < 0:
        return f'<span style="color:#EF5350">↓ {value:.1f}%</span>'
    else:
        return f'<span style="color:#757575">− {value:.1f}%</span>'
