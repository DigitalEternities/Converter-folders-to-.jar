import os
import sys
import zipfile
import time
from datetime import datetime

def check_storage_permission():
    """Проверяем разрешения на доступ к хранилищу"""
    if not os.path.exists('/sdcard'):
        print("\n[!] Termux не имеет доступа к хранилищу!")
        print("Выполните следующие команды:")
        print("1. termux-setup-storage")
        print("2. Разрешите доступ к файлам")
        return False
    return True

def create_manifest(folder_path):
    """Создает MANIFEST.MF если его нет"""
    meta_inf = os.path.join(folder_path, "META-INF")
    os.makedirs(meta_inf, exist_ok=True)
    
    manifest_path = os.path.join(meta_inf, "MANIFEST.MF")
    if not os.path.exists(manifest_path):
        with open(manifest_path, 'w') as f:
            f.write("Manifest-Version: 1.0\n")
            f.write("Created-By: Termux JAR Converter\n")
            f.write("Main-Class: Main\n")  # Можно указать главный класс

def validate_paths(folder_path, jar_path):
    """Проверяет корректность путей"""
    if not os.path.isdir(folder_path):
        raise ValueError(f"Папка не существует: {folder_path}")
    
    if os.path.commonpath([folder_path]) == os.path.commonpath([folder_path, jar_path]):
        raise ValueError("JAR файл не может находиться внутри конвертируемой папки")

def create_jar(folder_path, jar_path):
    """Основная функция создания JAR"""
    try:
        print(f"\n[+] Создаю JAR из: {folder_path}")
        print(f"[+] Сохраняю как: {jar_path}")
        
        validate_paths(folder_path, jar_path)
        create_manifest(folder_path)
        
        start_time = time.time()
        
        with zipfile.ZipFile(jar_path, 'w', zipfile.ZIP_DEFLATED) as jar:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path == jar_path:
                        continue
                    
                    rel_path = os.path.relpath(full_path, folder_path)
                    jar.write(full_path, rel_path)
                    print(f"Добавлен: {rel_path}")
        
        size = os.path.getsize(jar_path) / (1024 * 1024)
        print(f"\n[+] Успешно! Размер JAR: {size:.2f} MB")
        print(f"[+] Время создания: {time.time() - start_time:.2f} сек")
        return True
    
    except Exception as e:
        print(f"\n[!] Ошибка: {str(e)}")
        return False

def monitor_changes(folder_path, jar_path, interval=5):
    """Мониторит изменения и обновляет JAR"""
    print(f"\n[+] Запущен мониторинг: {folder_path}")
    print("[+] Нажмите Ctrl+C для остановки")
    
    last_state = {}
    
    # Первоначальное сканирование
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            last_state[path] = os.path.getmtime(path)
    
    try:
        while True:
            changed = False
            
            # Проверка изменений
            current_state = {}
            for root, _, files in os.walk(folder_path):
                for file in files:
                    path = os.path.join(root, file)
                    if path == jar_path:
                        continue
                    
                    current_state[path] = os.path.getmtime(path)
                    if path not in last_state or current_state[path] != last_state[path]:
                        print(f"Обнаружено изменение: {path}")
                        changed = True
            
            # Проверка удаленных файлов
            for path in list(last_state.keys()):
                if path not in current_state:
                    print(f"Файл удален: {path}")
                    changed = True
            
            if changed:
                print("\n[+] Обнаружены изменения, пересоздаю JAR...")
                if create_jar(folder_path, jar_path):
                    print(f"[+] JAR обновлен: {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print("[!] Не удалось обновить JAR")
                
                last_state = current_state
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n[+] Мониторинг остановлен")

def main():
    print("\n=== Termux Folder to JAR Converter ===")
    print("=== Полная версия с мониторингом ===\n")
    
    if not check_storage_permission():
        sys.exit(1)
    
    # Ввод путей
    folder_path = input("Введите путь к папке: ").strip()
    jar_name = input("Введите имя JAR (по умолчанию output.jar): ").strip() or "output.jar"
    
    # Автоматическое определение пути для сохранения
    if not os.path.isabs(jar_name):
        jar_path = os.path.join(os.getcwd(), jar_name)
    else:
        jar_path = jar_name
    
    # Создание JAR
    if not create_jar(folder_path, jar_path):
        sys.exit(1)
    
    # Запуск мониторинга
    monitor = input("\nЗапустить мониторинг изменений? (y/n): ").lower()
    if monitor == 'y':
        monitor_changes(folder_path, jar_path)
    else:
        print("\n[+] Готово! JAR файл создан.")

if __name__ == "__main__":
    # Проверка зависимостей
    try:
        import zipfile
    except ImportError:
        print("[!] Установите zipfile: pip install zipfile")
        sys.exit(1)
    
    main()
