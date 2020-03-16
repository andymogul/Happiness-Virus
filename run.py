import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import visualize

running = False
def run():
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(width, height)

    counter=0
    while running:
        counter += 1
        ret, img = cap.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if counter % 10 == 0:
                mood, emoji_img = visualize.img2mood(img)
                
                if mood != 3:
                    text = 'Come on. Smile!'
                    loc_x = 195
                    loc_y = 120
                else:
                    text = 'Your smile is beautiful!'
                    loc_x = 135
                    loc_y = 120
                

                emoji_img = cv2.cvtColor(emoji_img, cv2.COLOR_BGR2RGB)
                emoji_img = cv2.cvtColor(emoji_img, cv2.COLOR_BGR2RGB)
                cv2.putText(emoji_img, text, (loc_x, loc_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)
                h,w,c = emoji_img.shape
                qImg = QtGui.QImage(emoji_img.data, w, h, w*c, QtGui.QImage.Format_RGB888)

                pixmap = QtGui.QPixmap.fromImage(qImg)
                label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()
    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")

def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())