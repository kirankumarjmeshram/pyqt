import sys
import os
from datetime import datetime
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube, Playlist

class DownloadThread(QThread):
    single_progress_signal = pyqtSignal(int)
    total_progress_signal = pyqtSignal(int, int)  # Signal for total progress and downloaded video count

    def __init__(self, playlist_url, resolution, save_folder):
        super().__init__()
        self.playlist_url = playlist_url
        self.resolution = resolution
        self.save_folder = save_folder

    def run(self):
        try:
            playlist = Playlist(self.playlist_url)
            videos = playlist.video_urls
            total_videos = len(videos)
            downloaded_videos = 0

            total_bytes_all = 0
            downloaded_bytes_all = 0

            for video_url in videos:
                yt = YouTube(video_url)
                video = yt.streams.filter(file_extension="mp4", progressive=True, resolution=self.resolution).first()

                save_path = os.path.join(self.save_folder, f'{yt.title}.mp4')
                
                with urllib.request.urlopen(video.url) as response:
                    total_bytes = int(response.info()['Content-Length'])
                    total_bytes_all += total_bytes
                    downloaded_bytes = 0
                    chunk_size = 1024  # 1 KB
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        downloaded_bytes_all += len(chunk)
                        downloaded_bytes += len(chunk)
                        progress_single = int((downloaded_bytes / total_bytes) * 100)
                        progress_all = int((downloaded_bytes_all / total_bytes_all) * 100)
                        self.single_progress_signal.emit(progress_single)
                        self.total_progress_signal.emit(progress_all, downloaded_videos)

                        with open(save_path, 'ab') as file:
                            file.write(chunk)

                downloaded_videos += 1

        except Exception as e:
            print(f"Error: {e}")

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.download_thread = None  # Initialize the thread as a member variable

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Playlist Downloader')
        self.setGeometry(300, 300, 500, 250)

        self.playlist_label = QLabel('Enter YouTube Playlist URL:')
        self.playlist_input = QLineEdit()
        
        self.resolution_label = QLabel('Select Resolution:')
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(['720p', '480p', '360p', '240p'])  # Add resolutions
        
        self.download_button = QPushButton('Download Playlist')
        self.download_button.clicked.connect(self.start_download)

        self.progress_single_bar = QProgressBar()
        self.progress_single_bar.setValue(0)

        self.progress_total_bar = QProgressBar()
        self.progress_total_bar.setValue(0)

        self.label_total_videos = QLabel('')

        vbox = QVBoxLayout()
        vbox.addWidget(self.playlist_label)
        vbox.addWidget(self.playlist_input)
        vbox.addWidget(self.resolution_label)
        vbox.addWidget(self.resolution_combo)
        vbox.addWidget(self.progress_single_bar)
        vbox.addWidget(self.progress_total_bar)
        vbox.addWidget(self.label_total_videos)
        vbox.addWidget(self.download_button)
        vbox.addStretch()

        self.setLayout(vbox)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            # If a thread is already running, don't start a new one
            return

        playlist_url = self.playlist_input.text()
        resolution = self.resolution_combo.currentText()
        save_folder = 'playlist_videos'

        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        self.download_thread = DownloadThread(playlist_url, resolution, save_folder)
        self.download_thread.single_progress_signal.connect(self.update_single_progress)
        self.download_thread.total_progress_signal.connect(self.update_total_progress)
        self.download_thread.start()

    def update_single_progress(self, progress):
        self.progress_single_bar.setValue(progress)

    def update_total_progress(self, progress, downloaded_videos):
        self.progress_total_bar.setValue(progress)
        self.label_total_videos.setText(f"Downloaded: {downloaded_videos} / Total: Calculating...")

    def closeEvent(self, event):
        # Ensure that the thread is stopped before the application exits
        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
