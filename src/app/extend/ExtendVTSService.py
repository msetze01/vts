from app.VTSService import VTSService
from app.VTSRequest import VTSRequest
from app.extend.ExtendTokenDynamoDbCacheClient import ExtendTokenDynamoDbCacheClient
from app.extend.ExtendApiClient import ExtendApiClient
from app.extend.ExtendSSMConfigClient import ExtendSSMConfigClient


class ExtendVTSService(VTSService):
    def __init__(self, request: VTSRequest):
        super().__init__(request, ExtendTokenDynamoDbCacheClient(), ExtendApiClient(), ExtendSSMConfigClient()) 
