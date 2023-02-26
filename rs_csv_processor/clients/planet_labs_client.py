import os

from rs_csv_processor.utils.geometry import AreaLocation


class PlanetLabsClient:
    @staticmethod
    def _get_api_key_from_file(input_key_path: str | None) -> str:
        return open(input_key_path).read()

    def __init__(
            self,
            start_time: int,
            end_time: int,
            area_of_interest: AreaLocation,

    ):
        self.start_time = start_time
        self.end_time = end_time
        self.area_of_interest = area_of_interest





"""
@Misc
{,
  author =    {Planet Labs PBC},
  organization = {Planet},
  title =     {Planet Application Program Interface: In Space for Life on Earth},
  year =      {2018--},
  url = "https://api.planet.com"
}
  """