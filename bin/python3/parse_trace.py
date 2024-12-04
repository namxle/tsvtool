import csv
import re
import sys
import argparse


def seconds_to_time(total_seconds):
    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Build the time string
    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours}h")
    if minutes > 0:
        time_parts.append(f"{minutes}m")
    if seconds > 0 or not time_parts:  # Always include seconds if no other parts
        time_parts.append(f"{seconds}s")

    return " ".join(time_parts)


def time_to_seconds(time_str):
    # Match time components (e.g., 1h, 10m, 20s)
    pattern = r"(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?"
    match = re.match(pattern, time_str.strip())

    if not match:
        raise ValueError(f"Invalid time format: {time_str}")

    # Extract hours, minutes, and seconds (default to 0 if not present)
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    # Convert to total seconds
    return hours * 3600 + minutes * 60 + seconds


# Examples
# print(time_to_seconds("1m 60s"))  # Output: 620
# print(time_to_seconds("1h 10m 20s"))  # Output: 4220
# print(seconds_to_time(620))  # Output: "10m 20s"
# print(seconds_to_time(4220))  # Output: "1h 10m 20s"


def run(input, output):
    # Calculate timeline
    timeline = {
        "mapping": 0,
        "sorting": 0,
        "mark_duplicates": 0,  # = METRICS_CALCULATION + REMOVE_DUPLICATE_READS
        "BQSR": 0,  # = FILTER_MQ + BQSR
        "indel_realigner": 0,  # = FILTER_MQ + INDEL_REALIGNER
        "variant_calling": 0,  # = VARIANT_CALLING + VQSR
        "MT": 0,
        "CNV": 0,
        "SV": 0,
        "QC": 0,
        "STR": 0,
        "total": 0,
    }

    text_mapping = {
        "mapping": "Mapping reads",
        "sorting": "Sorting bam",
        "mark_duplicates": "Mark duplicate reads",
        "BQSR": "BQSR",
        "indel_realigner": "Indel realigner",
        "variant_calling": "Variant calling + VQSR",
        "MT": "Variant MT calling",
        "CNV": "CNV calling",
        "SV": "SV calling",
        "QC": "QC",
        "STR": "STR",
        "total": "Total time",
    }

    # Open the file and read it
    with open(input, mode="r", newline="", encoding="utf-8") as file:
        # Use csv.DictReader to parse the TSV file with the first line as headers
        tsv_reader = csv.DictReader(file, delimiter="\t")

        # Convert the data into a list of dictionaries
        data = [row for row in tsv_reader if row["status"] == "COMPLETED"]

    # Process data
    for datum in data:
        name = datum["name"]
        rt = time_to_seconds(datum["realtime"])
        if "MAPPING_READS" in name:
            timeline["mapping"] = rt

        if "SORTING_BAM" in name:
            timeline["sorting"] = rt

        if "METRICS_CALCULATION" in name or "REMOVE_DUPLICATE_READS" in name:
            timeline["mark_duplicates"] += rt

        if "BQSR_STAGE_1" in name or "FILTER_MQ" in name:
            timeline["BQSR"] += rt

        if "INDEL_REALIGNER" in name or "FILTER_MQ" in name:
            timeline["indel_realigner"] += rt

        if "VARIANT_HC_CALLING" in name or "VQSR" in name:
            timeline["variant_calling"] += rt

        if "VARIANT_MT_CALLING" in name:
            timeline["MT"] = rt

        if "DELLY_CNV" in name:
            timeline["CNV"] = rt

        if "DELLY_SV" in name:
            timeline["SV"] = rt

        if "STR" in name:
            timeline["STR"] = rt

        if "WGS_QC" in name:
            timeline["QC"] = rt

    timeline["total"] = sum(
        [
            timeline["mapping"],
            timeline["sorting"],
            timeline["mark_duplicates"],
            max(
                (timeline["indel_realigner"] + timeline["QC"]),
                (
                    max(timeline["indel_realigner"], timeline["BQSR"])
                    + timeline["variant_calling"]
                ),
            ),
        ]
    )

    with open(output, "w", encoding="utf-8") as file:
        for key, value in timeline.items():
            text = f"{text_mapping[key]}: {seconds_to_time(value)}\n"
            file.write(text)


# Create the parser
parser = argparse.ArgumentParser(description="Trace parsing script")

# Add arguments
parser.add_argument("-i", "--input", type=str, required=True, help="Input")
parser.add_argument("-o", "--output", type=str, required=True, help="Output")

# Parse the arguments
args = parser.parse_args()

run(input=args.input, output=args.output)
