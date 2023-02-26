from logging import Logger

from rs_csv_processor.resources.constants import SrsDefaultValues
from rs_csv_processor.utils.srs_utils import SrsUtils
from rs_csv_processor.vaidations.failure_messages import FailureMessages


class SrsValidations:
    target_headers = [
        "TIMESTAMP",
        "EXTRACTED_NDVI",
        "CACULATED_NDVI",
        "VALIDATION_STATUS"
    ]

    ndvi_calculation_field_names = {
        'up_NIR': "UpNIR_1_Avg",
        'up_RED': "UpRed_1_Avg",
        'down_NIR': "DownNIR_{sensor_num}_Avg",
        'down_RED': "DownRed_{sensor_num}_Avg"
    }

    administrative_field_names = [
        "RECORD",
        "Batt_Min",
        "PTemp"
    ]

    def __init__(
            self,
            input_dat_path: str,
            collection_hour: int = SrsDefaultValues.collection_hour,
            collection_minutes: int = SrsDefaultValues.collection_minutes,
            input_time_field_name: str = SrsDefaultValues.dat_date_field_name,
            ndvi_field_name_template: str = SrsDefaultValues.ndvi_field_name_template,
            allowed_error_range: float = SrsDefaultValues.ndvi_validation_allowed_error_range,
            logger: Logger = None
    ):
        self.input_dat_path = input_dat_path
        self.input_raw_data = SrsUtils.read_dat_as_csv(input_dat_path)
        self.headers = self.input_raw_data[0]
        self.collection_hour = collection_hour
        self.collection_minutes = collection_minutes
        self.input_time_field_name = input_time_field_name
        self.ndvi_field_name_template = ndvi_field_name_template
        self.allowed_error_range = allowed_error_range
        self.timestamp_ind = self._assign_field_ind(self.target_headers[0])
        self.validation_failures: dict = {}
        self.logger = logger

    def _assign_field_ind(self, field_name: str):
        return self.input_raw_data[0].index(field_name)

    def test_calculated_ndvi_is_aligned_with_sensors_derived_ndvi_for_row(
            self, row: list[str], sensor_num: int | str, line_num: int | str) -> bool:
        ndvi_valid = False
        extracted_ndvi = None
        calculated_ndvi = None

        ndvi_field_ind = self.headers.index(self.ndvi_field_name_template.format(sensor_num=sensor_num))
        up_nir_ind = self.headers.index(self.ndvi_calculation_field_names.get('up_NIR'))
        up_red_ind = self.headers.index(self.ndvi_calculation_field_names.get('up_RED'))
        down_nir_ind = self.headers.index(self.ndvi_calculation_field_names.get('down_NIR').format(
            sensor_num=sensor_num))
        down_red_ind = self.headers.index(self.ndvi_calculation_field_names.get('down_RED').format(
            sensor_num=sensor_num))

        try:
            extracted_ndvi = float(row[ndvi_field_ind])
            up_nir = float(row[up_nir_ind])
            up_red = float(row[up_red_ind])
            down_nir = float(row[down_nir_ind])
            down_red = float(row[down_red_ind])
            calculated_ndvi = ((down_nir / up_nir) - (down_red / up_red)) / ((down_nir / up_nir) + (down_red / up_red))
        except ValueError:
            for element in [row[ndvi_field_ind], row[up_nir_ind], row[up_red_ind],
                            row[down_nir_ind], row[down_red_ind]]:
                try:
                    float(element)
                except ValueError:
                    log_message = FailureMessages.SrsDataTypeErrorMessage.format(
                        line_num=line_num,
                        sensor_num=sensor_num,
                        data_value=element
                    )
                    if not self.validation_failures.get(line_num):
                        self.validation_failures[line_num] = {sensor_num: log_message}
                    else:
                        self.validation_failures[line_num][sensor_num] = log_message
                    if self.logger:
                        self.logger.warning(log_message)

        if (not extracted_ndvi or not calculated_ndvi) or \
                (abs(calculated_ndvi - extracted_ndvi) <= self.allowed_error_range):
            ndvi_valid = True
        return ndvi_valid

    def validate_ndvi_values(self, sensors_num: int = 3) -> None:
        for i, row in enumerate(self.input_raw_data[1:]):
            line_num = i + 2 + 3   #considering lines that were removed in original file
            for sensor_num in range(1, sensors_num + 1):
                if self.test_calculated_ndvi_is_aligned_with_sensors_derived_ndvi_for_row(
                    row=row,
                    sensor_num=sensor_num,
                    line_num=line_num
                ):
                    continue
                else:
                    log_message = FailureMessages.SrsNdviValidationFailureMessage.format(
                        line_num=line_num,
                        sensor_num=sensor_num,
                        allowed_diff=self.allowed_error_range
                    )
                    if self.logger:
                        self.logger.warning(log_message)
                    if not self.validation_failures.get(line_num):
                        self.validation_failures[line_num] = {sensor_num: log_message}
                    else:
                        self.validation_failures[line_num][sensor_num] = log_message
