#!/usr/bin/env python3
import os
import json
import streamlit as st
import pandas as pd
from app import create_srt_from_stt_json

# Set page configuration
st.set_page_config(
    page_title="Sarvam SRT Generator",
    page_icon="🎬",
    layout="wide",
)

# Add some custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        height: 300px;
    }
    .stButton button {
        width: 100%;
    }
    .output-box {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        color: #333333;
        font-family: monospace;
    }
    .speaker-00 {
        color: #1f77b4;
        font-weight: bold;
    }
    .speaker-01 {
        color: #ff7f0e;
        font-weight: bold;
    }
    .speaker-02 {
        color: #2ca02c;
        font-weight: bold;
    }
    .speaker-03 {
        color: #d62728;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Page title and description
    st.title("🎬 Sarvam SRT Generator")
    st.subheader("Create SRT subtitles from Sarvam API diarized transcript responses")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. Upload a JSON file with Sarvam API response **OR**
        2. Paste the JSON content directly
        3. Click "Generate SRT File"
        4. Preview the generated SRT content
        5. Download the SRT file
        """)
        
        st.header("JSON Format")
        st.markdown("""
        ```json
        {
            "request_id": "...",
            "transcript": "...",
            "language_code": "...",
            "diarized_transcript": {
                "entries": [
                    {
                        "transcript": "...",
                        "start_time_seconds": 1.5,
                        "end_time_seconds": 4.2,
                        "speaker_id": "SPEAKER_00"
                    },
                    ...
                ]
            }
        }
        ```
        """)
    
    # Main content area
    input_method = st.radio(
        "Select input method:",
        ["Upload JSON file", "Paste JSON content"]
    )
    
    json_data = None
    file_name = "transcript"
    
    if input_method == "Upload JSON file":
        uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
        if uploaded_file:
            try:
                file_name = os.path.splitext(uploaded_file.name)[0]
                json_data = json.load(uploaded_file)
                st.success("JSON file loaded successfully!")
                
                # Display a preview
                st.subheader("JSON Preview")
                if "request_id" in json_data:
                    st.info(f"Request ID: {json_data['request_id']}")
                if "language_code" in json_data:
                    st.info(f"Language: {json_data['language_code']}")
                
                # Display entries count if available
                if "diarized_transcript" in json_data and "entries" in json_data["diarized_transcript"]:
                    entries = json_data["diarized_transcript"]["entries"]
                    st.info(f"Found {len(entries)} transcript entries")
                    
                    # Display a sample of entries in a table
                    sample_entries = entries[:3]  # Show first 3 entries
                    if sample_entries:
                        df = pd.DataFrame([
                            {
                                "Speaker": entry.get("speaker_id", ""),
                                "Start": entry.get("start_time_seconds", 0),
                                "End": entry.get("end_time_seconds", 0),
                                "Text": entry.get("transcript", "")
                            }
                            for entry in sample_entries
                        ])
                        st.dataframe(df)
                        
                        if len(entries) > 3:
                            st.text(f"... and {len(entries) - 3} more entries")
            except Exception as e:
                st.error(f"Error loading JSON file: {str(e)}")
    else:
        json_text = st.text_area(
            "Paste JSON content here:",
            height=300,
            help="Paste the Sarvam API response JSON content here"
        )
        if json_text:
            try:
                json_data = json.loads(json_text)
                st.success("JSON content parsed successfully!")
                
                # Get request ID for file naming if available
                if "request_id" in json_data:
                    file_name = json_data["request_id"]
            except Exception as e:
                st.error(f"Error parsing JSON: {str(e)}")
    
    # Output file name input
    output_file_name = st.text_input("Output SRT file name:", value=f"{file_name}.srt")
    
    # Process button
    if st.button("Generate SRT File", type="primary"):
        if not json_data:
            st.error("Please provide JSON data first!")
        else:
            try:
                # Create output path
                output_path = os.path.join(output_dir, output_file_name)
                
                # Generate SRT file
                with st.spinner("Generating SRT file..."):
                    srt_file = create_srt_from_stt_json(json_data, output_path)
                
                st.success(f"SRT file created successfully!")
                
                # Read and display the SRT content
                with open(srt_file, "r", encoding="utf-8") as f:
                    srt_content = f.read()
                
                st.subheader("SRT File Preview")
                
                # Create a formatted preview with syntax highlighting for speakers
                formatted_lines = []
                for line in srt_content.split("\n"):
                    if line.startswith("[SPEAKER_"):
                        speaker = line[1:10]  # Extract SPEAKER_XX
                        speaker_class = speaker.lower().replace("_", "-")
                        text = line[12:]  # Get text after ]: 
                        formatted_lines.append(f'<span class="{speaker_class}">{speaker}</span>: {text}')
                    else:
                        formatted_lines.append(line)
                
                formatted_srt = "<br>".join(formatted_lines)
                
                # Display in a container with styling
                st.markdown('<div class="output-box">' + formatted_srt + '</div>', unsafe_allow_html=True)
                
                # Download button
                with open(srt_file, "r", encoding="utf-8") as f:
                    srt_bytes = f.read().encode()
                    
                st.download_button(
                    label="Download SRT File",
                    data=srt_bytes,
                    file_name=os.path.basename(srt_file),
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"Error generating SRT file: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("Sarvam SRT Generator | Created with Streamlit")

if __name__ == "__main__":
    main() 