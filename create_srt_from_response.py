#!/usr/bin/env python3
import os
import json
import sys
import argparse
from app import create_srt_from_stt_json, create_srt_from_stt_json_file

def main():
    """
    Create SRT file from Sarvam API diarized transcript response.
    The script can accept input in multiple ways:
    1. Directly from a JSON file
    2. From standard input (piped input)
    3. From command-line arguments
    """
    parser = argparse.ArgumentParser(description='Create SRT file from Sarvam API diarized transcript')
    parser.add_argument('--json-file', help='Path to JSON file containing API response')
    parser.add_argument('--json-string', help='JSON string of API response')
    parser.add_argument('--output', help='Output path for the SRT file')
    
    args = parser.parse_args()
    
    # Initialize output path
    output_path = args.output
    
    # Process based on input method
    if args.json_file:
        # Process from JSON file
        print(f"Reading API response from file: {args.json_file}")
        srt_path = create_srt_from_stt_json_file(args.json_file, output_path)
        print(f"✅ SRT file created at: {srt_path}")
        return
    
    elif args.json_string:
        # Process from JSON string provided as argument
        print("Processing API response from command line argument")
        json_data = args.json_string
    
    elif not sys.stdin.isatty():
        # Process from piped stdin
        print("Reading API response from standard input...")
        json_data = sys.stdin.read().strip()
    
    else:
        # If no input provided, prompt the user
        print("Please paste the API response JSON below (press Ctrl+D when done):")
        json_data = sys.stdin.read().strip()
        
    if not json_data:
        print("❌ Error: No JSON data provided")
        parser.print_help()
        return
    
    try:
        # Process the JSON data and create SRT file
        srt_path = create_srt_from_stt_json(json_data, output_path)
        print(f"✅ SRT file created at: {srt_path}")
        
        # Display a preview of the generated SRT file
        print("\nSRT file content preview:")
        print("-" * 50)
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            preview_lines = 15  # Show first 15 lines or fewer
            for line in lines[:preview_lines]:
                print(line.rstrip())
            
            if len(lines) > preview_lines:
                print("...")
                
                # Try to determine the number of entries
                json_obj = json.loads(json_data) if isinstance(json_data, str) else json_data
                if 'diarized_transcript' in json_obj and 'entries' in json_obj['diarized_transcript']:
                    print(f"Total entries: {len(json_obj['diarized_transcript']['entries'])}")
                else:
                    print(f"Total lines: {len(lines)}")
        
    except Exception as e:
        print(f"❌ Error processing JSON data: {str(e)}")
        return

if __name__ == "__main__":
    main() 