import logging
import traceback
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BaseHandler:
    __error_message = 'ERROR'
    __success_message = 'SUCCESS'
    __default_attribute_error_message = 'There is no {0} in Event\'s attributes.'

    @classmethod
    def _handle_success(cls, key, body=None):

        return_body = {key: body} if body is not None else {}
        return {
            'statusCode': HTTPStatus.OK,
            'message': cls.__success_message,
            'body': return_body
        }

    @classmethod
    def _handle_error(cls, message, code):

        return {
            'statusCode': code,
            'message': f'{cls.__error_message}: {message}',
            'body': {}
        }

    @classmethod
    def _extract_from_event(cls, event, key, function, error_message=None):

        if key not in event:
            error_message = error_message if error_message is not None else \
                cls.__default_attribute_error_message.format(key)
            raise AttributeError(error_message)
        return function(event[key])

    @staticmethod
    def _decorate_handler(func):

        def decorated_handler(self, event, context):
            logger.info(f'Event: {event}')
            logger.info(f'Context: {context}')
            try:
                output_value = func(self, event, context)
            except AttributeError as exception:
                traceback.print_tb(exception.__traceback__)
                output_value = BaseHandler._handle_error(
                    str(exception), HTTPStatus.BAD_REQUEST
                )
            except KeyError as exception:
                traceback.print_tb(exception.__traceback__)
                output_value = BaseHandler._handle_error(
                    str(exception), HTTPStatus.BAD_REQUEST
                )
            except ValueError as exception:
                traceback.print_tb(exception.__traceback__)
                output_value = BaseHandler._handle_error(
                    str(exception), HTTPStatus.BAD_REQUEST
                )
            except Exception as exception:
                traceback.print_tb(exception.__traceback__)
                output_value = BaseHandler._handle_error(
                    str(exception), HTTPStatus.INTERNAL_SERVER_ERROR
                )
            logger.info(f'Output: {output_value}')
            return output_value
        return decorated_handler
