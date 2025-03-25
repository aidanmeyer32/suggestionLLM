import json
import logging
from pathlib import Path
from typing import Dict
import os
from dotenv import load_dotenv

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('json_validation.log'),
            logging.StreamHandler()
        ]
    )

def validate_and_fix_jsonl(input_file: str, output_file: str) -> Dict[str, int]:
    """Validate and fix JSONL file with detailed statistics"""
    stats = {
        "total_lines": 0,
        "valid_lines": 0,
        "fixed_lines": 0,
        "failed_lines": 0
    }
    
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file '{input_file}' does not exist")
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            for line_num, line in enumerate(infile, 1):
                stats["total_lines"] += 1
                line = line.strip()
                
                if not line:  # Skip empty lines
                    continue
                
                try:
                    # Attempt to parse the line as JSON
                    json_obj = json.loads(line)
                    
                    # Ensure the JSON object is in the correct format
                    if isinstance(json_obj, dict) and "messages" in json_obj:
                        # Write the valid JSON object to the output file
                        outfile.write(json.dumps(json_obj) + '\n')
                        stats["valid_lines"] += 1
                    else:
                        logging.warning(f"Line {line_num} is not in the expected format: {line[:100]}...")
                        stats["failed_lines"] += 1
                    
                except json.JSONDecodeError:
                    logging.warning(f"Invalid JSON on line {line_num}: {line[:100]}...")
                    stats["failed_lines"] += 1
                
                if line_num % 1000 == 0:
                    logging.info(f"Processed {line_num} lines...")
        
        logging.info("Validation complete. Statistics:")
        for key, value in stats.items():
            logging.info(f"{key}: {value}")
        
        return stats
    
    except Exception as e:
        logging.error(f"Critical error during validation: {str(e)}")
        raise

if __name__ == "__main__":
    setup_logging()
    
    try:
        input_file = "merged-final-dataset.jsonl"
        output_file = "validated-final-datasetj-2.jsonl"
        
        stats = validate_and_fix_jsonl(input_file, output_file)
        logging.info("Process completed successfully")
        
    except Exception as e:
        logging.error(f"Program terminated with error: {str(e)}")
