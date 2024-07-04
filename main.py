import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
current_path = os.environ.get('PATH')
ffmpeg_path = os.path.join(os.getcwd(), r"libs/ffmpeg/bin")
os.environ['PATH'] = ffmpeg_path + os.pathsep + current_path
import random
import keyboard

import gui

def generate_random_excluding(exclusion_list, range_start, range_end):
    valid_numbers = [num for num in range(range_start, range_end + 1) if num not in exclusion_list]
    if not valid_numbers:
        raise ValueError("No valid numbers available in the given range")
    
    return random.choice(valid_numbers)

def speak_translations_from_dictionnary(dictionnary, speaker):
    for russian, english in dictionnary.items():
        speaker.speak(russian)

def main():
    m_gui_ctrl = gui.GuiController()
    print("Ready !\nPress Ctrl+T to show input text window.\nPress Shift+T to use mouse position.\n Press '+' to exit.")
    # m_gui_ctrl.openOverlay("Please work")
    keyboard.wait('+')
    # m_gui_ctrl.closeOverlay()
    os._exit(0)

if __name__ == "__main__":
    main()