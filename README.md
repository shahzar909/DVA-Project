Real-Time AQI Dashboard

A desktop-based Air Quality Index (AQI) monitoring dashboard developed using Python. This application utilizes the **OpenWeatherMap Air Pollution API** to display real-time AQI data for major Indian cities, supported by interactive and dynamic data visualizations.

 Project Overview

This project aims to visualize air quality data in a user-friendly interface, enabling users to:
- View real-time AQI readings for selected cities
- Interpret air quality using WHO standard levels
- Explore air quality insights through various charts and graphs

 Application Features

-  Real-time AQI fetching using OpenWeatherMap API  
-  Interactive charts: Line, Bar, Pie, Scatter, and Histogram  
-  AQI category interpretation (Good to Very Poor)  
-  Pre-configured for major Indian cities  
-  Built with Python's `Tkinter` GUI toolkit  

Supported Cities

- Delhi  
- Mumbai  
- Kolkata  
- Bangalore  
- Chennai  



 2. Install Dependencies

Ensure Python 3.7+ is installed. Then install required libraries:

```bash
pip install matplotlib requests
```

3. Obtain an API Key

This application requires a valid **OpenWeatherMap API Key**.

#### How to Get It:
1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up and log into your account
3. Navigate to **API Keys**
4. Generate a new API key

 4. Run the Application

```bash
python main.py
```
 5. Input Your API Key

- Enter your API key into the sidebar
- Select a city and click **"Get Real-Time AQI"**
 Visualizations

The dashboard provides the following data representations:

| Chart Type | Description |
|------------|-------------|
| **Line Chart** | Simulated AQI trend over time |
| **Bar Chart**  | AQI comparison across mock city values |
| **Pie Chart**  | AQI pollutant component breakdown |
| **Scatter Plot** | Randomized sensor-like data |
| **Histogram** | Distribution of AQI sample data |

 AQI Interpretation Scale

| AQI Level | Description | Icon |
|-----------|-------------|------|
| 1         | Good        | 😊   |
| 2         | Fair        | 🙂   |
| 3         | Moderate    | 😐   |
| 4         | Poor        | 😷   |
| 5         | Very Poor   | ☠️   |

 Notes

- This app uses randomized sample data for visualizations beyond real-time AQI.
- Future enhancements may include live charting, additional pollutants, and database integration.
