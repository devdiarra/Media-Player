import os.path
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
        self.create_bottom_frame()
        self.create_context_menu()

    def create_top_display(self):
        pass

    def create_button_frame(self):
        pass

    def create_list_box(self):
        pass

    def create_bottom_frame(self):
        pass

    def create_context_menu(self):
        pass

    def on_previous_track_button_clicked(self):
        pass

    def on_rewind_button_clicked(self):
        pass

    def on_play_stop_button_clicked(self):
        pass

    def on_pause_unpause_button_clicked(self):
        pass

    def on_mute_unmute_button_clicked(self):
        pass

    def on_fast_forward_button_clicked(self):
        pass

    def on_next_track_button_clicked(self):
        pass

    def on_volume_scale_changed(self, value):
        pass

    def on_add_file_button_clicked(self):
        self.add_audio_file()

    def on_remove_selected_button_clicked(self):
        self.remove_selected_files()

    def on_add_directory_button_clicked(self):
        self.add_all_audio_files_from_directory()

    def on_empty_play_list_button_clicked(self):
        pass

    def on_clear_play_list_button_clicked(self):
        self.clear_play_list()

    def on_remove_selected_context_menu_clicked(self):
        self.remove_selected_files()

    def on_play_list_double_clicked(self, event=None):
        pass

    def add_audio_file(self):
        audio_file = tkinter.filedialog.askopenfilename(
            filetypes=[
                ("All supported", ".mp3 .waw"),
                (".mp3 files", ".mp3"), (".waw files", ".waw"),
            ]
        )
        if audio_file:
            self.model.add_to_play_list(audio_file)
            file_path, file_name = os.path.split(audio_file)
            self.list_box.insert(tk.END, file_name)

    def remove_selected_files(self):
        try:
            selected_indexes = self.list_box.curselection()
            for index in reversed(selected_indexes):
                self.lis_box.delete(index)
                self.model.remove_item_from_play_list_at_index(index)
        except IndexError:
            pass



if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    model = model.Model()
    player = player.Player()
    app = View(root, model, player)
    root.mainloop()
