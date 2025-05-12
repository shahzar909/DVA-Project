import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns
import os
import json

# ----------------- File to Store API Key -----------------
API_FILE = "aqi_api_config.json"

def save_api_key(key):
    with open(API_FILE, "w") as f:
        json.dump({"api_key": key}, f)

def load_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return json.load(f).get("api_key", "")
    return ""

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
root.geometry("1600x900")
root.configure(bg="#f0f4f8")

# ----------------- Sidebar -----------------
sidebar = tk.Frame(root, width=280, bg="#2c3e50")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

style_label = {"bg": "#2c3e50", "fg": "white", "font": ("Segoe UI", 12)}

tk.Label(sidebar, text="Control Panel", bg="#2c3e50", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=20)
tk.Label(sidebar, text="API Key:", **style_label).pack()

api_entry = tk.Entry(sidebar, width=30)
api_entry.insert(0, load_api_key())
api_entry.config(state='disabled')
api_entry.pack(pady=5)

def enable_api_key_edit():
    api_entry.config(state='normal')
    messagebox.showinfo("Edit API Key", "You can now edit the API key. Don’t forget to click 'Save API Key' after editing.")

tk.Button(sidebar, text="Change API Key", command=enable_api_key_edit, bg="#f39c12", fg="white").pack(pady=5)

def save_key():
    key = api_entry.get().strip()
    if key:
        save_api_key(key)
        api_entry.config(state='disabled')
        messagebox.showinfo("Saved", "API Key saved and locked.")
    else:
        messagebox.showerror("Error", "API key cannot be empty.")

tk.Button(sidebar, text="Save API Key", command=save_key, bg="#16a085", fg="white").pack(pady=5)

tk.Label(sidebar, text="Select City:", **style_label).pack()
city_combobox = ttk.Combobox(sidebar, values=[
    "Delhi", "Mumbai", "Kolkata", "Bangalore", "Chennai",
    "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"
], width=27)
city_combobox.set("Delhi")
city_combobox.pack(pady=10)

# ----------------- Main Area -----------------
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas_frame = tk.Frame(main_frame, bg="white")
canvas_frame.pack(fill=tk.BOTH, expand=True)

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

def update_charts(aqi, components):
    labels = list(components.keys())
    values = list(components.values())

    ax1 = figures["bar"]["fig"].clear()
    ax1 = figures["bar"]["fig"].add_subplot(111)
    ax1.set_title("Pollutant Concentration (µg/m³)")
    ax1.bar(labels, values, color="#2980b9")
    ax1.tick_params(axis='x', rotation=45)
    figures["bar"]["canvas"].draw()

    ax2 = figures["pie"]["fig"].clear()
    ax2 = figures["pie"]["fig"].add_subplot(111)
    ax2.set_title("Pollutant Distribution")
    ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
    figures["pie"]["canvas"].draw()

    ax3 = figures["line"]["fig"].clear()
    ax3 = figures["line"]["fig"].add_subplot(111)
    ax3.set_title("Simulated PM2.5 Over Time")
    pm25_data = np.random.normal(components.get("pm2_5", 0), 2, 10)
    ax3.plot(pm25_data, marker='o', linestyle='-', color="#e67e22")
    ax3.set_ylabel("PM2.5 µg/m³")
    figures["line"]["canvas"].draw()

    ax4 = figures["heatmap"]["fig"].clear()
    ax4 = figures["heatmap"]["fig"].add_subplot(111)
    ax4.set_title("PM2.5 Heatmap")
    data = np.random.rand(10, 10)
    sns.heatmap(data, cmap="YlGnBu", ax=ax4)
    figures["heatmap"]["canvas"].draw()

    ax5 = figures["scatter"]["fig"].clear()
    ax5 = figures["scatter"]["fig"].add_subplot(111)
    ax5.set_title("PM10 vs CO")
    pm10_data = np.random.normal(components.get("pm10", 0), 10, 50)
    co_data = np.random.normal(components.get("co", 0), 5, 50)
    ax5.scatter(pm10_data, co_data, color="purple")
    ax5.set_xlabel("PM10 µg/m³")
    ax5.set_ylabel("CO µg/m³")
    figures["scatter"]["canvas"].draw()

def update_aqi():
    city = city_combobox.get()
    api_key = load_api_key()
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

def reset_dashboard():
    city_combobox.set("")
    aqi_label_value.config(text="AQI Not Available")
    for chart in figures.values():
        chart["fig"].clear()
        chart["canvas"].draw()

def open_compare_screen():
    def compare():
        c1 = combo_city1.get()
        c2 = combo_city2.get()
        key = load_api_key()
        if not key:
            messagebox.showerror("API Key Missing", "Enter API key before comparing.")
            return
        aqi1, _ = fetch_aqi(c1, key)
        aqi2, _ = fetch_aqi(c2, key)
        if aqi1 is None or aqi2 is None:
            messagebox.showerror("Error", "Failed to fetch AQI data.")
            return
        plt.figure(figsize=(6, 4))
        plt.bar([c1, c2], [aqi1, aqi2], color=["#3498db", "#e74c3c"])
        plt.title("AQI Comparison")
        plt.ylabel("AQI")
        plt.grid(True)
        plt.show()

    win = tk.Toplevel(root)
    win.title("Compare AQI")
    win.geometry("300x200")
    tk.Label(win, text="City 1").pack(pady=5)
    combo_city1 = ttk.Combobox(win, values=city_combobox["values"])
    combo_city1.pack()
    tk.Label(win, text="City 2").pack(pady=5)
    combo_city2 = ttk.Combobox(win, values=city_combobox["values"])
    combo_city2.pack()
    tk.Button(win, text="Compare", command=compare).pack(pady=10)

# ----------------- Buttons -----------------
tk.Button(sidebar, text="Get Real-Time AQI", command=update_aqi, bg="#27ae60", fg="white", font=("Segoe UI", 11)).pack(pady=20)
tk.Button(sidebar, text="Compare Two Cities", command=open_compare_screen, bg="#2980b9", fg="white", font=("Segoe UI", 11)).pack(pady=10)
tk.Button(sidebar, text="Reset", command=reset_dashboard, bg="#c0392b", fg="white", font=("Segoe UI", 11)).pack(pady=10)

root.mainloop()
