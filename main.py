import customtkinter
import os

from moviepy import editor
from tkinter import Label
from tkinter.filedialog import askopenfile


class VideoEditor:
    def __init__(self, video_path: str, audio_path: str, fps: int = 60):
        self.video_path = video_path
        self.audio_path = audio_path
        self.fps = fps 

    def add_audio_to_video(self):
        video_clip = editor.VideoFileClip(self.video_path)
        audio_clip = editor.AudioFileClip(self.audio_path)

        output_name = self.video_path.split("/")[-1]

        final_clip = video_clip.set_audio(audio_clip)
        
        if not "output" in os.listdir():
            os.mkdir("output")

        final_clip.write_videofile(f"output/{output_name}", fps=self.fps)

        for file in os.listdir():
            if file.endswith("mp3"):
                os.remove(file)


class TkinterApp:
    def __init__(self, app_title: str, window_dimensions: str = "450x260"):
        # App parameters

        self.app = customtkinter.CTk()
        self.app.geometry(window_dimensions)
        self.app.title(app_title)

        # Border 

        self.border = customtkinter.CTkFrame(master=self.app, width=250, height=240, corner_radius=15)
        
        self.border.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.border.grid_columnconfigure(0, weight=1)
        self.border.grid_columnconfigure(1, weight=1)
        self.border.grid_rowconfigure(0, minsize=10) 
        
        # Buttons

        self.video_upload_button = customtkinter.CTkButton(master=self.border, text="Upload Video", width=190, height=40,
                                        compound="right", command=self.upload_video)

        self.video_upload_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")


        self.audio_upload_button = customtkinter.CTkButton(master=self.border, text="Upload Audio", width=190, height=40,
                                        compound="right", fg_color="#D35B58", hover_color="#C77C78",
                                        command=self.upload_audio)
        self.audio_upload_button.grid(row=2, column=0, columnspan=2, padx=20, pady=40, sticky="ew")


        self.process_button = customtkinter.CTkButton(master=self.app, text="Start", width=130, height=70, border_width=3,
                                        corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                        command=self.merge_video_audio)
        self.process_button.grid(row=0, column=1, padx=20, pady=20)

        # Video and audio Path

        self.video_path = None
        self.audio_path = None

        # Initializing the app

        self.app.mainloop()


    def upload_video(self):
        # Asking for video file 
        opened_file = askopenfile(mode="r", filetypes=[("Video Files", "*mp4")])
        if opened_file: 
            self.video_path = opened_file.name
            Label(self.app, text="Video Uploaded Succesfully", foreground="green").grid(row=4, columnspan=3, pady=10)

    def upload_audio(self):
        # Asking for audio file 
        opened_file = askopenfile(mode="r", filetypes=[("Audio Files", "*mp3")])
        if opened_file:
            self.audio_path = opened_file.name
            Label(self.app, text="Audio Uploaded Succesfully", foreground="green").grid(row=4, columnspan=3, pady=10)

    def merge_video_audio(self):
        # Checking if both video and audio paths available
        if not self.video_path or not self.audio_path:
            return Label(self.app, text="Please upload video and video files", foreground="red").grid(row=4, columnspan=3, pady=10)

        videoclip_editor = VideoEditor(self.video_path, self.audio_path)
        videoclip_editor.add_audio_to_video()

        Label(self.app, text="Video created ! Please check the output folder to see the result", foreground="green").grid(row=4, columnspan=3, pady=10)


app = TkinterApp("Video Editor", "450x300")
