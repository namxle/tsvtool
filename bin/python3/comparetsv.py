#!/home/user/anaconda3/bin/python3.11

import argparse
import logging
import os
import time

mode = "exact"


@staticmethod
def get_data_dict(fields, line):
    line_data = line.split("\t")
    data = {}

    for i in range(len(fields)):
        data[fields[i]] = line_data[i]

    return data


@staticmethod
def parse_file(f):
    header_passed = False
    results = []
    fields = []
    with open(f) as file:
        for line in file:
            line = line.strip()
            if not header_passed:
                fields = line.split("\t")
                print(fields)
                header_passed = True
                continue

            dict = get_data_dict(fields=fields, line=line)
            results.append(dict)
    return results, fields


def run(file_a, file_b, key_column):
    global mode
    a_records, a_fields = parse_file(file_a)
    b_records, b_fields = parse_file(file_b)

    a_key_index = a_fields.index(key_column)
    b_key_index = a_fields.index(key_column)

    if len(a_records) != len(b_records) and mode == "exact":
        print("Different in length")
        exit(1)

    # Check fields
    fields_not_exist_in_a = [field for field in b_fields if field not in a_fields]
    fields_not_exist_in_b = [field for field in a_fields if field not in b_fields]

    print("Fields not exist in a:", str(fields_not_exist_in_a))
    print("Fields not exist in b:", str(fields_not_exist_in_b))

    # Check value
    for i in range(len(a_records)):
        for field in a_fields:
            if mode == "exact":
                if a_records[i][field] != b_records[i][field]:
                    print(
                        f"Different at index {i}, ID {a_records[i][a_fields[a_key_index]]}: {field}"
                    )
            else:
                if field not in b_records[i]:
                    pass
                else:
                    if a_records[i][field] != b_records[i][field]:
                        print(
                            f"Different at index {i}, ID {a_records[i][a_fields[a_key_index]]}: {field}"
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Compare fields of 2 TSV files and print the different"""
    )
    parser.add_argument(
        "-a",
        "--file-a",
        dest="file_a",
        type=str,
        help="First tsv file to be compared",
        required=True,
    )
    parser.add_argument(
        "-b",
        "--file-b",
        dest="file_b",
        type=str,
        help="Secodn tsv file to be compared",
        required=True,
    )
    parser.add_argument(
        "-k",
        "--key-column",
        dest="key_column",
        type=str,
        help="The key column number.",
        required=True,
        default=1,
    )
    parser.add_argument(
        "-m",
        "--mode",
        dest="mode",
        type=str,
        help="Compare mode. Can be exact or normal.",
        required=True,
        default="exact",
    )

    args = parser.parse_args()

    mode = args.mode

    run(file_a=args.file_a, file_b=args.file_b, key_column=args.key_column)
