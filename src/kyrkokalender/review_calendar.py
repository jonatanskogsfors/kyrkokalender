from pathlib import Path

import icalendar
import rich_click as click
from rich.console import Console
from rich.table import Table


@click.command()
@click.argument(
    "calendar_path",
    type=click.Path(exists=True, path_type=Path),
    help="The path to the calendar file.",
)
def cli(calendar_path: Path) -> None:
    calendar = icalendar.Calendar.from_ical(calendar_path.read_bytes())

    summary_table = Table(show_header=False)

    summary_table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    summary_table.add_column("Value", style="magenta")
    summary_table.add_row("Feasts", str(len(calendar.events)))
    first_feast = calendar.events[0]
    summary_table.add_row(
        "First", f"{first_feast['summary']} ({first_feast['dtstart'].dt})"
    )
    last_feast = calendar.events[-1]
    summary_table.add_row("Last", f"{last_feast['summary']} ({last_feast['dtstart'].dt})")

    console = Console()
    console.print(summary_table)

    full_table = Table()
    full_table.add_column("Sunday", justify="left", style="cyan", no_wrap=True)
    full_table.add_column("Date", justify="left", style="magenta", no_wrap=True)

    current_month = first_feast["dtstart"].dt.month
    for feast in calendar.events:
        if current_month != feast["dtstart"].dt.month:
            current_month = feast["dtstart"].dt.month
            full_table.add_section()
        full_table.add_row(feast["summary"], f"{feast['dtstart'].dt}")

    console.print(full_table)


if __name__ == "__main__":
    cli()
