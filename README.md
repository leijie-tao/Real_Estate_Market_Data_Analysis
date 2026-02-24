# 🏡 Silicon Valley Real Estate Market Analysis

### 📊 Data-Driven Insights into Housing in San Jose, Cupertino, Sunnyvale, and Santa Clara

<img width="1526" height="948" alt="Real_Estate_Map" src="https://github.com/user-attachments/assets/ecb4fa0b-e6ed-4c0a-8216-ebee3dd625e1" />

## 📖 Project Overview
This project performs a comprehensive data analysis of the real estate market in the core Silicon Valley area (San Jose, Santa Clara, Sunnyvale, Cupertino). By leveraging the **Zillow API (via RapidAPI)**, this tool scrapes real-time housing data, cleanses it for accuracy, and visualizes key market trends to aid in investment decision-making.

The analysis focuses on the correlation between **school district quality, housing prices, rental yields, and listing premiums**, providing a multi-dimensional view of the current market landscape.

## 🗝️ Key Features & Insights

### 1. Data Acquisition & Cleaning
- **Automated Scrapping**: Fetched 1200+ listings using Python `requests` with pagination handling.
- **Robust Cleaning**: Handled missing values, standardized city names (e.g., fixing 'Sanjose'), and removed outliers (e.g., price < $100k or > $15M).

### 2. Market Analysis (Visualizations)
- **🔥 Correlation Heatmap**: What are the primary factors that affect prices (Living Area, Beds, Baths or Year Built)?
 <img width="1000" height="800" alt="correlation_heatmap" src="https://github.com/user-attachments/assets/fab5e1f3-f638-4aaf-a568-1637e35a4f98" />
Price value is highly positively correlated with living area (0.75) and also highly correlated with rent estimate (0.69), followed by bathrooms (0.56) and bedrooms (0.53). It can be seen that in the core area of ​​Silicon Valley, the hard area of ​​the house and the resulting rental estimate are the core logic supporting house prices.

Gross rental yield (GYY) shows a significant negative correlation with price value (total property price) (-0.64). This illustrates a typical real estate investment pattern: the more expensive the property, the lower the rental yield. Therefore, for rental investment properties, it is essential to strictly control the total investment price to obtain a higher cash flow ratio.  
  
- **💰 Price vs. Living Area**: A scatter plot clustering listings by city to identify "Distribution of Price and Area".
  <img width="3000" height="1800" alt="scatter_area_price" src="https://github.com/user-attachments/assets/13ea0038-cc35-4a97-b704-4f012133ea2d" />  
House prices show a positive correlation with living area; for the same area, prices are generally lower in San Jose and higher in Cupertino.  
Mainstream Area Range: Most houses are concentrated in the 1000-2000 sq ft range. Mainstream Price Range: Prices are concentrated in the 1-2 million sq ft range.  
- **🏫 Education Premium**: Overlaid **School District Ratings (Zipcode level)** with property prices to visualize the "School District Premium."
  <img width="1526" height="948" alt="school_distribution_and_real_estate_price" src="https://github.com/user-attachments/assets/b7cdc48d-f1b3-478d-93ee-db3bffe43d01" />
  In the image, darker colors indicate higher school ratings for the corresponding areas. It can be seen that Cupertino has the highest school district ratings among the four cities, while the school districts near San Jose have lower ratings. This characteristic closely matches the distribution of housing prices, indicating that school districts have a significant impact on housing prices.
- **📋 Macro Comparison**: Generated summary tables comparing Average Price, Price/Sqft, and Inventory across 4 cities.
|    | City        |   avg_price |   avg_area |   mean_price_per_sqft |   median_price_per_sqft |   house_count |
|---:|:------------|------------:|-----------:|----------------------:|------------------------:|--------------:|
|  0 | Cupertino   | 2.16351e+06 |       1747 |               1223.85 |                    1084 |            13 |
|  1 | Santa Clara | 1.52474e+06 |       1684 |                939.69 |                     878 |            68 |
|  2 | Sunnyvale   | 1.37031e+06 |       1648 |                830.49 |                     892 |           117 |
|  3 | San Jose    | 1.2604e+06  |       1646 |                761.42 |                     731 |           730 |  
Cupertino (a tech company headquarters and top school district) boasts a commanding lead in average home prices (approximately $10,000) and average sales per square foot (1374.5), far exceeding the other three cities. It represents a typical scarce market characterized by "low supply and high premium" (only 15 units were available for sale in this sample).  
Santa Clara and Sunnyvale are similar in average size (around 1700 sqft), with Santa Clara having a slightly higher average house price (around $10,000). Their median sales per square foot (870 vs. $892) are extremely close. This indicates that the purchasing power thresholds for buyers in these two tech-focused areas with optimal commutes are highly overlapping.  
San Jose has an extremely abundant housing supply (732 units for sale), driving the average price down to around $10,000, and boasts the lowest median sales per square foot among the four major cities (730). Given San Jose's vast geographical area, it's a buyer's market for those without a strong need for large living spaces or top-tier school districts.  
  
- **📈 Investment Metrics**:
  <img width="4500" height="1800" alt="Investment_Analysis_Boxplots" src="https://github.com/user-attachments/assets/3204370d-6812-4bbe-a4b9-ae4817c3466e" />  
    - **Gross Rental Yield**: Calculated using Zillow Rent Zestimates.  
      The average gross rental yield in the US in Q4 2025 was 6.56%. The overall yield in the four Silicon Valley cities was below the national average, ranging from 2.5% to 5%. Cupertino's gross rental yield was lower than the other three cities. This is because Cupertino's high base price (denominator) significantly compresses the rent-to-price ratio, making the school district factor more important than the rental investment factor.  
    - **Premium Ratio**: Analyzed market sentiment by comparing Listing Price vs. Zestimate.  
      Compared to Zestimate, the current listing prices in the four cities generally have a premium of about 2.5% to 5%, and the data variance is small, reflecting that the market pricing is very transparent and consistent.  

## 🛠️ Tech Stack
- **Language**: Python 3.9+
- **Data Collection**: `Requests`, Zillow API (RapidAPI)
- **Data Manipulation**: `Pandas`, `NumPy`
- **Visualization**: `Plotly` (Interactive Maps), `Seaborn`, `Matplotlib`
- **Format**: CSV, GeoJSON

## 📂 Project Structure
```text
├── API_Scrapping.py        # Script to fetch raw data from Zillow
├── Clean_data.py           # Data cleaning & feature engineering (Yield, Premium)
├── Map_Visualization.py    # Interactive map with School Districts & Listings
├── Data_Visualization.py   # Statistical charts (Heatmap, Boxplots, Scatter)
├── sv_housing_clean.csv    # Processed dataset ready for analysis
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation