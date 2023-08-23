import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

import model
import player

class View:
    def __init__(self, root, model, player):
        self.root = root
        self.model = model
        self.player = player
        self.create_gui()

    def create_gui(self):
        self.root.title("")
        self.create_top_display()
        self.create_button_frame()
        self.create_list_box()
        self.create_button_frame()
        self.create_context_menu()

    def create_top_display(self):
        pass

    def create_button_frame(self):
        pass

    def create_list_box(self):
        pass

    def create_context_menu(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    model = model.Model()
    player = player.Player()
    app = View(root, model, player)
    root.mainloop()
