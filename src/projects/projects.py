import json
import re
import os
from docx import Document
class DocxConverter:
    def __init__(self, docx_filepath, txt_filepath):
        self.docx_filepath = docx_filepath
        print(self.docx_filepath)
        self.txt_filepath = txt_filepath
        print(self.txt_filepath)

    def convert_to_txt(self):
        try:
            document = Document(self.docx_filepath)
            with open(self.txt_filepath, 'w', encoding='utf-8') as txt_file:
                for paragraph in document.paragraphs:
                    txt_file.write(paragraph.text + '\n')
            print(f"Файл '{self.txt_filepath}' успешно создан.")
        except Exception as e:
            print(f"Ошибка при конвертации DOCX в TXT: {e}")


class DataExtractor:
    def __init__(self, txt_filepath):
        self.txt_filepath = txt_filepath
        self.data = self.initialize_data_structure()

    @staticmethod
    def initialize_data_structure():
        return {
            "ФИО": "",
            "Название проекта": "",
            "Регион проекта": "",
            "Логотип проекта": "",
            "Контакты": {},
            "Вкладка Общее": {
                "Блок Общая информация": {
                    "Масштаб реализации проекта": "",
                    "Дата начала и окончания проекта": ""
                },
                "Блок Дополнительная информация об авторе проекта": {
                    "Опыт автора проекта": "",
                    "Описание функционала автора проекта": "",
                    "Адрес регистрации автора проекта": "",
                    "Добавить резюме": "",
                    "Видео-визитка": ""
                }
            },
            "Вкладка О проекте": {
                "Блок Информация о проекте": {
                    "Краткая информация о проекте": "",
                    "Описание проблемы": "",
                    "Основные целевые группы": "",
                    "Основная цель проекта": "",
                    "Опыт успешной реализации проекта": "",
                    "Перспектива развития и потенциал проекта": ""
                },
                "Блок Задачи": [],
                "Блок География проекта": []
            },
            "Вкладка Команда": {
                "Блок Команда": {
                    "Наставники": []
                }
            },
            "Вкладка Результаты": {
                "Дата плановых значений результатов": "",
                "Плановое количество мероприятий": "",
                "Ед. измерения (мероприятия)": "Ед.",
                "Крайняя дата проведения мероприятий": "",
                "Плановое количество участников мероприятий": "",
                "Ед. измерения (участники)": "Чел.",
                "Плановое количество публикаций": "",
                "Ед. измерения (публикации)": "Ед.",
                "Плановое количество просмотров публикаций": "",
                "Ед. измерения (просмотры)": "Ед.",
                "Социальный эффект": ""
            },
            "Вкладка Календарный план": {
                "Блок Задачи": []
            },
            "Вкладка Медиа": {
                "Ресурсы": []
            },
            "Вкладка Софинансирование": {
                "Блок Собственные средства": [],
                "Блок Партнер": []
            },
            "Вкладка Доп. Файлы": []
        }

    def extract_between_headers(self, lines, start_headers, end_header=None):
        is_collecting = False
        collected_lines = []

        # Если start_headers - это строка, преобразуем её в список для унификации
        if isinstance(start_headers, str):
            start_headers = [start_headers]

        for line in lines:
            # Начинаем собирать строки после нахождения одного из начальных заголовков
            if any(line.startswith(header) for header in start_headers):
                is_collecting = True
                continue
            # Останавливаем сбор данных при нахождении конечного заголовка
            if end_header and line.startswith(end_header):
                break
            # Если мы находимся в режиме сбора, добавляем строки
            if is_collecting:
                stripped_line = line.strip()  # Убираем лишние пробелы
                if stripped_line:  # Проверяем, что строка не пустая
                    collected_lines.append(stripped_line)

        return collected_lines  # Возвращаем список строк

    def extract_data(self):
        try:
            with open(self.txt_filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue

                # Extracting values based on headers
                if "ФИО:" in line:
                    self.data["ФИО"] = line.split("ФИО:")[1].strip()
                elif "Название проекта:" in line:
                    self.data["Название проекта"] = line.split("Название проекта:")[1].strip()
                elif "Регион проекта:" in line:
                    self.data["Регион проекта"] = line.split("Регион проекта:")[1].strip()
                elif "Логотип проекта:" in line:
                    self.data["Логотип проекта"] = line.split("Логотип проекта:")[1].strip()
                elif "Контакты:" in line:
                    contacts = line.split("Контакты:")[1].strip().split(", ")
                    if len(contacts) > 0:
                        self.data["Контакты"]["Телефон"] = contacts[0]
                    if len(contacts) > 1:
                        self.data["Контакты"]["Email"] = contacts[1]

                # Extracting data between headers
                if "Масштаб реализации проекта:" in line:
                    self.data["Вкладка Общее"]["Блок Общая информация"]["Масштаб реализации проекта"] = \
                        self.extract_between_headers(lines[i:], "Масштаб реализации проекта:", "Дата начала и окончания проекта:")
                elif "Дата начала и окончания проекта:" in line:
                    self.data["Вкладка Общее"]["Блок Общая информация"]["Дата начала и окончания проекта"] = \
                        self.extract_between_headers(lines[i:], "Дата начала и окончания проекта:", 'Блок "Дополнительная информация об авторе проекта"')

                if "Опыт автора проекта:" in line:
                    self.data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"]["Опыт автора проекта"] = \
                        self.extract_between_headers(lines[i:], "Опыт автора проекта:", "Описание функционала автора проекта:")
                elif "Описание функционала автора проекта:" in line:
                    self.data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"]["Описание функционала автора проекта"] = \
                        self.extract_between_headers(lines[i:], "Описание функционала автора проекта:", "Адрес регистрации автора проекта:")
                elif "Адрес регистрации автора проекта:" in line:
                    self.data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"]["Адрес регистрации автора проекта"] = \
                        self.extract_between_headers(lines[i:], "Адрес регистрации автора проекта:", "Добавить резюме:")
                elif "Видео-визитка (ссылка на ролик на любом видеохостинге):" in line:
                    self.data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"]["Видео-визитка"] = \
                        self.extract_between_headers(lines[i:], "Видео-визитка (ссылка на ролик на любом видеохостинге):", 'Вкладка "О проекте"')

                if "Краткая информация о проекте:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Краткая информация о проекте"] = \
                        self.extract_between_headers(lines[i:], "Краткая информация о проекте:", "Описание проблемы, решению/снижению которой посвящен проект:")
                elif "Описание проблемы, решению/снижению которой посвящен проект:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Описание проблемы"] = \
                        self.extract_between_headers(lines[i:], "Описание проблемы, решению/снижению которой посвящен проект:", "Основные целевые группы, на которые направлен проект:")
                elif "Основные целевые группы, на которые направлен проект:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Основные целевые группы"] = \
                        self.extract_between_headers(lines[i:], "Основные целевые группы, на которые направлен проект:", "Основная цель проекта:")
                elif "Основная цель проекта:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Основная цель проекта"] = \
                        self.extract_between_headers(lines[i:], "Основная цель проекта:", "Опыт успешной реализации проекта:")
                elif "Опыт успешной реализации проекта:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Опыт успешной реализации проекта"] = \
                        self.extract_between_headers(lines[i:], "Опыт успешной реализации проекта:", "Перспектива развития и потенциал проекта:")
                elif "Перспектива развития и потенциал проекта:" in line:
                    self.data["Вкладка О проекте"]["Блок Информация о проекте"]["Перспектива развития и потенциал проекта"] = \
                        self.extract_between_headers(lines[i:], "Перспектива развития и потенциал проекта:", 'Блок "Задачи"')

                if "Поставленная задача:" in line:
                    task = line.split("Поставленная задача:")[1].strip()
                    if task not in self.data["Вкладка О проекте"]["Блок Задачи"]:
                        self.data["Вкладка О проекте"]["Блок Задачи"].append(task)

                if "Выберите регион или федеральный округ:" in line:
                    region = line.split("Выберите регион или федеральный округ:")[1].strip()
                    address_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    address = address_line.split("Адрес:")[1].strip() if "Адрес:" in address_line else ""
                    self.data["Вкладка О проекте"]["Блок География проекта"].append({
                        "Регион": region,
                        "Адрес": address
                    })

                if "ФИО наставника:" in line:
                    mentor_info = {
                        "ФИО": line.split("ФИО наставника:")[1].strip()
                    }
                    for j in range(i + 1, len(lines)):
                        next_line = lines[j].strip()
                        if "E-mail наставника:" in next_line:
                            mentor_info["E-mail"] = next_line.split("E-mail наставника:")[1].strip()
                        elif "Роль в проекте:" in next_line:
                            mentor_info["Роль в проекте"] = next_line.split("Роль в проекте:")[1].strip()
                        elif "Добавить резюме:" in next_line:
                            mentor_info["Добавить резюме"] = next_line.split("Добавить резюме:")[1].strip()
                        elif "Компетенции, опыт, подтверждающие возможность участника выполнять роль в команде:" in next_line:
                            mentor_info["Компетенции"] = next_line.split("Компетенции, опыт, подтверждающие возможность участника выполнять роль в команде:")[1].strip()
                        else:
                            break
                    self.data["Вкладка Команда"]["Блок Команда"]["Наставники"].append(mentor_info)


                if "Социальный эффект:" in line:
                    self.data["Вкладка Результаты"]["Социальный эффект"] = \
                        self.extract_between_headers(lines[i:], "Социальный эффект:", 'Вкладка "Календарный план"')

                if "Файл с подробным медиа-планом:" in line:
                    self.data["Вкладка Медиа"]["Файл с подробным медиа-планом:"] = \
                        self.extract_between_headers(lines[i:], "Файл с подробным медиа-планом:", 'Вкладка "Расходы"')

            self.data["Вкладка Результаты"] = self.result_extraction(lines)

            self.data["Вкладка Календарный план"] = self.extract_calendar_plan(lines)
            self.data["Вкладка Медиа"] = self.extract_media(lines)
            self.data["Вкладка Софинансирование"] = self.extract_cofinancing(lines)
            self.data["Вкладка Доп. Файлы"] = self.extraction_additional_files(lines)



        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")

        return self.data

    def result_extraction(self, lines):
        result_extraction = {
            "Вкладка Результаты": {
                "Дата плановых значений результатов": "",
                "Плановое количество мероприятий": "",
                "Крайняя дата проведения мероприятий": "",
                "Плановое количество участников мероприятий": "",
                "Плановое количество публикаций": "",
                "Плановое количество просмотров публикаций": "",
                "Социальный эффект": ""
            }
        }

        combined_lines = self.extract_between_headers(lines, 'Вкладка "Результаты"', 'Вкладка "Календарный план"')
        # Удаление всех данных, оставляя только числа
        numbers_only = self.extract_numbers(combined_lines)


        # Присвоение значений в словарь результата
        result_extraction["Вкладка Результаты"]["Дата плановых значений результатов"] = numbers_only[0] if len(
            numbers_only) > 0 else "Нет данных"
        result_extraction["Вкладка Результаты"]["Плановое количество мероприятий"] = numbers_only[1] if len(
            numbers_only) > 1 else "Нет данных"
        result_extraction["Вкладка Результаты"]["Крайняя дата проведения мероприятий"] = numbers_only[2] if len(
            numbers_only) > 2 else "Нет данных"
        result_extraction["Вкладка Результаты"]["Плановое количество участников мероприятий"] = numbers_only[3] if len(
            numbers_only) > 3 else "Нет данных"
        result_extraction["Вкладка Результаты"]["Плановое количество публикаций"] = numbers_only[4] if len(
            numbers_only) > 4 else "Нет данных"
        result_extraction["Вкладка Результаты"]["Плановое количество просмотров публикаций"] = numbers_only[5] if len(
            numbers_only) > 5 else "Нет данных"

        # Извлечение социального эффекта
        social_effect = self.extract_between_headers(
            combined_lines,
            'Социальный эффект:',
            ''  # Конец блока, если нет дополнительного текста после
        )
        result_extraction["Вкладка Результаты"]["Социальный эффект"] = social_effect if social_effect else "Нет данных"

        return result_extraction

    def extract_media(self, lines):
        media_section = {
            "Ресурсы": [],
            "Файл с подробным медиа-планом": []
        }
        current_resource = None
        collecting_links = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Вид ресурса:"):
                if current_resource is not None:
                    media_section["Ресурсы"].append(current_resource)
                current_resource = {
                    "Вид ресурса": line.split("Вид ресурса:")[1].strip(),
                    "Месяц публикации": "",
                    "Планируемое количество просмотров": "",
                    "Ссылки на ресурсы": "",
                    "Почему выбран такой формат медиа": ""
                }
                collecting_links = False

            if current_resource is not None:
                if line.startswith("Месяц публикации:"):
                    current_resource["Месяц публикации"] = line.split("Месяц публикации:")[1].strip()
                elif line.startswith("Планируемое количество просмотров:"):
                    current_resource["Планируемое количество просмотров"] = line.split("Планируемое количество просмотров:")[1].strip()
                elif line.startswith("Ссылки на ресурсы:"):
                    collecting_links = True
                    current_resource["Ссылки на ресурсы"] = line.split("Ссылки на ресурсы:")[1].strip() + " "
                elif line.startswith("Почему выбран такой формат медиа:"):
                    collecting_links = False
                    current_resource["Почему выбран такой формат медиа"] = line.split("Почему выбран такой формат медиа:")[1].strip()
                elif collecting_links:
                    current_resource["Ссылки на ресурсы"] += line + " "

            media_plan =  self.extract_between_headers(lines,"Файл с подробным медиа-планом:", 'Вкладка "Расходы"')
        if current_resource is not None:
            media_section["Ресурсы"].append(current_resource)
            media_section["Файл с подробным медиа-планом"].append(media_plan)

        return media_section

    def extract_calendar_plan(self, lines):
        calendar_plan = {
            "Блок Задачи": []
        }
        task_info = {}
        current_events = []

        for line in lines:
            line = line.strip()

            if line.startswith('Вкладка "Календарный план"'):
                continue

            if line.startswith('Добавить мероприятие:'):
                continue

            if "Поставленная задача:" in line:
                if task_info and current_events:
                    task_info["Мероприятия"] = current_events
                    calendar_plan["Блок Задачи"].append(task_info)

                task_info = {
                    "Поставленная задача": line.split("Поставленная задача:")[1].strip()
                }
                current_events = []

            elif "Название мероприятия:" in line:
                event_info = {
                    "Название": line.split("Название мероприятия:")[1].strip()
                }
                current_events.append(event_info)

            elif "Крайняя дата выполнения:" in line:
                if current_events:
                    current_events[-1]["Крайняя дата"] = line.split("Крайняя дата выполнения:")[1].strip()

            elif "Описание мероприятия:" in line:
                if current_events:
                    current_events[-1]["Описание"] = line.split("Описание мероприятия:")[1].strip()

            elif "Количество уникальных участников:" in line:
                if current_events:
                    current_events[-1]["Количество уникальных участников"] = line.split("Количество уникальных участников:")[1].strip()

            elif "Количество повторяющихся участников:" in line:
                if current_events:
                    current_events[-1]["Количество повторяющихся участников"] = line.split("Количество повторяющихся участников:")[1].strip()

            elif "Количество публикаций:" in line:
                if current_events:
                    current_events[-1]["Количество публикаций"] = line.split("Количество публикаций:")[1].strip()

            elif "Количество просмотров:" in line:
                if current_events:
                    current_events[-1]["Количество просмотров"] = line.split("Количество просмотров:")[1].strip()

            elif "Дополнительная информация:" in line:
                if current_events:
                    current_events[-1]["Дополнительная информация"] = line.split("Дополнительная информация:")[1].strip()

        if task_info and current_events:
            task_info["Мероприятия"] = current_events
            calendar_plan["Блок Задачи"].append(task_info)

        return calendar_plan

    def extract_cofinancing(self,lines):
        json_structure = {
            "Блок Собственные средства": {
                "Перечень расходов": [],
                "Сумма рассходов": []
            },
            "Блок Партнер": []
        }

        combined_lines = "\n".join(lines)

        # Extracting own funding expenses
        description_match = re.search(r'Перечень расходов: (.+?)Добавить:', combined_lines, re.DOTALL)
        if description_match:
            expenses = [
                line.strip() for line in description_match.group(1).strip().split('\n')
                if line.strip()  # Remove empty lines
            ]
            json_structure["Блок Собственные средства"]["Перечень расходов"].extend(expenses)

        # Extracting own funding sums
        sum_matches = re.findall(r'Сумма, руб\.: (\d+)', combined_lines)
        for match in sum_matches:
            json_structure["Блок Собственные средства"]["Сумма рассходов"].append(f"Сумма: {match}")

        # Extracting partner information
        partner_matches = re.findall(
            r'Название партнера:\s*(.+?)\nТип поддержки:\s*(.+?)\nПеречень расходов:\s*(.+?)\nСумма, руб\.: (\d+)',
            combined_lines, re.DOTALL
        )

        for match in partner_matches:
            partner_info = {
                "Название партнера": match[0].strip(),
                "Тип поддержки": match[1].strip(),
                "Перечень расходов": match[2].strip(),
                "Сумма, руб.": match[3].strip(),
            }
            json_structure["Блок Партнер"].append(partner_info)

        return json_structure

    def extraction_additional_files(self, lines):
        json_structure = {
            "Вкладка Доп. Файлы": {
                "Файлы": []
            }
        }

        combined_lines = "\n".join(lines)


        # Извлечение дополнительных файлов
        file_matches = re.findall(
            r'Описание файла:\s*(.+?)\nВыберете файл:\s*(\S+)',
            combined_lines, re.DOTALL
        )

        for match in file_matches:
            file_info = {
                "Описание файла": match[0].strip(),
                "ID файла": match[1].strip()  # Добавляем ID файла, если нужно
            }
            json_structure["Вкладка Доп. Файлы"]["Файлы"].append(file_info)

        return json_structure

    def extract_numbers(self, data):
        results = []

        for text in data:
            # Найти все числа и даты в каждой строке
            found_items = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}|\d+', text)
            # Добавить найденные предметы в общий список
            results.extend(found_items)

        return results

