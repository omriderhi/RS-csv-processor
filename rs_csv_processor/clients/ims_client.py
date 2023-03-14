from __future__ import annotations

import json
import requests
from urllib.parse import urljoin
from datetime import datetime as dt


class ImsClient:
    base_url: str = "https://api.ims.gov.il/v1/Envista"
    ims_date_format: str = "%Y/%m/%d"
    params: list = [
        "api_token: str",
        "start_date: datetime.datetime",
        "end_date: datetime.datetime",
        "station_id or region_id or both: int",
        "region_focused: bool - set true if you want to collect data on regional scope"
    ]

    def __init__(
            self,
            api_token: str,
            start_date: dt,
            end_date: dt,
            station_id: int | None = None,
            region_id: int | None = None,
            region_focused: bool = False
    ):
        self.api_token = api_token
        self.start_date = start_date
        self.end_date = end_date
        assert region_id or station_id, IOError("Station id or Region id are required")
        self.station_id = station_id
        self.region_id = region_id
        self.region_focused = region_focused
        if region_id and not station_id:
            self.region_focused = True

    def _get_request(self):
        """
        example url from api doc:
        example url from api doc: https://api.ims.gov.il/v1/envista/stations/{STATION_NUM}/data?from={YYYY/MM/DD}&to={YYYY/MM/DD}
        :return: url
        """

        url_parts = []

        if self.region_focused:
            scope = "regions"
            scope_id = str(self.region_id)
        else:
            scope = "stations"
            scope_id = str(self.station_id)

        url_parts.append(scope)
        url_parts.append(scope_id)

        start_date = dt.strftime(self.start_date, self.ims_date_format)
        end_date = dt.strftime(self.end_date, self.ims_date_format)
        date_range = f"data?from={start_date}&to={end_date}"
        url_parts.append(date_range)
        return urljoin(self.base_url, "/".join(url_parts))

    def _get_raw_response(self):
        url = self._get_request()
        headers = {
           "Authorization": f"ApiToken {self.api_token}"
        }
        return requests.request("GET", url, headers=headers)

    def get_ims_source(self):
        response = self._get_raw_response()
        return json.loads(response.text.encode('utf8'))

    @staticmethod
    def from_dict(params_dict: dict) -> ImsClient:
        return ImsClient(**params_dict)
