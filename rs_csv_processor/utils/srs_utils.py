import csv
import datetime
from datetime import datetime as dt

from rs_csv_processor.resources.constants import SrsDefaultValues


class SrsUtils:
    def __init__(self, input_dat_path: str):
        self.input_dat_path = input_dat_path
        self.raw_data = SrsUtils.read_dat_as_csv(input_dat_path)

    @staticmethod
    def read_dat_as_csv(input_dat_path: str):
        with open(input_dat_path, 'r') as i_d:
            d_reader = csv.reader(i_d, delimiter=',', quotechar='|')
            return [row for row in d_reader if len(row) != 0]

    def get_relevant_indices_and_target_headers(self) -> tuple[list, list, list]:
        headers = self.raw_data[1]

        ndvi_data_headers = [header for header in headers if header.startswith('"NDVI')]
        ndvi_data_fields_indices = [headers.index(field) for field in ndvi_data_headers]

        administrative_fields_indices = [i for i in range(4)]
        administrative_fields = [header.replace('"', '') for header in headers[:4]]

        target_headers = administrative_fields + [header.replace('"', '') for header in ndvi_data_headers]

        return ndvi_data_fields_indices, administrative_fields_indices, target_headers

    def extract_from_fixed_hour_of_the_day(
            self,
            dat_date_format: str = SrsDefaultValues.dat_date_format,
            fixed_date_format: str = SrsDefaultValues.fixed_date_format,
            collection_hour: int = SrsDefaultValues.collection_hour,
            collection_minutes: int = SrsDefaultValues.collection_minutes
    ) -> list[list]:

        ndvi_data_fields_indices, administrative_fields_indices, target_headers = \
            self.get_relevant_indices_and_target_headers()

        relevant_csv_data = [target_headers]

        for line in self.raw_data[4:]:
            temp_record = []
            date = dt.strptime(line[0].replace('"', ''), dat_date_format)
            formatted_date = dt.strftime(date, fixed_date_format)
            line[0] = formatted_date
            if date.hour == collection_hour and date.minute == collection_minutes:
                for cell in line:
                    if line.index(cell) in administrative_fields_indices or line.index(cell) in ndvi_data_fields_indices:
                        temp_record.append(cell.replace('"', ''))
                relevant_csv_data.append(temp_record)

        return relevant_csv_data

    def extract_daily_dataset(
            self,
            collection_date: datetime,
            dat_date_format: str = SrsDefaultValues.dat_date_format,
            fixed_datetime__format: str = SrsDefaultValues.fixed_date_time_format,
    ):
        relevant_csv_data = []
        ndvi_data_fields_indices, administrative_fields_indices, target_headers = \
            self.get_relevant_indices_and_target_headers()
        relevant_csv_data.append(target_headers)
        for i, line in enumerate(self.raw_data[4:]):
            date = dt.strptime(line[0].replace('"', ''), dat_date_format)
            if date.date() == collection_date.date():
                formatted_date = dt.strftime(date, fixed_datetime__format)
                line[0] = formatted_date
                relevant_csv_data.append(line)

        return relevant_csv_data
