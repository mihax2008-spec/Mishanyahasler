import sqlite3
import math
import tkinter as tk
from tkinter import messagebox, ttk

def get_last_workout_from_db():
    """Автоматически берет последнее упражнение и вес из базы данных Первой версии"""
    try:
        conn = sqlite3.connect('workout_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT exercise_name, weight, reps FROM workouts ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.OperationalError:
        return None

def calculate_1rm(weight, reps):
    """Математическая модель Эпли для расчета Одноповторного Максимума (1RM)"""
    if reps <= 1:
        return weight
    return weight * (1 + reps / 30)

def simulate_experiment(exercise_name, base_weight, base_reps, fatigue_factor):
    """Возвращает лог симуляции в виде строки и суммарный тоннаж"""
    log_text = f"Упражнение: {exercise_name.upper()}\n"
    log_text += f"Исходные данные: {base_weight} кг х {base_reps} пов. (Фактор утомления: {fatigue_factor})\n"
    log_text += "-" * 50 + "\n"
    
    current_reps = base_reps
    total_volume = 0
    total_sets = 4
    
    for set_num in range(1, total_sets + 1):
        if set_num > 1:
            current_reps = max(0, round(base_reps - (set_num - 1) * fatigue_factor))
        
        if current_reps <= 0:
            log_text += f"Подход {set_num}: Отказ мышц! Не выполнено.\n"
            break
            
        set_volume = base_weight * current_reps
        total_volume += set_volume
        predicted_max = calculate_1rm(base_weight, current_reps)
        
        log_text += f"Подход #{set_num}: {base_weight} кг х {current_reps} пов. | Объем: {set_volume} кг | Сила: {predicted_max:.1f} кг\n"
        
    log_text += "-" * 50 + "\n"
    log_text += f"ИТОГ: Суммарный тоннаж = {total_volume} кг\n"
    return total_volume, log_text

# --- Графический интерфейс (GUI) ---

class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вычислительный эксперимент: Моделирование утомления")
        self.root.geometry("800x550")
        
        # Попытка загрузить данные из БД
        db_data = get_last_workout_from_db()
        if db_data:
            init_ex, init_w, init_r = db_data
            status_msg = "✓ Данные успешно загружены из вашей базы данных!"
        else:
            init_ex, init_w, init_r = "Жим штанги лежа", 80.0, 10
            status_msg = "⚠ БД не найдена или пуста. Используются параметры по умолчанию."
            
        # Панель статуса вверху
        lbl_status = tk.Label(root, text=status_msg, fg="green" if db_data else "orange", font=("Arial", 10, "italic"))
        lbl_status.pack(anchor=tk.W, padx=15, pady=5)
        
        # Главный контейнер на два столбца (Слева настройки, справа результаты)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # --- ЛЕВАЯ КОЛОНКА: Ввод параметров ---
        left_frame = tk.Frame(main_frame, width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Группа: Параметры упражнения
        input_frame = ttk.LabelFrame(left_frame, text=" Входные данные для теста ", padding=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Название упражнения:").pack(anchor=tk.W)
        self.entry_ex = tk.Entry(input_frame)
        self.entry_ex.insert(0, str(init_ex))
        self.entry_ex.pack(fill=tk.X, pady=2)
        
        tk.Label(input_frame, text="Рабочий вес (кг):").pack(anchor=tk.W)
        self.entry_w = tk.Entry(input_frame)
        self.entry_w.insert(0, str(init_w))
        self.entry_w.pack(fill=tk.X, pady=2)
        
        tk.Label(input_frame, text="Повторения в первом подходе:").pack(anchor=tk.W)
        self.entry_r = tk.Entry(input_frame)
        self.entry_r.insert(0, str(init_r))
        self.entry_r.pack(fill=tk.X, pady=2)
        
        # Группа: Настройки сценариев (Факторы утомления)
        scenarios_frame = ttk.LabelFrame(left_frame, text=" Настройка утомляемости ", padding=10)
        scenarios_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(scenarios_frame, text="Сценарий А (Длинный отдых):").pack(anchor=tk.W)
        self.scale_a = tk.Scale(scenarios_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.scale_a.set(0.5)
        self.scale_a.pack(fill=tk.X, pady=2)
        
        tk.Label(scenarios_frame, text="Сценарий Б (Короткий отдых):").pack(anchor=tk.W)
        self.scale_b = tk.Scale(scenarios_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.scale_b.set(1.5)
        self.scale_b.pack(fill=tk.X, pady=2)
        
        # Кнопка запуска расчета
        btn_calc = tk.Button(left_frame, text="Рассчитать эксперимент", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), command=self.run_analysis)
        btn_calc.pack(fill=tk.X, pady=10)
        
        # --- ПРАВАЯ КОЛОНКА: Вывод отчетов ---
        right_frame = ttk.LabelFrame(main_frame, text=" Результаты вычислительного эксперимента ", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Текстовое поле с прокруткой для логов и отчета
        self.txt_report = tk.Text(right_frame, wrap=tk.WORD, font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.txt_report.yview)
        self.txt_report.configure(yscroll=scrollbar.set)
        
        self.txt_report.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Сразу запускаем первичный расчет при открытии окна
        self.run_analysis()

    def run_analysis(self):
        """Считывает данные с формы, выполняет расчет двух сценариев и выводит отчет"""
        ex = self.entry_ex.get().strip()
        w_raw = self.entry_w.get().strip()
        r_raw = self.entry_r.get().strip()
        
        if not ex or not w_raw or not r_raw:
            messagebox.showwarning("Ошибка", "Заполните все текстовые поля ввода!")
            return
            
        try:
            weight = float(w_raw)
            reps = int(r_raw)
        except ValueError:
            messagebox.showerror("Ошибка", "Вес должен быть числом, а повторения — целым числом!")
            return
            
        fatigue_a = self.scale_a.get()
        fatigue_b = self.scale_b.get()
        
        # Вычисляем оба сценария
        vol_a, log_a = simulate_experiment(ex, weight, reps, fatigue_a)
        vol_b, log_b = simulate_experiment(ex, weight, reps, fatigue_b)
        
        # Математический анализ разницы эффективности
        if vol_a > 0:
            efficiency_loss = ((vol_a - vol_b) / vol_a) * 100
        else:
            efficiency_loss = 0.0
            
        # Формируем итоговый текстовый отчет для экрана
        report = "=== СЦЕНАРИЙ А (Длинный отдых / Низкое утомление) ===\n"
        report += log_a + "\n"
        report += "=== СЦЕНАРИЙ Б (Короткий отдых / Высокое утомление) ===\n"
        report += log_b + "\n"
        report += "=" * 55 + "\n"
        report += "АНАЛИЗ ЭФФЕКТИВНОСТИ ЭКСПЕРИМЕНТА\n"
        report += "=" * 55 + "\n"
        report += f"Потеря суммарной эффективности при коротком отдыхе составила: {efficiency_loss:.1f}%\n\n"
        report += "Вывод: Эксперимент наглядно доказывает математическую зависимость\n"
        report += "объема тренировки от времени восстановления между подходами.\n"
        
        # Отображаем сгенерированный текст в окне
        self.txt_report.config(state=tk.NORMAL)  # Разрешаем редактирование текста для обновления
        self.txt_report.delete("1.0", tk.END)    # Очищаем старые данные
        self.txt_report.insert(tk.END, report)   # Вставляем новый отчет
        self.txt_report.config(state=tk.DISABLED) # Запрещаем случайное ручное редактирование пользователем

if __name__ == "__main__":
    window = tk.Tk()
    app = ExperimentApp(window)
    window.mainloop()
