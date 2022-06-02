import json
import dataclasses


resp_headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Content-Type': 'application/json'
}

def ok(response):
    return {
        'statusCode': 200,
        'headers': resp_headers,
        'body': json.dumps(response, cls=DataclassEncoder)
    }


def notfound(response):
    return {
        'statusCode': 404,
        'header': resp_headers
    }


def unauthorized(response):
    return {
        'statusCode': 401,
        'headers': resp_headers,
        'body': json.dumps(response)
    }


def error(response):
    return {
        'statusCode': 500,
        'headers': resp_headers,
        'body': json.dumps(response)
    }


# Make dataclasses json serializable: https://stackoverflow.com/a/51286749
class DataclassEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)