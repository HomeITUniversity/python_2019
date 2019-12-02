import logging
import sys
from datetime import datetime
import simplejson

# ИМПОРТИРУЕМ СОЗДАННЫЙ КЛАСС
from api.telegram import Telegram

def create_logger(logger_name, file_name=None, level="WARNING"):

    logger_levels = {
                'CRITICAL': logging.CRITICAL,  # 50
                'ERROR': logging.ERROR,  # 40
                'WARNING': logging.WARNING,  # 30
                'INFO': logging.INFO,  # 20
                'DEBUG': logging.DEBUG,  # 10
            }

    level = logger_levels.get(level, logging.WARNING)

    file_name = file_name if file_name is not None else logger_name + '_' + str(datetime.date(datetime.now()).today()) + '.log'

    formatter = logging.Formatter('[%(asctime)s] - %(name)-20s - %(module)-20s - %(threadName)-20s - [%(levelname)-8s] - %(message)s')

    created_logger = logging.getLogger(logger_name)
    created_logger.setLevel(level)

    # File handler
    fh = logging.FileHandler(file_name, 'a', 'utf-8')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    created_logger.addHandler(fh)

    # Stream handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    created_logger.addHandler(ch)

    return created_logger

def my_func(resp):
    offset = None
    # проверяем все ли ок в ответе и парсим ответ (как обычный словарик)
    if resp.get("ok", False) is not False:
        if resp.get("result", False) is not False and len(resp['result']) > 0:
            for msg in resp['result']:
                # логгируем полученное текстовое сообщение
                logger.info("Полученное сообщение: {} От: {}".format(
                    msg['message']['text'],
                    msg['message']['from']['first_name']
                    ))
                #вызываем метод отправки собщения,передаем внутрь чат ид - кому отправить и текст который нужно отправить
                telegram.sendMessage(chat_id=msg['message']['from']['id'], text=f"Вы прислали: {msg['message']['text']}")

                offset = msg['update_id'] + 1

    return offset


if __name__ == '__main__':

    # создаем пустую переменную config
    config = None
    # открываем файлик на чтение как f
    with open("config/config.json") as f:

        # читаем в заранее созданную переменную из файла
        config = simplejson.load(f)

        # если нам нужно будет прочитать из СТРОКИ мы испльзуем loads

    logger = create_logger(logger_name=config['logger']["logger_name"], level="INFO")
    # создаем объект класса Телеграмм
    telegram = Telegram(logger=logger)

    # создаем переменную offset в которую будет записываться нами номер последнего обновления взятого с сервера
    offset = None
    while True:
        # вызываем у созданного объекта класса метод получить обновления
        resp = telegram.getUpdates(offset=offset)

        # передаем в функцию обработки ответа результаты
        offset = my_func(resp)

