import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            weight REAL NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            workout_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_workout(exercise, weight, sets, reps):
    """Сохранение новой тренировки в БД"""
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cursor.execute('''
        INSERT INTO workouts (exercise_name, weight, sets, reps, workout_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (exercise, weight, sets, reps, date_str))
    
    conn.commit()
    conn.close()

def get_history():
    """Получение всей истории из БД"""
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT workout_date, exercise_name, weight, sets, reps FROM workouts ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Графический интерфейс (GUI) ---

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер тренировок")
        self.root.geometry("650x450")
        
        # Левая панель: Форма ввода (используем ttk.LabelFrame для корректной поддержки padding)
        form_frame = ttk.LabelFrame(root, text=" Добавить тренировку ", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(form_frame, text="Упражнение:").pack(anchor=tk.W, pady=2)
        self.entry_ex = tk.Entry(form_frame, width=25)
        self.entry_ex.pack(fill=tk.X, pady=2)
        
        tk.Label(form_frame, text="Рабочий вес (кг):").pack(anchor=tk.W, pady=2)
        self.entry_w = tk.Entry(form_frame, width=25)
        self.entry_w.pack(fill=tk.X, pady=2)
        
        tk.Label(form_frame, text="Количество подходов:").pack(anchor=tk.W, pady=2)
        self.entry_s = tk.Entry(form_frame, width=25)
        self.entry_s.pack(fill=tk.X, pady=2)
        
        tk.Label(form_frame, text="Повторений в подходе:").pack(anchor=tk.W, pady=2)
        self.entry_r = tk.Entry(form_frame, width=25)
        self.entry_r.pack(fill=tk.X, pady=2)
        
        btn_add = tk.Button(form_frame, text="Сохранить", bg="#4CAF50", fg="white", command=self.save_data)
        btn_add.pack(fill=tk.X, pady=15)
        
        # Правая панель: Таблица истории (используем ttk.LabelFrame для корректной поддержки padding)
        history_frame = ttk.LabelFrame(root, text=" История тренировок ", padding=10)
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Настройка таблицы (Treeview)
        columns = ("date", "exercise", "weight", "sets", "reps")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("exercise", text="Упражнение")
        self.tree.heading("weight", text="Вес (кг)")
        self.tree.heading("sets", text="Подходы")
        self.tree.heading("reps", text="Повторы")
        
        self.tree.column("date", width=110, anchor=tk.CENTER)
        self.tree.column("exercise", width=120, anchor=tk.W)
        self.tree.column("weight", width=60, anchor=tk.CENTER)
        self.tree.column("sets", width=60, anchor=tk.CENTER)
        self.tree.column("reps", width=60, anchor=tk.CENTER)
        
        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Загружаем данные при старте
        self.update_table()

    def save_data(self):
        """Валидация и сохранение данных из формы"""
        ex = self.entry_ex.get().strip()
        w_raw = self.entry_w.get().strip()
        s_raw = self.entry_s.get().strip()
        r_raw = self.entry_r.get().strip()
        
        if not ex or not w_raw or not s_raw or not r_raw:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
            
        try:
            w = float(w_raw)
            s = int(s_raw)
            r = int(r_raw)
        except ValueError:
            messagebox.showerror("Ошибка", "Вес должен быть числом, а подходы и повторы — целыми числами!")
            return
            
        # Запись в БД и обновление интерфейса
        add_workout(ex, w, s, r)
        self.update_table()
        
        # Очистка полей ввода
        self.entry_ex.delete(0, tk.END)
        self.entry_w.delete(0, tk.END)
        self.entry_s.delete(0, tk.END)
        self.entry_r.delete(0, tk.END)
        messagebox.showinfo("Успех", "Тренировка успешно записана!")

    def update_table(self):
        """Обновление записей в таблице интерфейса"""
        # Очищаем старые строки
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Добавляем актуальные из БД
        for row in get_history():
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    init_db()
    window = tk.Tk()
    app = WorkoutApp(window)
    window.mainloop()
