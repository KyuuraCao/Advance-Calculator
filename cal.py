import tkinter as tk
from tkinter import ttk
import random
import math

class pyCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Advance Calculator")
        master.geometry("500x600")
        master.resizable(False, False)

        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.current_calculation = ""

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"), padding=3)

        result_frame = tk.Frame(self.master, bg="#FFD700")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.calculation_display = tk.Label(result_frame, text="", font=("Arial", 14), anchor="e", bg="#FFFACD")
        self.calculation_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))

        result_display = tk.Entry(result_frame, textvariable=self.result_var, font=("Arial", 24), justify="right", bd=10, bg="#FFFACD")
        result_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        button_frame = tk.Frame(self.master)
        button_frame.pack(fill=tk.BOTH, expand=True)

        buttons = [
            'sin', 'cos', 'tan', 'log10', 'ln',
            '(', ')', '^', 'sqrt', 'log2',
            '7', '8', '9', '/', 'logb',
            '4', '5', '6', '*', 'pi',
            '1', '2', '3', '-', 'e',
            '0', '.', '=', '+', 'C'
        ]

        row, col = 0, 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            btn = ttk.Button(button_frame, text=button, command=cmd)
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)
            col += 1
            if col > 4:
                col = 0
                row += 1

        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

        self.colorize_buttons()

    def click(self, key):
        if key == '=':
            try:
                result = self.evaluate_expression(self.current_calculation)
                self.result_var.set(result)
                self.current_calculation = str(result)
            except Exception as e:
                self.result_var.set("Error")
                self.current_calculation = ""
        elif key == 'C':
            self.clear()
        else:
            if self.result_var.get() == "0" or self.result_var.get() == "Error":
                self.current_calculation = key
            else:
                self.current_calculation += key
            self.result_var.set(self.current_calculation)
        
        self.calculation_display.config(text=self.current_calculation)

    def clear(self):
        self.result_var.set("0")
        self.current_calculation = ""
        self.calculation_display.config(text="")

    def colorize_buttons(self):
        bright_colors = ["#FF69B4", "#FF6347", "#FF7F50", "#FFD700", "#7FFFD4", "#00FA9A", "#00CED1", "#1E90FF"]
        for child in self.master.winfo_children():
            if isinstance(child, tk.Frame):
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, ttk.Button):
                        color = random.choice(bright_colors)
                        style = ttk.Style()
                        style.configure(f"{grandchild['text']}.TButton", background=color)
                        grandchild.configure(style=f"{grandchild['text']}.TButton")

    def on_enter(self, event):
        event.widget['style'] = f"hover.TButton"
        style = ttk.Style()
        style.configure(f"hover.TButton", background="#F0E68C", font=("Arial", 10, "bold"))

    def on_leave(self, event):
        button_text = event.widget['text']
        event.widget['style'] = f"{button_text}.TButton"

    def evaluate_expression(self, expression):
        # Replace mathematical functions and constants with their Python equivalents
        expression = expression.replace('^', '**')
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log10', 'math.log10')
        expression = expression.replace('ln', 'math.log')
        expression = expression.replace('log2', 'math.log2')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('pi', 'math.pi')
        expression = expression.replace('e', 'math.e')

        # Handle custom base logarithm
        if 'logb' in expression:
            base, value = expression.split('logb')
            return math.log(float(value), float(base))

        # Evaluate the expression
        return eval(expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = pyCalculator(root)
    root.mainloop()
