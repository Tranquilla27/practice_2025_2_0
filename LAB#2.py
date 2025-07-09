import tkinter as tk
from tkinter import messagebox, ttk

class MathEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Математический редактор формул")
        self.geometry("700x400")
        self.configure(bg="#f0f0f0")
        self.attributes('-topmost', False)

        self.formula_window = None
        self.input_frame = None
        self.variable_widgets = []
        self.main_formula_loaded = False
        self.nested_formulas = {}

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        formula_menu = tk.Menu(menubar, tearoff=0)
        formula_menu.add_command(label="Добавить формулу", command=self.start_formula_addition_from_menu)
        formula_menu.add_command(label="Поиск")
        formula_menu.add_command(label="Импорт")
        menubar.add_cascade(label="Формулы", menu=formula_menu)

        study_menu = tk.Menu(menubar, tearoff=0)
        study_menu.add_command(label="Выбрать тему", command=self.choose_topic_window)
        study_menu.add_command(label="Поиск")
        menubar.add_cascade(label="Обучение", menu=study_menu)

        menubar.add_command(label="Выход", command=self.quit)

        self.label = tk.Label(self, text="Математический редактор формул", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.label.pack(pady=120)

    def start_formula_addition_from_menu(self):
        popup = tk.Toplevel(self)
        popup.title("Выбор формулы")
        popup.geometry("300x150+%d+%d" % (self.winfo_x(), self.winfo_y()))
        popup.transient(self)
        popup.grab_set()
        popup.attributes('-topmost', True)

        tk.Label(popup, text="Здесь будет база данных с формулами", font=("Helvetica", 10)).pack(pady=15)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Отмена", command=popup.destroy).pack(side="left", padx=10)
        tk.Button(button_frame, text="Подтвердить", command=lambda: [popup.destroy(), self.insert_main_formula()]).pack(side="right", padx=10)

    def insert_main_formula(self):
        self.open_formula_editor()
        if self.main_formula_loaded:
            return

        main_frame = tk.Frame(self.formula_window, bg="#ffffff")
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        formula_frame = tk.Frame(main_frame, bg="#ffffff")
        formula_frame.pack(side="left", padx=10)

        formula_label = tk.Label(formula_frame, text="Формула: S = v * t (ПРИМЕР)", font=("Helvetica", 14), fg="blue", bg="#ffffff")
        formula_label.pack()

        self.input_frame = tk.Frame(main_frame, bg="#ffffff")
        self.input_frame.pack(side="left", padx=10, fill="both", expand=True)

        self.variable_widgets = []
        self.add_variable_input("v (скорость):")
        self.add_variable_input("t (время):")

        button_frame = tk.Frame(self.formula_window, pady=15, bg="#ffffff")
        button_frame.pack(side="bottom")

        tk.Button(button_frame, text="Добавить формулу", command=self.open_formula_popup).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Добавить спецсимвол", command=self.add_special_symbol).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Подсчитать ответ", command=self.calculate_result).grid(row=0, column=2, padx=5)

        self.main_formula_loaded = True

    def add_special_symbol(self):
        messagebox.showinfo("Спецсимвол", "Спецсимвол добавлен", parent=self.formula_window)

    def calculate_result(self):
        try:
            v_value = self.get_variable_value(0)
            t_value = self.get_variable_value(1)
            result = v_value * t_value
            messagebox.showinfo("Результат", f"Ответ: S = {result:.2f}", parent=self.formula_window)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e), parent=self.formula_window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}", parent=self.formula_window)

    def get_variable_value(self, index):
        label, widget = self.variable_widgets[index]
        if isinstance(widget, tk.Entry):
            value = widget.get()
            if not value:
                raise ValueError(f"Поле '{label.cget('text')}' не заполнено")
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Некорректное значение в поле '{label.cget('text')}'")
        else:
            if index not in self.nested_formulas:
                raise ValueError(f"Для формулы в поле '{label.cget('text')}' не заданы переменные")
            x_entry, y_entry = self.nested_formulas[index]
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
            except ValueError:
                raise ValueError(f"Некорректные значения для формулы в поле '{label.cget('text')}'")
            if y == 0:
                raise ValueError(f"Деление на ноль в формуле поля '{label.cget('text')}'")
            return (2 * x) / y

    def open_formula_editor(self):
        if self.formula_window and self.formula_window.winfo_exists():
            self.formula_window.lift()
            self.formula_window.focus_force()
            return
        self.formula_window = tk.Toplevel(self)
        self.formula_window.title("Редактор формул")
        self.formula_window.geometry("700x400+%d+%d" % (self.winfo_x(), self.winfo_y()))
        self.formula_window.attributes('-topmost', True)
        self.formula_window.configure(bg="#ffffff")
        self.formula_window.protocol("WM_DELETE_WINDOW", self.on_formula_window_close)

    def on_formula_window_close(self):
        self.main_formula_loaded = False
        self.variable_widgets = []
        self.nested_formulas = {}
        self.formula_window.destroy()

    def add_variable_input(self, label_text, parent=None):
        if parent is None:
            parent = self.input_frame
        label = tk.Label(parent, text=label_text, bg="#ffffff")
        label.pack(anchor="w")
        entry = tk.Entry(parent)
        entry.pack(fill="x", pady=2)
        self.variable_widgets.append((label, entry))

    def open_formula_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Добавление формулы")
        popup.geometry("300x150+%d+%d" % (self.winfo_x(), self.winfo_y()))
        popup.transient(self)
        popup.grab_set()
        popup.attributes('-topmost', True)
        tk.Label(popup, text="Здесь будет база данных с формулами", font=("Helvetica", 10)).pack(pady=15)
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Отмена", command=popup.destroy).pack(side="left", padx=10)
        tk.Button(button_frame, text="Подтвердить", command=lambda: [popup.destroy(), self.insert_formula_block()]).pack(side="right", padx=10)

    def insert_formula_block(self):
        for i, (label_widget, entry_widget) in enumerate(self.variable_widgets):
            if isinstance(entry_widget, tk.Entry) and not entry_widget.get():
                entry_widget.destroy()
                formula_text = "(2 * x) / y (ПРИМЕР)"
                formula = tk.Label(self.input_frame, text=formula_text, fg="green", font=("Helvetica", 12, "italic"), bg="#ffffff")
                formula.pack(fill="x", pady=2)
                self.variable_widgets[i] = (label_widget, formula)

                nested_frame = tk.Frame(self.input_frame, bg="#ffffff")
                nested_frame.pack(padx=20, pady=5, fill="x")
                x_label = tk.Label(nested_frame, text="x (значение):", bg="#ffffff")
                x_label.pack(anchor="w")
                x_entry = tk.Entry(nested_frame)
                x_entry.pack(fill="x", pady=2)
                y_label = tk.Label(nested_frame, text="y (знаменатель):", bg="#ffffff")
                y_label.pack(anchor="w")
                y_entry = tk.Entry(nested_frame)
                y_entry.pack(fill="x", pady=2)
                self.nested_formulas[i] = (x_entry, y_entry)
                messagebox.showinfo("Успешно", f"Формула добавлена в переменную {label_widget.cget('text')}", parent=self.formula_window)
                return
        messagebox.showinfo("Информация", "Нет доступных полей для замены формулой.", parent=self.formula_window)

    def choose_topic_window(self):
        popup = tk.Toplevel(self)
        popup.title("Выбор темы")
        popup.geometry("300x150+%d+%d" % (self.winfo_x(), self.winfo_y()))
        popup.transient(self)
        popup.grab_set()
        popup.attributes('-topmost', True)

        tk.Label(popup, text="Здесь будет база данных с темами", font=("Helvetica", 10)).pack(pady=15)
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Отмена", command=popup.destroy).pack(side="left", padx=10)
        tk.Button(button_frame, text="Продолжить", command=lambda: [popup.destroy(), self.open_study_window()]).pack(side="right", padx=10)

    def open_study_window(self):
        study = tk.Toplevel(self)
        study.title("Изучение тем")
        study.geometry("700x400+%d+%d" % (self.winfo_x(), self.winfo_y()))
        study.configure(bg="#f9f9f9")
        study.attributes('-topmost', True)
        study.transient(self)
        study.grab_set()

        ttk.Label(study, text="Выберите формат материала:", font=("Helvetica", 13)).pack(pady=30)

        middle_frame = ttk.Frame(study, padding=20)
        middle_frame.pack()

        style = ttk.Style()
        style.configure("Big.TButton", font=("Helvetica", 12), padding=8)

        buttons = ["Лекции", "Презентации", "Видеоматериалы"]
        for i, text in enumerate(buttons):
            ttk.Button(middle_frame, text=text, style="Big.TButton",
                       command=lambda t=text: messagebox.showinfo(t, f"Открыт раздел: {t}", parent=study)).grid(row=0, column=i, padx=5, pady=10)

        ttk.Button(middle_frame, text="Сохранение прогресса", style="Big.TButton",
                   command=lambda: messagebox.showinfo("Прогресс", "Прогресс сохранён", parent=study)).grid(row=1, columnspan=3, pady=20)

if __name__ == "__main__":
    app = MathEditorApp()
    app.mainloop()
