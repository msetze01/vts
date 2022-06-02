class ServiceException(Exception):
    pass


class ItemNotFoundException(ServiceException):
    pass


class InvalidInputException(ServiceException):
    pass

