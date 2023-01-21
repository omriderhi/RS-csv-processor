import dataclasses
import json
import os.path
from typing import Optional

DEFAULT_SOURCE_CONFIGURATIONS = importlib.resources.open_binary('resources', 'data.txt')

@dataclasses.dataclass
class SourceConfigurations:
    minimum_desired_value: Optional[float] = None
    maximum_desired_value: Optional[float] = None
    outlier_group_size: Optional[float] = None
    monthly_images: Optional[int] = None
    plot_specifications: Optional[dict] = None


class SiteConfigurations:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.full_configurations_dict: dict = self._read_json_file(json_path)
        self.sources: list = [source_name for source_name in self.full_configurations_dict.keys()]

    @staticmethod
    def _read_json_file(json_path: str = ) -> dict:
        with open(json_path, 'r') as jf:
            return json.load(jf)

    def get_source_configurations(self, source_name: str) -> SourceConfigurations:
        return SourceConfigurations(
            self.full_configurations_dict[source_name]
        )









