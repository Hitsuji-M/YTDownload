import tkinter as tk
from tkinter import StringVar, ttk, filedialog
from tkinter.messagebox import showinfo

import youtube_dl as ytdl
from youtube_dl.utils import DownloadError

import shutil

WINDOW_W = 600
WINDOW_H = 400

class AppYT():
    def __init__(self, root : tk.Tk) -> None:
        """
        Constructor of the AppYT class

        Change the main parameters of the window (title, geometry, ...) and launch the initial page creation

        Parameters
        ----------
        root : tkinter.Tk
            The master (root) container (instance of tkinter.Tk())

        Returns
        -------
        """


        self.root = root
        self.root.title("Youtube Downloader")
        self.root.resizable(False, False)
        self.root.iconphoto(False, tk.PhotoImage(file='img/youtube.png'))

        self.keepVideo = False
        self.currentDir = ""
        self.ytLink = ""

        self.setGeometry(WINDOW_W, WINDOW_H)
        self.initPage()
        self.showCred(150)


    def setGeometry(self, width : int, height : int) -> None:
        """
        Change the geometry of the root container

        Modify the width and length and center using the geometry of tkinter

        Parameters
        ----------
        width : int
            length in pixels of the window's width
        height : int
            length in pixels of the window's height

        Returns
        -------
        """

        SCREEN_W = self.root.winfo_screenwidth()
        SCREEN_H = self.root.winfo_screenheight()

        center_x = int(SCREEN_W/2 - width/2)
        center_y = int(SCREEN_H/2 - height/2)

        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')


    def clear(self) -> None:
        """
        Clear the root container

        Delete all the widgets in the root container

        Parameters
        ----------

        Returns
        -------
        """

        for widget in self.root.winfo_children():
            widget.destroy()


    def showCred(self, yPad : int) -> None:
        """
        Shows a credits message

        The credits message appears at the bottom of the window

        Parameters
        ----------
        yPad : int
            Length in pixels of the pad in Y

        Returns
        -------
        """

        msgCred = ttk.Label(
            self.root,
            text="Made with love by Hitsuji-M",  
        )
        msgCred.config(font=("Arial", 16, "bold"))
        msgCred.grid(row=10, pady=yPad)


#######################################


    def initPage(self) -> None:
        """
        Creates all the widgets of the initial page

        Add buttons, text, events of the initial page to download videos

        Parameters
        ----------

        Returns
        -------
        """

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)

        self.mainFrame = tk.Frame(
            self.root,
            borderwidth=0,
            highlightthickness=0
        )
        self.mainFrame.grid(rowspan=6)

        msgTitle = ttk.Label(
            self.mainFrame,
            text="Youtube Downloader",  
        )
        msgTitle.config(font=("Arial", 32, "bold"))
        msgTitle.grid(row=0)

        self.entryText = StringVar()
        self.entryText.set("Link here")

        self.link = ttk.Entry(self.mainFrame, textvariable=self.entryText)
        self.link.bind('<Button>', self.clearPlaceHolder)
        #self.link.bind('<Leave>', self.addPlaceHolder, '+') This line works but i prefer to remove it
        self.link.grid(row=1, pady=10)

        self.btnText = StringVar()
        self.btnText.set("Select folder") if self.currentDir == "" else self.btnText.set(self.currentDir)
        folderBtn = ttk.Button(self.mainFrame, command=self.selectFolder, textvariable=self.btnText)
        folderBtn.grid(row=2, pady=10)

        self.choice = StringVar()
        outputs = (('MP3', False, 0),
                   ('MP4', True, 2))

        self.radioFrame = ttk.LabelFrame(self.mainFrame)
        self.radioFrame.grid(row=3, rowspan=2, columnspan=3)

        for output in outputs:
            r = ttk.Radiobutton(
                self.radioFrame,
                text=output[0],
                value=output[1],
                variable=self.choice
            )
            r.grid(row=0, column=output[2])
        self.choice.set(0)

        btn = ttk.Button(
            self.radioFrame,
            text="Download",
            command=self.launchDl
        )
        btn.grid(row=1, column=1)


#######################################


    def selectFolder(self) -> None:
        """
        Select where to store the video

        Called by the button 'Select a folder' then ask for a directory with tkinter and store the answer

        Parameters
        ----------

        Returns
        -------
        """

        self.currentDir = filedialog.askdirectory()
        if self.currentDir == "":
            return
        self.btnText.set(self.currentDir)


    def launchDl(self) -> None:
        """
        Start the video download

        Retrieves all the user's inputs, stop the function if there's no directory or link
        Start the download and shows a message depending of the results

        Parameters
        ----------

        Returns
        -------
        """

        videoLink = self.link.get()

        if self.currentDir == "":
            showinfo(
                title="Error",
                message="You must choose a directory first"
            )
            return
        elif videoLink == "" or str.lower(videoLink) == "link here":
            showinfo(
                title="Error",
                message="You need to give a link"
            )
            return

        self.keepVideo = self.choice.get() == "1"
        self.ytLink = videoLink

        #self.clear()
        try:
            videoPath = self.dlVideo()
            showinfo(
                title="Success",
                message="Video successfully dowloaded at : " + videoPath
            )
        except DownloadError as _:
            showinfo(
                title="Error",
                message="An error occured"
            )

        self.entryText.set("Link here")
        self.ytLink = ""


    def dlVideo(self) -> str:
        """
        Download the YT wideo

        Check if the user wants an audio only or a video, then download it with the right filename and movess the video
        -> https://dev.to/stokry/download-youtube-video-to-mp3-with-python-26p

        Parameters

        Returns
        -------
        videoPath : str
            The full path to the video
        """

        # https://dev.to/stokry/download-youtube-video-to-mp3-with-python-26p (credentials)

        video_info = ytdl.YoutubeDL().extract_info(
            url = self.ytLink,
            download=False
        )

        if self.keepVideo:
            ext = ".mp4"
        else:
            ext = ".mp3"

        filename = f"{video_info['title']}{ext}".replace(":", "#") # and '#' replaces ':' in windows

        
        if self.keepVideo:
            options={'outtmpl':filename}
        else:
            options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':filename,
            }

        with ytdl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        videoPath = self.currentDir + "/" + filename
        shutil.move(filename, videoPath)
        return videoPath


    def clearPlaceHolder(self, _):
        self.entryText.set("")
    

    def addPlaceHolder(self, _):
        if (self.entryText.get != ""):
            self.entryText.set("Link here")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = AppYT(root)
    root.mainloop()