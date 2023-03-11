from enum import Enum


class DefaultValues(str, Enum):
    date_field_name = "DATE"


class FieldNames:
    ndvi_raw_suffix = "NDVI_RAW"
    ims_rainfall = 'RAINFALL'
    ims_temprature = 'TEMP'


class SrsDefaultValues:
    dat_date_format = '%Y-%m-%d %H:%M:%S'
    fixed_date_format = '%d/%m/%Y'
    fixed_date_time_format = '%d/%m/%Y %H:%M'
    collection_hour = 10
    collection_minutes = 00
    dat_date_field_name = "TIMESTAMP"
    ndvi_field_name_template = "NDVI_{sensor_num}_Avg"
    ndvi_validation_allowed_error_range = 0.01

