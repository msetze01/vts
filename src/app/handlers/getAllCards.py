import logging
from dataclasses import asdict
from app.extend.ExtendVTSService import ExtendVTSService
from app.VTSRequest import VTSRequest, VTSRequestUnauthorizedException
from app.utils.http import error, unauthorized, ok

def handler(event, context):
    try:
        request = VTSRequest.from_lambda_event(event)
        cards = ExtendVTSService(request).get_all_cards()

        response = []
        for card in cards:
            response.append(asdict(card))
        
        return ok(response)
    
    except VTSRequestUnauthorizedException as e:
        return unauthorized('Please provide a valid token and try again.')
    
    except Exception as e:
        logging.warn(e)
        return error('An unexpected error occurred. Please try again.')