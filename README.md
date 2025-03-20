# SRT Generator for Sarvam API

This tool creates SRT subtitle files from Sarvam Speech-to-Text API responses with diarized transcript data.

## Features

- Converts Sarvam API diarized transcript responses to standard SRT subtitle files
- Preserves speaker information in the subtitles
- Maintains accurate timestamps
- Multiple ways to input API response data
- Interactive web UI using Streamlit

## Streamlit Web Interface

The easiest way to use this tool is through the Streamlit web interface:

```bash
pip install streamlit pandas
streamlit run streamlit_app.py
```

This will launch a local web server and open the SRT Generator in your browser. With the web interface you can:

- Upload JSON files with API responses
- Paste JSON content directly
- Preview the generated SRT files
- Download SRT files with a single click
- See color-coded speaker labels

![Streamlit Interface](https://i.imgur.com/YWYfDaA.png)

## Command-line Usage

You can also use the command-line interface:

1. **Provide a JSON file:**
   ```
   python create_srt_from_response.py --json-file path/to/api_response.json --output output/subtitles.srt
   ```

2. **Provide a JSON string directly:**
   ```
   python create_srt_from_response.py --json-string '{"request_id":"123","diarized_transcript":{"entries":[...]}}'
   ```

3. **Pipe JSON data:**
   ```
   cat api_response.json | python create_srt_from_response.py
   ```

4. **Interactive input:**
   ```
   python create_srt_from_response.py
   ```
   Then paste your JSON data and press Ctrl+D when finished.

## Using in Your Code

```python
from app import create_srt_from_stt_json

# Your API response as a dictionary or JSON string
api_response = {
    "request_id": "20250320_3a2f210f-4291-416b-89e5-d6dee1f5a5ef",
    "transcript": "transcript_here.",
    "language_code": "en-IN",
    "diarized_transcript": {
        "entries": [
            {
                "transcript": "transcript_here",
                "start_time_seconds": 13.96,
                "end_time_seconds": 29.98,
                "speaker_id": "SPEAKER_00"
            },
            # More entries...
        ]
    }
}

# Create an SRT file
srt_file_path = create_srt_from_stt_json(api_response, "output/my_subtitles.srt")
print(f"SRT file created at: {srt_file_path}")
```

## Required JSON Format

The script expects Sarvam API responses in this format:

```json
{
    "request_id": "20250320_3a2f210f-4291-416b-89e5-d6dee1f5a5ef",
    "transcript": "transcript_here.",
    "language_code": "en-IN",
    "diarized_transcript": {
        "entries": [
            {
                "transcript": "transcript_here",
                "start_time_seconds": 13.96,
                "end_time_seconds": 29.98,
                "speaker_id": "SPEAKER_00"
            },
            {
                "transcript": "transcript_here",
                "start_time_seconds": 30.25,
                "end_time_seconds": 44.41,
                "speaker_id": "SPEAKER_00"
            }
        ]
    }
}
```

## Example

Create an SRT file from an example API response:

```bash
# Save this to a file named example.json
cat > example.json << 'EOL'
{
    "request_id": "20250320_3a2f210f-4291-416b-89e5-d6dee1f5a5ef",
    "transcript": "transcript_here.",
    "language_code": "en-IN",
    "diarized_transcript": {
        "entries": [
            {
                "transcript": "Hello, this is speaker zero.",
                "start_time_seconds": 1.5,
                "end_time_seconds": 4.2,
                "speaker_id": "SPEAKER_00"
            },
            {
                "transcript": "And this is speaker one responding.",
                "start_time_seconds": 4.8,
                "end_time_seconds": 7.3,
                "speaker_id": "SPEAKER_01"
            }
        ]
    }
}
EOL

# Generate the SRT file
python create_srt_from_response.py --json-file example.json --output example.srt

# View the result
cat example.srt
```

The resulting SRT file will look like:

```
1
00:00:01,500 --> 00:00:04,200
[SPEAKER_00]: Hello, this is speaker zero.

2
00:00:04,800 --> 00:00:07,300
[SPEAKER_01]: And this is speaker one responding.
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```

3. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ``` 