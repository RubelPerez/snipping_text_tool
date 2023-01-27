import os
import sys

import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets
from plyer import notification

from ocr import ocr_space_file


class snipping_tool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ")
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.setWindowOpacity(0.3)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print("Capture the screen...")

        self.showFullScreen()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("black"), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        QtCore.QTimer.singleShot(1000, self.screenshot)

    def screenshot(self):
        print("screenshot")
        screen = QtGui.QGuiApplication.primaryScreen()
        window = self.windowHandle()
        if window is not None:
            screen = window.screen()
        if screen is None:
            print("failed")
            return

        original_pixmap = screen.grabWindow(0)
        output_pixmap = original_pixmap.copy(
            QtCore.QRect(self.begin, self.end).normalized()
        )
        output_pixmap.save("capture.png")
        copy_to_clipboard()
        send_windows_notification()
        remove_capture()
        sys.exit()


def send_to_ocr():
    image_to_convert = ocr_space_file(filename=f'./capture.png', language='eng')
    return image_to_convert


def remove_capture():
    try:
        os.remove('./capture.png')
    except Exception as ex:
        print(f"Error deleting capture: {ex}")


def copy_to_clipboard():
    pyperclip.copy(str(send_to_ocr()))


def send_windows_notification():
    notification.notify(
        title="Image Converted!",
        message="and copied to clipboard!",
        timeout=2
    )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())
