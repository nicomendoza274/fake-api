from fastapi import status

from core.enums.error import ErrorEnum
from core.schemas.error import Error

GEN_1000 = Error(
    Code=ErrorEnum.GEN_1000.value,
    Exception="Bad Request Exception",
    Message="One or more attributes of the request do not match the expected value.",
    Status=status.HTTP_400_BAD_REQUEST,
)

GEN_1001 = Error(
    Code=ErrorEnum.GEN_1001.value,
    Exception="Database Exception",
    Message="There were failures related to the database level.",
    Status=status.HTTP_400_BAD_REQUEST,
)

GEN_1002 = Error(
    Code=ErrorEnum.GEN_1002.value,
    Exception="Validation Exception",
    Message="The data sent did not pass format or integrity validations.",
    Status=status.HTTP_400_BAD_REQUEST,
)

GEN_1003 = Error(
    Code=ErrorEnum.GEN_1003.value,
    Exception="Not Implemented Exception",
    Message="When the request refers to a functionality that has not yet been implemented.",
    Status=status.HTTP_400_BAD_REQUEST,
)

GEN_1004 = Error(
    Code=ErrorEnum.GEN_1004.value,
    Exception="Unsupported Media Type Exception",
    Message="When a content type is sent in the request that has not yet been implemented.",
    Status=status.HTTP_400_BAD_REQUEST,
)

GEN_2000 = Error(
    Code=ErrorEnum.GEN_2000.value,
    Exception="Unauthorized Exception",
    Message="The provided API Key is not valid",
    Status=status.HTTP_401_UNAUTHORIZED,
)

GEN_2001 = Error(
    Code=ErrorEnum.GEN_2001.value,
    Exception="Missing API Key Exception",
    Message="No API Key was provided in the request",
    Status=status.HTTP_401_UNAUTHORIZED,
)

GEN_2002 = Error(
    Code=ErrorEnum.GEN_2002.value,
    Exception="Invalid Credentials Exception",
    Message="The provided credentials (username or password) are incorrect.",
    Status=status.HTTP_401_UNAUTHORIZED,
)

GEN_3000 = Error(
    Code=ErrorEnum.GEN_3000.value,
    Exception="Forbidden Exception",
    Message="The API Key used does not have the necessary permissions to access the request resource.",
    Status=status.HTTP_403_FORBIDDEN,
)

GEN_3001 = Error(
    Code=ErrorEnum.GEN_3001.value,
    Exception="Already Exists Exception",
    Message="When trying to create a resource that already exist in the system.",
    Status=status.HTTP_403_FORBIDDEN,
)

GEN_4000 = Error(
    Code=ErrorEnum.GEN_4000.value,
    Exception="Not Found Exception",
    Message="The requested resource does not exist.",
    Status=status.HTTP_404_NOT_FOUND,
)

GEN_5000 = Error(
    Code=ErrorEnum.GEN_5000.value,
    Exception="Internal Server Error",
    Message="The limit of allowed request has been exceeded",
    Status=status.HTTP_429_TOO_MANY_REQUESTS,
)
