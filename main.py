from random import choice
import sounddevice as sd
import VA_functions
import torch
import time
import stt
import config
import os
import pyautogui
import subprocess


def va_respond(voice: str):
    """
    Обработка сказанного пользователем
    """
    if voice:
        print("Вы сказали: ", voice)

        if voice.startswith(config.VA_ALIAS):
            # Обращаются к ассистенту
            cmd = VA_functions.recognize_cmd(VA_functions.filter_cmd(voice))

            if not cmd['cmd']:
                va_say("Я вас слушаю...")
            else:
                execute_cmd(cmd['cmd'])


def va_say(text: str):
    """
    Воспроизведение текста голосовым помощником
    """
    sample_rate = 48000

    audio = model.apply_tts(
        text=text,
        speaker='xenia',
        sample_rate=sample_rate,
        put_accent=True,
        put_yo=True
    )

    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 0.5)
    sd.stop()


def execute_cmd(cmd: str):
    """
    Исполнение команды голосовым помощником
    """
    global volume_amount

    if cmd == "help":
        va_say(config.HELP_TEXT)

    elif cmd == "open_spotify":
        va_say("Открываю спотифай...")
        os.startfile(r"")  # Your path to...

    elif cmd == "open_telegram":
        va_say("Открываю телеграмм...")
        os.startfile(r"")  # Your path to...

    elif cmd == "open_browser":
        va_say("Открываю браузер...")
        os.startfile(r"")  # Your path to...

    elif cmd == "open_calculator":
        va_say("Открываю калькулятор...")
        os.startfile(r"C:\Windows\System32\calc.exe")

    elif cmd == "open_word":
        va_say("Открваю ворд...")
        os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

    elif cmd == "close_minecraft":
        VA_functions.kill_process("javaw.exe")

    elif cmd == "close_telegram":
        VA_functions.kill_process("Telegram.exe")

    elif cmd == "turn_up_volume":
        volume_amount += 1
        volume.SetMasterVolumeLevel(volume_amount, None)

    elif cmd == "turn_down_volume":
        volume_amount -= 1
        volume.SetMasterVolumeLevel(volume_amount, None)

    elif cmd == "clear_recycle_bin":
        subprocess.call(["cmd.exe", "/c", "echo Y|PowerShell.exe -NoProfile -Command Clear-RecycleBin"])

    elif cmd == "close_program":
        pyautogui.hotkey('alt', 'f4')

    elif cmd == "clear_RAM":
        pyautogui.hotkey('ctrl', 'f1')  # Clearing RAM is happening by Mem Reduct hotkey

    elif cmd == "restart_pc":
        os.system('shutdown /r /t 1')

    elif cmd == "turn_off_pc":
        os.system("shutdown /s /t 1")

    elif cmd == "exit":
        va_say(choice(config.FAREWELL))
        exit(0)


if __name__ == '__main__':
    # Параметры для голосовой модели
    device = torch.device('cpu')  # cuda, opengl, opencl, vulkan
    torch.set_num_threads(4)

    model, _ = torch.hub.load(
        repo_or_dir='snakers4/silero-models',
        model='silero_tts',
        language='ru',
        speaker='v3_1_ru'
    )

    model.to(device)  # Запуск голосовой модели

    # Для настройки звука Windows
    volume = VA_functions.regulation_volume()
    volume_amount = 0

    va_say(f"{choice(config.GREETINGS)} Я, {config.VA_NAME}, не самый умный голосовой помощник. Я вас слушаю...")

    stt.va_listen(va_respond)  # Запуск прослушивания команд
