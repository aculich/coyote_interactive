# Coyote Interactive: Design Document

## Design Philosophy

Coyote Interactive was designed with the following core principles:

1. **Character-Driven Interaction**: The system embodies a coyote character that responds to and comments on its environment, creating a sense of having a quirky, non-human companion.

2. **Physical Computing + AI**: Combining physical interfaces (buttons, LEDs) with AI capabilities to create a tactile, responsive experience that feels more alive than purely digital interfaces.

3. **Ambient Intelligence**: The system can passively monitor television content and actively engage when prompted, providing a balance between ambient presence and direct interaction.

4. **Modularity**: The architecture separates concerns (LED control, button handling, conversation management, etc.) to allow for flexible expansion and experimentation.

5. **Accessibility**: The system provides both visual (LEDs) and auditory (speech) feedback to create a multi-sensory experience.

## Technical Design

### System Architecture

The project follows a modular architecture with these key components:

1. **Main Controller** (`coyote.py`):
   - Coordinates all subsystems
   - Manages wake/sleep states
   - Handles the continuous transcription process
   - Responds to button events

2. **Input Systems**:
   - Button interface for triggering interactions
   - Audio capture for speech recognition
   - Television audio transcription

3. **Processing Systems**:
   - Speech-to-text conversion
   - LLM integration for generating responses
   - Conversation management

4. **Output Systems**:
   - Text-to-speech for audible responses
   - LED patterns for visual feedback

5. **Management Interface**:
   - Terminal-based utility for system control
   - Network, audio, and service management

### Interaction Flow

The system's main interaction flows are:

1. **Television Commentary**:
   - User presses TV button
   - System captures recent television transcript
   - AI generates commentary based on transcript
   - Commentary is spoken through text-to-speech
   - LEDs provide visual feedback throughout process

2. **Person Conversation**:
   - User presses intercom button
   - System captures speech while button is held
   - AI generates response based on captured speech
   - Response is spoken through text-to-speech
   - LEDs provide visual feedback throughout process

3. **Conversation Archive (BOOM)**:
   - In sleep mode, user presses both buttons
   - Current conversation is archived with timestamp
   - LEDs flash in an "erratic" pattern
   - Sound effect plays to confirm action

### Visual Design

#### LED Patterns

The system uses different LED patterns to communicate various states:

1. **Constant**: Solid light indicating active listening
2. **Flashing**: Regular on/off pattern indicating processing
3. **Breathing**: Gradual fade in/out mimicking breathing, indicating speaking
4. **Erratic**: Random flashing for special events (like the BOOM feature)

These patterns were designed to evoke different emotional responses and clearly communicate the system's current state to users.

## Creative Elements

### Character Development

The coyote character is designed to be:
- Observant and witty
- Slightly mischievous
- Curious about human activities
- Knowledgeable but with a non-human perspective

This character is expressed through:
- The prompt design for the LLM
- The choice of LED patterns
- The sound effects used for different events
- The physical housing and appearance of the installation

### Sound Design

The system incorporates sound effects for key events:
- Startup sound when the system initializes
- Conversation archive sound when using the BOOM feature

These sounds enhance the experience by providing clear auditory feedback for important state changes.

### Conversation Design

The conversation system is designed to:
1. Maintain context over time
2. Allow for natural interactions
3. Support both entertainment (TV commentary) and utility (direct questions)
4. Archive conversations for later review or analysis

## Evolution and Iterations

The commit history reveals several phases of development:

1. **Initial Framework** (3+ months ago):
   - Basic GPIO integration
   - Television commentary foundations
   - LED support implementation

2. **Conversation System** (3 months ago):
   - Person interaction capability
   - Speech capture and processing
   - Enhanced text handling for better speech synthesis

3. **System Enhancements** (2-3 weeks ago):
   - Sound effects integration
   - Conversation archiving
   - System service configuration

4. **Management Interface** (2 weeks ago - present):
   - Terminal-based system manager
   - Network and audio controls
   - Service management

Each phase built upon previous work while maintaining the core design philosophy of creating an engaging, character-driven interactive experience.

## Future Design Directions

Potential areas for design enhancement include:

1. **Enhanced Character Expression**: More varied LED patterns or additional physical expressions
2. **Context Awareness**: Improved environmental awareness through additional sensors
3. **Multi-Modal Interaction**: Supporting gestures or other non-verbal inputs
4. **Character Memory**: Better long-term memory of past interactions for more personalized responses
5. **Visual Interface**: Adding optional screen-based interactions to complement the current audio-focused design 