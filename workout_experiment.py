import math

def calculate_1rm(weight, reps):
    """Математическая модель Эпли для расчета Одноповторного Максимума (1RM)"""
    if reps == 1:
        return weight
    return weight * (1 + reps / 30)

def simulate_fatigue_experiment(base_weight, base_reps, fatigue_factor, total_sets):
    """
    Вычислительный эксперимент:
    Симуляция падения силовых показателей от подхода к подходу 
    под влиянием изменяемого коэффициента усталости (fatigue_factor).
    """
    print(f"\n--- СТАРТ ЭКСПЕРИМЕНТА ---")
    print(f"Входные данные: Начальный вес {base_weight} кг на {base_reps} повторений. Подходов: {total_sets}")
    print(f"Коэффициент утомляемости: {fatigue_factor} (влияние отдыха между подходами)")
    print("-" * 50)
    
    current_reps = base_reps
    total_volume = 0 # Общий тоннаж за тренировку
    
    for set_num in range(1, total_sets + 1):
        # Рассчитываем теоретический максимум на текущий подход с учетом накопленной усталости
        # Усталость снижает количество возможных повторений с каждым подходом
        if set_num > 1:
            # Математическая деградация повторений
            loss = (set_num - 1) * fatigue_factor
            current_reps = max(0, round(base_reps - loss))
        
        if current_reps <= 0:
            print(f"Подход {set_num}: Отказ мышц! Атлет не смог поднять вес.")
            break
            
        # Расчет тоннажа подхода
        set_volume = base_weight * current_reps
        total_volume += set_volume
        
        # Расчет прогнозируемого 1ПМ для этого подхода
        predicted_max = calculate_1rm(base_weight, current_reps)
        
        print(f"Подход {set_num}: {base_weight} кг х {current_reps} пов. | Тоннаж: {set_volume} кг | Прогноз 1ПМ: {predicted_max:.1f} кг")
        
    print("-" * 50)
    print(f"ИТОГ ЭКСПЕРИМЕНТА: Общий поднятый вес за тренировку = {total_volume} кг\n")
    return total_volume

if __name__ == "__main__":
    # Запуск серии контролируемых вычислительных тестов с изменением переменной утомляемости
    # Сценарий А: Атлет отдыхает долго (усталость низкая = 0.5 повтора теряется за подход)
    vol_a = simulate_fatigue_experiment(base_weight=100, base_reps=8, fatigue_factor=0.5, total_sets=4)
    
    # Сценарий Б: Атлет спешит и отдыхает мало (усталость высокая = 1.5 повтора теряется за подход)
    vol_b = simulate_fatigue_experiment(base_weight=100, base_reps=8, fatigue_factor=1.5, total_sets=4)
    
    # Анализ результатов эксперимента
    print("=== АНАЛИЗ РЕЗУЛЬТАТОВ ВЫЧИСЛЕНИЙ ===")
    print(f"Тоннаж при хорошем отдыхе: {vol_a} кг")
    print(f"Тоннаж при коротком отдыхе: {vol_b} кг")
    print(f"Математическая разница эффективности: {((vol_a - vol_b) / vol_a) * 100:.1f}% эффективности потеряно.")
