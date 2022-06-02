from app.ServiceException import ServiceException


class VTSRequestUnauthorizedException(ServiceException):
    pass


class VTSRequest(object):
    def __init__(self, token, cardId):
        self.token = token
        self.cardId = cardId

    @classmethod
    def from_lambda_event(cls, lambda_event):
        cardId = None
        headers = lambda_event.get('headers', None)
        if headers is None or 'token' not in headers:
            raise VTSRequestUnauthorizedException()
        token = headers['token']

        pathParams = lambda_event.get('pathParameters', None)
        if pathParams is not None:
            cardId = pathParams.get('cardId', None)

        return cls(token, cardId)