import tkinter as tk
from tkinter import messagebox
import numpy as np

def lagrange_interpolation(x, y, target):
    n = len(x)
    result = 0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (target - x[j]) / (x[i] - x[j])
        result += term
    return result

def linear_interpolation(x, y, target):
    for i in range(len(x) - 1):
        if x[i] <= target <= x[i + 1]:
            return y[i] + (y[i + 1] - y[i]) * (target - x[i]) / (x[i + 1] - x[i])
    return None

def calculate_error(predicted, actual):
    absolute_error = abs(predicted - actual)
    relative_error = (absolute_error / actual) * 100 if actual != 0 else float('inf')
    return absolute_error, relative_error

def interpolate():
    try:
        # Get inputs
        x_values = list(map(float, x_entry.get().split(',')))
        y_values = list(map(float, y_entry.get().split(',')))
        target = float(target_entry.get())
        actual = float(actual_entry.get())
        
        # Validate input
        if len(x_values) != len(y_values):
            messagebox.showerror("Input Error", "X and Y values must have the same length.")
            return

        # Determine the interpolation method
        if len(x_values) > 3:
            predicted = lagrange_interpolation(x_values, y_values, target)
            method = "Lagrange Interpolation"
        else:
            predicted = linear_interpolation(x_values, y_values, target)
            method = "Linear Interpolation"
        
        # Calculate errors
        absolute_error, relative_error = calculate_error(predicted, actual)
        
        # Display results
        result_text.set(f"Method: {method}\n"
                        f"Predicted Value: {predicted:.4f}\n"
                        f"Absolute Error: {absolute_error:.4f}\n"
                        f"Relative Error: {relative_error:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI
root = tk.Tk()
root.title("Interpolation Calculator")
root.geometry("400x400")

# Input fields
tk.Label(root, text="X Values (comma-separated):").pack()
x_entry = tk.Entry(root, width=50)
x_entry.pack()

tk.Label(root, text="Y Values (comma-separated):").pack()
y_entry = tk.Entry(root, width=50)
y_entry.pack()

tk.Label(root, text="Target X Value:").pack()
target_entry = tk.Entry(root, width=50)
target_entry.pack()

tk.Label(root, text="Actual Y Value:").pack()
actual_entry = tk.Entry(root, width=50)
actual_entry.pack()

# Interpolation button
interpolate_button = tk.Button(root, text="Interpolate", command=interpolate)
interpolate_button.pack(pady=10)

# Results display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

# Run the GUI
root.mainloop()
