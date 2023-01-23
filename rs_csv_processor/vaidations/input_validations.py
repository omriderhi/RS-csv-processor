import csv
from typing import Any

from rs_csv_processor.resources.Constants import DefaultValues
from rs_csv_processor.utils.time_utils import Date
from rs_csv_processor.vaidations.failure_messages import FailureMessages


class InputValidations:
    def __init__(self, csv_path: str):
        self.csv_path: str = csv_path
        self.csv_data: list[list] = self._read_csv(csv_path)
        self.validation_failures: dict[int, dict[int, str]] = {}

    @staticmethod
    def _read_csv(csv_path: str) -> list[list[Any]]:
        with open(csv_path, 'r') as cf:
            reader = csv.reader(cf)
            return [row for row in reader]

    def validate_raw_csv_structure(self, date_field_name: str = DefaultValues.DateFieldName) -> dict:
        failures_dict: dict[int, dict[int, str]] = {}

        headers = self.csv_data[0]
        self.validate_headers(headers, failures_dict)

        date_field_ind = headers.index(date_field_name)

        for i, row in enumerate(self.csv_data[1:]):
            line_num = i + 2
            self.validate_csv_row(row, failures_dict, line_num, date_field_ind)

        self.validation_failures.update(failures_dict)

    def validate_csv_row(
            self,
            row: list[Any],
            failures_dict: dict,
            line_num: int,
            date_field_ind: int
    ) -> None:
        for i, data_cell in enumerate(row):
            if i == date_field_ind:
                data_validation = Date.try_from_string(data_cell)
                if not data_validation:
                    if line_num not in failures_dict.keys():
                        failures_dict[line_num] = {}
                    failures_dict[line_num][i] = FailureMessages.DateFailureMessage.DateFailureMessage.value.format(
                        line_num=line_num,
                        raw_date=data_cell
                    )
                    continue
            else:
                data_validation = self.validate_content_values(data_cell)
                if not data_validation:
                    if line_num not in failures_dict.keys():
                        failures_dict[line_num] = {}
                    failures_dict[line_num][i] = FailureMessages.DataCellFailureMessage.value.format(
                        line_num=line_num,
                        data_cell=data_cell
                    )

    @staticmethod
    def validate_content_values(data_cell: str) -> bool:
        try:
            float(data_cell)
        except ValueError:
            return False
        return True

    @staticmethod
    def validate_headers(headers: list[Any], failures_dict: dict) -> bool:
        valid_headers = False
        for header in headers:
            try:
                float(header)
            except ValueError:
                valid_headers = True
        if not valid_headers:
            header_ind = headers.index(header)
            failures_dict[0][header_ind] = FailureMessages.HeaderFailureMessage.value.format(
                raw_str=header
            )
