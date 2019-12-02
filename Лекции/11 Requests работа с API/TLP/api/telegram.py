import requests, simplejson
class TG:
    def __init__(self):
        self.token = "token"
        self.telegram_id = "chat_id"
    def get_token(self):
        return self.token

    def get_telegram_id(self):
        return self.telegram_id

# создаем класс с именем Telegram
class Telegram:

    # метод инициализации класса, на вход принимает всегда первой переменной указатель на класс
    # переменная логгер может быть передана, а может и не быть, она передается чтобы при инициализации
    # вы создали копию этой переменной видной внутри класса
    # внутри класса глобально видны те переменные, которые объвлены в методе инит и записаны через self
    # пример с логгером
    def __init__(self, logger):
        self.TG = TG()
        self.logger = logger
        self.api_url = "https://api.telegram.org/bot{}/".format(self.TG.get_token())

    # создаем новый метод (этот метод будет доступен через объект_класса.getUpdates
    def getUpdates(self, offset):
        method = "getUpdates"
        # описываем параметры которые мы будем подставлять в GET запрос
        params = {
            "offset": offset,
            "timeout": 10
        }
        # отправляем гет запрос и записываем результат в переменную resp
        # в метод мы передаем ссылку, откуда нужно взять данные
        # параметры которые нужны срверу чтоб отдать вам именно те данные, что вы попросили
        # таймаут на вашем клиенте, спестя который ваш скрипт остановится если сервер удаленный завис
        resp = requests.get(url=self.api_url + method, params=params, timeout=30)

        self.logger.info(f"Status code: {resp.status_code} Reason: {resp.reason}")
        # проверяем что флаг resp.ok в True или resp.status_code == 200 - это говорит что все ок
        # если они другие, то в resp.reason будет описана причина неудачи
        if not resp.ok:
            self.logger.error("Не смог получить данные: {}".format(resp.reason))
            return
        else:

            # ответ от сервера, даже если они имеют тип json, будут в формате text и нам нужно
            # их преобразовать в нужный нам словарь, используем функцию loads
            json_resp = simplejson.loads(resp.text)
            return json_resp

    def sendMessage(self, chat_id, text):
        method = "sendMessage"
        # создаем словрь который хоти отправить на сервер
        params = {
            "chat_id": chat_id,
            "text": text
        }

        # методом пост передаем эти данные на сервер указанный в URL,
        # а наш словарь передаем как json, положив его в переменную json метода пост
        resp = requests.post(url=self.api_url + method, json=params, timeout=30)

        self.logger.info(f"Status code: {resp.status_code} Reason: {resp.reason}")

        if not resp.ok:
            self.logger.error("Не могу отправить сообщение: {}".format(resp.reason))
            return
        else:
            # если все ок, то парсим ответ в JSON.
            json_resp = simplejson.loads(resp.text)
            return json_resp





