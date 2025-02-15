# Speech-to-Text Chrome Extension
<p align="center">
<img src="https://github.com/user-attachments/assets/6b32aa5e-cc04-4528-bcd6-1428d125b5c3" alt="Description" width="200">
</p>

## Overview
This Chrome extension allows users to record their voice while interacting with a webpage. It captures spoken words along with user actions on the page and generates logs in both text and JSON format. This is useful for creating a knowledge base, documenting workflows, or analyzing user interactions.

## Features
- **Start Recording**: Capture voice input while performing actions on the webpage.
- **Stop Recording**: End the voice recording session.
- **Save Logs**: Save a `.txt` file containing recorded actions and speech transcripts.
- **Get Logs**: Retrieve a final `.json` file with structured data of voice transcripts and interactions.

## Prerequisites
To receive the recorded data from the browser, you need to start a local server.

### Setting Up the Local Server
1. Ensure you have Python installed on your system.
2. Navigate to the directory containing `server.py`.
3. Run the following command to start the local server:
   ```sh
   python server.py
   ```
4. Keep the server running while using the extension.

## How to Use the Extension
1. **Install the Extension**: Load the unpacked extension in Chrome Developer Mode.
2. **Pin the Extension**: Click the puzzle icon in Chrome and pin the Speech-to-Text extension for easy access.
3. **Use the Controls**:
   - Click **START** to begin recording your speech while interacting with the webpage.
   - Click **STOP** to stop recording.
   - Click **SAVE LOGS** to save a `.txt` file containing your actions and speech.
   - Click **GET JSON** to retrieve a structured JSON file with transcript and action data.

## Output Files
- **Text Logs (`.txt`)**: Contains a simple text format of recorded actions and speech.
- **JSON Logs (`.json`)**: A structured format containing voice transcripts along with user interactions.

## Use Cases
- Creating a **knowledge base** by documenting voice instructions and actions.
- Enhancing **user experience analysis** by tracking interactions.
- Simplifying **workflow documentation** through audio-visual logs.

## Support
If you encounter any issues, ensure the local server is running and that the extension has the necessary permissions. For further assistance, open an issue or reach out to the developer.

