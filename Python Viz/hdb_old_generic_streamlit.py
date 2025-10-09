import streamlit as st
import pandas as pd
import joblib
import numpy as np
from PIL import Image

import math

# --- Title and Description ---
st.set_page_config(page_title="Generic HDB Resale Price Prediction", layout="wide")


# Inject custom CSS for the sidebar background
st.markdown("""
    <style>
    /* Sidebar background image */
    [data-testid="stSidebar"] {
        background-image: url("https://www.homeguide.com.sg/wp-content/uploads/2018/02/New-HDB-Grant-Could-Allow-Flat-Owners-to-Customise-Their-Homes.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
    }

    /* White overlay ("white-wash") on top of the background */
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.75); /* white wash */
        z-index: 0;
    }

    /* Make sure sidebar content appears above the overlay */
    [data-testid="stSidebar"] > div:first-child {
        position: relative;
        z-index: 1;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🏠 Generic HDB Resale Price Prediction App - Accuracy Model")



st.markdown("""
This interactive app predicts future HDB resale prices in Singapore using a machine learning model trained 
on historical resale transactions and economic indicators (CPI).  
            
**How it works:**  
- Leveraging [past HDB resale data](Data.gov.sg), this Random Forest model predicts both real (inflation-adjusted) 
            and nominal prices tailored to your selected flat configuration.
- Future CPI values were forecasted with linear regression, adjusting predicted HDB prices for inflation.
""")

# --- Images for Visual Appeal ---
st.markdown("""
---
<span style="font-size:10px;">
*This is a baseline model and does not currently 
    incorporate additional features
    such as nearby amenities.</span>
""", unsafe_allow_html=True)

st.image(
    "hdb1.png",
    caption="*Forecasts for 1 room flats were excluded due to insufficient data and inaccurate predictions during model training.*",
    use_container_width=True
)

# --- Sidebar for User Input ---
st.sidebar.header("Select Flat Features")

flat_types = ['2 room', '3 room', '4 room', '5 room', 'executive', 'multi generation']
towns = ['ang mo kio', 'bedok', 'bishan', 'bukit batok', 'bukit merah', 'bukit panjang', 'bukit timah',
         'central area', 'choa chu kang', 'clementi', 'geylang', 'hougang', 'jurong east', 'jurong west',
         'kallang whampoa', 'marine parade', 'pasir ris', 'punggol', 'queenstown', 'sengkang', 'serangoon',
         'tampines', 'toa payoh', 'woodlands', 'yishun']
storey_ranges = ['01 TO 03', '04 TO 06', '07 TO 09', '10 TO 12', '13 TO 15', '16 TO 18', '19 TO 21',
                 '22 TO 24', '25 TO 27', '28 TO 30', '31 TO 33', '34 TO 36', '37 TO 39', '40 TO 42',
                 '43 TO 45', '46 TO 48', '49 TO 51']



year = st.sidebar.slider("Year of Purchase", min_value=2025, max_value=2040, value=2025)
lease_years_left = st.sidebar.slider("Lease Years Left", min_value=1, max_value=99, value=65)
flat_type = st.sidebar.selectbox("Flat Type", flat_types)
town = st.sidebar.selectbox("Town", towns)
storey_range = st.sidebar.selectbox("Storey Range", storey_ranges)

# Prepare input dict & DataFrame for prediction
input_dict = {
    'year': year,
    'lease_years_left': lease_years_left,
    'flat_type': flat_type,
    'town': town,
    'storey_range': storey_range,
}
input_df = pd.DataFrame([input_dict])

# Load the saved model pipeline
from huggingface_hub import hf_hub_download

@st.cache_resource
def load_model():
    model_path = hf_hub_download(
        repo_id="jayelleteo/hdb_predict",      
        filename="hdb_price_model.joblib"       
    )
    return joblib.load(model_path)

model = load_model()

# Load and cache CPI forecast data
@st.cache_data
def load_cpi_forecast():
    df = pd.read_csv("for_model_future_cpi_forecast.csv")
    df.set_index('year', inplace=True)  # set year as index for easy lookup
    return df

cpi_forecast_df = load_cpi_forecast()

# Function to get CPI for selected year
def get_cpi_for_year(year):
    try:
        return cpi_forecast_df.loc[year, 'cpi']
    except KeyError:
        return cpi_forecast_2020_2040['cpi'].median()  # fallback CPI if year not found

cpi = get_cpi_for_year(year)

# Predict real (inflation-adjusted) price
predicted_real_price = model.predict(input_df)[0]

# Calculate nominal price based on CPI (assuming base CPI=100)
predicted_nominal_price = predicted_real_price * (cpi / 100)

# --- Display Results ---
st.header("Predicted HDB Resale Prices")
st.markdown(f"""
- **Year:** {year}
- **Lease Years Left:** {lease_years_left}
- **Flat Type:** {flat_type.title()}
- **Town:** {town.title()}
- **Storey Range:** {storey_range}

""")

st.success(f"**Predicted Real Price (Inflation-adjusted):** SGD ${predicted_real_price:,.0f}")
st.info(f"**Predicted Nominal Price:** SGD ${predicted_nominal_price:,.0f} (using forecasted CPI: {cpi:.2f})")

# --- Model Summary ---
st.markdown("""
---
### About this Model
- **Data:** Multiple HDB resale transactions (1990-2020) data sets from Data.gov.sg were merged, cleaned and analysed via Python. 
- **Model:** 
            HDB Price Prediction -- Random Forest Regressor |
            CPI Forecasting -- Linear Regression.
- **Output:** Predicted prices based on selected features multiplied by forecasted CPI value.
- **Feature Engineering** : Then, nominal prices were adjusted for inflation with Consumer Price Index (CPI) data, reflecting real prices.
- **Features:** Year, Lease Years Left, Flat Type, Town, Storey Range

""")

st.markdown("<br>", unsafe_allow_html=True)          
st.markdown("""
<div style='text-align: center; font-size: 0.8em; color: grey;'>
    <em>This app is part of Jia Ling's personal project and accuracy may vary due to unpredictable changes in seasonality or economic events.</em>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)        

################################################################################################
# --- Links to Personal Websites & Portfolio ---

import base64

import streamlit as st
import base64

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{b64_str}"

image_path = img_to_base64("hero-banner.jpg")

html_code = f"""
<style>
.container {{
  position: relative;
  width: 330px;
  height: 330px;
  margin: auto;
  margin-top: 40px;
}}

.photo {{
  width: 330px;
  height: 330px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  margin: auto;
  position: relative;
  z-index: 1;
  box-shadow: 0 0 15px rgba(0,0,0,0.3);
}}

/* Wavy pink border animation using SVG filter */
@keyframes wave-border {{
  0% {{
    filter: url(#wavy);
  }}
  50% {{
    filter: url(#wavy);
    transform: rotate(1deg);
  }}
  100% {{
    filter: url(#wavy);
    transform: rotate(-1deg);
  }}
}}

.photo-wrapper {{
  position: relative;
  width: 330px;
  height: 330px;
  border-radius: 120%;
  padding: 0px;
  background: transparent;
  animation: wave-border 4s ease-in-out infinite;
  box-shadow: 0 0 50px 6px #ff69b4;
  margin: auto;
}}

</style>

<div class="container">
  <div class="photo-wrapper">
    <img src="{image_path}" alt="My Photo" class="photo" />
  </div>
</div>

<div style="text-align: center; margin-top: 30px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333;">
<p style="font-size: 0.8rem; color: #6c757d; font-style: italic;">
  <br><br>Hi, I am Teo Jia Ling (Jayelle). <br> I love visualizing and deriving insights from complicated data! </p>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)



##################################################################################
st.markdown("---")
st.title("Check Out Jayelle's Portfolio!")

# Display your photo (adjust width as needed)
#st.image(image, width=200, caption="I am Jialing (Jayelle). <br> I love visualizing and deriving insights from complicated data!")

st.markdown("""
Welcome! Here are some of my personal websites and portfolio pages where you can learn more about me and my work:
""")

# List of links
links = {
    "Personal Website 1": "https://jayelle0609.github.io/",
    "Portfolio Website 2": "https://jayelle0609.github.io/",
    "Tableau Visualizations": "https://public.tableau.com/app/profile/jialingteo/vizzes",
    "GitHub Projects & Code": "https://github.com/jayelle0609",
    "Specificity HDB Model App": "https://jayellehdbs.streamlit.app/",
    "Dad Jokes Generator App (API Automated)": "https://jayelledadjokes.streamlit.app/"
}

for name, url in links.items():
    st.markdown(f"- [{name}]({url})")

st.markdown("""
---
*Feel free to reach out or explore more!*  
<span style="font-size:10px;">
[Email Me!](mailto:jayelleteo@gmail.com) | [WhatsApp Me!](https://wa.me/6580402496)
</span>
<br>
<span style="font-size:12px; color:gray;">
<em>I have some caveats regarding the newer model. While the new model offers greater specificity, its overall accuracy may not generalize well.  <a href="https://github.com/jayelle0609/HDB_Historical_Price_Analysis/blob/main/README.md#3-forecasting" target="_blank">See why here</a>.</em>
</span>
""", unsafe_allow_html=True)
