from enum import Enum


class FailureMessages(str, Enum):
    DateFailureMessage = "Line number {line_num}: the format of {raw_date} is not valid for parsing"
    DataCellFailureMessage = "Line number {line_num}: data - {data_cell} could not be converted to float"
    HeaderFailureMessage = "Header {raw_str} is a number, which should be a descriptive string"
