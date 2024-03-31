import time, unpacking, start
from logger import lof_file
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, LoggingEventHandler


path, patterns, program = start.get_setting()

print(f'Отслеживаемая директория = {path}')
lof_file(f'Отслеживаемая директория = {path}\n')
print(f'Отслеживаемые форматы = {patterns}')
lof_file(f'Отслеживаемые форматы = {patterns}\n')
print(f'Используемая программа = {program}')
lof_file(f'Используемая программа = {program}\n')


class CustomEventHandler(PatternMatchingEventHandler):

    def on_created(self, event):
        super().on_created(event)
        time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
        what = 'папка' if event.is_directory else 'файл'
        if what == 'папка':
            #print(event.src_path)
            print(f"{time_now} - Добавлена {what}: {event.src_path}")
            lof_file(f"{time_now} - Добавлена {what}: {event.src_path}\n")

        elif what == 'файл' and path in event.src_path and event.src_path.count('\\') == 2:
            time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
            print(f"{time_now} - Добавлен {what}: {event.src_path}")
            lof_file(f"{time_now} - Добавлен {what}: {event.src_path}\n")
            try:
                true_false, file = unpacking.unzip(event.src_path)
                if true_false:
                    time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
                    print(f"{time_now} - Создана папка: {event.src_path.split('.')[0:-1][0]}")
                    lof_file(f"{time_now} - Создана папка: {event.src_path.split('.')[0:-1][0]}\n")
                else:
                    try:
                        print(f'Файл {event.src_path} через минуту будет пересканирован,'
                              f'\nВозможно он ещё не прогрузился \nНе отвечайте на запрос если он ещё пишется на диск')
                        lof_file(f'Файл {event.src_path} через минуту будет пересканирован, '
                                 f'\nВозмжно он ещё не прогрузился\nНе отвечайте на запрос если он ещё пишется на диск\n')
                        an = 1
                        ans = 0

                        def answer():
                            time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
                            answer1 = input(f"{time_now} - {what}: {file} не был распакован, повторить? Y/N   ")

                            if answer1 in 'Yy':
                                unpacking.unzip(file)
                            elif answer1 in 'Nn':
                                time_now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
                                print(f"{time_now} - {what}: {file} был пропущен !!!!")
                                lof_file(f"{time_now} - {what}: {file} был пропущен !!!!\n")

                        def countdown():

                            if not ans:
                                time.sleep(80)
                                print(f'Повторное разархивирование...{file}')
                                lof_file(f'Повторное разархивирование...{file}\n')
                                true = False
                                while not true:
                                    true, false = unpacking.unzip(file)
                                global an
                                an = 0

                        task1 = Thread(target=countdown, daemon=True)
                        task2 = Thread(target=answer, daemon=True)
                        task1.start()
                        task2.start()
                    except Exception:
                        pass

            except Exception as Exc:
                print(f"{time_now} - Произошла ошибка, возможно архив распакован")
                lof_file(f"{time_now} - Произошла ошибка, возможно архив распакован\n")


event_handler = CustomEventHandler(patterns=patterns)
event_handler2 = LoggingEventHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.schedule(event_handler2, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()