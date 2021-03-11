import json
from src.gnomo_lambdas.services.tenant_service import TenantService
from src.gnomo_lambdas.helpers.decimal_encoder import DecimalEncoder


def lambda_handler(event, context):
    print('event: ', event)

    body = json.loads(event.get('body', {}))

    doc_id = body.get('docId')
    name = body.get('alias')
    metadata = body.get('metadata', {})

    service = TenantService()
    result = service.report_tenant(doc_id, name, metadata)

    return {
        'statusCode': 200,
        'body': json.dumps(result, cls=DecimalEncoder)
    }
