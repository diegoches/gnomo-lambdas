from datetime import  datetime


class DateHelper:

    @classmethod
    def generate_current_date(cls) -> str:
        current_datetime = datetime.now()
        return current_datetime.isoformat(timespec='seconds')
