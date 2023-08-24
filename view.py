import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import itertools
import model
import player



class View:
    current_track_index = 0
    toggle_play_stop = itertools.cycle(["play", "stop"])
    toggle_pause_unpause = itertools.cycle(["pause", "unpause"])
    toggle_mute_unmute = itertools.cycle(["mute", "unmute"
                                          ])

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
        self.play_previous_track()

    def on_rewind_button_clicked(self):
        self.player.rewind()

    def on_play_stop_button_clicked(self):
        action = next(self.toggle_play_stop)
        if action == "play":
            try:
                self.current_track_index = self.list_box.curselection()[0]
            except IndexError:
                self.current_track_index = 0
            self.start_play()
        elif action == 'stop':
            self.stop_play()



    def on_pause_unpause_button_clicked(self):
        action = next(self.toggle_pause_unpause)
        if action == 'pause':
            self.player.pause()
        elif action == 'unpause':
            self.player.unpause()

    def on_mute_unmute_button_clicked(self):
        action = next(self.toggle_mute_unmute)
        if action == 'mute':
            self.volume_at_time_of_mute = self.player.volume
            self.player.mute()
            self.volume_scale.set(0)
            self.mute_unmute_button.config(imgage=self.mute_icon)
        elif action == 'unmute':
            self.player.unmute(self.volume_at_time_of_mute)
            self.volume_scale.set(self.volume_at_time_of_mute)
            self.mute_unmute_button.config(images=self.unmute_icon)


    def on_fast_forward_button_clicked(self):
        self.player.fast_forward()

    def on_next_track_button_clicked(self):
        self.play_next_track()

    def on_volume_scale_changed(self, value):
        self.player.volume = self.volume_set.get()
        if self.volume_scale.get() == 0.0:
            self.mute_unmute_button.config(image=self.mute_icon)
        else:
            self.on_mute_unmute_button.config(image=self.unmute_icon)

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
        self.current_track_index = int(self.list_box.curselection()[0])
        self.start_play()

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

    def add_all_audio_files_from_directory(self):
        directory_path = tkinter.filedialog.askdirectory()
        if not directory_path: return
        audio_files_in_directory = self.get_all_audio_file_from_directory(directory_path)
        for audio_file in audio_files_in_directory:
            self.model.add_to_play_list(audio_file)
            file_path, file_name = os.path.split(audio_file)
            self.list_box.insert(tk.END, file_name)

    def get_all_audio_file_from_directory(self, directory_path):
        audio_files_in_directory = []
        for (dirpath, dirnames, filenames) in os.walk(directory_path):
            for audio_file in filenames:
                if audio_file.endswith(".mp3") or audio_file.endswith(".waw"):
                    audio_files_in_directory.append(dirpath + "/" +  audio_file)
        return audio_files_in_directory

    def empty_play_list(self):
        self.model.empty_list()
        self.list_box.delete(0, tk.END)

    def start_play(self):
        try:
            audio_file = self.model.get_file_to_play(self.current_track_index)
        except IndexError:
            return
        self.on_play_stop_button.config(image=self.stop_icon)
        self.player.play_media(audio_file)

    def stop_play(self):
        self.play_stop_button.config(images=self.play_icon)
        self.player.stop()

    def clear_play_list(self):
        pass

    def play_previous_track(self):
        self.current_track_index = max(0, self.current_track_index - 1)
        self.start_play()

    def play_next_track(self):
        self.current_track_index = min(self.list_box.size() - 1, self.current_track_index + 1)
        self.start_play()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    model = model.Model()
    player = player.Player()
    app = View(root, model, player)
    root.mainloop()
