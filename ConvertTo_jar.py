import os
import shutil
import zipfile
import time
from datetime import datetime

def create_jar_from_folder(folder_path, output_jar_path):
    """
    Создает JAR-файл из указанной папки
    """
    try:
        # Создаем временную папку для манифеста
        temp_dir = os.path.join(folder_path, "META-INF")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Создаем простой манифест, если его нет
        manifest_path = os.path.join(temp_dir, "MANIFEST.MF")
        if not os.path.exists(manifest_path):
            with open(manifest_path, "w") as f:
                f.write("Manifest-Version: 1.0\nCreated-By: FolderToJAR Converter\n")
        
        # Создаем JAR-файл (по сути ZIP с другой расширением)
        with zipfile.ZipFile(output_jar_path, 'w', zipfile.ZIP_DEFLATED) as jar:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Исключаем сам создаваемый JAR-файл
                    if file_path != output_jar_path:
                        arcname = os.path.relpath(file_path, folder_path)
                        jar.write(file_path, arcname)
        
        print(f"\nУспешно создан JAR-файл: {output_jar_path}")
        return True
    
    except Exception as e:
        print(f"\nОшибка при создании JAR-файла: {e}")
        return False

def monitor_and_update(folder_path, jar_path, interval=5):
    """
    Мониторит изменения в папке и обновляет JAR-файл
    """
    print(f"\nМониторинг папки: {folder_path}")
    print(f"JAR-файл будет обновляться автоматически каждые {interval} секунд")
    print("Нажмите Ctrl+C для выхода...\n")
    
    # Словарь для хранения времени последнего изменения файлов
    last_modified = {}
    
    # Инициализация словаря
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified[file_path] = os.path.getmtime(file_path)
    
    try:
        while True:
            updated = False
            
            # Проверка изменений в существующих файлах
            for file_path in list(last_modified.keys()):
                if not os.path.exists(file_path):
                    # Файл был удален
                    del last_modified[file_path]
                    updated = True
                    print(f"Файл удален: {file_path}")
                else:
                    current_mtime = os.path.getmtime(file_path)
                    if current_mtime > last_modified[file_path]:
                        # Файл был изменен
                        last_modified[file_path] = current_mtime
                        updated = True
                        print(f"Файл изменен: {file_path}")
            
            # Проверка новых файлов
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in last_modified and file_path != jar_path:
                        last_modified[file_path] = os.path.getmtime(file_path)
                        updated = True
                        print(f"Новый файл: {file_path}")
            
            # Если были изменения, обновляем JAR
            if updated:
                if create_jar_from_folder(folder_path, jar_path):
                    print(f"JAR обновлен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("Ошибка при обновлении JAR")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nМониторинг остановлен.")

def main():
    print("=== Folder to JAR Converter for Termux ===")
    
    # Запрос пути к папке
    folder_path = input("Введите путь к папке для конвертации: ").strip()
    
    # Проверка существования папки
    if not os.path.isdir(folder_path):
        print(f"Ошибка: Папка '{folder_path}' не существует!")
        return
    
    # Определение имени JAR-файла
    folder_name = os.path.basename(os.path.normpath(folder_path))
    default_jar_name = f"{folder_name}.jar"
    jar_path = input(f"Введите путь для JAR-файла (по умолчанию {default_jar_name}): ").strip()
    
    if not jar_path:
        jar_path = default_jar_name
    
    # Создание начального JAR-файла
    if not create_jar_from_folder(folder_path, jar_path):
        return
    
    # Запуск мониторинга
    monitor_and_update(folder_path, jar_path)

if __name__ == "__main__":
    # Проверка наличия необходимых модулей
    try:
        import zipfile
    except ImportError:
        print("Ошибка: Необходимо установить модуль zipfile.")
        print("Попробуйте выполнить: pkg install python")
        exit(1)
    
    main() import os
import shutil
import zipfile
import time
from datetime import datetime

def create_jar_from_folder(folder_path, output_jar_path):
    """
    Создает JAR-файл из указанной папки
    """
    try:
        # Создаем временную папку для манифеста
        temp_dir = os.path.join(folder_path, "META-INF")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Создаем простой манифест, если его нет
        manifest_path = os.path.join(temp_dir, "MANIFEST.MF")
        if not os.path.exists(manifest_path):
            with open(manifest_path, "w") as f:
                f.write("Manifest-Version: 1.0\nCreated-By: FolderToJAR Converter\n")
        
        # Создаем JAR-файл (по сути ZIP с другой расширением)
        with zipfile.ZipFile(output_jar_path, 'w', zipfile.ZIP_DEFLATED) as jar:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Исключаем сам создаваемый JAR-файл
                    if file_path != output_jar_path:
                        arcname = os.path.relpath(file_path, folder_path)
                        jar.write(file_path, arcname)
        
        print(f"\nУспешно создан JAR-файл: {output_jar_path}")
        return True
    
    except Exception as e:
        print(f"\nОшибка при создании JAR-файла: {e}")
        return False

def monitor_and_update(folder_path, jar_path, interval=5):
    """
    Мониторит изменения в папке и обновляет JAR-файл
    """
    print(f"\nМониторинг папки: {folder_path}")
    print(f"JAR-файл будет обновляться автоматически каждые {interval} секунд")
    print("Нажмите Ctrl+C для выхода...\n")
    
    # Словарь для хранения времени последнего изменения файлов
    last_modified = {}
    
    # Инициализация словаря
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified[file_path] = os.path.getmtime(file_path)
    
    try:
        while True:
            updated = False
            
            # Проверка изменений в существующих файлах
            for file_path in list(last_modified.keys()):
                if not os.path.exists(file_path):
                    # Файл был удален
                    del last_modified[file_path]
                    updated = True
                    print(f"Файл удален: {file_path}")
                else:
                    current_mtime = os.path.getmtime(file_path)
                    if current_mtime > last_modified[file_path]:
                        # Файл был изменен
                        last_modified[file_path] = current_mtime
                        updated = True
                        print(f"Файл изменен: {file_path}")
            
            # Проверка новых файлов
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in last_modified and file_path != jar_path:
                        last_modified[file_path] = os.path.getmtime(file_path)
                        updated = True
                        print(f"Новый файл: {file_path}")
            
            # Если были изменения, обновляем JAR
            if updated:
                if create_jar_from_folder(folder_path, jar_path):
                    print(f"JAR обновлен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("Ошибка при обновлении JAR")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nМониторинг остановлен.")

def main():
    print("=== Folder to JAR Converter for Termux ===")
    
    # Запрос пути к папке
    folder_path = input("Введите путь к папке для конвертации: ").strip()
    
    # Проверка существования папки
    if not os.path.isdir(folder_path):
        print(f"Ошибка: Папка '{folder_path}' не существует!")
        return
    
    # Определение имени JAR-файла
    folder_name = os.path.basename(os.path.normpath(folder_path))
    default_jar_name = f"{folder_name}.jar"
    jar_path = input(f"Введите путь для JAR-файла (по умолчанию {default_jar_name}): ").strip()
    
    if not jar_path:
        jar_path = default_jar_name
    
    # Создание начального JAR-файла
    if not create_jar_from_folder(folder_path, jar_path):
        return
    
    # Запуск мониторинга
    monitor_and_update(folder_path, jar_path)

if __name__ == "__main__":
    # Проверка наличия необходимых модулей
    try:
        import zipfile
    except ImportError:
        print("Ошибка: Необходимо установить модуль zipfile.")
        print("Попробуйте выполнить: pkg install python")
        exit(1)
    
    main()
