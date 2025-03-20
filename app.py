#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("srt_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_remainder = seconds % 60
    milliseconds = int((seconds_remainder % 1) * 1000)
    seconds_int = int(seconds_remainder)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"

def create_srt_from_stt_json(json_data, output_path=None):
    """
    Create an SRT subtitle file from the diarized transcript in STT JSON output.
    
    Args:
        json_data (dict or str): The JSON data from STT output, either as a dict or JSON string
        output_path (str, optional): Path to save the SRT file. If None, a default path will be used.
        
    Returns:
        str: Path to the generated SRT file
    """
    # Parse JSON if it's a string
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError as e:
            error_msg = f"Error parsing JSON: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    # Check if the expected structure exists
    if 'diarized_transcript' not in json_data or 'entries' not in json_data['diarized_transcript']:
        error_msg = "Invalid JSON format: 'diarized_transcript' or 'entries' not found"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Extract transcript entries
    entries = json_data['diarized_transcript']['entries']
    
    # Create a default output path if not specified
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        request_id = json_data.get('request_id', 'transcript')
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{request_id}_{timestamp}.srt")
    else:
        # Make sure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Write SRT file
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, entry in enumerate(entries, 1):
            start_time = format_timestamp(entry['start_time_seconds'])
            end_time = format_timestamp(entry['end_time_seconds'])
            
            # Format text with speaker label if available
            speaker_id = entry.get('speaker_id', '')
            text = entry.get('transcript', '')
            
            if speaker_id:
                formatted_text = f"[{speaker_id}]: {text}"
            else:
                formatted_text = text
            
            # Write SRT format
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{formatted_text}\n\n")
    
    logger.info(f"✅ SRT file created at {output_path}")
    print(f"✅ SRT file created at {output_path}")
    return output_path

def create_srt_from_stt_json_file(json_file_path, output_path=None):
    """
    Create an SRT subtitle file from a JSON file containing STT output.
    
    Args:
        json_file_path (str): Path to the JSON file with STT output
        output_path (str, optional): Path to save the SRT file. If None, a default path will be used.
        
    Returns:
        str: Path to the generated SRT file
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        return create_srt_from_stt_json(json_data, output_path)
    except Exception as e:
        error_msg = f"Error processing JSON file {json_file_path}: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        raise

def extract_audio(video_path, output_path):
    """Extract audio from video using ffmpeg"""
    try:
        import subprocess
        command = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit encoding
            '-ar', '16000',  # 16kHz sampling rate
            '-ac', '1',  # Mono channel
            output_path
        ]
        print(f"📊 Extracting audio with command: {' '.join(command)}")
        subprocess.run(command, check=True, capture_output=True)
        print(f"✅ Audio extraction completed: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting audio: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ ffmpeg not found. Please install ffmpeg to process video files.")
        return False

# Define the public API
__all__ = ['create_srt_from_stt_json', 'create_srt_from_stt_json_file', 'extract_audio']

# Example usage
if __name__ == "__main__":
    # Sample data (similar to the example provided)
    sample_data = json.load(open('data/0.json'))
    
    # Create an SRT file from the sample data
    srt_file = create_srt_from_stt_json(sample_data)
    print(f"Example SRT file created at: {srt_file}")
