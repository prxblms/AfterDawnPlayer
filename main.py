from src.ui_elements import *



app_width = 620 # window width
app_height = 300 # window height



audio_extensions = (".mp3", ".wav", ".flac", ".ogg", ".aac", ".wma", ".m4a", ".aiff")
playlist = []



class MainFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width = width, height = height, fg_color = '#232323')

        # Configure the grid for MainFrame layout.
        self.grid_columnconfigure(1, weight  = 1)
        self.grid_rowconfigure(1, weight = 1)

        self.control_buttons()
        self.music_list()
        self.app_title()


    def control_buttons(self):
        # Configure Control Buttons.
        width = app_width - 40
        height = 40
        fg_color = '#0078ff'

        # Control Buttons frame.
        self.buttons_frame = DrawFrame(self, width= width, height = height, fg_color = fg_color)
        self.buttons_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nsew')

        # Pause music button.
        self.pause_btn = DrawButton(self.buttons_frame, text = "Pause Music", command = self.pause_music)
        self.pause_btn.grid(row = 0, column = 1, padx = 5, pady = 5)

        # Add music button.
        self.add_music_btn = DrawButton(self.buttons_frame, text = "Add Music", command = self.add_music)
        self.add_music_btn.grid(row = 0, column = 0, padx = 5, pady = 5)


    def music_list(self):
        # Configure Music List.
        width = app_width - 40
        height = 60
        fg_color = '#3d3d3d'

        # Music list, scrollable frame.
        self.music_list_frame = DrawScrollableFrame(self, width = width, height = height, fg_color = fg_color, label_anchor = 's', command = self.button_events, music_list = playlist)
        self.music_list_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')


    def app_title(self):
        # Configure Title:
        text = "After Dawn Music Player"
        width = app_width
        height = 40
        fg_color = '#0078ff'
        text_fg_color = 'transparent'
        font = ('Impact', 30)

        # Title frame.
        self.title_frame = DrawFrame(self, width = width, height = height, fg_color = fg_color)
        self.title_frame.grid(row = 0, column = 0, sticky = 'nsew')

        # Title text label.
        self.title_label = DrawLabel(
            self.title_frame,
            text = text,
            width = width,
            height = height,
            fg_color = text_fg_color,
            font = font
            )
        self.title_label.grid(row = 0, column = 0)


    def pause_music(self):
        mixer.music.pause()


    def add_music(self):
        try:
            folder = filedialog.askdirectory(title = "Select your music folder.")
            files = os.listdir(folder)

            for music in files:
                if music.lower().endswith(audio_extensions):
                    if os.path.join(folder, music) in playlist:
                        print("this song was just added.")
                        return
                    else:
                        playlist.append(os.path.join(folder, music))
                        print(playlist)

            self.update_music_list()

        except Exception as error:
            print(error)


    def update_music_list(self):
        # Detroy other widgets.
        for widget in self.music_list_frame.winfo_children():
            widget.destroy()

        # Configure Music List.
        width = app_width - 40
        height = 60
        fg_color = '#3d3d3d'

        # Music list, scrollable frame.
        self.music_list_frame = DrawScrollableFrame(self, width = width, height = height, fg_color = fg_color, command = self.button_events, music_list = playlist)
        self.music_list_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')


    def button_events(self):
        print(f"radiobutton frame modified: {self.music_list_frame.get_checked_item()}")
        music_name = self.music_list_frame.get_checked_item()
        if music_name in playlist:
            index = playlist.index(music_name)
            mixer.music.load(playlist[index])
            mixer.music.play()


class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(" After Dawn Music Player")
        self.geometry(f'{app_width}x{app_height}')
        self.resizable(False, False)

        # Configure the grid for main layout of window.
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # Main frame to group all frames.
        self.main_frame = MainFrame(self, width = app_width, height = app_height)
        self.main_frame.grid(row = 0, column = 0, sticky = "nsew")

        # Initialize Pygame mixer.
        mixer.init()


if __name__ == '__main__':
    app = MusicPlayer()
    app.mainloop()