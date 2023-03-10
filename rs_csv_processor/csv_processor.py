from rs_csv_processor.resources.constants import FieldNames
import pandas as pd

"""
class CsvProcessor:

    def filter_extremes_in_df(csv_df: pd.DataFrame, source_configurations: dict,
                              raw_field_name: str = FieldNames.ndvi_raw_suffix):
        ndvi_values = [ndvi_value for _, ndvi_value in csv_df[raw_field_name].iteritems() if ndvi_value]

        if source_configurations.get('min'):
            possible_min = float(source_configurations.get('min'))
        else:
            possible_min = min(ndvi_values)
        if source_configurations.get('max'):
            possible_max = float(source_configurations.get('max'))
        else:
            possible_max = max(ndvi_values)

        filtered_values = []

        for i, row in csv_df.iterrows():
            raw_ndvi = row[raw_field_name]
            try:
                raw_ndvi = float(raw_ndvi)
            except ValueError:
                print(f'can not convert this value: {raw_ndvi} from {row[0]} - Skipping')
                continue
            except TypeError:
                print(f'can not convert this value: {raw_ndvi} from {row[0]} - Skipping')
                continue

            if possible_min <= raw_ndvi <= possible_max:
                filtered_values.append(raw_ndvi)
            else:
                filtered_values.append(None)

        csv_df.insert(
            len(csv_df.keys()),
            f"{source.source_name}_{FieldNames.ndvi_raw_suffix}",
            filtered_values
        )

        return csv_df
"""