import boto3
from app.ConfigClient import ConfigClient

extend_pw_parameter_name = 'extend_pw'


class ExtendSSMConfigClient(ConfigClient):
    def __init__(self):
        self._client = boto3.client('ssm', region_name='us-east-1')


    def _get_extend_pw(self):
        response = self._client.get_parameter(Name=extend_pw_parameter_name)
        return response['Parameter']['Value']
