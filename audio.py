import soundfile as sf
import numpy as np
from pvrecorder import PvRecorder
from pydub import AudioSegment
import os
from datetime import datetime
import json
from openai import OpenAI
import sys

# Переменная для отслеживания состояния записи
is_recording = False
recorder = None
output_file = 'audio_recording.wav'
client = OpenAI()


def start_recording():
    global recorder, is_recording
    is_recording = True
    recorder = PvRecorder(device_index=-1, frame_length=512)
    recorder.start()
    print("Началась запись аудио...")

    audio_frames = []

    try:
        while is_recording:
            frame = recorder.read()
            audio_frames.append(frame)

            # Проверка на наличие файла-сигнала
            if os.path.exists("stop_signal.txt"):
                is_recording = False  # Остановить запись, если файл-сигнал обнаружен
                os.remove("stop_signal.txt")  # Удалить файл-сигнал

    except KeyboardInterrupt:
        stop_recording()

    # Сохраняем запись в файл после завершения
    if audio_frames:  # Проверяем, есть ли записанные данные
        audio_data = np.concatenate(audio_frames, axis=0)
        audio_data = audio_data.astype(np.int16)
        sf.write(output_file, audio_data, samplerate=16000)
        print(f"Аудио сохранено в файл {output_file}")
        stop_recording()
        convert_wav_to_mp3(output_file, "audio.mp3")
        speech2text("audio.mp3")
        

def stop_recording():
    global recorder, is_recording
    is_recording = False
    if recorder:
        recorder.stop()
        recorder.delete()
    print("Запись остановлена.")



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
        "timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
        "text": transcript.text,
        "id": int(datetime.now().month) + int(datetime.now().day) + int(datetime.now().hour) + int(datetime.now().second)
    }
    with open("audio.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Данные успешно сохранены в json формате")
    os.remove(file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Укажите функцию: start или stop.")
        sys.exit(1)

    command = sys.argv[1]
    if command == "start":
        start_recording()
    elif command == "stop":
        stop_recording()
    else:
        print("Неизвестная команда.")