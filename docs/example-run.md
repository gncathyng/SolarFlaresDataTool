# Example Run
This example shows how the CLI tool work when extracting solar event data.

## Input
Command:
```bash
python cli.py```

User input:
```2015```

## Process
The script:
* connects to the NOAA SWPC FTP archive
* downloads all event files for the selected year
* parses event records into structured fields
* aggregates all events into a single dataset

## Output
Example console output:
```
Found 365 files for 2015.

[1/365] Downloading 20150101events.txt...
Parsing 20150101events.txt...

...

Done.
Saved raw files in: raw_2015/
Saved CSV: solar_events_2015.csv
Total events extracted: 12000

Event counts by type:
XRA: 350
FLA: 500
RSP: 200
```

## Notes
* The number of files depends on the year
* Event counts vary based on solar activity
* Output CSV can be used for further analysis or future API queries
