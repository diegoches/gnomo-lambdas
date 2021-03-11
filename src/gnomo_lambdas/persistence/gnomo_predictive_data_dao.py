from botocore.exceptions import ClientError
from typing import Dict, Any
from src.gnomo_lambdas.adapters.dynamodb_adapter import DynamoDBAdapter
from src.gnomo_lambdas.helpers.date_helper import DateHelper


class GnomoPredictiveDataDAO(DynamoDBAdapter):

    __table_name = 'GnomoPredictionData'

    def __init__(self, dynamo_table: Any = None):
        if dynamo_table is None:
            super().__init__(self.__table_name)
        else:
            self.dynamo_table = dynamo_table

    def create(self, doc_id: str, name: str, metadata: Dict, label: int) -> Dict:
        try:
            current_date = DateHelper.generate_current_date()
            item = {
                'country_model': 'PE|TENANT_DEBTOR',
                'doc_id': doc_id,
                'alias': name,
                'metadata': metadata,
                'log_data': {
                    'creation_date': current_date,
                    'update_date': current_date,
                    'reason': 'Report',
                    'author': 'User'
                },
                'reported_label': label,
                'ttl_date': current_date
            }
            self._dynamo_table.put_item(Item=item)
            return item
        except ClientError as client_error:
            message = f'Failed to create predictive data in DynamoDB for: ' \
                      f'{name} with document id: {doc_id}'
            raise self._client_error_fallback(client_error, message)
        except Exception as exception:
            message = f'Something went wrong when creating predictive data for: ' \
                      f'{name} with document id: {doc_id}'
            raise self._global_error_fallback(exception, message)

    def get(self, doc_id: str) -> Dict:
        try:
            response = self._dynamo_table.get_item(
                Key={'country_model': 'PE|TENANT_DEBTOR', 'doc_id': doc_id}
            )
        except ClientError as client_error:
            message = f'Failed to get predictive data in DynamoDB for doc_id: {doc_id}'
            raise self._client_error_fallback(client_error, message)

        except Exception as exception:
            message = f'Something went wrong when getting predictive data for doc_id: {doc_id}'
            raise self._global_error_fallback(exception, message)

        if 'Item' not in response:
            message = f'The predictive data with the doc_id {doc_id} does not exist.'
            raise KeyError(message)

        return response['Item']
