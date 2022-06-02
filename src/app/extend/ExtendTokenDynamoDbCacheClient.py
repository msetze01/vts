from abc import abstractmethod
import boto3
import time
from app.CacheClient import CacheClient


class ExtendTokenDynamoDbCacheClient(CacheClient):
    def __init__(self):
        self.client = boto3.client('dynamodb', region_name='us-east-1')
        self.tablename = 'vts_tokencache'
        self.resource = boto3.resource('dynamodb')


    def get(self, key):
        response = self.client.get_item(
            TableName=self.tablename,
            Key={ 'email': { 'S': key } },
            ProjectionExpression='signintoken, refreshtoken'
        )
        if 'Item' in response:
            return (response['Item']['signintoken']['S'], response['Item']['refreshtoken']['S'])
        return (None, None)

        
    def remove(self, key):
        self.client.delete_item(
            TableName=self.tablename,
            Key={ 'email': { 'S': key } }
        )


    def insert(self, key, data={}):
        self.remove(key)
        ttl = 600 + int(time.time()) # expire after 10 mins

        table = self.resource.Table(self.tablename)
        table.put_item(Item={
            'email': key, 
            'refreshtoken': data['refreshtoken'],
            'signintoken': data['token'],
            'ttl': ttl
        })
