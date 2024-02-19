import tkinter as tk


class BlinkingLabel(tk.Label):
    """Classe qui permet de créer un label qui clignote"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.toggle = True
        self.after(100, self.blink)  # 1er appel après 100 ms

    def blink(self):
        """Méthode qui permet de faire clignoter un label"""
        if self.toggle:
            self.configure(fg='green')
        else:
            self.configure(fg='white')
        self.toggle = not self.toggle
        self.after(200, self.blink)  # appel récursif
