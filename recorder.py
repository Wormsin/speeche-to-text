import pvrecorder
import wave
from pynput import keyboard
import threading
import struct  
from datetime import datetime
from openai import OpenAI
import json
from pydub import AudioSegment
import os  

# Настройки записи
sample_rate = 16000  # Частота дискретизации
channels = 1  # Каналы (моно)
chunk_size = 1024  # Размер буфера
#output_file = "output.wav"  # Имя выходного файла

# Флаг для определения, началась ли запись
is_recording = False
frames = []  # Для хранения записанных данных
recorder = None  # Объект pvrecorder
recording_thread = None  # Поток для записи

start_time = None
client = OpenAI()


def convert_wav_to_mp3(wav_file, mp3_file):
    # Загружаем wav файл
    audio = AudioSegment.from_wav(wav_file)
    
    # Экспортируем в mp3
    audio.export(mp3_file, format="mp3")
    os.remove(wav_file)

def speech2text(file_name):
    
    global client

    audio_file = open(file_name, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
    
    data = {
        "timestamp": file_name[:-4  ],
        "text": transcript.text,
        "id": int(datetime.now().month) + int(datetime.now().day) + int(datetime.now().hour) + int(datetime.now().second)
    }
    with open("audio.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Данные успешно сохранены в json формате")
    os.remove(file_name)


# Функция для начала записи 
def start_recording():
    global recorder, frames, is_recording, recording_thread, start_time
    recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=chunk_size)
    recorder.start()
    frames = []
    is_recording = True
    print("Запись началась.")
    start_time = datetime.now().strftime("%H-%M-%S")
    # Запускаем запись в отдельном потоке
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()
  
# Функция для остановки записи и сохранения файла
def stop_recording():
    global recorder, frames, is_recording, start_time
    is_recording = False  # Сначала меняем флаг
    recording_thread.join()  # Ожидаем завершения потока записи

    recorder.stop()
    recorder.delete()

    end_time = datetime.now().strftime("%H-%M-%S")
    output_file = f"{start_time}-{end_time}.wav"
    # Сохранение в WAV файл
    with wave.open(output_file, 'w') as wf:
        wf.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        wf.writeframes(struct.pack("h" * len(frames), *frames))
    
    convert_wav_to_mp3(output_file, f"{start_time}-{end_time}.mp3")
    output_file = f"{start_time}-{end_time}.mp3"
    print(f"Запись остановлена. Файл сохранён: {output_file}")
    speech2text(output_file)

# Функция для записи аудио во время работы программы
def record_audio():
    global frames
    while is_recording:
        data = recorder.read()
        frames.extend(data)

# Обработка нажатий клавиш
def on_press(key):
    global is_recording
    try:
        # Если нажата пробел и запись ещё не началась, то начать запись
        if key == keyboard.Key.space and not is_recording:
            start_recording()
        # Если нажата пробел и запись уже идет, то остановить запись
        elif key == keyboard.Key.space and is_recording:
            stop_recording()
        elif key.char == 'q':
            print("Выход из программы...")
            return False  # Остановить слушателя
    except AttributeError:
        pass
    

# Основная функция для запуска прослушивания клавиш
def main():
    print("Нажмите пробел для начала записи и снова нажмите пробел для её остановки. Нажмите Esc для выхода.")
    print("Нажмите 'q' для выхода из программы.")

    # Создание слушателя для клавиатуры
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
        

if __name__ == "__main__":
    main()