import streamlit as st
import pandas as pd
from pathlib import Path

def load_data():
    """Load data from CSV files in the data directory"""
    data_dir = Path.cwd() / 'data'
    
    # Create dummy data if no data files exist
    if not data_dir.exists() or not list(data_dir.glob("*.csv")):
        data_dir.mkdir(exist_ok=True)
        
        # Create sample producers data
        producers_data = pd.DataFrame({
            'id': range(1, 6),
            'name': ['Green Valley Farm', 'Mountain Ridge Dairy', 'Sunshine Orchards', 
                     'Riverbed Vegetables', 'Happy Hens Poultry'],
            'location': ['Alpine County', 'Sierra Hills', 'Sunvalley', 
                         'Riverside', 'Meadowlands'],
            'products': ['Vegetables, Herbs', 'Milk, Cheese, Yogurt', 'Apples, Pears, Peaches', 
                         'Tomatoes, Lettuce, Carrots', 'Eggs, Chicken'],
            'sustainable': [True, True, False, True, True],
            'distance_miles': [12, 25, 18, 8, 30]
        })
        producers_data.to_csv(data_dir / 'producers.csv', index=False)
        
        # Create sample products data
        products_data = pd.DataFrame({
            'id': range(1, 11),
            'name': ['Organic Kale', 'Artisan Cheese', 'Fresh Eggs', 'Grass-fed Beef', 
                     'Honey', 'Heirloom Tomatoes', 'Apple Cider', 'Sourdough Bread', 
                     'Free-range Chicken', 'Organic Strawberries'],
            'category': ['Vegetable', 'Dairy', 'Poultry', 'Meat', 'Other', 
                         'Vegetable', 'Beverage', 'Bakery', 'Poultry', 'Fruit'],
            'price': [3.99, 8.50, 5.75, 12.99, 7.25, 4.50, 6.99, 5.50, 9.99, 4.75],
            'producer_id': [1, 2, 5, 3, 4, 1, 3, 4, 5, 1],
            'in_season': [True, True, True, True, True, False, False, True, True, False]
        })
        products_data.to_csv(data_dir / 'products.csv', index=False)
        
        # Create sample sales data
        import numpy as np
        np.random.seed(42)
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        product_ids = products_data['id'].tolist()
        
        sales_data = []
        for month in months:
            for product_id in product_ids:
                # Generate random sales data
                quantity = np.random.randint(10, 100)
                price = products_data.loc[products_data['id'] == product_id, 'price'].values[0]
                sales_data.append({
                    'month': month,
                    'product_id': product_id,
                    'quantity': quantity,
                    'revenue': round(quantity * price, 2)
                })
        
        sales_df = pd.DataFrame(sales_data)
        sales_df.to_csv(data_dir / 'sales.csv', index=False)
        
        st.success("Sample data created successfully!")
    
    # Load the data
    try:
        producers = pd.read_csv(data_dir / 'producers.csv')
        products = pd.read_csv(data_dir / 'products.csv')
        sales = pd.read_csv(data_dir / 'sales.csv')
        return {
            'producers': producers,
            'products': products,
            'sales': sales
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    if 'data' not in st.session_state or not st.session_state.data_loaded:
        st.session_state.data = load_data()
        if st.session_state.data:
            st.session_state.data_loaded = True
            
    # Additional session state variables can be initialized here
    if 'selected_producer' not in st.session_state:
        st.session_state.selected_producer = None
        
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None
        
    if 'filter_settings' not in st.session_state:
        st.session_state.filter_settings = {
            'sustainable_only': False,
            'in_season_only': False,
            'max_distance': 50
        }
