from schemas.error import ErrorDescription

GEN_4000 = ErrorDescription(
    Code="GEN-4000",
    Exception="Not Found Exception",
    Message="The requested resource does not exist.",
)

GEN_2002 = ErrorDescription(
    Code="GEN-2002",
    Exception="InvalidCredentialException",
    Message="The provided credentials (username or password) are incorrect.",
)
