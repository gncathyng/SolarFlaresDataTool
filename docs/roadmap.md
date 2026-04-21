# Project Roadmap

## Current Version (v1)
- CLI tool to download NOAA SWPC event files
- Parses raw event text into structured data
- Exports cleaned data to CSV
- Provides summary statistics (event counts)

## Short-Term Improvements
- Add command-line arguments
- Allow filtering by event type
- Improve parsing robustness for edge cases
- Add more test coverage for parsing functions

## Medium-Term Goals
- Refactor code into modules:
  - `ftp_utils.py` (data fetching)
  - `parser.py` (event parsing)
  - `export.py` (CSV output)
- Improve performance for large datasets
- Add logging instead of print statements

## Long-Term Goal (API + Interface)

### API Layer
- Buid API
- Example endpoints:
  - `/events?year=2015`
  - `/events?type=XRA`
  - `/summary?year=2015`
- Return structured JSON instead of CSV

### Interface/Frontent
- Build an interactive interface for querying solar event data
- Allow users to: 
  - Search by event type, date range, peak time, GOES class and region
  - View summaries (counts, most common event type)
  - Explore returned records in a table format

- Possible tools:
  - Streamlit (quick prototype)
  - React + FastAPI (full web app)

## Concept Note
The final system will resemble an interactive solar event retrieval interface, where users can
query standardized SWPC event records.
The current CLI tool serves as the data processing backbone for this future system.

## Vision
Transform this project from a command-line data pipeline into a full data platform with:
- a structured API
- an interactive interface
- real-time querying capabilities for solar event data
