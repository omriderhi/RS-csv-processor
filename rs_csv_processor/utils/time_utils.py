from dateutil.parser import parse as parse_date
from dateutil.parser import ParserError


class Date:
    @staticmethod
    def try_from_string(raw_date: str) -> bool:
        try:
            parse_date(raw_date)
        except ParserError:
            return False
        return True
