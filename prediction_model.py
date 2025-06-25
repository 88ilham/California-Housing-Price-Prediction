import pandas as pd
import streamlit as st
import pickle
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="🏡 California Housing Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
/* Main container */
.css-18e3th9 {
    padding: 2rem;
    background-color: #fafafa;
}

/* Sidebar */
.css-1d391kg {
    background-color: #f0f8ff;
    padding: 1.5rem;
    border-radius: 10px;
}

/* Headers */
h1, h2, h3 {
    color: #5a67d8 !important;
    font-family: 'Arial Rounded MT Bold', sans-serif;
}

/* Input widgets */
.stNumberInput>div>div>input, .stSelectbox>div>div>select {
    font-size: 16px !important;
    border-radius: 8px !important;
    border: 1px solid #cbd5e0 !important;
}

/* Prediction highlight */
.highlight-box {
    background-color: #ebf8ff;
    border-left: 5px solid #4299e1;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Buttons and interactive elements */
.stButton>button {
    background-color: #667eea;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #5a67d8;
}

/* Custom emoji styling */
.emoji-feature {
    font-size: 1.5rem;
    margin-right: 0.5rem;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# Function to format currency
def format_currency(amount):
    return f"💰 {int(amount):,} $"

def load_header_image():
    return None

# Main function
def user_input_feature():
    # Sidebar header
    st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h2 style='color: #5a67d8;'>🏠 Housing Features</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Input features
    with st.sidebar.expander("🏡 Basic Information", expanded=True):
        total_rooms = st.number_input(
            label="🚪 Number of Rooms", 
            min_value=2.0, 
            max_value=32627.0, 
            value=500.0,
            help="Number of rooms in the area"
        )

        total_bedrooms = st.number_input(
            label="🛏️ Number of Bedrooms", 
            min_value=2337.0, 
            max_value=6445.0, 
            value=5000.0,
            help="Number of bedrooms in the area"
        )

        housing_median_age = st.number_input(
            label="🔢 Building Age", 
            min_value=1.0, 
            max_value=52.0, 
            value=50.0,
            help="Age of the building"
        )

        median_house_value = st.number_input(
            label="💰 Nearby Troperty Value", 
            min_value=14999.0, 
            max_value=500001.0, 
            value=100000.0,
            help="The value of the property nearby"
        )
    
    with st.sidebar.expander("📍 Location Features", expanded=True):
        ocean_proximity = st.selectbox(
            label="🌊 Distance from the Sea Age", 
            options=('Island', 'Near Ocean', 'Near Bay', '<1H Ocean', 'Inland'),
            help="How close is the area to the sea?"
        )

        latitude = st.number_input(
            label="📏 Latitude", 
            min_value=32.54, 
            max_value=41.95, 
            value=35.00,
            help="Enter the latitude of the area"
        )

        longitude = st.number_input(
            label="📏 Longitude", 
            min_value=-124.35, 
            max_value=-114.31, 
            value=-120.00,
            help="Enter the longitude of the area"
        )
    
    with st.sidebar.expander("🌆 Neighborhood", expanded=True):
        population = st.number_input(
            label="🤖 Population Density", 
            min_value=3.0, 
            max_value=35682.0, 
            value=5000.0,
            help="Number of Population in the area"
        )
        
        households = st.number_input(
            label="🛖 Households Nearby", 
            min_value=1.0, 
            max_value=6082.0, 
            value=5000.0,
            help="Number of households near the area"
        )

        median_income = st.number_input(
            label="💳 Household Income Income", 
            min_value=0.4999, 
            max_value=15.0001, 
            value=5.0,
            help="Households income near the area"
        )
        

    # Create DataFrame with input features
    df = pd.DataFrame({
        'longitude': [longitude],
        'latitude': [latitude],
        'housing_median_age': [housing_median_age],
        'total_rooms': [total_rooms],
        'total_bedrooms': [total_bedrooms],
        'population': [population],
        'households': [households],
        'median_income': [median_income],
        'ocean_proximity': [ocean_proximity],
        'median_house_value': [median_house_value],
    })
    
    return df

def main():
    """Main function"""
    # Title
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #5a67d8;'>🏖️ California Housing Price Predictor</h1>
        <p style='font-size: 1.1rem; color: #ffffff;'>
        Discover the best value of your property's ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Collect user input
    df_customer = user_input_feature()
    
    # Prediction section
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <h2 style='color: #5a67d8;'>✨ Price Prediction ✨</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Load pre-trained model
    try:
        model_loaded = pickle.load(open('final_model.sav', 'rb'))
        
        # Make prediction
        predicted_price = model_loaded.predict(df_customer)[0]
        
        # Create columns for better layout
        col1, col2 = st.columns([1, 1.2])
        
        # Display input features
        with col1:
            st.markdown("""
            📋 Property Details</h3>
            </div>
            """, unsafe_allow_html=True)
            
            features_display = df_customer.transpose()
            features_display.columns = ['Value']
            st.dataframe(features_display, use_container_width=True,
                        height=min(500, 35 * len(features_display)))
        
        # Display prediction
        with col2:
            st.markdown(f"""
            <div class='highlight-box'>
                <div style='text-align: center;'>
                    <h3 style='margin-top: 0; color: #2b6cb0;'>Estimated Value</h3>
                    <h1 style='color: #2c5282; margin: 1rem 0;'>{format_currency(predicted_price)}</h1>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Model performance metrics
            st.markdown("""
            <div style='margin-top: 1.5rem;'>
                <h3 style='color: #4a5568;'>📊 Model Confidence</h3>
                <div style='display: flex; gap: 1rem; margin-top: 1rem;'>
                    <div style='flex: 1; background-color: #ebf8ff; padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0; font-weight: bold; color: #2b6cb0;'>Accuracy</p>
                        <p style='margin: 0.5rem 0 0; font-size: 1.2rem; color: #2b6cb0'>83.2%</p>  <!-- Changed color -->
                    </div>
                    <div style='flex: 1; background-color: #fff5f5; padding: 1rem; border-radius: 8px;'>
                        <p style='margin: 0; font-weight: bold; color: #c53030;'>Avg Error</p>
                        <p style='margin: 0.5rem 0 0; font-size: 1.2rem; color: #c53030'>±$31,500 </p>  <!-- Added color -->
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Disclaimer and additional info
        st.markdown("""
            <div style='border: 1px solid #718096; padding: 1rem; border-radius: 8px; margin-top: 1.5rem;'>
                <h3 style='color: #363942; margin-top: 0;'>💡 Disclaimer</h3>
                <ul style='color: #ffffff;'>
                    <li>This estimate is based on current market trends</li>
                    <li>For precise valuation, consult with local real estate experts</li>
                    <li>Prices may vary based on property condition and timing</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("""
        ❌ Oops! We couldn't find the prediction model. 
        Please make sure 'final_model.sav' is in the right place.
        """)
    except Exception as e:
        st.error(f"""
        🛑 Something went wrong!
        Error: {str(e)}
        """)

# Run the app
if __name__ == '__main__':
    main()
