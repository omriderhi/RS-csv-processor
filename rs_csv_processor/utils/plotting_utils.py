import os
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

from rs_csv_processor.entities.entities import Source, Site
from rs_csv_processor.models.plot_models import SourcePlotConfigurations, SitePlotConfigurations
from rs_csv_processor.resources.constants import FieldNames
from rs_csv_processor.utils.time_utils import get_source_timeframe


class PlotUtils:
    @staticmethod
    def visualize_data_cleaning_flow(cleaned_source: Source, source_plot_configs: SourcePlotConfigurations,
                                     site_name: str, output_folder: Optional[str]):
        ndvi_keys = [key for key in cleaned_source.source_data if key.startswith('NDVI')]
        source_color = source_plot_configs.color
        source_linestyle = source_plot_configs.line_style

        figures_num = len(ndvi_keys)
        fig, axes = plt.subplots(sharex=True, nrows=figures_num, ncols=1, figsize=(150, 50))
        fig.suptitle(f'{cleaned_source.source_name} Data Cleaning flow in {site_name}', size=80, x=0.5, y=1.03)
        x = cleaned_source.source_data['DATE']

        for i, ndvi_key in enumerate(ndvi_keys):
            mask = np.isfinite(cleaned_source.source_data[ndvi_key])
            axes[i].set_title(f'{ndvi_key}', fontsize=60)
            axes[i].set_ylabel('NDVI', fontsize=40)
            axes[i].tick_params(
                labelsize=40
            )
            axes[i].xaxis.set_major_locator(mdates.MonthLocator(interval=4))
            axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
            axes[i].plot(
                x[mask],
                cleaned_source.source_data[ndvi_key][mask],
                color=source_color,
                linestyle=source_linestyle,
                linewidth=4,
                label='DATE'
            )
            if output_folder:
                fig.savefig(
                    os.path.join(output_folder, 'data_cleaning', site_name, f'{cleaned_source.source_name}.png')
                )
            else:
                plt.show(fig)

    @staticmethod
    def plot_site_data(
            site: Site, site_plot_configurations: SitePlotConfigurations, sources_names_to_plot: list[str],
            focus_on_source: Optional[str] = None, output_path: Optional[str] = None):
        site_df = site.site_data
        if focus_on_source:
            start_ind, end_ind = get_source_timeframe(site_df, source_name=focus_on_source)
            site_df = site_df.loc[start_ind:end_ind, :]
        dates = np.array([dt.fromtimestamp(ts) for ts in site_df.index])

        fig, ax = plt.subplots(figsize=(20, 5))
        ax.set_title(f'{site.site_name} all data')
        if focus_on_source:
            ax.set_title(f'{site.site_name} all data focused on {focus_on_source}')

        for field_name in site_df:
            source_name = field_name.split(' ')[-1]
            if source_name not in sources_names_to_plot:
                continue
            mask = np.isfinite(site_df[field_name])
            source_plot_configurations = site_plot_configurations.sources_configurations.get(source_name)
            if source_name.startswith(FieldNames.ims_rainfall):
                ax1 = ax.twinx()
                plt.gca().invert_yaxis()
                ax1.bar(
                    dates,
                    site_df[field_name],
                    label=source_name,
                )
            elif source_name.startswith(FieldNames.ims_temprature):
                ax1 = ax.twinx()
                ax1.plot(
                    dates[mask],
                    site_df[field_name][mask],
                    color=source_plot_configurations.color,
                    label=source_name,
                    linestyle=source_plot_configurations.line_style,
                    linewidth=0.2
                )
            else:
                label = source_plot_configurations.hide_from_legend if source_plot_configurations.hide_from_legend else\
                    source_name
                ax.plot(
                    dates[mask],
                    site_df[field_name][mask],
                    color=source_plot_configurations.color,
                    label=label,
                    linestyle=source_plot_configurations.line_style
                )
        fig.legend(
            loc='upper right',
            ncol=2
        )
        fig.dpi = 400
        fig.tight_layout()
        output_filename = f'{site.site_name}_all_data.png'
        if not output_path:
            plt.show(fig)
        elif focus_on_source:
            output_filename = f'{site.site_name}_all_data_focused_on_{focus_on_source}.png'
            fig.savefig(os.path.join(output_path, output_filename), bbox_inches='tight')
        else:
            fig.savefig(os.path.join(output_path, output_filename), bbox_inches='tight')
