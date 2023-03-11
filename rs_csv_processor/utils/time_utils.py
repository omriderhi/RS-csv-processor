import pandas as pd
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


def get_source_timeframe(site_df: pd.DataFrame, source_name: str) -> tuple[int, int]:
    filled_df = site_df.fillna(False)
    nsrs_fieldnames = []
    for key in site_df:
        splitted_key = key.split(' ')
        source_field_name = splitted_key[-1]
        source = source_field_name.split('_')[0]
        if source.startswith(source_name):
            nsrs_fieldnames.append(key)
    start_ind = 0
    end_ind = 0
    for i, row in filled_df.iterrows():
        values_existance = [row[nsrs_field] for nsrs_field in nsrs_fieldnames]
        if any(values_existance):
            if start_ind == 0:
                start_ind = i
            else:
                if i < start_ind:
                    start_ind = i
                if i > end_ind:
                    end_ind = i
    return start_ind, end_ind
