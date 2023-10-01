import sys
import requests
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox
from pytube import YouTube
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QByteArray

class SingleVideoDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(200, 200, 400, 600)

        self.initUi()
        self.downloadResolution=None
        self.videotitle = None
        self.selected_option = []
        self.choice=None
        self.resolutions=None
        self.url=None
        self.downloadstreams=[]
        # ____________________________________________________________
    def initUi(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter Video URL:")
        layout.addWidget(self.label)

        self.url_entry = QLineEdit()
        layout.addWidget(self.url_entry)

        self.searchBbutton = QPushButton("Search Video")
        self.searchBbutton.clicked.connect(self.search_video)
        layout.addWidget(self.searchBbutton)

        self.options = []
        self.combo_box = QComboBox()
        self.combo_box.currentTextChanged.connect(self.update)

        layout.addWidget(self.combo_box)

        self.thumbnail = None




        self.downloadBbutton = QPushButton("Download Video")
        self.downloadBbutton.clicked.connect(self.downloadVideo)
        layout.addWidget(self.downloadBbutton)

        self.status_label = QLabel(self)

        layout.addWidget(self.status_label)

        self.pixmap = QPixmap()

        self.image_label = QLabel(self)

        layout.addWidget(self.image_label)



        self.setLayout(layout)

    def update(self):
        self.choice=self.combo_box.currentText()
        print(self.choice)






    def search_video(self):
        self.url = self.url_entry.text()
        # url = "https://www.youtube.com/watch?v=YLslsZuEaNE"
        try:
            yt = YouTube(self.url)
            self.resolutions = yt.streams.filter( progressive=True)

            # print(resolutions)
            self.thumbnail = yt.thumbnail_url
            formatCount=0
            self.videotitle = yt.title
            length=yt.length
            views = yt.views
            self.status_label.setText(f"Title : {self.videotitle} : length {length}  views : {views} ")
            self.getThumbnail()

            for stream in self.resolutions:

                formatCount +=1
                pattern = r'res=\S+'
                match = re.findall(pattern, str(stream))
                if stream.type=="video":
                    if match:
                        # print(stream)
                        strings_list = match
                        pattern = r'"([^"]+)"'
                        extracted_string = re.search(pattern, strings_list[0]).group(1)
                        # print("Extracted:", extracted_string)
                        self.options.append(extracted_string)
                        self.combo_box.addItems(self.options)
                        self.downloadResolution=self.resolutions.filter(res=self.choice)
                        self.downloadstreams.append(stream)
                        print("streams downloadble : ",self.downloadstreams)



                    else:
                        print(f"available resolutions : {formatCount}")
                else:
                    print("non video file")


            print(f"choice {self.choice}")
        except Exception as e:
            print("An error occurred:", e)

    def getThumbnail(self):

        response = requests.get(self.thumbnail)
        image_data = response.content
        self.pixmap.loadFromData(image_data)
        width = 200  # Set your desired width
        height = 150  # Set your desired height
        scaled_pixmap = self.pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)


        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


    def downloadVideo(self):

        try:

            dt=YouTube(self.url)
            clip=dt.streams.filter(res=self.choice)
            print("clip: ",clip)
            clip.download(output_path=r'C:\Users\Ranga\PycharmProjects\downtube_v0.10')



        except Exception as e2:
            print(e2)



class PlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Playlist Downloader")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Playlist URL:")
        layout.addWidget(self.label)

        self.url_entry = QLineEdit()
        layout.addWidget(self.url_entry)

        self.download_button = QPushButton("Download Playlist")
        self.download_button.clicked.connect(self.download_playlist)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_playlist(self):
        # url = self.url_entry.text()
        url="https://www.youtube.com/watch?v=YLslsZuEaNE"
        try:
            playlist = YouTube(url)
            for video in playlist.video_urls:
                yt = YouTube(video)
                video_stream = yt.streams.get_highest_resolution()
                video_stream.download()
            print("Playlist download completed!")
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    single_video_app = SingleVideoDownloader()
    playlist_app = PlaylistDownloader()

    single_video_app.show()
    # playlist_app.show()

    sys.exit(app.exec_())
