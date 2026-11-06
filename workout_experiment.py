import sqlite3
import math

def get_last_workout_from_db():
    """Автоматически берет последнее упражнение и вес из базы данных Первой версии"""
    try:
        conn = sqlite3.connect('workout_tracker.db')
        cursor = conn.cursor()
        # Выбираем самую последнюю запись из таблицы
        cursor.execute('SELECT exercise_name, weight, reps FROM workouts ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.OperationalError:
        # Если первая версия еще не запускалась и файла БД нет
        return None

def calculate_1rm(weight, reps):
    """Математическая модель Эпли для расчета Одноповторного Максимума (1RM)"""
    if reps == 1:
        return weight
    return weight * (1 + reps / 30)

def run_experiment(exercise_name, base_weight, base_reps, fatigue_factor):
    """
    Вычислительный эксперимент: симуляция падения сил (деградации повторов)
    в зависимости от коэффициента утомляемости (времени отдыха)
    """
    print(f"\n[ЭКСПЕРИМЕНТ] Моделирование для упражнения: {exercise_name.upper()}")
    print(f"Исходные данные из БД: {base_weight} кг на {base_reps} пов. (Фактор утомления: {fatigue_factor})")
    print("-" * 65)
    
    current_reps = base_reps
    total_volume = 0
    total_sets = 4 # Моделируем стандартные 4 подхода
    
    for set_num in range(1, total_sets + 1):
        if set_num > 1:
            # Математическое угасание сил от подхода к подходу
            current_reps = max(0, round(base_reps - (set_num - 1) * fatigue_factor))
        
        if current_reps <= 0:
            print(f"Подход {set_num}: Отказ мышц! Атлет не смог выполнить упражнение.")
            break
            
        set_volume = base_weight * current_reps
        total_volume += set_volume
        predicted_max = calculate_1rm(base_weight, current_reps)
        
        print(f"Подход #{set_num}: {base_weight} кг х {current_reps} пов. | Объем: {set_volume} кг | Прогноз силы: {predicted_max:.1f} кг")
        
    print("-" * 65)
    print(f"ИТОГ ЭКСПЕРИМЕНТА: Суммарный тоннаж = {total_volume} кг")
    return total_volume

if __name__ == "__main__":
    print("=== ЗАПУСК ВЕРСИИ 2: ВЫЧИСЛИТЕЛЬНЫЙ ЭКСПЕРИМЕНТ ===")
    
    # 1. Пробуем получить данные из БД первой версии
    db_data = get_last_workout_from_db()
    
    if db_data:
        exercise, weight, reps = db_data
        print("✓ Данные успешно подтянуты из базы данных вашей 1-й версии!")
    else:
        # Если в БД пусто или файла нет, используем тестовые данные (заглушку)
        print("⚠ База данных пуста или не найдена. Используем тестовые параметры по умолчанию.")
        exercise, weight, reps = "Жим штанги лежа", 80.0, 10
        
    # 2. Проводим сравнительный вычислительный эксперимент
    print("\nСценарий А: Отдых 3 минуты (Низкая утомляемость = 0.5)")
    vol_a = run_experiment(exercise, weight, reps, fatigue_factor=0.5)
    
    print("\nСценарий Б: Отдых 1 минута (Высокая утомляемость = 1.5)")
    vol_b = run_experiment(exercise, weight, reps, fatigue_factor=1.5)
    
    # 3. Математический анализ результатов для отчета
    print("\n" + "="*40)
    print("АНАЛИЗ ВЫЧИСЛИТЕЛЬНОГО ЭКСПЕРИМЕНТА")
    print("="*40)
    efficiency_loss = ((vol_a - vol_b) / vol_a) * 100
    print(f"Потеря суммарной эффективности при коротком отдыхе составила: {efficiency_loss:.1f}%")
    print("Эксперимент наглядно доказывает математическую зависимость объема тренировки от времени восстановления.")

