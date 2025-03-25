#this script will merge the separate JSONL files into one single file. 

import os

def merge_jsonl_files(input_directory, output_file):
    # Open the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate through all files in the input directory
        for filename in os.listdir(input_directory):
            if filename.endswith(".jsonl"):
                file_path = os.path.join(input_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Write each line from the input file to the output file
                    for line in file:
                        outfile.write(line)
    
    print(f"All files have been concatenated into {output_file}")

# Main execution block
if __name__ == "__main__":
    input_directory = "jsonl-files"  # Directory containing JSONL files
    output_file = "merged-final-dataset"  # Output JSONL file
    merge_jsonl_files(input_directory, output_file)
