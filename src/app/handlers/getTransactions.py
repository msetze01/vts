import logging
from dataclasses import asdict
from app.utils.http import error, unauthorized, ok
from app.extend.ExtendVTSService import ExtendVTSService
from app.VTSRequest import VTSRequest, VTSRequestUnauthorizedException


def handler(event, context):
    try:
        request = VTSRequest.from_lambda_event(event)
        card_transactions = ExtendVTSService(request).get_all_transactions()

        response = []
        for card in card_transactions:
            transactions = []
            for trans in card_transactions[card]:
                transactions.append(asdict(trans))

            response.append({
                'cardId': card,
                'transactions': transactions
            })
        
        return ok(response)
    
    except VTSRequestUnauthorizedException as e:
        return unauthorized('Please provide a valid token and try again.')
    
    except Exception as e:
        logging.warn(e)
        return error('An unexpected error occurred. Please try again.')