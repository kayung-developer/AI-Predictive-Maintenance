import random
import tkinter as tk
import customtkinter as ctk
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import joblib  # For saving/loading models



# Function to generate random colors
def generate_random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to generate button colors based on functionality
def generate_button_colors(button_type):
    # Define default colors for each button type
    if button_type == "Upload Data":
        bg_color = generate_random_color()
        hover_color = generate_random_color()
    elif button_type == "Train Model":
        bg_color = generate_random_color()
        hover_color = generate_random_color()
    elif button_type == "Predict Maintenance":
        bg_color = generate_random_color()
        hover_color = generate_random_color()
    elif button_type == "Show Visualization":
        bg_color = generate_random_color()
        hover_color = generate_random_color()
    else:
        bg_color = generate_random_color()
        hover_color = generate_random_color()

    return bg_color, hover_color

# Example of AI-based predictive maintenance model (simplified)
class PredictiveMaintenanceAI:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()

    def train_model(self, data):
        # Preprocessing and model training
        X = data.drop(columns=['Failure'])
        y = data['Failure']
        X_scaled = self.scaler.fit_transform(X)

        self.model = RandomForestClassifier()
        self.model.fit(X_scaled, y)

        # Save the trained model
        joblib.dump(self.model, 'predictive_maintenance_model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')

    def predict(self, data):
        if self.model is None:
            raise ValueError("Model is not trained yet.")

        X_scaled = self.scaler.transform(data)
        predictions = self.model.predict(X_scaled)
        return predictions


# Create UI for Predictive Maintenance Application
class PredictiveMaintenanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI for Predictive Maintenance in Manufacturing")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg="white")

        self.data = {
            'Machine': ['Machine 1', 'Machine 2', 'Machine 3', 'Machine 4', 'Machine 5'],
            'Failure': ['Failure', 'Success', 'Failure', 'Failure', 'Success'],
            'Time_to_failure': [30, 200, 45, 50, 100]
        }

        self.df = pd.DataFrame(self.data)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=6, sticky="nsew")

        #self.upload_button = ctk.CTkButton(self.sidebar, text="Upload Data", command=self.upload_data)
        #self.upload_button.grid(row=1, column=0, padx=20, pady=10)

        #self.train_button = ctk.CTkButton(self.sidebar, text="Train Model", command=self.train_model)
        #self.train_button.grid(row=2, column=0, padx=20, pady=10)

        #self.predict_button = ctk.CTkButton(self.sidebar, text="Predict Maintenance", command=self.predict_maintenance)
        #self.predict_button.grid(row=3, column=0, padx=20, pady=10)

        #self.plot_button = ctk.CTkButton(self.sidebar, text="Show Visualization", command=self.plot_data)
        #self.plot_button.grid(row=4, column=0, padx=20, pady=10)

        # Create buttons with random colors based on functionality
        self.upload_button = self.create_button("Upload Data")
        self.upload_button.grid(row=1, column=0, padx=20, pady=10)

        self.train_button = self.create_button("Train Model")
        self.train_button.grid(row=2, column=0, padx=20, pady=10)

        self.predict_button = self.create_button("Predict Maintenance")
        self.predict_button.grid(row=3, column=0, padx=20, pady=10)

        self.plot_button = self.create_button("Show Visualization")
        self.plot_button.grid(row=4, column=0, padx=20, pady=10)

        self.results_text = ctk.CTkTextbox(self, width=500, height=300)
        self.results_text.grid(row=1, column=1, rowspan=4, padx=20, pady=10)



        self.data = None
        self.model = PredictiveMaintenanceAI()

    def create_button(self, button_type):
        # Generate colors for the button based on functionality
        bg_color, hover_color = generate_button_colors(button_type)

        # Use switch-case equivalent for method selection
        button_methods = {
            "Upload Data": self.upload_data,
            "Train Model": self.train_model,
            "Predict Maintenance": self.predict_maintenance,
            "Show Visualization": self.plot_data
        }

        # Create button and assign the corresponding function
        button = ctk.CTkButton(self.sidebar, text=button_type, command=button_methods[button_type],
                               fg_color=bg_color, hover_color=hover_color)
        return button
    def upload_data(self):
        # Placeholder: Upload data logic
        file_path = ctk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.results_text.insert(tk.END, f"Data loaded from {file_path}\n")

    def train_model(self):
        if self.data is None:
            self.results_text.insert(tk.END, "No data uploaded.\n")
            return

        try:
            self.model.train_model(self.data)
            self.results_text.insert(tk.END, "Model training completed and saved.\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Error training model: {e}\n")

    def predict_maintenance(self):
        if self.data is None:
            self.results_text.insert(tk.END, "No data uploaded.\n")
            return

        try:
            predictions = self.model.predict(self.data.drop(columns=['Failure']))
            self.results_text.insert(tk.END, f"Predictions: {predictions}\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Error predicting maintenance: {e}\n")

    def plot_data(self):
        # Check if data is available

        if self.data is None:
            self.results_text.insert(tk.END, "No data to plot.\n")
            return

        # Check if the 'Failure' column exists
        if 'Failure' not in self.data.columns:
            self.results_text.insert(tk.END, "'Failure' column not found in data.\n")
            return

        # Check for the unique values in 'Failure' (for success/failure categories)
        failure_counts = self.data['Failure'].value_counts()

        # If 'Failure' column contains more than two categories (e.g., 'Failure' and 'Success'),
        # we will plot them separately.
        if len(failure_counts) > 1:
            plt.figure(figsize=(6, 4))
            failure_counts.plot(kind='bar', color=['red', 'green'])  # Custom colors for failure/success
            plt.title("Failure Distribution")
            plt.xlabel("Failure Type")
            plt.ylabel("Count")
            failure_type = "Failure Types"
        else:
            # If only one type (failure or success), we will show just success or failure count
            plt.figure(figsize=(6, 4))
            self.data['Failure'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red'])
            plt.title("Success vs Failure")
            failure_type = "Success vs Failure"

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), self)
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        canvas.draw()

        # Provide a message about what was plotted
        self.results_text.insert(tk.END, f"{failure_type} plotted successfully.\n")


if __name__ == "__main__":
    app = PredictiveMaintenanceApp()
    app.mainloop()
