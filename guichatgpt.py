import os
import openai
import gensim
from gensim.summarization.summarizer import summarize, keywords
from PyQt5 import QtWidgets, QtGui, QtCore

openai.api_key = "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"

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'OpenAI Image Viewer'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 600
        self.initUI()

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

    def generate_image(self):
        question = self.question_input.text()

        # OpenAI API
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": question}
          ]
        )
        ksh_question = completion.choices[0].text
        ksh_keyword = keywords(ksh_question, word_count=5)
        ksh_strkeyword = ' ,'. join(ksh_keyword)
        response = openai.Image.create(
          prompt=ksh_strkeyword,
          n=1,
          size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # PyQt Display Image
        image = QtGui.QImage()
        image.loadFromData(QtCore.QByteArray.fromBase64(requests.get(image_url).content))
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    
