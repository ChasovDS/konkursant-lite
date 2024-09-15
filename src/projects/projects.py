import json
from docx import Document


def docx_to_txt(docx_filepath, txt_filepath):
    """Конвертирует DOCX файл в TXT."""
    document = Document(docx_filepath)
    with open(txt_filepath, 'w', encoding='utf-8') as txt_file:
        for paragraph in document.paragraphs:
            txt_file.write(paragraph.text + '\n')


def extract_between_headers(lines, start_header, end_header):
    """Извлекает текст между двумя заголовками."""
    data = []
    is_collecting = False

    for line in lines:
        line = line.strip()
        if line.startswith(start_header):
            is_collecting = True
            continue
        if line.startswith(end_header) and is_collecting:
            break
        if is_collecting:
            data.append(line)

    return ' '.join(data).strip()


def extract_data_from_txt(filepath):
    """Извлекает данные из текстового файла и структурирует их."""
    data = {
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
        }

    }

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        # Извлечение значений по заголовкам с использованием extract_between_headers
        if "ФИО:" in line:
            data["ФИО"] = line.split("ФИО:")[1].strip()
        elif "Название проекта:" in line:
            data["Название проекта"] = line.split("Название проекта:")[1].strip()
        elif "Регион проекта:" in line:
            data["Регион проекта"] = line.split("Регион проекта:")[1].strip()
        elif "Логотип проекта:" in line:
            data["Логотип проекта"] = line.split("Логотип проекта:")[1].strip()
        elif "Контакты:" in line:
            contacts = line.split("Контакты:")[1].strip().split(", ")
            if len(contacts) > 0:
                data["Контакты"]["Телефон"] = contacts[0]
            if len(contacts) > 1:
                data["Контакты"]["Email"] = contacts[1]

        # Извлечение текстов между заголовками для блока Общая информация
        if "Масштаб реализации проекта:" in line:
            data["Вкладка Общее"]["Блок Общая информация"]["Масштаб реализации проекта"] = extract_between_headers(lines[i:], "Масштаб реализации проекта:", "Дата начала и окончания проекта:")
        elif "Дата начала и окончания проекта:" in line:
            data["Вкладка Общее"]["Блок Общая информация"]["Дата начала и окончания проекта"] = extract_between_headers(lines[i:], "Дата начала и окончания проекта:", 'Блок "Дополнительная информация об авторе проекта"')

        # Извлечение текстов между заголовками для блока Дополнительная информация об авторе проекта
        if "Опыт автора проекта:" in line:
            data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"][
                "Опыт автора проекта"] = extract_between_headers(lines[i:], "Опыт автора проекта:",
                                                                 "Описание функционала автора проекта:")
        elif "Описание функционала автора проекта:" in line:
            data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"][
                "Описание функционала автора проекта"] = extract_between_headers(lines[i:],
                                                                                 "Описание функционала автора проекта:",
                                                                                 "Адрес регистрации автора проекта:")
        elif "Адрес регистрации автора проекта:" in line:
            data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"][
                "Адрес регистрации автора проекта"] = extract_between_headers(lines[i:],
                                                                              "Адрес регистрации автора проекта:",
                                                                              "Добавить резюме:")

        elif "Видео-визитка (ссылка на ролик на любом видеохостинге):" in line:
            data["Вкладка Общее"]["Блок Дополнительная информация об авторе проекта"][
                "Видео-визитка"] = extract_between_headers(lines[i:],
                                                           "Видео-визитка (ссылка на ролик на любом видеохостинге):",
                                                           'Вкладка "О проекте"')

        # Извлечение текстов между заголовками для блока Информация о проекте
        elif "Краткая информация о проекте:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"][
                "Краткая информация о проекте"] = extract_between_headers(lines[i:], "Краткая информация о проекте:",
                                                                          "Описание проблемы, решению/снижению которой посвящен проект:")
        elif "Описание проблемы, решению/снижению которой посвящен проект:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"]["Описание проблемы"] = extract_between_headers(
                lines[i:], "Описание проблемы, решению/снижению которой посвящен проект:",
                "Основные целевые группы, на которые направлен проект:")
        elif "Основные целевые группы, на которые направлен проект:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"]["Основные целевые группы"] = extract_between_headers(
                lines[i:], "Основные целевые группы, на которые направлен проект:", "Основная цель проекта:")
        elif "Основная цель проекта:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"]["Основная цель проекта"] = extract_between_headers(
                lines[i:], "Основная цель проекта:", "Опыт успешной реализации проекта:")
        elif "Опыт успешной реализации проекта:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"][
                "Опыт успешной реализации проекта"] = extract_between_headers(lines[i:],
                                                                              "Опыт успешной реализации проекта:",
                                                                              "Перспектива развития и потенциал проекта:")
        elif "Перспектива развития и потенциал проекта:" in line:
            data["Вкладка О проекте"]["Блок Информация о проекте"][
                "Перспектива развития и потенциал проекта"] = extract_between_headers(lines[i:],
                                                                                      "Перспектива развития и потенциал проекта:",
                                                                                      'Блок "Задачи"')

        # Обработка блока Задачи
        if "Поставленная задача:" in line:
            task = line.split("Поставленная задача:")[1].strip()
            data["Вкладка О проекте"]["Блок Задачи"].append(task)

        # Обработка блока География проекта
        if "Выберите регион или федеральный округ:" in line:
            region = line.split("Выберите регион или федеральный округ:")[1].strip()
            address_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            address = address_line.split("Адрес:")[1].strip() if "Адрес:" in address_line else ""
            data["Вкладка О проекте"]["Блок География проекта"].append({
                "Регион": region,
                "Адрес": address
            })
        # Обработка блока Наставники
        if "ФИО наставника:" in line:
            mentor_info = {
                "ФИО": line.split("ФИО наставника:")[1].strip()
            }
            # Извлечение данных о наставнике
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
                    # Если встретили новый блок, выходим из цикла
                    break
            data["Вкладка Команда"]["Блок Команда"]["Наставники"].append(mentor_info)



            # Извлечение данных из раздела "Календарный план"
            calendar_plan_data = extract_calendar_plan(lines)
            data.update(calendar_plan_data)
    return data






