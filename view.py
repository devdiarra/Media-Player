import os
import Pmw
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import itertools
import model
import player
from seekbar import Seekbar
from helpers import *

SEEKBAR_WIDTH = 360



class View:
    loop_choices = [("No Loop", 1), ("Loop Current", 2), ("Loop All", 3)]
    current_track_index = 0
    toggle_play_stop = itertools.cycle(["play", "stop"])
    toggle_pause_unpause = itertools.cycle(["pause", "unpause"])
    toggle_mute_unmute = itertools.cycle(["mute", "unmute"
                                          ])

    def __init__(self, root, model, player):
        self.show_context_menu = None
        self.root = root
        self.model = model
        self.player = player
        self.create_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.close_player)
        self.root.bind("<<SeekbarPositionChanged>>", self.seek_new_position)

    def create_gui(self):
        self.root.title("")
        self.balloon = Pmw.Balloon(self.root)
        self.create_top_display()
        self.create_button_frame()
        self.create_list_box()
        self.create_bottom_frame()
        self.create_context_menu()

    def create_top_display(self):
        frame = tk.Frame(self.root)
        glass_from_image = tk.PhotoImage(file='./icons/glass_frame.gif')
        self.canvas = tk.Canvas(frame, width=370, height=90)
        self.canvas.image = glass_from_image
        self.canvas.grid(row=1)
        self.console = self.canvas.create_image(
            0, 10, anchor=tk.NW, image=glass_from_image
        )
        self.clock = self.canvas.create_text(
            125, 68, anchor=tk.W, fill="#CBE4F6", text="00:00"
        )
        self.track_length_text = self.canvas.create_text(
            167, 68, anchor=tk.W, fill="#9CEDAC", text="of 00:00"
        )
        self.track_name = self.canvas.create_text(
            50, 35, anchor=tk.W, fill="#9CEDAC", text='\"Currently playing: none \"'
        )
        self.seek_bar = Seekbar(frame, background="blue", width=SEEKBAR_WIDTH, height=10)
        self.seek_bar.grid(row=2, columnspan=10, sticky='ew', padx=5)
        frame.grid(row=1, columnspan=10, sticky='ew', padx=5)

    def create_button_frame(self):
        frame = tk.Frame(self.root)
        previous_track_icon = tk.PhotoImage(file='./icons/previous_track.gif')
        previous_track_button = tk.Button(frame, image=previous_track_icon, borderwidth=0, padx=5,
                                          command=self.on_previous_track_button_clicked)
        previous_track_button.image = previous_track_icon
        previous_track_button.grid(row=3, column=1, sticky='w')
        self.balloon.bind(previous_track_button, "Previous Song")

        # display rewind button
        rewind_icon = tk.PhotoImage(file='./icons/rewind.gif')
        rewind_button = tk.Button(
            frame, image=rewind_icon, borderwidth=0, padx=0, command=self.on_rewind_button_clicked)
        rewind_button.image = rewind_icon
        rewind_button.grid(row=3, column=2, sticky='w')
        self.balloon.bind(previous_track_button, 'Rewind')

        # display play button
        self.play_icon = tk.PhotoImage(file='./icons/play.gif')
        self.stop_icon = tk.PhotoImage(file='./icons/stop.gif')
        self.play_stop_button = tk.Button(
            frame, image=self.play_icon, borderwidth=0, padx=0, command=self.on_play_stop_button_clicked)
        self.play_stop_button.image = self.play_icon
        self.play_stop_button.grid(row=3, column=3)
        self.balloon.bind(self.play_stop_button, 'Play/Stop song')

        # display pause button
        pause_icon = tk.PhotoImage(file='./icons/pause.gif')
        pause_unpause_button = tk.Button(
            frame, image=pause_icon, borderwidth=0, padx=0, command=self.on_pause_unpause_button_clicked)
        pause_unpause_button.image = pause_icon
        pause_unpause_button.grid(row=3, column=4)
        self.balloon.bind(pause_unpause_button, 'Pause')

        # display fast forward button
        fast_forward_icon = tk.PhotoImage(file='./icons/fast_forward.gif')
        fast_forward_button = tk.Button(
            frame, image=fast_forward_icon, borderwidth=0, padx=0, command=self.on_fast_forward_button_clicked)
        fast_forward_button.image = fast_forward_icon
        fast_forward_button.grid(row=3, column=5)
        self.balloon.bind(fast_forward_button, 'Fast Forward')

        # display next button
        next_track_icon = tk.PhotoImage(
            file='./icons/next_track.gif')
        next_track_button = tk.Button(
            frame, image=next_track_icon, borderwidth=0, padx=0, command=self.on_next_track_button_clicked)
        next_track_button.image = next_track_icon
        next_track_button.grid(row=3, column=6)
        self.balloon.bind(next_track_button, 'Next Track')

        # display mute and unmute button
        self.mute_icon = tk.PhotoImage(
            file='./icons/mute.gif')
        self.unmute_icon = tk.PhotoImage(
            file='./icons/unmute.gif')
        self.mute_unmute_button = tk.Button(
            frame, image=self.unmute_icon, text='unmute', borderwidth=0, padx=0,
            command=self.on_mute_unmute_button_clicked)
        self.mute_unmute_button.image = self.unmute_icon
        self.mute_unmute_button.grid(row=3, column=7)
        self.balloon.bind(self.mute_unmute_button, 'Mute/Unmute')

        # display volume scale button
        self.volume_scale = tkinter.ttk.Scale(
            frame, from_=0.0, to=1.0, command=self.on_volume_scale_changed)
        self.volume_scale.set(0.6)
        self.volume_scale.grid(row=3, column=8, padx=5)

        # display frame with grid manager
        frame.grid(row=3, columnspan=5, sticky='w', pady=4, padx=5)

    def create_list_box(self):
        frame = tk.Frame(self.root)
        self.list_box = tk.Listbox(frame, activestyle='none', cursor='hand2',
                                   bg='#1C3D7D', fg='#A0B9E9', selectmode=tk.EXTENDED, height=10)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.list_box.bind(
            "<Double-Button-1>", self.on_play_list_double_clicked)
        self.list_box.bind("<Button-3>", self.show_context_menu)
        scroll_bar = tk.Scrollbar(frame)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.list_box.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self.list_box.yview)
        frame.grid(row=4, padx=5, columnspan=10, sticky='ew')

    def create_bottom_frame(self):
        frame = tk.Frame(self.root)

        add_file_icon = tk.PhotoImage(
            file='./icons/add_file.gif')
        add_file_button = tk.Button(frame, image=add_file_icon, borderwidth=0,
                                    padx=0, text='Add File', command=self.on_add_file_button_clicked)
        add_file_button.image = add_file_icon
        add_file_button.grid(row=5, column=1)

        remove_selected_icon = tk.PhotoImage(
            file='./icons/delete_selected.gif')
        remove_selected_button = tk.Button(
            frame, image=remove_selected_icon, borderwidth=0, padx=0, text='Delete',
            command=self.on_remove_selected_button_clicked)
        remove_selected_button.image = remove_selected_icon
        remove_selected_button.grid(row=5, column=2)

        add_directory_icon = tk.PhotoImage(
            file='./icons/add_directory.gif')
        add_directory_button = tk.Button(frame, image=add_directory_icon, borderwidth=0,
                                         padx=0, text='Add Dir', command=self.on_add_directory_button_clicked)
        add_directory_button.image = add_directory_icon
        add_directory_button.grid(row=5, column=3)

        empty_play_list_icon = tk.PhotoImage(
            file='./icons/clear_play_list.gif')
        empty_play_list_button = tk.Button(frame, image=empty_play_list_icon, borderwidth=0,
                                           padx=0, text='Clear All', command=self.on_clear_play_list_button_clicked)
        empty_play_list_button.image = empty_play_list_icon
        empty_play_list_button.grid(row=5, column=4)

        self.loop_value = tk.IntVar()
        self.loop_value.set(3)
        for txt, val in self.loop_choices:
            tk.Radiobutton(frame, text=txt, variable=self.loop_value, value=val).grid(
                row=5, column=4 + val, pady=3)

        frame.grid(row=5, sticky='w', padx=5)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.list_box, tearoff=0)
        self.context_menu.add_command(
            label="Delete", command=self.on_remove_selected_context_menu_clicked)

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
            self.mute_unmute_button.config(image=self.mute_icon)
        elif action == 'unmute':
            self.player.unmute(self.volume_at_time_of_mute)
            self.volume_scale.set(self.volume_at_time_of_mute)
            self.mute_unmute_button.config(image=self.unmute_icon)

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
                    audio_files_in_directory.append(dirpath + "/" + audio_file)
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
        self.play_stop_button.config(image=self.play_icon)
        self.player.stop()

    def clear_play_list(self):
        pass

    def play_previous_track(self):
        self.current_track_index = max(0, self.current_track_index - 1)
        self.start_play()

    def play_next_track(self):
        self.current_track_index = min(self.list_box.size() - 1, self.current_track_index + 1)
        self.start_play()

    def manage_one_time_track_updates_on(self):
        self.update_now_playing_text()
        self.display_track_duration()

    def update_now_playing_text(self):
        current_track = self.model.play_list[self.current_track_index]
        file_path, file_name = os.path.split(current_track)
        truncated_track_name = truncate_text(file_name, 40)
        self.canvas.itemconfig(self.track_name, text=truncated_track_name)

    def display_track_duration(self):
        self.track_length = self.player.track_length
        minutes, seconds = get_time_in_minute_seconds(self.track_length)
        track_length_string = "of {0:02d}:{1:02d}".format(minutes, seconds)
        self.canvas.itemconfig(self.track_length_text, text=track_length_string)

    def manage_periodic_update_during(self):
        self.update_clock()
        self.update_seek_bar()
        self.root.after(1000, self.manage_one_time_track_updates_on)

    def update_clock(self):
        self.elapsed_play_duration = self.player.elapsed_play_duration
        minutes, seconds = get_time_in_minute_seconds(self.elapsed_play_duration)
        current_time_string = '{0:02d}:{1:02d}'.format(minutes, seconds)
        self.canvas.itemconfig(self.clock, text=current_time_string)

    def update_seek_bar(self):
        seekbar_bar_position = SEEKBAR_WIDTH * self.player.elapsed_play_duration / self.track_length
        self.seek_bar.slide_to_position(seekbar_bar_position)

    def seek_new_position(self, event=None):
        time = self.player.track_length * event.x / SEEKBAR_WIDTH
        self.player.seek(time)

    def manage_periodic_updates_during_play(self):
        self.update_clock()
        self.update_seek_bar()
        if not self.player.is_playing():
            if self.not_to_loop(): return
        self.root.after(1000, self.manage_periodic_update_during)

    def not_to_loop(self):
        selected_loop_choice = self.loop_value.get()
        if selected_loop_choice == 1:
            return True
        elif selected_loop_choice == 2:
            self.start_play()
        elif selected_loop_choice == 3:
            self.play_next_track()
        return True

    def close_player(self):
        self.player.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    model = model.Model()
    player = player.Player()
    app = View(root, model, player)
    root.mainloop()
