
import argparse
from ics import Calendar
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description="Display ICS events in Markdown format")
    parser.add_argument("input_ics", nargs="?", default="calendar.ics",
                        help="Input ICS file (default: calendar.ics)")
    parser.add_argument("--timezone", default="local",
                        help="Input an IANA timezone (default: local)")
    parser.add_argument("--include-datetime", action="store_true",
                        help="Include start and end datetime")
    parser.add_argument("--include-location", action="store_true",
                        help="Include event location")
    parser.add_argument("--include-description", action="store_true",
                        help="Include event description")
    parser.add_argument("--include-all", action="store_true",
                        help="Include all event details (datetime, location, description)")
    return parser.parse_args()

def main():
    opts = parse_arguments()

    # If include-all flag is set, set all relevant flags
    if(opts.include_all):
        opts.include_datetime = True
        opts.include_location = True
        opts.include_description = True

    # Read input ICS file to calendar object
    try:
        with open(opts.input_ics, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())
    except FileNotFoundError:
        raise SystemExit(f"Error: Input file '{opts.input_ics}' not found.")

    # Sort events chronologically
    events = sorted(calendar.events, key=lambda e: e.begin)

    if not events:
        print("No events found in the calendar.")
        return

    # Loop through events and print details
    for idx, event in enumerate(events, 1):

        print(f"{f"\n## {event.name}" if event.name else '## Untitled Event'}\n")

        if opts.include_datetime:
            print(f"  Start: {event.begin.to(opts.timezone).format('YYYY-MM-DD HH:mm')}")
            print(f"  End:   {event.end.to(opts.timezone).format('YYYY-MM-DD HH:mm')}")

        if opts.include_location and event.location:
            print(f"  Location: {event.location}")

        if opts.include_description and event.description:
            print("  Description:")
            for line in event.description.strip().splitlines():
                print(f"  {line}")

if __name__ == "__main__":
    main()