def extract_calendar_plan(lines):
    """Извлекает задачи и мероприятия из раздела 'Календарный план'."""
    calendar_plan = {
        "Вкладка Календарный план": {
            "Блок Задачи": []
        }
    }

    task_info = {}  # Информация о текущей задаче
    current_events = []  # Список мероприятий для текущей задачи

    for line in lines:
        line = line.strip()

        if line.startswith('Вкладка "Календарный план"'):
            continue

        if line.startswith('Добавить мероприятие:'):
            continue  # Игнорируем, это просто подтверждение

        if "Поставленная задача:" in line:
            # Если есть существующая задача с мероприятиями, добавляем её в календарный план
            if task_info and current_events:
                task_info["Мероприятия"] = current_events
                calendar_plan ["Вкладка Календарный план"]["Блок Задачи"].append(task_info)

            # Начинаем новую задачу
            task_info = {
                "Поставленная задача": line.split("Поставленная задача:")[1].strip()
            }
            current_events = []  # Сброс списка мероприятий

        elif "Название мероприятия:" in line:
            event_info = {
                "Название": line.split("Название мероприятия:")[1].strip()
            }
            current_events.append(event_info)  # Добавляем новое мероприятие

        elif "Крайняя дата выполнения:" in line:
            if current_events:  # Проверяем, есть ли мероприятия
                current_events[-1]["Крайняя дата"] = line.split("Крайняя дата выполнения:")[1].strip()

        elif "Описание мероприятия:" in line:
            if current_events:
                current_events[-1]["Описание"] = line.split("Описание мероприятия:")[1].strip()

        elif "Количество уникальных участников:" in line:
            if current_events:
                current_events[-1]["Количество уникальных участников"] = \
                line.split("Количество уникальных участников:")[1].strip()

        elif "Количество повторяющихся участников:" in line:
            if current_events:
                current_events[-1]["Количество повторяющихся участников"] = \
                line.split("Количество повторяющихся участников:")[1].strip()

        elif "Количество публикаций:" in line:
            if current_events:
                current_events[-1]["Количество публикаций"] = line.split("Количество публикаций:")[1].strip()

        elif "Количество просмотров:" in line:
            if current_events:
                current_events[-1]["Количество просмотров"] = line.split("Количество просмотров:")[1].strip()

        elif "Дополнительная информация:" in line:
            if current_events:
                current_events[-1]["Дополнительная информация"] = line.split("Дополнительная информация:")[1].strip()

    # Добавляем последнюю задачу, если мероприятия есть
    if task_info and current_events:
        task_info["Мероприятия"] = current_events
        calendar_plan ["Вкладка Календарный план"]["Блок Задачи"].append(task_info)

    return calendar_plan


def main():
    docx_filepath = "2.docx"  # Замените на путь к вашему файлу DOCX
    txt_filepath = "project.txt"

    # Конвертация DOCX в TXT
    docx_to_txt(docx_filepath, txt_filepath)

    # Извлечение данных из TXT
    extracted_data = extract_data_from_txt(txt_filepath)

    # Сохранение данных в JSON
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
