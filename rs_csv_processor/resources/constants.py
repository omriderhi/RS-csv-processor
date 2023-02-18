from enum import Enum


class DefaultValues(str, Enum):
    date_field_name = "DATE"


class FieldNames:
    ndvi_raw_field_name_suffix = "NDVI_RAW"


class SrsDefaultValues:
    dat_date_format = '%Y-%m-%d %H:%M:%S'
    fixed_date_format = '%d/%m/%Y'
    fixed_date_time_format = '%d/%m/%Y %H:%M'
    collection_hour = 10
    collection_minutes = 00
