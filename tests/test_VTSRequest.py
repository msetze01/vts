import pytest
from app.VTSRequest import VTSRequest, VTSRequestUnauthorizedException


def test_from_lambda_event_when_token_present_returns_new_instance_with_token():
    lambda_event = { 'headers': { 'token': 'abc' } }
    actual = VTSRequest.from_lambda_event(lambda_event)
    assert actual.token == 'abc'  
    assert actual.cardId is None 


def test_from_lambda_event_when_token_missing_raises_exception():
    with pytest.raises(VTSRequestUnauthorizedException):
        lambda_event = {}
        actual = VTSRequest.from_lambda_event(lambda_event)


def test_from_lamdba_event_when_path_param_present_returns_new_instance_with_card_id():
    lambda_event = { 
        'headers': { 'token': 'abc' },
        'pathParameters': { 'cardId': '123' }
    }
    actual = VTSRequest.from_lambda_event(lambda_event)
    assert actual.cardId == '123'    


def test_ctor_when_called_sets_token_and_cardid():
    actual = VTSRequest('token', 'cardId')
    assert actual.token == 'token'
    assert actual.cardId == 'cardId'
