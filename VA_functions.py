"""
Все ф-ции, которые нужны для работы голосового ассистента вынесены в этот модуль
"""

from fuzzywuzzy import fuzz
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import config
import psutil


def filter_cmd(raw_voice: str):
    """
    Фильтруем команду
    """
    for x in config.VA_ALIAS:
        raw_voice = raw_voice.replace(x, "").strip()

    for x in config.VA_TBR:
        raw_voice = raw_voice.replace(x, "").strip()

    return raw_voice


def recognize_cmd(cmd: str):
    """
    Распознавание команды
    """
    rc = {
        'cmd': '',
        'percent': 0
    }

    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)

            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def regulation_volume():
    """
    Регуляция громкости Windows
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    return cast(interface, POINTER(IAudioEndpointVolume))


def kill_process(name: str):
    """
    Ф-ция завершения выбранных процессов
    """
    for process in list(psutil.process_iter()):
        if process.name() == name:
            process.terminate()
