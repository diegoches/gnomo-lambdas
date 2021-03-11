from decimal import Decimal
from json import JSONEncoder


class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)