class JSONWriter:
    @staticmethod
    def write_to_json(data, json_filepath):
        try:
            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при записи JSON файла: {e}")


def convert_docx_to_json(docx_filepath):
    # Получаем путь к родительской папке
    parent_folder = os.path.dirname(os.path.dirname(docx_filepath))

    # Получаем только имя файла без расширения
    file_name = os.path.splitext(os.path.basename(docx_filepath))[0]

    # Формируем полные пути для txt и json файлов
    txt_filepath = os.path.join(parent_folder, "project_pages", "projects_txt", f"{file_name}.txt")
    json_filepath = os.path.join(parent_folder,  "project_pages", "projects_json", f"{file_name}.json")
    # Конвертация DOCX в TXT
    converter = DocxConverter(docx_filepath, txt_filepath)
    converter.convert_to_txt()

    # Извлечение данных из TXT
    extractor = DataExtractor(txt_filepath)
    data = extractor.extract_data()

    # Запись данных в JSON файл
    writer = JSONWriter()
    writer.write_to_json(data, json_filepath)

    return json_filepath


def main():
    docx_filepath = "2.docx"  # Путь к файлу проекта

    txt_filepath = "project.txt"
    json_filepath = "output.json"

    # Конвертация DOCX в TXT
    converter = DocxConverter(docx_filepath, txt_filepath)
    converter.convert_to_txt()

    # Извлечение данных из TXT
    extractor = DataExtractor(txt_filepath)
    data = extractor.extract_data()

    # Запись данных в JSON файл
    writer = JSONWriter()
    writer.write_to_json(data, json_filepath)


if __name__ == "__main__":
    main()