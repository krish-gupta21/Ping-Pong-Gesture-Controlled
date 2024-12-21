# Gesture-Controlled Ping Pong Game

A fun and interactive ping pong game controlled by hand gestures using a webcam. This project combines the power of **MediaPipe**, **OpenCV**, and **Pygame** to create a real-time, gesture-based gaming experience.

## Features
- **Real-Time Hand Tracking**: Uses MediaPipe to detect hand gestures.
- **Interactive Gameplay**: Control paddles with your hand movements via webcam.
- **Dynamic Background**: Webcam feed displayed as the game background.
- **Score Tracking**: Keep track of your score as you play.
- **Game Over Screen**: Displays final score with a restart option.
---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.7 or above
- OpenCV (`cv2`)
- Pygame
- MediaPipe

### Steps

1. Install Dependecies:
   ```bash
   pip install pygame opencv-python mediapipe

2. Clone the repository:
   ```bash
   git clone https://github.com/krish-gupta21/Ping-Pong-Gesture-Controlled-.git
   cd Ping-Pong-Gesture-Controlled
   
3. Give file permisions:
   ```bash
   chmod +x pingpong.py

4. Run the file:
   ```bash
   python pingpong.py

### 🔧 Installing Dependencies

If you encounter missing dependencies, install them using the following command:

```bash
pip install -r requirements.txt --break-system-packages


---

## 🎮 Game Manual

### How to Play:
1. **Start the Game**:
   - Run the script using the command: `python pingpong.py`.
2. **Control the Paddles**:
   - Move your **left hand** to control the **left paddle**.
   - Move your **right hand** to control the **right paddle**.
3. **Objective**:
   - Prevent the ball from going out of bounds by hitting it with the paddles.
4. **Scoring**:
   - Earn points every time the ball hits a paddle.
5. **Game Over**:
   - The game ends if the ball goes out of bounds. Click restart button to reatart the game.

### 📝 Tip:
Play in a well-lit environment for better hand detection accuracy.


   
