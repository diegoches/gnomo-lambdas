import json
from src.gnomo_lambdas.services.tenant_service import TenantService


def lambda_handler(event, context):
    print(event)

    body = json.loads(event.get('body', {}))

    doc_id = body.get('docId')
    name = body.get('name')

    service = TenantService()
    result = service.report_tenant(doc_id, name)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
