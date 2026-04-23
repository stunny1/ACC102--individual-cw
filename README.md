# Project Title
## 1. Problem & User 
This project visualizes the judicial risk of foreign investment in China by analyzing legal disputes over the years. It is aimed at stakeholders in the legal, financial, and investment sectors who need to understand the risks associated with foreign investment in China.
## 2. Data 
- **Source**: The data is derived from publicly available sources like Qichacha, Aiqicha, and China Judgments Online.
- **Access Date**: 2026
- **Key Fields**:
  - Company Name
  - Case Name
  - Court Region

## 3. Methods (main Python steps)
The project follows these steps:

（1） **Data Cleaning**
   - Extract the key columns from the raw data and perform necessary aggregations and statistics. This includes extracting company names, case names, regions, and case dates, and preparing them for further analysis.

（2） **Data Analysis**
   -  Calculate year-over-year growth rates and categorize data by province. This allows me to perform regression analysis and hypothesis testing to understand trends in foreign investment-related legal disputes.

（3）**Data Visualization**
   - Visualize the processed data using various plotting techniques, including heatmaps, line charts, and bar charts. These visualizations help in understanding the distribution of cases across different regions and trends over time.

## 4. Key Findings 
- A heatmap displaying the distribution of foreign investment-related cases across China's provinces.
- Total case counts and growth rate analysis.
- Regression analysis results showing the relationship between the number of cases and the year.
- Hypothesis testing for statistical significance of the year-on-year case trend.
## 5. How to run (optional but valuable)
#To run this project, follow these steps:

#（1）Install Dependencies
- First, you need to install the required Python dependencies. In your terminal, run:

pip install -r requirements.txt
- If you don't have a requirements.txt file, you can manually install the necessary libraries using the following commands:

pip install streamlit pandas matplotlib plotly statsmodels geopandas folium

#（2）Run the Streamlit App

Once dependencies are installed, you can run the Streamlit app. In your terminal, run:

streamlit run app.py

#（3）Data Files

Ensure that the following data files are in place:
- data/raw/FDI.xlsx for the FDI data.
- data/processed/ directory for processed files (e.g., company_data.csv, case_data.csv, court_data.csv, etc.).

#（4）Then you can see the results.
## 6. Product link / Demo
## 7. Limitations & next steps
- Limitations: This database has certain limitations, as some detailed information is only available to platform members. The data is presented in the form of pre-collected local files, meaning it cannot be updated in real-time. Furthermore, the analysis performed is mainly descriptive, with no advanced predictive modeling or deeper insights derived yet.
- Next Steps: Future work can involve updating the dataset with more recent information, conducting more advanced statistical or machine learning analysis, and integrating real-time data sources to make the analysis more dynamic.
