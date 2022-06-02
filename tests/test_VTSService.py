import pytest
from unittest import TestCase
from unittest.mock import MagicMock
from app.ServiceException import ServiceException
from app.VTSRequest import VTSRequest
from app.VTSService import VTSService
from app.CacheClient import CacheClient
from app.extend.ExtendApiClient import ExtendApiClient
from app.ConfigClient import ConfigClient
from app.extend.ExtendApiResults import ExtendApiCardResult, ExtendApiRefreshResult, ExtendApiSigninResult, ExtendApiTransactionResult, ExtendApiVirtualCard


class VTSServiceTestCase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        # Request
        self.request = VTSRequest('token', 'cardid')

        # CacheClient mock
        self.mock_cache = CacheClient()
        self.mock_cache.get = MagicMock()
        self.mock_cache.get.return_value = (None, None)      
        self.mock_cache.insert = MagicMock()

        # ConfigClient mock
        self.mock_config = ConfigClient()
        self.mock_config._get_extend_pw = MagicMock()

        # API client mock
        self.mock_api = ExtendApiClient()
        self.mock_api.signin = MagicMock()
        self.mock_api.signin.return_value = ExtendApiSigninResult('token', 'refreshToken')
        self.mock_api.refresh_token = MagicMock()
        self.mock_api.refresh_token.return_value = ExtendApiRefreshResult('newToken')


    def test_ctor_when_called_with_valid_request_is_initialized(self):
        request = VTSRequest('token', 'cardId')
        service = VTSService(request, None, None, None)
        assert service._request is request
        assert service._signintoken is None
        assert service._refreshtoken is None


    def test_refreshtokens_when_called_without_force_and_empty_cache_refreshes_token(self):
        # Arrange
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)
        
        # Act
        service.refreshtokens()

        # Assert
        assert self.mock_api.signin.call_count == 1
        assert self.mock_cache.insert.call_count == 1
        assert self.mock_config._get_extend_pw.call_count == 1

    def test_refreshtokens_when_called_with_cached_token_assigns_tokens(self):
        # Arrange
        self.mock_cache.get = MagicMock()
        self.mock_cache.get.return_value = ('token', 'refreshToken')
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)
        
        # Act
        service.refreshtokens()
    
        # Assert
        assert self.mock_cache.get.call_count == 1
        assert self.mock_cache.insert.call_count == 0
        assert self.mock_config._get_extend_pw.call_count == 0
        assert self.mock_api.signin.call_count == 0
        assert service._refreshtoken == 'refreshToken'
        assert service._signintoken == 'token'

    def test_getrefreshtoken_when_called_without_retrying_and_valid_api_response_returns_new_token(self):
        # Arrange
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)
        service._signintoken = 'token'
        service._refreshtoken = 'refreshToken'

        # Act
        actual = service.getrefreshtoken()

        # Assert
        assert actual == 'newToken'
        assert self.mock_api.refresh_token.call_count == 1
        assert self.mock_api.signin.call_count == 0


    def test_getrefreshtoken_when_called_with_retry_and_signin_successful_returns_new_token(self):
        # Arrange
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)

        # Act
        actual = service.getrefreshtoken(True)

        # Assert
        assert actual == 'newToken'
        assert self.mock_api.signin.call_count == 1
        assert self.mock_api.refresh_token.call_count == 1


    def test_getrefreshtoken_when_called_with_retry_and_signin_throws_exception_reraises_exception(self):
        # Arrange
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)
        self.mock_api.refresh_token = MagicMock(side_effect=ServiceException('no bueno'))

        # Act and Assert
        with pytest.raises(ServiceException):
            service.getrefreshtoken(True)

    def test_get_active_cards_when_called_filters_results(self):
        # Arrange
        service = VTSService(self.request, self.mock_cache, self.mock_api, self.mock_config)
        service.getrefreshtoken = MagicMock()
        service.getrefreshtoken.return_value = 'token'
        self.mock_api.list_cards = MagicMock()
        self.mock_api.list_cards.return_value = self._mock_card_response()

        # Act
        result = service.get_active_cards()

        # Assert
        assert len(result) == 1
        assert result[0].id == 'id1'

    
    def _mock_card_response(self):
        return ExtendApiCardResult(virtualCards=[
            ExtendApiVirtualCard('id1', 'displayName1', 100, 0, '1234', 'ACTIVE'),
            ExtendApiVirtualCard('id2', 'displayName2', 200, 0, '2345', 'INACTIVE'),            
        ])