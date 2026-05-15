class BaseBookingException(Exception):
    status_code = 500
    detail = ""

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail


class RoomNotAvailableException(BaseBookingException):
    status_code = 409
    detail = "Нет доступных комнат"


class RoomNotFoundException(BaseBookingException):
    status_code = 404
    detail = "Комната не найдена"


class InvalidBookingDatesException(BaseBookingException):
    status_code = 400
    detail = "Дата заезда должна быть раньше даты выезда"


class UserAlreadyExistsException(BaseBookingException):
    status_code = 409
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BaseBookingException):
    status_code = 401
    detail = "Неверная почта или пароль"


class BookingNotFoundException(BaseBookingException):
    status_code = 404
    detail = "Бронирование не найдено"
