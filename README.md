# 🏠 HDB Resale Price Forecasting Project

This is my GitHub Repository, where I have uploaded my Python code used to clean, merge, validate and visualize the data.

## 📌 Project Summary

This project aims to analyze and forecast HDB resale prices in Singapore using historical data. The workflow has starts in Python and ends in Tableau:

## A. Python Workflow

### 1. **Data Cleaning & Preprocessing**
- Merging multiple datasets from Data.gov.sg.
- Handling missing values and inconsistent formats.
- Feature engineering (e.g., lease years left, inflation adjustment).

---

### 2. **Exploratory Data Analysis (EDA)**
- Visualizing trends and distributions of resale prices by year, flat type, town, model, and storey range.
- Adjusting prices for inflation using the Consumer Price Index (CPI).
- Highlighting key economic events and their impact on prices.

---

### 3. **Forecasting**
- Build a Random Forest Regression model to to predict future HDB prices based on user-selected features, adjusted for CPI inflation.
- CPI values were forecasted with linear regression.
- **Deployed the model on a web app** for user predictions
- CHECK MY MODEL OUT!!! 🕺🕺😊😊
- 🤖 [Specific HDB Price Prediction App (New Model - More Features)](https://jayellehdbspecific.streamlit.app/)
- 🤖 [Generic HDB Price Prediction App (Old Model - More Generic and Accurate)](https://jayellehdbgeneral.streamlit.app/)

 ### Old and New Model Evaluation

- New model : Considers more features such as floor square area, flat model.
- However, that is determined generally by the flat type always.
- New model can lead to inaccurate predictions if one selects ridiculous parameters like 300sqm flat area (HUGE!) and 2 room flat.

- In the old model, we left that out. One can only select flat type and that led to more generic and accurate predictions.
- I still do feel more comfortable with my old model, but will add my new model for people who want to explore with more features.
---

### 4. **Visualization**
- Creating insightful plots in Python and Tableau to identify factors affecting HDB resale prices.

---
## B. Tableau Workflow

 [📊 Tableau Visualizations : HDB Historical Sales Analysis & Forecast](https://public.tableau.com/app/profile/jialingteo/viz/HDBSalesPatternandPriceForecast/HDBHistoricalSalesAnalysisForecast)

- Factors affecting HDB resale prices
- Historical HDB prices by year and flat type
- Forecast of total HDB sales, revenue, and average prices
- General trend of HDB prices by town and flat type across years with forecast
---

## 📂 Data Sources

- [Data.gov.sg HDB Resale Flat Prices](https://data.gov.sg/dataset/resale-flat-prices)  
- May have missed out some links but all data is found in the [Data Folder](https://github.com/jayelle0609/HDB_Historical_Price_Analysis/tree/main/Data)

---

## 👩‍💻 Author

**Jialing Teo**  
📌 [GitHub](https://github.com/jayelle0609)  

📊 [Tableau Public](https://public.tableau.com/app/profile/jialingteo)

💻 [Portfolio Website](https://jayelle0609.github.io/)

🤖 [Specific HDB Price Prediction App](https://jayellehdbspecific.streamlit.app/) (More feature specificity but may sacrifice accuracy)

🤖 [Generic HDB Price Prediction App](https://jayellehdbgeneral.streamlit.app/) (I find this better and more accurate)

🤖 [Dad Jokes Generator APP (API Automated)](https://jayelledadjokes.streamlit.app)

---

