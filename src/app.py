from tkinter import Tk

import sys
sys.path.append("..")

from src.login_screen import LoginPage


class PasswordManagerApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.current_frames = []

        self._frame = None
        self.init_frame(LoginPage)
        
    def init_frame(self, frame_class):
        new_frame = frame_class(self)
        self._frame = new_frame
        self.current_frames = self.winfo_children()
        self._frame.pack()
    
    def switch_frame(self, frame_class, password=None):
        """Destroys current frame and replaces it with a new one."""
        if password:
            new_frame = frame_class(master=self, master_password=password)
        else:
            new_frame = frame_class(self)

        for child in self.winfo_children():
            if child in self.current_frames:
                child.destroy()

        self.current_frames = self.winfo_children()
        self._frame = new_frame
        self._frame.pack()
