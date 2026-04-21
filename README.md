# SolarFlaresDataTool

A Python command-line tool for downloading NOAA SWPC daily solar event files for a selected year, parsing the event records, and exporting the results to a CSV file.

## Overview

This project connects to the NOAA Space Weather Prediction Center (SWPC) FTP archive, downloads all daily event files for a chosen year, extracts structured solar event data, and saves the results in CSV format for further analysis.

The tool also prints a summary of event counts by type after processing all files.

## Features

- Connects to the NOAA SWPC FTP archive
- Downloads daily event files for a selected year
- Parses event records into structured fields
- Exports results to a CSV file
- Prints a summary of event counts by type

## Data Source

NOAA Space Weather Prediction Center (SWPC)  
FTP archive: `ftp.swpc.noaa.gov/pub/indices/events`

## Requirements

- Python 3.x
- Standard library only (`ftplib`, `os`, `re`, `csv`)

## How to Run

Run the script from the project folder:

```bash
python cli.py
```
Then eneter a yeear when prompted, for example: 2015

Output

The script creates:

* a folder containing the downloaded raw event files (e.g., raw_2015/)
* a CSV file containing parsed event data (e.g., solar_events_2015.csv)

Project Structure
SolarFlaresDataTool/
├── cli.py
├── README.md

Notes

This project is a lightweight research tool for processing archived solar event data.
SolarFlaresDataTool

A Python command-line tool for downloading NOAA SWPC daily solar event files for a selected year, parsing the event records, and exporting the results to a CSV file.

Overview

This project connects to the NOAA Space Weather Prediction Center (SWPC) FTP archive, downloads all daily event files for a chosen year, extracts structured solar event data, and saves the results in CSV format for further analysis.

The tool also prints a summary of event counts by type after processing all files.

Features

* Connects to the NOAA SWPC FTP archive
* Downloads daily event files for a selected year
* Parses event records into structured fields
* Exports results to a CSV file
* Prints a summary of event counts by type

Data Source

NOAA Space Weather Prediction Center (SWPC)
FTP archive: ftp.swpc.noaa.gov/pub/indices/events

Requirements

* Python 3.x
* Standard library only (ftplib, os, re, csv)

How to Run

Run the script from the project folder:

python cli.py

Then enter a year when prompted, for example:

2015

Output

The script creates:

* a folder containing the downloaded raw event files (e.g., raw_2015/)
* a CSV file containing parsed event data (e.g., solar_events_2015.csv)

Project Structure

SolarFlaresDataTool/
├── cli.py
├── README.md

Notes

This project is a lightweight research tool for processing archived solar event data.
