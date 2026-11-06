import sqlite3
from datetime import datetime

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()
    
    # Таблица для логов тренировок
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
    print("✓ Тренировка успешно записана в базу данных!")

def show_history():
    """Вывод всей истории из БД"""
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT workout_date, exercise_name, weight, sets, reps FROM workouts')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("История тренировок пока пуста.")
        return
        
    print("\n=== ИСТОРИЯ ТРЕНИРОВОК ===")
    print(f"{'Дата':<17} | {'Упражнение':<15} | {'Вес':<6} | {'Подходы':<7} | {'Повторы'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<17} | {row[1]:<15} | {row[2]:<6} | {row[3]:<7} | {row[4]}")
    print("=" * 60)

# Простой текстовый интерфейс управления
if __name__ == "__main__":
    init_db()
    while True:
        print("\n1. Добавить тренировку")
        print("2. Посмотреть историю")
        print("3. Выйти")
        choice = input("Выберите действие: ")
        
        if choice == '1':
            ex = input("Название упражнения (например, Жим лежа): ")
            w = float(input("Рабочий вес (кг): "))
            s = int(input("Количество подходов: "))
            r = int(input("Количество повторений в подходе: "))
            add_workout(ex, w, s, r)
        elif choice == '2':
            show_history()
        elif choice == '3':
            break
        else:
            print("Неверный ввод.")
