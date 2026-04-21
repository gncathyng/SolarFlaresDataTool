"""
CLI tool for downloading NOAA SWPC daily solar event files for a selected year, parsing
the event records, and exporting the results to a CSV file.

This script connects to the NOAA FTP archive: ftp://ftp.swpc.noaa.gov/pub/indices/events, downloads
all event files for the requested year, extracts structured event data, and prints a summary of 
event counts by type.
"""

from ftplib import FTP
import os
import re
import csv

FTP_HOST = "ftp.swpc.noaa.gov"
FTP_DIR = "/pub/indices/events"

# Connect to the NOAA SWPC FTP server and move into the events directory
def connect_ftp():
    ftp = FTP(FTP_HOST)
    ftp.login()
    ftp.cwd(FTP_DIR)
    return ftp

# Return all event filenames for the selected year from the FTP directory
def list_year_files(ftp, year):
    pattern = re.compile(rf"^{year}\d{{4}}events\.txt$")
    files = ftp.nlst()
    return sorted([f for f in files if pattern.match(f)])

# Download one event file from the FTP server into the local raw data folder
def download_file(ftp, filename, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    local_path = os.path.join(save_dir, filename)

    with open(local_path, "w", encoding="utf-8") as f:
        ftp.retrlines(f"RETR {filename}", lambda line: f.write(line + "\n"))

    return local_path

# Convert raw time strings into HH:MM format and handle missing values
def normalize_time(t):
    t = t.strip()
    if not t or t == "////":
        return ""
    if len(t) == 4 and t.isdigit():
        return f"{t[:2]}:{t[2:]}"
    return t

# Check whether a split line has the basic structure of a valid event record
def looks_like_event_line(parts):
    if len(parts) < 5:
        return False
    if not parts[0].isdigit():
        return False
    if not parts[1].isalpha():
        return False
    return True

# Parse one event line into a structured dictionary of event fields
def parse_event_line(line, current_date, source_file):
    parts = line.split()

    if not looks_like_event_line(parts):
        return None

    event_number = parts[0]
    event_type = parts[1]

    start_time = normalize_time(parts[2]) if len(parts) > 2 else ""
    peak_time = normalize_time(parts[3]) if len(parts) > 3 else ""
    end_time = normalize_time(parts[4]) if len(parts) > 4 else ""

    region = ""
    position = ""
    importance = ""
    goes_class = ""

    # Remaining tokens may contain optional metadata such as position, GOES class, and region
    extra_tokens = parts[5:] if len(parts) > 5 else []

    # Extract heliographic position
    for token in extra_tokens:
        if re.fullmatch(r"[NS]\d{2,3}[EW]\d{2,3}", token):
            position = token
            break

    # Extract GOES flare class
    for token in extra_tokens:
        if re.fullmatch(r"[BCMX]\d+(\.\d+)?", token):
            goes_class = token
            break

    # Extract active region number when present
    for token in extra_tokens:
        if token.isdigit() and len(token) >= 3:
            region = token
            break

    # Extract importance code if present
    for token in extra_tokens:
        if re.fullmatch(r"[1-4][BFN]?", token) or re.fullmatch(r"[SF]\w*", token):
            importance = token
            break

    return {
        "date": current_date,
        "event_number": event_number,
        "event_type": event_type,
        "start_time": start_time,
        "peak_time": peak_time,
        "end_time": end_time,
        "importance": importance,
        "goes_class": goes_class,
        "position": position,
        "region": region,
        "extra_data": " ".join(extra_tokens),
        "source_file": source_file,
        "raw_line": line.strip(),
    }

# Read one downloaded event file and extract all event records from
def parse_file(filepath):
    events = []
    current_date = ""

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

	    # Capture the date header so each event can be assigned to the correct day
            if line.startswith(":Date:"):
                parts = line.split()
                if len(parts) >= 4:
                    year = parts[1]
                    month = parts[2].zfill(2)
                    day = parts[3].zfill(2)
                    current_date = f"{year}-{month}-{day}"
                continue

	    # Skip lines until a valid date header has been found
            if not current_date:
                continue

            event = parse_event_line(line, current_date, os.path.basename(filepath))
            if event:
                events.append(event)

    return events

# Write the parse event records to a CSV file with consistent column names
def write_csv(events, output_csv):
    fieldnames = [
        "date",
        "event_number",
        "event_type",
        "start_time",
        "peak_time",
        "end_time",
        "importance",
        "goes_class",
        "position",
        "region",
        "extra_data",
        "source_file",
        "raw_line",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

# Run the full workflow in main: download files, parse events, export CSV, and print a summary
def main():
    year = input("Enter year (example: 2015): ").strip()
    raw_dir = f"raw_{year}"
    output_csv = f"solar_events_{year}.csv"

    ftp = connect_ftp()
    try:
        year_files = list_year_files(ftp, year)

        if not year_files:
            print(f"No files found for year {year}.")
            return

        print(f"Found {len(year_files)} files for {year}.")

        all_events = []

        for i, filename in enumerate(year_files, start=1):
            print(f"[{i}/{len(year_files)}] Downloading {filename}...")
            local_path = download_file(ftp, filename, raw_dir)

            print(f"Parsing {filename}...")
            events = parse_file(local_path)
            all_events.extend(events)

        write_csv(all_events, output_csv)

        print("\nDone.")
        print(f"Saved raw files in: {raw_dir}/")
        print(f"Saved CSV: {output_csv}")
        print(f"Total events extracted: {len(all_events)}")

	# Count how many events were found for each event type
        event_counts = {}
        for event in all_events:
            etype = event["event_type"]
            event_counts[etype] = event_counts.get(etype, 0) + 1

        print("\nEvent counts by type:")
        for etype, count in sorted(event_counts.items()):
            print(f"{etype}: {count}")

    finally:
        ftp.quit()


if __name__ == "__main__":
    main()

