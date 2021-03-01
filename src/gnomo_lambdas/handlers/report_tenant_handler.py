import json
from random import seed, random

seed(1)

def lambda_handler(event, context):

    parameters = event.get('queryStringParameters', {})
    doc_id = parameters.get('docID', parameters.get('dni', None))
    score = random() if doc_id is not None else None

    print(event)

    dummy_score = {
        'docId': doc_id,
        'score': score
    }

    return {
        'statusCode': 200,
        'body': json.dumps(dummy_score)
    }
