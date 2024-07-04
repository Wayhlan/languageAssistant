import os
import keyboard
import tkinter as tk
import threading
from queue import Queue

import translator
import neuralSpeaker

window_name = "Input"

class GuiController():
    def __init__(self):
        self.input_queue = Queue()
        self.translator = translator.Translator()
        self.speaker = neuralSpeaker.NeuralSpeaker()
        keyboard.add_hotkey('ctrl+t', self.on_ctrl_t)

    def getQueue(self):
        return self.input_queue

    def on_ctrl_t(self):
        threading.Thread(target=self.show_input_window).start()

    def show_input_window(self):
        global input_text
        def on_ok():
            global input_text
            input_text = entry_var.get()
            self.input_queue.put(input_text)
            print(f'You entered: {input_text}')
            translation = self.translator.translate_text(input_text)
            print(f"Translation : {translation}")
            self.speaker.speak(input_text)
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

# def on_ctrl_c():
#     print('You pressed CTRL+C! Exiting gracefully...')
#     os._exit(0)
# keyboard.add_hotkey('ctrl+c', on_ctrl_c)