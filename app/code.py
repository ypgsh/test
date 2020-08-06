from enum import Enum

class ReturnCode(Enum):
    SUCCESS = 0
    FAILURE = 1

    USERNAME_OR_PASSWORD_ERROR = 1001
    GET_USER_INFO_ERROR = 1002
    NOT_LOGIN = 1003
    FORBIDDEN = 1004
    NOT_FOUND = 1005
    TEST_ERROR = 1005

