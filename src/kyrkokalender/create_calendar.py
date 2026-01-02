import json
import sys
import tempfile
from http.client import responses
from pathlib import Path

import httpx
import rich_click as click

from kyrkokalender import church_calendar

API_URL = "https://www.svenskakyrkan.se/webapi/api-v2/churchcalendar/{}?apiKey={}"


@click.command()
@click.argument("year", type=int, help="The year (counted from Advent Sunday) to create.")
@click.option("-r", "--reload", is_flag=True, help="Force new download of calender data.")
@click.option("--api-key", type=str, default=None, help="The API key to use.")
@click.option(
    "--api-key-path",
    type=click.Path(path_type=Path),
    default=Path(".api_key"),
    help="File containing The API key to use.",
)
def cli(year: int, reload: bool, api_key: str | None, api_key_path: Path) -> None:
    tmp_dir = Path(tempfile.gettempdir())
    cached_response_path = tmp_dir / f"kyrkokalender/{year}_response.json"
    if not cached_response_path.exists() or reload:
        if api_key or (api_key_path and api_key_path.exists()):
            api_key = api_key or api_key_path.read_text()
        else:
            sys.exit(
                "API key not provided. Add it with --api-key or --api-key-path. If your"
                "current directory has a file named .api_key, it will be used"
                "automatically."
            )

        url = API_URL.format(year, api_key)
        print("Fetching calendar data...")
        try:
            api_response = httpx.get(url)
            api_response.raise_for_status()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            print(f"Error from server: {status_code} ({responses[status_code]})")
            match status_code:
                case 404 | 416:
                    print("Check year.")
                case 401:
                    print("Check API key.")
                case _:
                    print("Unknown error")
            sys.exit()

        calendar_data = api_response.json()
        cached_response_path.parent.mkdir(parents=True, exist_ok=True)
        with cached_response_path.open("w") as cache_file:
            json.dump(calendar_data, cache_file, indent=4)
    else:
        print("Opening cached response...")
        calendar_data = json.loads(cached_response_path.read_text())

    calendar = church_calendar.calendar_for_feasts(year, calendar_data)
    ics_path = Path(f"kyrkoåret_{year}.ics")
    print(f"Calendar created with {len(calendar.events)} feasts.")
    print(f"Writing ICS file to {ics_path.absolute()}")
    ics_path.write_bytes(calendar.to_ical())


if __name__ == "__main__":
    cli()
