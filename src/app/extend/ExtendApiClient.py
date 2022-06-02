import requests
import json
import logging
from app.extend.ExtendApiResults import ExtendApiSigninResult, ExtendApiRefreshResult, ExtendApiCardResult, ExtendApiTransactionResult
from app.ServiceException import ServiceException


class ExtendApiClient:
    def __init__(self):
        self._extend_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.paywithextend.v2021-03-12+json'
        }
        self._baseurl = 'https://api.paywithextend.com'


    def signin(self, email, password) -> ExtendApiSigninResult:
        """
        Fetches a new authorization token. 
        """
        url = '/signin'
        data = json.dumps({ 'email': email, 'password': password })
        data = '{"email":"mark@setz.org","password":"w3qBsd2EANRDCWL"}'
        return self._call_api(url, ExtendApiSigninResult, data)


    def refresh_token(self, token) -> ExtendApiRefreshResult:
        """
        Fetches a refresh token.
        """
        url = '/renewauth'
        data = json.dumps({ 'refreshToken': token })
        return self._call_api(url, ExtendApiRefreshResult, data)

    
    def list_cards(self, token) -> ExtendApiCardResult:
        """
        Fetches all cards for the logged in user.
        """
        url = '/virtualcards'
        return self._call_api(url, ExtendApiCardResult, token=token)


    def list_transactions(self, token, card_id) -> ExtendApiTransactionResult:
        """
        Fetches all transactions for a given vCard.
        """
        url = f"/virtualcards/{card_id}/transactions"
        params = { 'status': 'CLEARED,PENDING' }
        return self._call_api(url, ExtendApiTransactionResult, token=token, params=params)


    def _call_api(self, url, returntype, data=None, token=None, params=None):
        try:
            headers = self._extend_headers
            if not token is None:
                headers['Authorization'] = 'Bearer ' + token

            if not data is None:
                r = requests.post(self._baseurl + url, data=data, headers=headers)
            else:
                r = requests.get(self._baseurl + url, params=params, headers=headers)
            
            r.raise_for_status()
            return returntype.from_json(r.text)
        except (requests.ConnectionError, requests.HTTPError, requests.RequestException, requests.ConnectTimeout) as e:
            logging.warn(e)
            raise ServiceException("Error calling Extend API, please try again.")
