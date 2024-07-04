import os
import keyboard
import tkinter as tk
import threading
from queue import Queue
import pyautogui
from pynput import keyboard as kb
import pytesseract

import translator
import neuralSpeaker
import overlay

tesseract_custom_config = r'--oem 1' # --psm 7' # -c tessedit_char_whitelist=-[],0123456789'
start_position = None
stop_position = None
is_ctrl_pressed = False

class GuiController():
    def __init__(self):
        self.input_queue = Queue()
        self.translator = translator.Translator()
        self.speaker = neuralSpeaker.NeuralSpeaker()
        # Path to your Tesseract executable (you may not need to set this if Tesseract is in your system PATH)
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        keyboard.add_hotkey('ctrl+t', self.on_ctrl_t)
        keyboard.add_hotkey('ctrl+l', self.on_ctrl_l)
        keyboard.add_hotkey('shift+t', self.on_shift_t)
        self.overlay = overlay.OverlayApp()


    def closeOverlay(self):
        self.overlay.close_overlay()
    def openOverlay(self, text, location=None):
        self.overlay.open_overlay_threaded(text, location)

    def setOverlayText(self, text):
        self.overlay.set_label_text(text)

    def getQueue(self):
        return self.input_queue

    def on_ctrl_t(self):
        print("*** Starting input window thread ***")
        threading.Thread(target=self.show_input_window).start()

    def on_ctrl_l(self):
        threading.Thread(target=self.listen_last_translation).start()

    def on_shift_t(self):
        print("*** Starting mouse position recording thread ***")
        threading.Thread(target=self.record_mouse_on_ctrl).start()

    def listen_last_translation(self):
        self.speaker.runAudioFile()

    def show_input_window(self):
        global input_text
        def on_ok():
            global input_text
            input_text = entry_var.get()
            self.input_queue.put((input_text, None))
            root.destroy()

        root = tk.Tk()
        root.attributes('-topmost', True)
        root.update()
        
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Input text")
        label.pack(side="left")

        entry_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_var)
        entry.pack(side="left", fill="x", expand=True)

        ok_button = tk.Button(frame, text="OK", command=on_ok)
        ok_button.pack(side="left")

        frame.pack(fill="x")
        root.mainloop()

    def on_press(self, key):
        global start_position, is_ctrl_pressed
        try:
            if key == kb.Key.ctrl_l and not is_ctrl_pressed:
                is_ctrl_pressed = True
                start_position = pyautogui.position()
                print(f'Start Position: {start_position}')
        except AttributeError:
            pass

    def on_release(self, key):
        global stop_position, is_ctrl_pressed
        try:
            if key == kb.Key.ctrl_l:
                stop_position = pyautogui.position()
                print(f'Stop Position: {stop_position}')
                is_ctrl_pressed = False

                location = (start_position[0], start_position[1], stop_position[0] - start_position[0], stop_position[1] - start_position[1])

                screenshot = pyautogui.screenshot(region=location)
                screenshot.save('res/tmp/dbg_screen.jpg')
                input_text = pytesseract.image_to_string(screenshot, config=tesseract_custom_config, lang='rus')
                if not input_text: return False
                self.input_queue.put((input_text, location))
                return False
        except AttributeError:
            pass
        except Exception as e:
            print(f"*** Exception while getting image or text or translation : {e}")

    def record_mouse_on_ctrl(self):
        with kb.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
