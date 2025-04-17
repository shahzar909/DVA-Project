import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ----------------- AQI Fetch Function -----------------
def fetch_aqi(city, api_key):
    try:
        cities_coords = {
            "Delhi": (28.6139, 77.2090),
            "Mumbai": (19.0760, 72.8777),
            "Kolkata": (22.5726, 88.3639),
            "Bangalore": (12.9716, 77.5946),
            "Chennai": (13.0827, 80.2707),
        }
        lat, lon = cities_coords.get(city, (28.6139, 77.2090))
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        res = requests.get(url).json()
        print("API Response:", res)
        aqi = res['list'][0]['main']['aqi']
        return aqi
    except Exception as e:
        print("Error:", e)
        return None

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Real-Time AQI Dashboard")
root.geometry("1300x800")

# ----------------- Sidebar -----------------
sidebar = tk.Frame(root, width=250, bg="#add8e6")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(sidebar, text="Control Panel", bg="#add8e6", font=("Helvetica", 14, "bold")).pack(pady=20)

tk.Label(sidebar, text="Enter API Key:", bg="#add8e6").pack()
api_entry = tk.Entry(sidebar, width=30)
api_entry.pack(pady=5)

tk.Label(sidebar, text="Select City for AQI:", bg="#add8e6").pack()
city_combobox = ttk.Combobox(sidebar, values=["Delhi", "Mumbai", "Kolkata", "Bangalore", "Chennai"], width=27)
city_combobox.current(0)
city_combobox.pack(pady=10)

# ----------------- Main Area -----------------
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_frame = tk.Frame(main_frame)
canvas_frame.pack()

# Initialize figure containers
figures = {}

def create_chart(name, fig, row, col):
    figures[name] = {
        "fig": fig,
        "canvas": FigureCanvasTkAgg(fig, master=canvas_frame)
    }
    figures[name]["canvas"].get_tk_widget().grid(row=row, column=col, padx=10, pady=10)

# Create empty charts to be filled on AQI update
create_chart("line", plt.Figure(figsize=(3, 2.5), dpi=100), 0, 0)
create_chart("bar", plt.Figure(figsize=(3, 2.5), dpi=100), 0, 1)
create_chart("pie", plt.Figure(figsize=(3, 2.5), dpi=100), 0, 2)
create_chart("scatter", plt.Figure(figsize=(3, 2.5), dpi=100), 1, 0)
create_chart("hist", plt.Figure(figsize=(3, 2.5), dpi=100), 1, 1)

# AQI Display
aqi_label_title = tk.Label(canvas_frame, text="Real-Time AQI", font=("Helvetica", 16))
aqi_label_title.grid(row=1, column=2, pady=10)

aqi_label_value = tk.Label(canvas_frame, text="AQI Data Not Available", font=("Helvetica", 14))
aqi_label_value.grid(row=2, column=2)

# ----------------- Button Action -----------------
def update_charts(aqi):
    # Update Line Chart
    ax1 = figures["line"]["fig"].clear()
    ax1 = figures["line"]["fig"].add_subplot(111)
    ax1.set_title("AQI Over Time")
    ax1.plot(np.arange(10), np.random.randint(aqi-20, aqi+20, 10))
    figures["line"]["canvas"].draw()

    # Update Bar Chart
    ax2 = figures["bar"]["fig"].clear()
    ax2 = figures["bar"]["fig"].add_subplot(111)
    ax2.set_title("City Comparison")
    ax2.bar(["A", "B", "C"], [aqi, aqi+10, aqi-10])
    figures["bar"]["canvas"].draw()

    # Update Pie Chart
    ax3 = figures["pie"]["fig"].clear()
    ax3 = figures["pie"]["fig"].add_subplot(111)
    ax3.set_title("AQI Component Split")
    ax3.pie([20, 30, 25, 25], labels=["PM2.5", "PM10", "NO2", "O3"], autopct='%1.1f%%')
    figures["pie"]["canvas"].draw()

    # Scatter Plot
    ax4 = figures["scatter"]["fig"].clear()
    ax4 = figures["scatter"]["fig"].add_subplot(111)
    ax4.set_title("Sensor Readings")
    x = np.random.rand(25) * 100
    y = np.random.rand(25) * aqi
    ax4.scatter(x, y)
    figures["scatter"]["canvas"].draw()

    # Histogram
    ax5 = figures["hist"]["fig"].clear()
    ax5 = figures["hist"]["fig"].add_subplot(111)
    ax5.set_title("Random Pollution Samples")
    ax5.hist(np.random.normal(aqi, 10, 1000), bins=30)
    figures["hist"]["canvas"].draw()

def update_aqi():
    city = city_combobox.get()
    api_key = api_entry.get().strip()
    if not api_key:
        messagebox.showwarning("Missing API Key", "Please enter a valid API key!")
        return
    aqi = fetch_aqi(city, api_key)
    if aqi is not None:
        aqi_status = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor ☠️"
        }
        aqi_label_value.config(text=f"{city}: AQI {aqi} - {aqi_status.get(aqi, 'Unknown')}")
        update_charts(aqi)
    else:
        aqi_label_value.config(text="Failed to fetch AQI")

# Button to fetch AQI
tk.Button(sidebar, text="Get Real-Time AQI", command=update_aqi, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
