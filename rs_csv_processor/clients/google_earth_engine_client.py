import ee
from datetime import datetime
import pandas as pd
import altair as alt
import numpy as np
import folium
import shapely


class GeeClient:
    ee.Authenticate()
    ee.Initialize()

    @staticmethod
    def get_raw_data(
            source_id,
            start_time: datetime,
            end_time: datetime,
            bands: tuple[str],
            geometry: shapely.Point | shapely.Polygon
    ):
        date_range = ee.DateRange(ee.Date(start_time), ee.Date(end_time))
        image_collection = \
            ee.ImageCollection(source_id).filterDate(date_range).select(*bands)

        # bounds = ee.Geometry(geometry)





