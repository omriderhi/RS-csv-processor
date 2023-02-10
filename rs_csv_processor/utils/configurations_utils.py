import dataclasses
import importlib.resources
import json
from typing import Optional, Tuple

from rs_csv_processor.utils.geometry import PointLocation

DEFAULT_SOURCE_CONFIGURATIONS = importlib.resources.open_text('resources', 'source_configurations_template.json')


def read_json_file(json_path: Optional[str] = None) -> dict:
    if json_path:
        with open(json_path, 'r') as jf:
            return json.load(jf)
    else:
        return json.load(DEFAULT_SOURCE_CONFIGURATIONS)


@dataclasses.dataclass
class SourceConfigurations:
    minimum_desired_value: Optional[float] = None
    maximum_desired_value: Optional[float] = None
    outlier_distance_factor: Optional[float] = None
    monthly_images: Optional[int] = None
    plot_specifications: Optional[dict] = None


class SiteConfigurations:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.raw_configurations_dict: dict = read_json_file(json_path)
        self.sources: list = [source_name for source_name in self.raw_configurations_dict.keys()]
        self.site_configurations: dict[str, SourceConfigurations] = {
            source_name: self._get_source_configurations(source_name) for source_name in self.sources
        }

    def _get_source_configurations(self, source_name: str) -> SourceConfigurations:
        return SourceConfigurations(
            self.raw_configurations_dict[source_name]
        )

    @classmethod
    def get_default_configurations(cls, location_coordinates: Tuple[float]):
        return {
            "location": PointLocation.from_coords(location_coordinates),
        }
