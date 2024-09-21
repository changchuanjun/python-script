import re
import csv
import argparse
import sys

def parse_meme_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    motifs = re.findall(r'MOTIF\s+(\d+).*?width\s+=\s+(\d+).*?Motif \1 sites sorted by position p-value.*?-{80}\n(.*?)\n-{80}', content, re.DOTALL)

    results = []
    for motif_num, width, sites in motifs:
        width = int(width)
        for line in sites.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 3:
                sequence_name = parts[0]
                try:
                    start = int(parts[1])
                    end = start + width - 1
                    results.append([sequence_name, start, end, f"motif{motif_num}"])
                except ValueError:
                    # Skip lines that don't have a valid start position
                    continue

    # Sort results by Sequence name
    results.sort(key=lambda x: x[0])

    return results

def write_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sequence name", "Start", "End", "Motif"])
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Extract motif data from MEME output file.")
    parser.add_argument("input_file", help="Path to the MEME output file")
    parser.add_argument("-o", "--output", default="meme_results.csv", help="Output CSV file name")
    
    args = parser.parse_args()

    try:
        data = parse_meme_file(args.input_file)
        write_csv(data, args.output)
        print(f"Data successfully extracted and saved to {args.output}")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


