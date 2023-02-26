from enum import Enum


class FailureMessages(str, Enum):
    DateFailureMessage = "Line number {line_num}: the format of {raw_date} is not valid for parsing"
    DataCellFailureMessage = "Line number {line_num}: data - {data_cell} could not be converted to float"
    HeaderFailureMessage = "Header {raw_str} is a number, which should be a descriptive string"
    SrsNdviValidationFailureMessage = "Line number {line_num}: Sensor {sensor_num}: calculative ndvi and extracted " \
                                      "ndvi diff is grater then {allowed_diff}"
    SrsDataTypeErrorMessage = "Line number {line_num}: Sensor {sensor_num}: {data_value} is invalid data " \
                              "type for calculations"

