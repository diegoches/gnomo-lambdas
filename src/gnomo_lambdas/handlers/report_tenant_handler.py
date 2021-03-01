import json


def lambda_handler(event, context):
    print(event)
    print('VAMOOOOOO')

    dummy_score = {
        'message': 'Sape'
    }

    return {
        'statusCode': 200,
        'body': json.dumps(dummy_score)
    }
