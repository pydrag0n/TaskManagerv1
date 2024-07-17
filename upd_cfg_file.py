import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class ConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == 'config.json':
            print('Config file modified. Reloading...')
            # Перезаписывайте конфигурационный файл и инициализируйте переменные заново
            with open('config.json', 'r') as f:
                config = json.load(f)
            a = config['a']
            b = config['b']
            print('Config reloaded.')

observer = Observer()
observer.schedule(ConfigHandler('config.py', recursive=True))
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()