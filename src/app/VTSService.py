from app.VTSRequest import VTSRequest
from app.extend.ExtendApiClient import ExtendApiClient
from app.CacheClient import CacheClient
from app.ConfigClient import ConfigClient
from app.ServiceException import ItemNotFoundException, ServiceException


class VTSService:
    def __init__(self, request: VTSRequest, cache_client: CacheClient, api_client: ExtendApiClient, config_client: ConfigClient):
        self._request = request
        self._signintoken = None
        self._refreshtoken = None
        self._cache = cache_client
        self._client = api_client
        self._config = config_client

    
    def refreshtokens(self):
        email = self._request.token # from our APIG, token header value is our cache key
        (self._signintoken, self._refreshtoken) = self._cache.get(email)
        if self._signintoken is None:
            pw = self._config._get_extend_pw()
            response = self._client.signin(email, pw)
            self._signintoken = response.token
            self._refreshtoken = response.refreshToken
            self._cache.insert(email, { 'token': self._signintoken, 'refreshtoken': self._refreshtoken })


    def getrefreshtoken(self, retry=False):
        if retry or self._signintoken is None or self._refreshtoken is None:
            self.refreshtokens()
        try:
            return self._client.refresh_token(self._refreshtoken).token
        except ServiceException as e:
            if retry: 
                raise e
            return self.getrefreshtoken(True)


    def get_all_cards(self):
        token = self.getrefreshtoken()
        cards = self._client.list_cards(token).virtualCards
        return cards


    def get_active_cards(self):
        token = self.getrefreshtoken()
        cards = self._client.list_cards(token).virtualCards
        active_cards = list(filter(lambda x: (x.status  == "ACTIVE"), cards)) 
        return active_cards

    
    def get_card(self, card_id):
        token = self.getrefreshtoken()
        cards = self._client.list_cards(token).virtualCards
        cards_filtered = list(filter(lambda x: (x.id == card_id), cards)) 
        if len(cards_filtered) == 1:
            return cards_filtered[0]
        raise ItemNotFoundException('Invalid card ID.')


    def get_card_transactions(self, card_id):
        token = self.getrefreshtoken()
        transactions = self._client.list_transactions(token, card_id).transactions
        return transactions


    def get_all_transactions(self):
        cards = self.get_all_cards()
        results = {}
        for card in cards:
            results[card.id] = []
            card_transactions = self.get_card_transactions(card.id)
            for trans in card_transactions:
                results[card.id].append(trans)
        return results