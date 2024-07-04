import pandas as pd
import argparse


@staticmethod
def run(input, output):
    # Read the TSV file
    df = pd.read_csv(input, sep="\t")

    # Write the DataFrame to an Excel file
    df.to_excel(output, index=False, engine="openpyxl")

    print(f"TSV file '{input}' has been converted to Excel file '{output}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""TSV to Excel""")
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        help="TSV input file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        help="XLSX output file",
        required=True,
    )

    args = parser.parse_args()

    run(input=args.input, output=args.output)
