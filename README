# Calendar Tools

A collection of Python tools used to parse and manipulate ICS calendar files.

## ics-splitter.py

Used to split an ICS file by filtering on a date range.

Example:
`python ics-splitter.py calendar.ics --start-date 2025-01-01 --end-date 2025-12-31`

## ics-reader.py

Used to list all events in an ICS file.

Example:
`python ics-reader.py calendar-filtered.ics --include-datetime --include-location`

## ics-toMarkdown.py

Similar to ics-reader.py, but prints events in a markdown-friendly format.

Example:
`python ics-toMarkdown.py calendar.ics --include-all`

Timestamps are displayed in the local time zone by default, but an IANA time zone can be specified to convert events to a specific time zone:
`python ics-toMarkdown.py calendar.ics --include-all --timezone "America/Chicago"`
