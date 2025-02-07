from fastapi import HTTPException, status

class BadRequestException(HTTPException):
    def __init__(self, description: str = "Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=description)

class UnauthorizedException(HTTPException):
    def __init__(self, description: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=description)

class ForbiddenException(HTTPException):
    def __init__(self, description: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=description)

class NotFoundException(HTTPException):
    def __init__(self, description: str = "Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=description)

class ConflictException(HTTPException):
    def __init__(self, description: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=description)

class InternalServerErrorException(HTTPException):
    def __init__(self, description: str = "Internal Server Error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=description)

class NotImplementedException(HTTPException):
    def __init__(self, description: str = "Not Implemented"):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=description)

class ServiceUnavailableException(HTTPException):
    def __init__(self, description: str = "Service Unavailable"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=description)

class GatewayTimeoutException(HTTPException):
    def __init__(self, description: str = "Gateway Timeout"):
        super().__init__(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=description)

# Adicione outras exceções personalizadas conforme necessário
