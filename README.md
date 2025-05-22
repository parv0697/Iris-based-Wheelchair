# Eye-Controlled Wheelchair

This project uses computer vision to detect pupil movements and control a wheelchair based on eye gaze.

## Functionality

The system operates as follows:
1.  A webcam captures live video input.
2.  Python scripts process the video frames:
    *   `haarcascade_eye.xml` (and potentially `haarcascade_frontalface_alt.xml`) are used with OpenCV to detect faces and then eyes within those faces.
    *   The `pupil_detect.py` script, or similar logic within `eye_detect.py` and `iris_based_wheelchair.py`, refines the eye region to pinpoint the pupil. This often involves image thresholding, contour detection, and selecting the pupil based on characteristics like size and darkness.
    *   `iris_based_wheelchair.py` is the main script that interprets the pupil's horizontal position (left, center, right) to determine the intended direction of movement.
3.  Based on the detected pupil position, commands are sent via a serial connection (e.g., to 'COM5') to an Arduino.
4.  The Arduino (running the `sketch_apr09a/sketch_apr09a.ino` sketch) receives these commands and controls the wheelchair's motors to move it left, right, or forward.

Key Python scripts:
*   **`iris_based_wheelchair.py`**: Main script for video processing, pupil tracking, command generation, and serial communication with the Arduino.
*   **`eye_detect.py`**: Appears to be an earlier or alternative version for eye and pupil detection, focusing on visual feedback (drawing rectangles/circles) and printing detected direction.
*   **`pupil_detect.py`**: Provides functions specifically for pupil detection using the MSER (Maximally Stable Extremal Regions) algorithm, including helpers for image masking and feature sorting.

## Features

*   Real-time face and eye detection using Haar cascades.
*   Pupil detection and tracking within the detected eye region.
*   Control of a wheelchair (via Arduino) based on gaze direction:
    *   Look left to turn left.
    *   Look right to turn right.
    *   Look center/forward to move forward.
*   Serial communication interface between the Python script and the Arduino.
*   Visual feedback of detected eyes and pupils on the video stream.

## Requirements

### Hardware
*   Webcam
*   Arduino (e.g., Arduino Uno)
*   Wheelchair equipped with motor drivers compatible with Arduino control.
*   Computer to run the Python scripts.

### Software
*   Python 3.x
*   OpenCV (`opencv-python`)
*   NumPy (`numpy`)
*   PySerial (`pyserial`)
*   Arduino IDE (for uploading the sketch to the Arduino)

## Setup and Usage

1.  **Install Python Dependencies:**
    Open a terminal or command prompt and install the required Python libraries:
    ```bash
    pip install opencv-python numpy pyserial
    ```

2.  **Set up Arduino:**
    *   Connect the Arduino to your computer.
    *   Open the `sketch_apr09a/sketch_apr09a.ino` file in the Arduino IDE.
    *   Select the correct board and port from the Tools menu.
    *   Upload the sketch to your Arduino.

3.  **Configure Serial Port:**
    *   In the `iris_based_wheelchair.py` script, ensure the `ArduinoSerial = serial.Serial('COM5',9600)` line matches the serial port your Arduino is connected to. On Linux or macOS, the port might look like `/dev/ttyUSB0` or `/dev/ttyACM0`. On Windows, it's typically `COMX` (e.g., `COM3`, `COM5`). You can find the correct port in the Arduino IDE (Tools > Port).

4.  **Connect Hardware:**
    *   Ensure the webcam is connected to your computer.
    *   Ensure the Arduino is connected to the wheelchair's motor control system as per your wheelchair's design.

5.  **Run the Application:**
    *   Navigate to the project directory in your terminal.
    *   Execute the main script:
        ```bash
        python iris_based_wheelchair.py
        ```
    *   A window should appear showing the webcam feed with eye and pupil detection overlays.
    *   Position your face so the camera can clearly see your eyes.
    *   Control the wheelchair by looking left, right, or keeping your gaze centered for forward movement (as configured in the script).
    *   Press 'q' to quit the application.

**Note:** The sensitivity and specific ranges for 'left', 'forward', and 'right' might need adjustment within the `iris_based_wheelchair.py` script (e.g., the `if i > 40:`, `elif i > 25 and i <= 35:`, `elif i < 24:` conditions) depending on your camera, lighting, and personal eye movement range.

## Additional Components

### Haar Cascades
*   **`haarcascade_eye.xml`**: An OpenCV Haar cascade file used for detecting eyes.
*   **`haarcascade_frontalface_alt.xml`**: An OpenCV Haar cascade file used for detecting frontal faces. These are pre-trained classifiers that allow the software to identify these features in the video frames.

### Arduino Sketch
*   **`sketch_apr09a/sketch_apr09a.ino`**: The Arduino program that runs on the microcontroller. It listens for serial commands (representing 'left', 'right', 'forward') sent by the Python script and translates these commands into electrical signals to control the wheelchair's motors.

## Future Improvements

*   **Obstacle Avoidance:** Integrate ultrasonic or infrared sensors for basic obstacle detection and automatic stopping.
*   **Enhanced Commands:** Implement more complex commands, such as 'stop', 'backward', or variable speed control, possibly using blink detection or specific gaze patterns.
*   **Calibration Routine:** Add an automated calibration process to better adapt to individual users' eye characteristics and gaze ranges.
*   **GUI Interface:** Develop a simple Graphical User Interface (GUI) for easier configuration, starting/stopping the system, and viewing diagnostic information.
*   **Wireless Communication:** Replace serial communication with Bluetooth or Wi-Fi for a wireless connection between the computer and Arduino.
*   **Adaptive Learning:** Implement machine learning techniques to improve pupil detection accuracy and adapt to changing lighting conditions.
*   **Power Management:** Display battery levels for the wheelchair and control system.
