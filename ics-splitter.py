import argparse
from datetime import datetime, timedelta
from ics import Calendar, Event

# Parse arguements
def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter ICS events by date range")
    parser.add_argument(
        "input_ics",
        nargs="?",
        default="calendar.ics",
        help="Input ICS file (default: calendar.ics)"
    )
    parser.add_argument(
        "output_ics",
        nargs="?",
        default="calendar-filtered.ics",
        help="Output ICS file (default: calendar-filtered.ics)"
    )
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    return parser.parse_args()


def main():
    opts = parse_arguments()

    # Start date at time 00:00
    start_date = datetime.strptime(opts.start_date, "%Y-%m-%d")

    # End date with 1 day added to be inclusive of the whole day.
    end_date = datetime.strptime(opts.end_date, "%Y-%m-%d") + timedelta(days=1) 

    if end_date <= start_date:
        raise SystemExit("Error: --end-date must be the same or after --start-date.")
    
    print(f"Window: [{start_date} .. {end_date}]")

    # Read input ICS file to calendar object
    try:
        with open(opts.input_ics, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())
    except FileNotFoundError:
        raise SystemExit(f"Error: Input file '{opts.input_ics}' not found.")

    # Initiailize new calendar object and counters
    filtered = Calendar()
    kept = 0
    total = 0

    # Loop through all events in the input ICS file
    for event in calendar.events:
        total += 1
        
        # Normalize to local time
        event_start = event.begin.to('local').naive
        event_end = event.end.to('local').naive

        # Keep events that intersect start_date and end_date
        if (event_end > start_date) and (event_start < end_date):
            filtered.events.add(event)
            kept += 1

    # Write output ICS file
    with open(opts.output_ics, "w", encoding="utf-8") as out:
        out.writelines(filtered.serialize_iter())

    print(f"Filtered {kept}/{total} events into {opts.output_ics}")
    

if __name__ == "__main__":
    main()