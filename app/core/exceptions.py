from fastapi import HTTPException, status


class CRMException(HTTPException):
    """CRM系统基础异常类"""

    pass


class UserNotFoundError(CRMException):
    """用户未找到异常"""

    def __init__(self, detail: str = "用户不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserAlreadyExistsError(CRMException):
    """用户已存在异常"""

    def __init__(self, detail: str = "用户已存在"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidCredentialsError(CRMException):
    """无效凭据异常"""

    def __init__(self, detail: str = "用户名或密码错误"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InsufficientPermissionsError(CRMException):
    """权限不足异常"""

    def __init__(self, detail: str = "权限不足"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidTokenError(CRMException):
    """无效令牌异常"""

    def __init__(self, detail: str = "认证失败"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserDisabledError(CRMException):
    """用户被禁用异常"""

    def __init__(self, detail: str = "用户已禁用"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidSystemCodeError(CRMException):
    """无效系统码异常"""

    def __init__(self, detail: str = "系统码错误"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class SuperAdminOperationError(CRMException):
    """超级管理员操作异常"""

    def __init__(self, detail: str = "不允许操作超级管理员"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class RecordNotFoundError(CRMException):
    """记录未找到异常"""

    def __init__(self, detail: str = "记录不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateRecordError(CRMException):
    """重复记录异常"""

    def __init__(self, detail: str = "记录已存在"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ValidationError(CRMException):
    """验证错误异常"""

    def __init__(self, detail: str = "数据验证失败"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
