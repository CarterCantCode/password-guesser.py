# PASSWORD BRUTE-FORCE AUTOMATION TOOL

## OVERVIEW
This is a password brute-forcing automation tool written in Python, designed to attempt to guess a password by systematically trying all possible combinations of a given character set (`charset`) and maximum password length (`max_len`). It includes functionality for template matching (via image recognition) to detect a correct password, with progress feedback and checkpoints.

## FEATURES
- **Brute-force Attack**: Attempts all combinations of a given character set and maximum password length.
- **Template Matching**: Uses image recognition to determine if a password attempt is correct.
- **Progress Feedback**: A live progress bar shows the percentage of password combinations tested.
- **Resume from Checkpoints**: Saves and loads progress using a checkpoint file.
- **Pause and Resume**: Pause the brute-force process and resume from where it left off.
- **GUI Interface**: Built using Tkinter for user-friendly interaction.

## REQUIREMENTS
- Python 3.x
- Tkinter (for GUI)
- OpenCV (`cv2` library for image matching)
- PyAutoGUI (for GUI automation)

    install the required libraries using 'pip':
    '''bash
    pip install opencv-python pyautogui numpy
