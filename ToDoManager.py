import json
import time
import datetime
import os

# Программа мини менеджер задач
# функционал:
# 1) Добавление задач
# 2) Удаление задач
# 3) Пометка задач как "Выполнено"
# 4) Вывод списка на экран
# 5) Сохранение в JSON

TASKS_FILE = 'tasks.json'
tasks = []  # Глобальная переменная для хранения задач

def load_tasks():
    """Загрузка задач из файла"""
    global tasks
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            print("Задачи загружены!")
        else:
            tasks = []
            print("Файл задач не найден, создан новый список.")
    except Exception as e:
        print(f"Ошибка при загрузке задач: {e}")
        tasks = []

def save_tasks():
    """Сохранение задач в файл"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении задач: {e}")
        return False

def show_tasks():
    """Вывод списка задач на экран"""
    if not tasks:
        print("Задач нет!")
        return
    
    print("\n" + "="*50)
    print("ТЕКУЩИЕ ЗАДАЧИ:")
    print("="*50)
    
    for task in tasks:
        status = "ВЫПОЛНЕНО" if task['done'] else "В ПРОЦЕССЕ"
        task_id = task['id']
        title = task['title']
        created = datetime.datetime.fromisoformat(task['created']).strftime("%d.%m.%Y %H:%M")
        
        print(f"ID: {task_id} | [{status}]")
        print(f"Задача: {title}")
        print(f"Создана: {created}")
        print("-" * 40)

def add_task():
    """Добавление новой задачи"""
    global tasks
    title = input("Введите описание задачи: ").strip()
    if not title:
        print("Ошибка: описание задачи не может быть пустым!")
        return
    
    new_id = max((t['id'] for t in tasks), default=0) + 1
    new_task = {
        'id': new_id,
        'title': title,
        'done': False,
        'created': datetime.datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    if save_tasks():
        print(f"Задача '{title}' добавлена с ID: {new_id}")
    else:
        print("Ошибка при сохранении задачи!")

def delete_task():
    """Удаление задачи по ID"""
    global tasks
    show_tasks()
    if not tasks:
        return
    
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
        task_to_delete = None
        
        for task in tasks:
            if task['id'] == task_id:
                task_to_delete = task
                break
        
        if task_to_delete:
            tasks.remove(task_to_delete)
            if save_tasks():
                print(f"Задача '{task_to_delete['title']}' удалена!")
            else:
                print("Ошибка при сохранении изменений!")
        else:
            print(f"Задача с ID {task_id} не найдена!")
            
    except ValueError:
        print("Ошибка: введите корректный числовой ID!")

def mark_done():
    """Пометка задачи как выполненной"""
    global tasks
    show_tasks()
    if not tasks:
        return
    
    try:
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))
        task_found = False
        
        for task in tasks:
            if task['id'] == task_id:
                if not task['done']:
                    task['done'] = True
                    if save_tasks():
                        print(f"Задача '{task['title']}' отмечена как выполненная!")
                    else:
                        print("Ошибка при сохранении изменений!")
                else:
                    print("Эта задача уже выполнена!")
                task_found = True
                break
        
        if not task_found:
            print(f"Задача с ID {task_id} не найдена!")
            
    except ValueError:
        print("Ошибка: введите корректный числовой ID!")

def mark_undone():
    """Снятие отметки о выполнении"""
    global tasks
    show_tasks()
    if not tasks:
        return
    
    try:
        task_id = int(input("Введите ID задачи для снятия отметки выполнения: "))
        task_found = False
        
        for task in tasks:
            if task['id'] == task_id:
                if task['done']:
                    task['done'] = False
                    if save_tasks():
                        print(f"Задача '{task['title']}' снова в работе!")
                    else:
                        print("Ошибка при сохранении изменений!")
                else:
                    print("Эта задача еще не была выполнена!")
                task_found = True
                break
        
        if not task_found:
            print(f"Задача с ID {task_id} не найдена!")
            
    except ValueError:
        print("Ошибка: введите корректный числовой ID!")

def clear_completed():
    """Удаление всех выполненных задач"""
    global tasks
    completed_tasks = [task for task in tasks if task['done']]
    if not completed_tasks:
        print("Нет выполненных задач для удаления!")
        return
    
    print(f"Найдено выполненных задач: {len(completed_tasks)}")
    confirm = input("Удалить все выполненные задачи? (y/n): ").lower()
    
    if confirm == 'y':
        tasks = [task for task in tasks if not task['done']]
        if save_tasks():
            print("Все выполненные задачи удалены!")
        else:
            print("Ошибка при сохранении изменений!")

def main():
    """Основная функция программы"""
    load_tasks()
    
    while True:
        print("\n" + "="*40)
        print("МЕНЕДЖЕР ЗАДАЧ")
        print("="*40)
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("4. Отметить как выполненную")
        print("5. Вернуть в работу")
        print("6. Удалить выполненные задачи")
        print("7. Выход")
        print("-"*40)
        
        choice = input("Выберите действие (1-7): ").strip()
        
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            mark_done()
        elif choice == '5':
            mark_undone()
        elif choice == '6':
            clear_completed()
        elif choice == '7':
            print("Сохранение задач...")
            save_tasks()
            print("До свидания!")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")
        
        time.sleep(1)  # Пауза для удобства чтения

if __name__ == "__main__":
    main()