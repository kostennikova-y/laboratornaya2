import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("350x450")
        self.window.configure(bg='#f0f0f0')
        
        # Переменные калькулятора
        self.memory = 0
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Поле вывода
        display_frame = tk.Frame(self.window, bg='#f0f0f0')
        display_frame.pack(padx=10, pady=10, fill=tk.X)
        
        display = tk.Entry(display_frame, textvariable=self.result_var, 
                          font=('Arial', 18), justify='right', 
                          state='readonly', bg='white', bd=2, relief='sunken')
        display.pack(fill=tk.X, ipady=8)
        
        # Фрейм для кнопок
        buttons_frame = tk.Frame(self.window, bg='#f0f0f0')
        buttons_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Расположение кнопок
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['M+', '0', '.', '='],
            ['sin', 'cos', 'x²', '√'],
            ['x^y', 'floor', 'ceil', 'MR']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                color = '#e0e0e0'
                if text in ['=', '+', '-', '*', '/']:
                    color = '#ff9999'
                elif text in ['C', '⌫']:
                    color = '#ffcc99'
                elif text in ['sin', 'cos', 'x²', '√', 'floor', 'ceil', 'x^y']:
                    color = '#ccffcc'
                
                btn = tk.Button(buttons_frame, text=text, font=('Arial', 12),
                               bg=color, command=lambda t=text: self.button_click(t),
                               relief='raised', bd=2)
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
        
        # Настройка размеров кнопок
        for i in range(len(buttons)):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def button_click(self, text):
        try:
            if text.isdigit() or text == '.':
                self.input_number(text)
            elif text in ['+', '-', '*', '/', '%']:
                self.input_operator(text)
            elif text == '=':
                self.calculate()
            elif text == 'C':
                self.clear()
            elif text == '⌫':
                self.backspace()
            elif text in ['sin', 'cos', 'x²', '√', 'floor', 'ceil']:
                self.unary_operation(text)
            elif text == 'x^y':
                self.input_operator('^')
            elif text in ['M+', 'MR']:
                self.memory_operation(text)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            self.clear()
    
    def input_number(self, num):
        if self.current_input == "0" or self.result_var.get() == "Error":
            self.current_input = num
        else:
            self.current_input += num
        self.result_var.set(self.current_input)
    
    def input_operator(self, op):
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/', '%', '^']:
            self.current_input += op
            self.result_var.set(self.current_input)
    
    def unary_operation(self, func):
        if not self.current_input:
            return
            
        try:
            value = float(self.current_input)
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'x²':
                result = value ** 2
            elif func == '√':
                result = math.sqrt(value)
            elif func == 'floor':
                result = math.floor(value)
            elif func == 'ceil':
                result = math.ceil(value)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except ValueError as e:
            self.result_var.set("Error")
            self.current_input = ""
    
    def calculate(self):
        try:
            # Заменяем операторы для eval
            expression = self.current_input.replace('^', '**')
            
            # Обрабатываем процент
            if '%' in expression:
                parts = expression.split('%')
                if len(parts) == 2:
                    expression = f"{parts[0]}*{parts[1]}/100"
            
            result = eval(expression)
            
            # Форматируем результат
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            
        except:
            self.result_var.set("Error")
            self.current_input = ""
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input if self.current_input else "0")
    
    def memory_operation(self, op):
        try:
            current_value = float(self.result_var.get())
            if op == 'M+':
                self.memory += current_value
                messagebox.showinfo("Память", f"Значение добавлено в память: {self.memory}")
            elif op == 'MR':
                self.current_input = str(self.memory)
                self.result_var.set(self.current_input)
        except:
            messagebox.showerror("Ошибка", "Некорректное значение")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
