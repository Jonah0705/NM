import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


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
        x_values = []
        y_values = []
        for row in rows:
            x_val = row[0].get()
            y_val = row[1].get()
            if not x_val or not y_val:
                raise ValueError("All X and Y values must be filled.")
            x_values.append(float(x_val))
            y_values.append(float(y_val))

        target = target_entry.get()
        if not target:
            raise ValueError("Target value must be filled.")
        target = float(target)

        if len(x_values) != len(set(x_values)):
            raise ValueError("X values must be unique.")

        if len(x_values) < 2:
            raise ValueError("At least two data points are required.")

        if target < min(x_values) or target > max(x_values):
            raise ValueError("Target value must be within the range of X values.")

        if len(x_values) > 3:
            predicted = cubic_spline_interpolation(x_values, y_values, target)
            method = "Cubic Spline Interpolation"
        elif len(x_values) > 2:
            predicted = lagrange_interpolation(x_values, y_values, target)
            method = "Lagrange Interpolation"
        else:
            predicted = linear_interpolation(x_values, y_values, target)
            method = "Linear Interpolation"

        result_text.set(f"Method: {method}\nPredicted Value: {predicted:.4f}\n")
        true_value_frame.pack(pady=10)

        plot_graph(x_values, y_values, target, predicted)
    except Exception as e:
        result_text.set("")
        messagebox.showerror("Error", str(e))


def calculate_true_error():
    try:
        actual = float(true_value_entry.get())
        predicted = float(result_text.get().split("\n")[1].split(": ")[1])
        absolute_error, relative_error = calculate_error(predicted, actual)

        result_text.set(result_text.get() +
                        f"Absolute Error: {absolute_error:.4f}\nRelative Error: {relative_error:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_row():
    row = [tk.Entry(data_frame, width=10), tk.Entry(data_frame, width=10)]
    row[0].grid(row=len(rows) + 1, column=0, padx=5, pady=2)
    row[1].grid(row=len(rows) + 1, column=1, padx=5, pady=2)
    delete_button = tk.Button(data_frame, text="Delete", command=lambda: delete_row(row), bg="lightcoral")
    delete_button.grid(row=len(rows) + 1, column=2, padx=5, pady=2)
    row.append(delete_button)
    rows.append(row)
    refresh_delete_buttons()


def delete_row(row):
    for widget in row:
        widget.destroy()
    rows.remove(row)
    refresh_rows()


def refresh_rows():
    for i, row in enumerate(rows):
        row[0].grid(row=i + 1, column=0, padx=5, pady=2)
        row[1].grid(row=i + 1, column=1, padx=5, pady=2)
        row[2].grid(row=i + 1, column=2, padx=5, pady=2)
    refresh_delete_buttons()


def refresh_delete_buttons():
    for row in rows:
        if len(rows) > 1:
            row[2].grid()
        else:
            row[2].grid_remove()


def navigate(event):
    current = event.widget
    row, col = None, None

    for r_idx, row_widgets in enumerate(rows):
        if current in row_widgets[:2]:
            row, col = r_idx, row_widgets.index(current)

    if row is not None and col is not None:
        if event.keysym == "Up" and row > 0:
            rows[row - 1][col].focus()
        elif event.keysym == "Down" and row < len(rows) - 1:
            rows[row + 1][col].focus()
        elif event.keysym == "Left" and col > 0:
            rows[row][col - 1].focus()
        elif event.keysym == "Right" and col < 1:
            rows[row][col + 1].focus()


def clear_all():
    for row in rows:
        for entry in row[:2]:
            entry.delete(0, tk.END)
    target_entry.delete(0, tk.END)
    true_value_entry.delete(0, tk.END)
    result_text.set("")
    true_value_frame.pack_forget()


root = tk.Tk()
root.title("Interpolation Calculator")
root.geometry("600x700")
root.resizable(False, False)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)
tk.Label(input_frame, text="Enter Data Points (X and Y):", font=("Arial", 12)).pack()

data_frame = tk.Frame(input_frame)
data_frame.pack()

headers = ["X", "Y"]
for col, text in enumerate(headers):
    tk.Label(data_frame, text=text, width=10, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=col, padx=5, pady=5)
tk.Label(data_frame, text="Actions", width=10, font=("Arial", 10, "bold"), bg="lightgray").grid(row=0, column=2, padx=5, pady=5)

rows = []
for _ in range(2):
    add_row()

add_row_button = tk.Button(input_frame, text="Add Row", command=add_row, bg="lightblue", font=("Arial", 10, "bold"))
add_row_button.pack(pady=5)

target_frame = tk.Frame(root)
target_frame.pack(pady=10)
tk.Label(target_frame, text="Target X Value:", font=("Arial", 12)).pack(side=tk.LEFT)
target_entry = tk.Entry(target_frame, width=20)
target_entry.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
predict_button = tk.Button(button_frame, text="Predict", command=interpolate, bg="green", fg="white", font=("Arial", 12, "bold"))
predict_button.pack(side=tk.LEFT, padx=5)
clear_button = tk.Button(button_frame, text="Clear", command=clear_all, bg="red", fg="white", font=("Arial", 12, "bold"))
clear_button.pack(side=tk.LEFT, padx=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), justify="left", wraplength=500)
result_label.pack(pady=10)

true_value_frame = tk.Frame(root)
tk.Label(true_value_frame, text="Enter True Value:", font=("Arial", 12)).pack(side=tk.LEFT)
true_value_entry = tk.Entry(true_value_frame, width=15)
true_value_entry.pack(side=tk.LEFT, padx=5)
tk.Button(true_value_frame, text="Calculate Error", command=calculate_true_error, bg="orange", font=("Arial", 10, "bold")).pack(side=tk.LEFT)

root.bind("<Up>", navigate)
root.bind("<Down>", navigate)
root.bind("<Left>", navigate)
root.bind("<Right>", navigate)

root.mainloop()
