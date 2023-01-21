from typing import Tuple, List, Optional

from rs_csv_processor.resources.Constants import DefaultValues


class InputValidations:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def validate_raw_csv_structure(self, csv_data: List[List], date_field_name: str = DefaultValues.DateFieldName) ->\
            Tuple[bool, dict, Optional[str]]:
        """
        runs group of validations of csv structure
        :param csv_data:
        :param date_field_name:
        :return:
        """
        input_csv_valid = True
        types_dict = {}
        error_message = None

        headers = csv_data[0]
        if len(headers) != 2:
            raise Exception(f'each csv file should have only two headers, {self.csv_path} has {len(headers)} headers')
        else:
            for header in headers:
                types_dict[header] = None
        for i, row in enumerate(csv_data[1:]):
            line_num = i + 2



        return input_csv_valid, types_dict, error_message
