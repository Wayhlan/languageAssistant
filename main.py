import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
current_path = os.environ.get('PATH')
ffmpeg_path = os.path.join(os.getcwd(), r"libs/ffmpeg/bin")
os.environ['PATH'] = ffmpeg_path + os.pathsep + current_path
import queue
import time
# import random
import keyboard

import gui


def on_press_minus():
    print("You pressed '-'! Exiting...")
    os._exit(0)
if __name__ == "__main__":
    m_gui_ctrl = gui.GuiController()
    m_queue = m_gui_ctrl.getQueue()
    keyboard.add_hotkey('-', on_press_minus)
    print("Ready !\nPress Ctrl+T to show input text window.\nPress Shift+T to use mouse position.\n Press '+' to exit.")
    while True:
        try:
            input_text, location = m_queue.get(timeout=1)
            print(f'Input text : {input_text}')
            translation = m_gui_ctrl.translator.translate_text(input_text)
            print(f"Translation : {translation}")
            m_gui_ctrl.openOverlay(translation, location)
            m_gui_ctrl.speaker.speak(input_text)
            time.sleep(2)
            m_gui_ctrl.closeOverlay()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Exception occured while processing input text :\n {input_text}\n Exception : {e}")
            break
    # keyboard.wait('+')
    os._exit(0)


# def generate_random_excluding(exclusion_list, range_start, range_end):
#     valid_numbers = [num for num in range(range_start, range_end + 1) if num not in exclusion_list]
#     if not valid_numbers:
#         raise ValueError("No valid numbers available in the given range")
    
#     return random.choice(valid_numbers)

# def speak_translations_from_dictionnary(dictionnary, speaker):
#     for russian, english in dictionnary.items():
#         speaker.speak(russian)
