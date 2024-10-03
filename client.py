import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

with open("server.cfg", "r") as f:
    config = f.read().split("\n")
    for i in range(0, len(config)):
        config[i] = config[i].split("=")[1]
    print(config)
    SERVER_IP = config[0]
    SERVER_PORT = config[1]

class Window(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setUrl(QUrl("http://127.0.0.1:80"))

app = QApplication(sys.argv)
app.setApplicationName('MUSS-CLIENT')

window = Window()
window.showFullScreen()
app.exec_()