from rest_framework.exceptions import APIException


class BusinessLogicError(APIException):
    """Error de lógica de negocio con status 400 por defecto."""

    status_code = 400
    default_code = "business_logic_error"
