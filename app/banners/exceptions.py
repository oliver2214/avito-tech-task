from fastapi import HTTPException

class UnauthorizedException(HTTPException):
    def __init__(self, detail="Пользователь не авторизован"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail="Пользователь не имеет доступа"):
        super().__init__(status_code=403, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail="Баннер не найден"):
        super().__init__(status_code=404, detail=detail)

class InvalidDataException(HTTPException):
    def __init__(self, detail="Некорректные данные"):
        super().__init__(status_code=400, detail=detail)
