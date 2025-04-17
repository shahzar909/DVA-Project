import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

# ----------------- AQI Fetch Function -----------------
def fetch_aqi(city, api_key):
    try:
        cities_coords = {
            "Delhi": (28.6139, 77.2090),
            "Mumbai": (19.0760, 72.8777),
            "Kolkata": (22.5726, 88.3639),
            "Bangalore": (12.9716, 77.5946),
            "Chennai": (13.0827, 80.2707),
            "Hyderabad": (17.3850, 78.4867),
            "Ahmedabad": (23.0225, 72.5714),
            "Pune": (18.5204, 73.8567),
            "Jaipur": (26.9124, 75.7873),
            "Lucknow": (26.8467, 80.9462)
        }
        lat, lon = cities_coords.get(city, (28.6139, 77.2090))
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        res = requests.get(url).json()
        aqi = res['list'][0]['main']['aqi']
        components = res['list'][0]['components']
        return aqi, components
    except Exception as e:
        print("Error:", e)
        return None, {}

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Real-Time AQI Dashboard")
root.geometry("1600x900")  # Adjusted for better visual space
root.configure(bg="#f0f4f8")

# ----------------- Sidebar -----------------
sidebar = tk.Frame(root, width=280, bg="#2c3e50")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

style_label = {"bg": "#2c3e50", "fg": "white", "font": ("Segoe UI", 12)}

tk.Label(sidebar, text="Control Panel", bg="#2c3e50", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=20)
tk.Label(sidebar, text="Enter API Key:", **style_label).pack()
api_entry = tk.Entry(sidebar, width=30)
api_entry.pack(pady=5)

tk.Label(sidebar, text="Select City:", **style_label).pack()
city_combobox = ttk.Combobox(sidebar, values=list({
    "Delhi", "Mumbai", "Kolkata", "Bangalore", "Chennai",
    "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"
}), width=27)
city_combobox.current(0)
city_combobox.pack(pady=10)

# ----------------- Main Area -----------------
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas_frame = tk.Frame(main_frame, bg="white")
canvas_frame.pack(fill=tk.BOTH, expand=True)

# Use grid layout for the visualizations
canvas_frame.grid_rowconfigure(0, weight=1)
canvas_frame.grid_rowconfigure(1, weight=1)
canvas_frame.grid_rowconfigure(2, weight=1)
canvas_frame.grid_columnconfigure(0, weight=1)
canvas_frame.grid_columnconfigure(1, weight=1)
canvas_frame.grid_columnconfigure(2, weight=1)

figures = {}

def create_chart(name, fig, row, col):
    figures[name] = {
        "fig": fig,
        "canvas": FigureCanvasTkAgg(fig, master=canvas_frame)
    }
    figures[name]["canvas"].get_tk_widget().grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

create_chart("bar", plt.Figure(figsize=(5, 3), dpi=100), 0, 0)
create_chart("pie", plt.Figure(figsize=(5, 3), dpi=100), 0, 1)
create_chart("line", plt.Figure(figsize=(5, 3), dpi=100), 1, 0)
create_chart("heatmap", plt.Figure(figsize=(5, 3), dpi=100), 1, 1)
create_chart("scatter", plt.Figure(figsize=(5, 3), dpi=100), 2, 0)

aqi_label_title = tk.Label(canvas_frame, text="Real-Time AQI", font=("Segoe UI", 18, "bold"), bg="white")
aqi_label_title.grid(row=0, column=2, pady=10)

aqi_label_value = tk.Label(canvas_frame, text="AQI Not Available", font=("Segoe UI", 14), bg="white")
aqi_label_value.grid(row=1, column=2)

# ----------------- Update Charts -----------------
def update_charts(aqi, components):
    # Bar Chart
    ax1 = figures["bar"]["fig"].clear()
    ax1 = figures["bar"]["fig"].add_subplot(111)
    ax1.set_title("Pollutant Concentration (µg/m³)")
    labels = list(components.keys())
    values = list(components.values())
    ax1.bar(labels, values, color="#2980b9")
    ax1.tick_params(axis='x', rotation=45)
    figures["bar"]["canvas"].draw()

    # Pie Chart
    ax2 = figures["pie"]["fig"].clear()
    ax2 = figures["pie"]["fig"].add_subplot(111)
    ax2.set_title("Pollutant Distribution")
    ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
    figures["pie"]["canvas"].draw()

    # Line Chart (simulated time variation)
    ax3 = figures["line"]["fig"].clear()
    ax3 = figures["line"]["fig"].add_subplot(111)
    ax3.set_title("Simulated PM2.5 Over Time")
    pm25_data = np.random.normal(components.get("pm2_5", 0), 2, 10)
    ax3.plot(pm25_data, marker='o', linestyle='-', color="#e67e22")
    ax3.set_ylabel("PM2.5 µg/m³")
    figures["line"]["canvas"].draw()

    # Heatmap (simulated)
    ax4 = figures["heatmap"]["fig"].clear()
    ax4 = figures["heatmap"]["fig"].add_subplot(111)
    ax4.set_title("PM2.5 Heatmap")
    data = np.random.rand(10, 10)  # Simulated heatmap data
    sns.heatmap(data, cmap="YlGnBu", ax=ax4)
    figures["heatmap"]["canvas"].draw()

    # Scatter Plot (PM10 vs CO)
    ax5 = figures["scatter"]["fig"].clear()
    ax5 = figures["scatter"]["fig"].add_subplot(111)
    ax5.set_title("PM10 vs CO")
    pm10_data = np.random.normal(components.get("pm10", 0), 10, 50)
    co_data = np.random.normal(components.get("co", 0), 5, 50)
    ax5.scatter(pm10_data, co_data, color="purple")
    ax5.set_xlabel("PM10 µg/m³")
    ax5.set_ylabel("CO µg/m³")
    figures["scatter"]["canvas"].draw()

# ----------------- AQI Fetch and Update -----------------
def update_aqi():
    city = city_combobox.get()
    api_key = api_entry.get().strip()
    if not api_key:
        messagebox.showwarning("Missing API Key", "Please enter a valid API key!")
        return
    aqi, components = fetch_aqi(city, api_key)
    if aqi is not None:
        aqi_status = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor ☠️"
        }
        aqi_label_value.config(text=f"{city}: AQI {aqi} - {aqi_status.get(aqi, 'Unknown')}")
        update_charts(aqi, components)
    else:
        aqi_label_value.config(text="Failed to fetch AQI")

# ----------------- Button -----------------
tk.Button(sidebar, text="Get Real-Time AQI", command=update_aqi, bg="#27ae60", fg="white", font=("Segoe UI", 11)).pack(pady=20)

root.mainloop()
