from __future__ import annotations

from logging import Logger
from typing import Optional


class PlotConfigurationsBase:
    def __init__(self,
                 color: str,
                 line_style: str
                 ):
        self.color = color
        self.line_style = line_style

    @staticmethod
    def get_default_plot_configurations() -> PlotConfigurationsBase:
        return PlotConfigurationsBase(
            color='cyan',
            line_style='solid'
        )


class SourcePlotConfigurations(PlotConfigurationsBase):
    def __init__(
            self,
            source_name: str,
            color: str,
            line_style: str,
            label: bool = True
    ):
        self.source_name = source_name
        self.label = source_name if label else '_Hidden'
        super().__init__(
            color=color,
            line_style=line_style
        )


class SitePlotConfigurations:
    def __init__(
            self,
            site_name: str,
            sources_configurations: list[SourcePlotConfigurations]
    ):
        self.site_name = site_name
        self.sources_configurations = {
            source_plot_configurations.source_name: source_plot_configurations for
            source_plot_configurations in sources_configurations
        }

    def validate_overlapping_plot_configs(self, logger: Optional[Logger] = None) -> bool:
        colors_dict: dict[str, list[str]] = {}
        line_styles_dict: dict[str, list[str]] = {}
        for source_configuration in self.sources_configurations:
            source_color = source_configuration.color
            if source_color in colors_dict.keys():
                colors_dict[source_color].append(source_configuration.source_name)
            else:
                colors_dict[source_color] = [source_configuration.source_name]

            source_line_style = source_configuration.line_style
            if source_line_style in line_styles_dict.keys():
                line_styles_dict[source_line_style].append(source_configuration.source_name)
            else:
                line_styles_dict[source_line_style] = [source_configuration.source_name]

        overlapping_colors_sources = []
        for color, sources_names in colors_dict.items():
            if len(sources_names) < 2:
                continue
            else:
                if logger:
                    logger.warning(f'you have overlapping color: {color}.  between the sources: {sources_names}')
                overlapping_colors_sources.append(sources_names)

        for line_style, sources_names in line_styles_dict.items():
            if len(sources_names) < 2:
                continue
            elif sources_names in overlapping_colors_sources:
                if logger:
                    logger.error(f'you have overlapping color and line style between the sources: {sources_names}')
                return False
            else:
                if logger:
                    logger.warning(f'you have overlapping color: {line_style}.  between the sources: {sources_names}')

        return True


