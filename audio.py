from os.path import join
from os import listdir
import threading
import yt_dlp as ytdl


class Download:

    save_path = f'<your buffer>'

    def __init__(self, url):
        self.url = url
    
    def __await__(self):
        self.file_existed = False
        self._send_task(self._get_info)
        while self.iscrawlering:
            yield
        if self.file_existed:
            return self._path
        self._send_task(self._download)
        print('downloading')
        while self.iscrawlering:
            yield
        return self._path

    def _get_info(self):
        with ytdl.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)
        id = info['id']
        paths = [file_name for file_name in listdir(self.save_path) if file_name[:-4] == id]
        if paths:
            self._path = join(self.save_path, paths[0])
            print('exist')
            self.file_existed = True
        else:
            self.file_existed = False
        self.iscrawlering = False

    def _send_task(self, func):
        self.iscrawlering = True
        task = threading.Thread(target=func)
        task.start()
        
    def _download(self):
        ydl_opts = {
        'progress_hooks': [self._set_path],    
        'outtmpl': join(self.save_path, '%(id)s.%(ext)s'),
        'format': 'worstaudio',
        'hls-use-mpegts': True,
        }
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        print('success???')
        self.iscrawlering = False

    def _set_path(self, d):
        if d['status'] == 'finished':
            self._path = join(self.save_path, d['filename'])
