class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class UserNotFoundError(AppException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=404, detail=detail)


class RoomNotFoundError(AppException):
    def __init__(self, detail: str = "Room not found"):
        super().__init__(status_code=404, detail=detail)


class TimeslotNotFoundError(AppException):
    def __init__(self, detail: str = "Timeslot not found"):
        super().__init__(status_code=404, detail=detail)


class BookingNotFoundError(AppException):
    def __init__(self, detail: str = "Booking not found"):
        super().__init__(status_code=404, detail=detail)


class BookingAlreadyExistsError(AppException):
    def __init__(self, detail: str = "Timeslot is already booked"):
        super().__init__(status_code=400, detail=detail)


class TimeslotPassedError(AppException):
    def __init__(self, detail: str = "Timeslot already passed"):
        super().__init__(status_code=400, detail=detail)


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=403, detail=detail)
