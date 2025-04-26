# TAFSIRI - A Sign Recognizer

## Overview

The ASL Sign Recognizer is an interactive application that uses computer vision and AI to recognize American Sign Language (ASL) signs. The application captures hand gestures through a camera, analyzes them using Groq AI's language model, and provides spoken feedback. Additionally, it incorporates speech recognition to enable two-way communication.

## Features

- **Real-time Video Capture**: Live camera feed for ASL sign capture
- **Sign Recognition**: Uses Groq AI (Meta Llama 4 Scout model) to identify ASL signs
- **Text-to-Speech**: Converts recognized signs to spoken words
- **Speech Recognition**: Captures user's spoken responses
- **Interactive Interface**: User-friendly design with clear visual cues

## System Requirements

- Python 3.x
- Windows operating system (required for winsound module)
- Webcam or camera device
- Internet connection (for Groq AI API access)

## Dependencies

- tkinter: For the graphical user interface
- OpenCV (cv2): For video capture and image processing
- PIL (Python Imaging Library): For image handling in the GUI
- pyttsx3: For text-to-speech conversion
- speech_recognition: For speech recognition functionality
- groq: For AI-powered image analysis
- winsound: For audio feedback cues

## Installation

1. Install required Python packages:
   ```
   pip install opencv-python pillow pyttsx3 SpeechRecognition groq
   ```

2. Ensure you have a valid Groq API key

## Usage Instructions

1. **Launch the Application**:
   Run the main script to start the application

2. **Starting a Session**:
   - Position your hand in front of the camera
   - Click "▶ Start Capturing" to begin sign recognition

3. **Recognition Process**:
   - The system will play a beep to signal it's about to take a picture
   - Hold your ASL sign steady during capture
   - The app will process the image and identify the sign
   - The recognized sign will be displayed and spoken aloud

4. **Voice Response**:
   - After sign recognition, a speech input window appears
   - Speak your response when prompted
   - Your speech will be transcribed and displayed
   - You can skip the speaking step using the "Skip Speaking" button

5. **Ending a Session**:
   - Click the "🛑 Stop" button to halt the recognition process
   - Close the window to exit the application

## Technical Details

### Application Flow

1. Video is captured from the default camera (index 0)
2. When capturing, the application:
   - Signals with a beep
   - Captures a frame and saves as "capture.jpg"
   - Encodes the image in base64 format
   - Sends it to Groq AI with a prompt to identify the ASL sign
   - Displays and speaks the AI's response
   - Opens a speech recognition window for user response
   - Returns to sign capturing mode after the voice interaction

### API Integration

The application uses Groq's API with the Meta Llama 4 Scout model to analyze images. The prompt specifically asks the AI to focus on the hand gesture and identify the ASL sign.

### UI Components

- Main window with video feed display
- Control buttons for starting and stopping capture
- Response label showing recognized signs
- Speech input popup window with transcription display

## Troubleshooting

- **Camera Not Working**: Ensure your camera is properly connected and not in use by another application
- **Recognition Errors**: Position your hand clearly in the frame with good lighting
- **API Connection Issues**: Check your internet connection and Groq API key validity
- **Speech Recognition Problems**: Speak clearly in a quiet environment for best results

## Privacy Note

The application captures images and audio which are sent to external services (Groq AI and Google Speech Recognition). These services process the data according to their respective privacy policies.

## License

This application uses the Groq API which requires a valid API key and is subject to Groq's terms of service.
