from __future__ import annotations

from typing import Any, Optional
import pandas as pd

from rs_csv_processor.models.plot_models import SourcePlotConfigurations
from rs_csv_processor.utils.configurations_utils import read_json_file
from rs_csv_processor.utils.geometry import PointLocation


class Source:
    def __init__(
            self,
            source_name: str,
            source_label: str | None = None,
            source_configurations: Optional[dict[str, Any]] = None,
            source_data: pd.DataFrame = pd.DataFrame(),
            plot_configurations: SourcePlotConfigurations = SourcePlotConfigurations.get_default_plot_configurations()
                 ):
        self.source_name = source_name
        self.source_label = source_label
        self.source_configurations = source_configurations
        self.source_data = source_data
        self.plot_configurations = plot_configurations

    @staticmethod
    def from_files(source_name: str, configurations_path: str = None, data_file_path: str = None) -> Source:
        source_configurations = read_json_file(configurations_path)
        return Source(
            source_name=source_name,
            source_data=pd.read_csv(data_file_path),
            source_configurations=source_configurations
        )


class Site:
    def __init__(
            self,
            site_name: str,
            location: tuple,
            site_data: pd.DataFrame = pd.DataFrame(),
            sources_configurations: Optional[dict[str, Any]] = None,
    ):
        self.site_name = site_name
        self.location = PointLocation.from_tuple(location)
        self.site_data = site_data
        self.sources_configurations = sources_configurations
        self.sources: list[Source] = []

    def add_source(self, source: Source):
        self.sources_configurations[source.source_name] = source.source_configurations

        self.site_data = self.site_data.join(
            source.source_data,
            how='outer',
            rsuffix=f'_{source.source_name}',
            sort=True
        )

    @staticmethod
    def from_files(site_name: str, configurations_path: str = None, data_file_path: str = None):
        site_configurations = read_json_file(configurations_path)
        return Site(
            site_name=site_name,
            site_data=pd.read_csv(data_file_path),
            sources_configurations=site_configurations,
            location=site_configurations.get('location')
            # TODO- add a site configuration template with 'location' key in it
        )

    def generate_site_data_from_sources(self):
        for source in self.sources:
            self.add_source(source)
