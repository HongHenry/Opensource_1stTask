import os
import openai
import spacy
import requests
from spacy.lang.en.stop_words import STOP_WORDS
from PyQt5 import QtWidgets, QtGui, QtCore

openai.api_key = "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"
nlp = spacy.load("en_core_web_sm")

class ImageGenerationThread(QtCore.QThread):
    image_generated = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        completion = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate an image based on the question: {self.question}\nKeywords: {', '.join(self.get_keywords(self.question))}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        response = openai.Image.create(
            prompt=f"Keywords: {', '.join(self.get_keywords(self.question))}\n{completion.choices[0].text}",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        image = QtGui.QImage()
        image.loadFromData(QtCore.QByteArray.fromBase64(requests.get(image_url).content))
        self.image_generated.emit(image)

    def get_keywords(self, text):
        doc = nlp(text)
        keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return keywords[:5]

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'OpenAI Image Viewer'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 600
        self.initUI()
        self.image_thread = None  # 초기화

    def initUI(self):
        # UI elements
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.question_label = QtWidgets.QLabel('무엇을 물어볼까요?', self)
        self.question_label.setGeometry(QtCore.QRect(20, 20, 300, 20))
        self.question_input = QtWidgets.QLineEdit(self)
        self.question_input.setGeometry(QtCore.QRect(20, 50, 300, 20))
        self.generate_btn = QtWidgets.QPushButton('이미지 생성', self)
        self.generate_btn.setGeometry(QtCore.QRect(350, 50, 100, 20))
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setGeometry(QtCore.QRect(20, 100, 560, 480))

        # Button click event
        self.generate_btn.clicked.connect(self.generate_image)

        self.show()

        # 애플리케이션이 종료될 때 스레드 객체를 삭제하도록 설정
        app.aboutToQuit.connect(self.cleanup)

    def generate_image(self):
        question = self.question_input.text()

        # 이미 스레드가 실행 중인 경우, 종료
        if self.image_thread is not None and self.image_thread.isRunning():
            self.image_thread.quit()
            self.image_thread.wait()

        # Start image generation thread
        self.image_thread = ImageGenerationThread(question)
        self.image_thread.image_generated.connect(self.display_image)
        self.image_thread.start()

    def display_image(self, image):
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def cleanup(self):
        if self.image_thread is not None and self.image_thread.isRunning():
            self.image_thread.quit()
            self.image_thread.wait()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
