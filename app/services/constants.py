"""Сборник строк используемых в приложении.
"""
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

API_CREATE_MEET_ROOM = 'Создаёт новую переговорную комнату'
API_GET_MEET_ROOMS = 'Возвращает список переговорных комнат'
API_UPDATE_MEET_ROOM = 'Обновляет данные переговорной комнаты'
API_DELETE_MEET_ROOM = 'Удаляет переговорную комнату'

API_CREATE_RESERVATION = 'Создаёт новую бронь на комнату'
API_GET_RESERVATION = 'Возвращает список броней'
API_UPDATE_RESERVATION = 'Обновляет данные брони на комнату'
API_DELETE_RESERVATION = 'Удаляет бронь'
API_BUSY_PERIODS = 'Взовращает занятые периоды времени для указанной комнаты'

API_GOOGLE_UPLOAD = 'Загружает данные с google-диска'

ROOM_BUSY = 'Занято с %s до %s'

ERR_ROOM_NAME_BUSY = 'Комната с таким именем (`%s`) уже существует!'
ERR_ROOM_NOT_FOUND_ID = 'Комната с `id = %s` не найдена!'
ERR_NULL_VALUE = 'Значение `%s` не может быть пустым!'
ERR_NOT_ENOUGH_VALUES = 'Недостаточно значений!'
ERR_START_TIME = 'Текущее время больше переданного!'
ERR_PERIOD_RESERVATION = 'Начало брони %s не раньше окончания %s!'
ERR_TIME_RESERVATION = 'Комната %s занята: %s!'
ERR_RESERVATION_NOT_FOUND_ID = 'Бронь с `id = %s` не найдена!'
ERR_NOT_OWNER = 'Доступ к чужим объектам запрщён!'
