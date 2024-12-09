import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Interpolation Methods
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

def cubic_spline_interpolation(x, y, target):
    cs = CubicSpline(x, y)
    return cs(target)

def calculate_error(predicted, actual):
    absolute_error = abs(predicted - actual)
    relative_error = (absolute_error / actual) * 100 if actual != 0 else float('inf')
    return absolute_error, relative_error

def plot_graph(x, y, target, predicted):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', label='Data Points')
    plt.axvline(target, color='red', linestyle='--', label='Target X')
    plt.scatter([target], [predicted], color='green', label=f'Predicted Y: {predicted:.4f}')
    
    # Plot interpolation methods
    xp = np.linspace(min(x), max(x), 500)
    lagrange_y = [lagrange_interpolation(x, y, xi) for xi in xp]
    cubic_y = CubicSpline(x, y)(xp)
    plt.plot(xp, lagrange_y, color='purple', linestyle='-', label='Lagrange Interpolation')
    plt.plot(xp, cubic_y, color='orange', linestyle='--', label='Cubic Spline Interpolation')
    
    plt.title('Interpolation Results')
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.legend()
    plt.grid(True)
    plt.show()

def interpolate():
    try:
        # Collect inputs
        x_values = [float(row[0].get()) for row in rows]
        y_values = [float(row[1].get()) for row in rows]
        target = float(target_entry.get())
        
        # Check for duplicate x values
        if len(x_values) != len(set(x_values)):
            messagebox.showerror("Input Error", "X values must be unique.")
            return
        
        if len(x_values) < 2:
            messagebox.showerror("Input Error", "At least two data points are required.")
            return
        
        # Choose interpolation method
        if len(x_values) > 3:
            predicted = cubic_spline_interpolation(x_values, y_values, target)
            method = "Cubic Spline Interpolation"
        elif len(x_values) > 2:
            predicted = lagrange_interpolation(x_values, y_values, target)
            method = "Lagrange Interpolation"
        else:
            predicted = linear_interpolation(x_values, y_values, target)
            method = "Linear Interpolation"
        
        # Display predictions
        result_text.set(f"Method: {method}\n"
                        f"Predicted Value: {predicted:.4f}\n")
        
        # Enable true value input for error calculation
        true_value_frame.pack(pady=10)
        predict_button.config(state=tk.DISABLED)

        # Plot the graph
        plot_graph(x_values, y_values, target, predicted)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def calculate_true_error():
    try:
        actual = float(true_value_entry.get())
        predicted = float(result_text.get().split("\n")[1].split(": ")[1])
        absolute_error, relative_error = calculate_error(predicted, actual)
        
        result_text.set(result_text.get() +
                        f"Absolute Error: {absolute_error:.4f}\n"
                        f"Relative Error: {relative_error:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_row():
    row = [tk.Entry(data_frame, width=10), tk.Entry(data_frame, width=10)]
    row[0].grid(row=len(rows), column=0, padx=5, pady=2)
    row[1].grid(row=len(rows), column=1, padx=5, pady=2)
    rows.append(row)

# GUI Setup
root = tk.Tk()
root.title("Enhanced Interpolation Calculator")
root.geometry("600x600")

# Data Input
tk.Label(root, text="Enter Data Points (X and Y):").pack(pady=5)
data_frame = tk.Frame(root)
data_frame.pack()

# Headers
tk.Label(data_frame, text="X", width=10).grid(row=0, column=0)
tk.Label(data_frame, text="Y", width=10).grid(row=0, column=1)

# Add initial rows
rows = []
for _ in range(2):
    add_row()

tk.Button(root, text="Add Row", command=add_row).pack(pady=5)

# Target Input
tk.Label(root, text="Target X Value:").pack()
target_entry = tk.Entry(root, width=30)
target_entry.pack()

# Interpolate Button
predict_button = tk.Button(root, text="Predict", command=interpolate)
predict_button.pack(pady=10)

# Results Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

# True Value Error Calculation
true_value_frame = tk.Frame(root)
tk.Label(true_value_frame, text="Enter True Value:").pack(side=tk.LEFT)
true_value_entry = tk.Entry(true_value_frame, width=15)
true_value_entry.pack(side=tk.LEFT, padx=5)
tk.Button(true_value_frame, text="Calculate Error", command=calculate_true_error).pack(side=tk.LEFT)

# Start GUI
root.mainloop()
