import tkinter as tk
import threading

class OverlayApp:
    def __init__(self):
        self.root = None
        self.lbl = None
        self.overlay_thread = None
        self.stop_event = threading.Event()

    def open_overlay(self, text):
        self.root = tk.Tk()
        self.root.title("")
        self.root.tk_setPalette("#000000")
        self.root.wm_overrideredirect(1)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.7)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        overlay_width = screen_width
        overlay_height = screen_height // 7

        self.root.geometry(f"{overlay_width}x{overlay_height}+60+60")

        self.lbl = tk.Label(self.root, fg="#FFFFFF", font=("Tahoma", 12, "bold"))
        self.lbl.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.lbl.configure(text=text)
        
        self.check_stop_event()
        self.root.mainloop()
        
    def check_stop_event(self):
        if self.stop_event.is_set():
            self.root.destroy()
        else:
            self.root.after(100, self.check_stop_event)

    def close_overlay(self):
        self.stop_event.set()
        if self.overlay_thread:
            self.overlay_thread.join()
            self.overlay_thread = None
            self.root = None

    def open_overlay_threaded(self, text):
        self.stop_event.clear()
        self.overlay_thread = threading.Thread(target=self.open_overlay, args=(text,))
        self.overlay_thread.start()
