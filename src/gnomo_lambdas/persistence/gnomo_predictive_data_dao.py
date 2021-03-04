from botocore.exceptions import ClientError
from typing import Dict, Any
from src.gnomo_lambdas.adapters.dynamodb_adapter import DynamoDBAdapter


class GnomoPredictiveDataDAO(DynamoDBAdapter):

    __table_name = 'GnomoPredictionData'

    def __init__(self, dynamo_table: Any = None):
        if dynamo_table is None:
            super().__init__(self.__table_name)
        else:
            self.dynamo_table = dynamo_table

    def create(self, doc_id: str, name: str) -> Dict:
        try:
            item = {
                'country_model': 'PE|TENANT_DEBTOR',
                'doc_id': doc_id,
                'alias': name
            }
            response = self._dynamo_table.put_item(Item=item)
            return response.get('Item', {})
        except ClientError as client_error:
            message = f'Failed to create predictive data in DynamoDB for: ' \
                      f'{name} with document id: {doc_id}'
            raise self._client_error_fallback(client_error, message)
        except Exception as exception:
            message = f'Something went wrong when creating predictive data for: ' \
                      f'{name} with document id: {doc_id}'
            raise self._global_error_fallback(exception, message)
