import logging
from dataclasses import asdict
from app.utils.http import ok, error, notfound, unauthorized
from app.extend.ExtendVTSService import ExtendVTSService
from app.VTSRequest import VTSRequest, VTSRequestUnauthorizedException
from app.ServiceException import InvalidInputException, ItemNotFoundException


def handler(event, context):
    try:
        request = VTSRequest.from_lambda_event(event)
        if request.cardId is None: 
            raise InvalidInputException('Missing required parameter: cardId')

        transactions = ExtendVTSService(request).get_card_transactions(request.cardId)
        
        results = []
        for trans in transactions:
            results.append(asdict(trans))

        return ok(results)

    except VTSRequestUnauthorizedException as e:
        return unauthorized('Please provide a valid token and try again.')

    except (ItemNotFoundException, InvalidInputException) as e:
        return notfound(e)

    except Exception as e:
        logging.warn(e)
        return error('An unexpected error occurred. Please try again.')