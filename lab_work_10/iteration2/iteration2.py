import concurrent.futures as ftres
from functools import partial
from typing import Callable, List
from iteration1.iteration1 import integrate

def integrate_threaded(f: Callable[[float], float], 
                       a: float, 
                       b: float, 
                       *, 
                       n_jobs: int = 2, 
                       n_iter: int = 10000) -> float:
    """
    Вычисляет интеграл с использованием многопоточности.
    
    Args:
        f: Интегрируемая функция.
        a: Нижний предел.
        b: Верхний предел.
        n_jobs: Количество потоков.
        n_iter: Общее количество итераций.
    
    Returns:
        Приближенное значение интеграла.
    """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    
    # Создаем частичную функцию с зафиксированными аргументами
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    
    step = (b - a) / n_jobs
    fs: List[ftres.Future] = []
    
    # Создаем задачи для каждого потока
    for i in range(n_jobs):
        a_i = a + i * step
        b_i = a + (i + 1) * step
        print(f"Поток {i}, границы: [{a_i:.3f}, {b_i:.3f}]")
        fs.append(spawn(a_i, b_i))
    
    # Собираем результаты
    results = [f.result() for f in ftres.as_completed(fs)]
    return sum(results)