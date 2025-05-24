![Coyote Image](coyote.png)

# Coyote Interactive

## Overview
Coyote Interactive is a modular, AI-powered interactive installation that brings a coyote character to life through various hardware interfaces. The system can respond to physical button interactions, comment on television content, engage in conversations, and provide visual feedback through LED indicators.

Built on a Raspberry Pi platform with Python, the project combines hardware integration (GPIO pins, LEDs, buttons), audio processing (speech-to-text and text-to-speech), and LLM-based AI responses to create an engaging, interactive character.

## Key Features

### Core Functionality
- **Conversation with AI**: Interact with an AI-powered coyote character through an intercom system
- **Television Commentary**: The coyote comments on what's happening on television
- **Continuous Transcription**: Real-time audio-to-text using whisper-stream
- **Visual Feedback**: LED patterns indicate different system states and activities
- **Physical Interaction**: Hardware buttons trigger different interaction modes
- **Wake/Sleep Modes**: System operates in different modes based on switch position

### System Components
- **LEDs**: Control of different LED patterns (breathing, flashing, erratic, constant)
- **Buttons**: Handling of button press/release events
- **Audio Processing**: Text-to-speech and speech-to-text conversion
- **Conversation Management**: Storing, archiving, and managing conversation history
- **System Management**: Terminal-based utility for controlling network, audio, and services

### Special Features
- **Conversation Archiving**: BOOM feature triggers timestamped conversation backup
- **Auto-start on Boot**: System automatically starts using systemd user services
- **System Manager**: Terminal utility for managing all system components

## Hardware Requirements
- Raspberry Pi (with GPIO pins)
- LEDs for visual feedback
- Buttons/switches for physical interaction
- Microphone for audio input
- Speaker for audio output

## Software Dependencies
- Python 3.8+
- gpiozero for GPIO control
- lgpio for low-level GPIO operations
- OpenAI or compatible API for LLM integration
- whisper-stream for speech recognition
- Textual for TUI interface
- Various system utilities (PulseAudio, NetworkManager, etc.)

## Setup and Installation
See the detailed setup instructions below for how to install and configure the system.

## Usage
The system operates in two main modes:
- **Wake Mode**: Actively responds to button presses for TV or person interactions
- **Sleep Mode**: System is idle but monitors for the "BOOM" button combination

### Running the System
- Manually: `python coyote.py` 
- System Manager: `./manager/run_manager.py`
- Auto-start: Configured systemd service (`coyote.service`)

## System Architecture
The codebase follows a modular approach with components for:
- Main program logic (`coyote.py`)
- Hardware control (buttons, LEDs)
- Audio processing (speech recognition, synthesis)
- AI interaction (prompts, conversation management)
- System management (network, audio, services)

## Demo Video
[![Watch on YouTube](https://img.shields.io/badge/Watch%20on-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=pncuq-U_tuU)  
[![Video Thumbnail](https://img.youtube.com/vi/pncuq-U_tuU/0.jpg)](https://www.youtube.com/watch?v=pncuq-U_tuU)

## Auto-start Configuration
The system is configured to automatically start on boot using systemd:
- Service runs in a Byobu session for easy attachment/detachment
- Full environment context is maintained (Python virtual environment, working directory, etc.)
- Environment variables for speech models are properly configured
- To attach to the running session: `byobu attach -t coyote_session` (or use alias `b`)
- To check service status: `systemctl --user status coyote.service`

### Setting Up Auto-start (Systemd Service)

1. **Copy the service file to systemd user directory**:
   ```bash
   mkdir -p ~/.config/systemd/user/
   cp /home/robot/coyote_interactive/coyote.service ~/.config/systemd/user/
   ```

2. **Reload systemd configuration**:
   ```bash
   systemctl --user daemon-reload
   ```

3. **Enable the service to start at boot**:
   ```bash
   systemctl --user enable coyote.service
   ```

4. **Enable lingering (to start service without user login)**:
   ```bash
   sudo loginctl enable-linger $USER
   ```

5. **Start the service immediately**:
   ```bash
   systemctl --user start coyote.service
   ```

6. **Create convenient alias to attach to session** (add to ~/.bashrc):
   ```bash
   echo "alias b='byobu attach -t coyote_session'" >> ~/.bashrc
   source ~/.bashrc
   ```

## System Manager

For complete details about the system manager utility, see the [manager README](manager/README.md).

