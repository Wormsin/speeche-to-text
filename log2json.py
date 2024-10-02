import re
import json
import os 

def extract_name_or_placeholder(element):
    """Функция для извлечения атрибута name или placeholder, если они есть."""
    name_match = re.search(r'name="([^"]+)"', element)
    placeholder_match = re.search(r'placeholder="([^"]+)"', element)
    
    if name_match:
        return name_match.group(1)
    elif placeholder_match:
        return placeholder_match.group(1)
    else:
        return "svg"  # Возвращаем "svg", если нет name или placeholder

def logs_to_json(logs_filename, audio_filename):
    """Функция для преобразования логов в формат JSON и добавления данных из audio.json."""
    
    # Чтение данных из файла с логами
    with open(logs_filename, 'r', encoding='utf-8') as file:
        logs = file.readlines()

    actions = []
    
    for log in logs:
        # Ищем элемент с использованием регулярного выражения
        element_match = re.search(r'Клик по элементу:\s*(.*)', log)
        
        if element_match:
            element = element_match.group(1)
            name_or_placeholder = extract_name_or_placeholder(element)
            actions.append({"Клик по элементу": name_or_placeholder})

    # Чтение данных из audio.json
    with open(audio_filename, 'r', encoding='utf-8') as audio_file:
        audio_data = json.load(audio_file)

    # Включаем audio_actions после поля "text"
    output_data = {
        "timestamp": audio_data["timestamp"],
        "text": audio_data["text"],
        "audio_actions": actions,
        "id": audio_data["id"]
    }
    output_filename = audio_data["timestamp"]+".json"
    # Записываем финальные данные в output.json
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)


def action():
    file_name = "/home/wormsin/Downloads/BP_logs/logs.txt"
    logs_to_json(file_name, 'audio.json')
    os.remove(file_name)
    os.remove('audio.json')
    