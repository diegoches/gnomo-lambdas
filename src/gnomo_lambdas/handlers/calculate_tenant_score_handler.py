import json
from src.gnomo_lambdas.services.tenant_service import TenantService
from src.gnomo_lambdas.helpers.decimal_encoder import DecimalEncoder


def lambda_handler(event, context):
    print('event: ', event)

    parameters = event.get('queryStringParameters', {})
    doc_id = parameters.get('docID', parameters.get('dni', None))

    service = TenantService()
    score = service.get_prediction(doc_id)

    dummy_score = {
        'docId': doc_id,
        'score': float(score)
    }

    return {
        'statusCode': 200,
        'body': json.dumps(dummy_score,cls=DecimalEncoder)
    }
