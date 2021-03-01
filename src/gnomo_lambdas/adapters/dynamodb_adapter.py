import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()


class DynamoDBAdapter(object):

    def __init__(self, table_name: str, region: str = None):
        dynamodb = boto3.resource('dynamodb') \
            if region is None else boto3.resource('dynamodb', region_name=region)
        self.dynamo_table = dynamodb.Table(table_name)

    def _get_table_name(self, table_alias):
        cfn_client = boto3.client('cloudformation')
        try:
            stack_exports = cfn_client.list_exports()['Exports']
            return [export for export in stack_exports if export['Name'] == table_alias][0]['Value']
        except IndexError as error:
            logger.info(f'{table_alias} not found in exports list: {stack_exports}')
            raise error
        except Exception as error:
            logger.info('Failed to call cfn list_exports()')
            raise error

    @staticmethod
    def _client_error_fallback(error: ClientError, message: str):
        error_message = error.response['Error']['Message']
        error_message = f'{message}: {error_message}'
        logger.info(error_message)
        return Exception(error_message)

    @staticmethod
    def _global_error_fallback(error: Exception, message: str):
        error_message = f'{message}: {error}'
        logger.info(error_message)
        return Exception(error_message)

    @staticmethod
    def _is_conditional_check_failed_exception(exception: ClientError):
        return exception.response['Error']['Code'] == 'ConditionalCheckFailedException'  # noqa

    @staticmethod
    def _return_default_if_condition_fails(exception: ClientError, exception_message: str,
                                           default_not_found_message: str):
        if DynamoDBAdapter._is_conditional_check_failed_exception(exception):
            return DynamoDBAdapter._client_error_fallback(exception, default_not_found_message)
        else:
            return DynamoDBAdapter._client_error_fallback(exception, exception_message)
