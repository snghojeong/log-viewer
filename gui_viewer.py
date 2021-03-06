import geolo_view
import sys
import re
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class EditDialog(QDialog):

    def __init__(self, parent = None):
        super(EditDialog, self).__init__(parent)

        self.txt = ''
        if os.path.isfile('logviewer.cfg'):
            f = open('logviewer.cfg','r')
            with f:
                self.txt = f.read()

        vbox = QVBoxLayout(self)
        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setText(self.txt)
        vbox.addWidget(self.te)
        vbox.addStretch()

    @staticmethod
    def getFilter(parent = None):
        dialog = EditDialog(parent)
        dialog.exec_()
        return dialog.txt


class MainWidget(QWidget):

    def __init__(self, fname = ""):
        super().__init__()

        self.log_cnt = 2000

        self.filter_date = QLabel()
        self.filter_date.setText('')
        self.filter_lv = QLabel()
        self.filter_lv.setText('')
        self.filter_qlabel = QLabel()
        self.filter_qlabel.setText('')
        self.filter_md = QLabel()
        self.filter_md.setText('')
        self.filter_msg = QLabel()
        self.filter_msg.setText('')

        self.initUI()

        self.pos_list = list()
        self.pos_list.append(0)

        self.find_pos_list = list()

        self.fname = fname
        if self.fname != "":
            self.prev_pos = 0
            self.next_pos = self.load_file(self.fname, 0)
            scrollBar = self.tb.verticalScrollBar()
            scrollBar.setValue(0)

    def initUI(self):
        vbox = QVBoxLayout()

        # Filter Area
        self.date_le = QLineEdit()
        self.date_cbox = QComboBox()
        self.date_cbox.setLineEdit(self.date_le)
        self.date_cbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.date_le.setText('DATE')
        self.date_le.returnPressed.connect(self.apply_filter)
        self.date_le.textChanged.connect(self.filter_date.setText)

        self.lvle = QLineEdit()
        self.lv_cbox = QComboBox()
        self.lv_cbox.setLineEdit(self.lvle)
        self.lv_cbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lvle.setText('LEVEL')
        self.lvle.returnPressed.connect(self.apply_filter)
        self.lvle.textChanged.connect(self.filter_lv.setText)

        self.qlle = QLineEdit()
        self.ql_cbox = QComboBox()
        self.ql_cbox.setLineEdit(self.qlle)
        self.ql_cbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.qlle.setText('QLABEL')
        self.qlle.returnPressed.connect(self.apply_filter)
        self.qlle.textChanged.connect(self.filter_qlabel.setText)

        self.mdle = QLineEdit()
        self.md_cbox = QComboBox()
        self.md_cbox.setLineEdit(self.mdle)
        self.md_cbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.mdle.setText('MODULE')
        self.mdle.returnPressed.connect(self.apply_filter)
        self.mdle.textChanged.connect(self.filter_md.setText)

        self.msgle = QLineEdit()
        self.msg_cbox = QComboBox()
        self.msg_cbox.setLineEdit(self.msgle)
        self.msgle.setText('MESSAGE')
        self.msgle.returnPressed.connect(self.apply_filter)
        self.msgle.textChanged.connect(self.filter_msg.setText)

        fltrbox = QHBoxLayout()
        fltrbox.addWidget(self.date_cbox, 0)
        fltrbox.addWidget(self.lv_cbox, 1)
        fltrbox.addWidget(self.ql_cbox, 2)
        fltrbox.addWidget(self.md_cbox, 3)
        fltrbox.addWidget(self.msg_cbox, 4)

        vbox.addLayout(fltrbox, 0)

        # Text browser
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        fontdb = QFontDatabase()
        self.tb.setFont(fontdb.systemFont(QFontDatabase.FixedFont))

        vbox.addWidget(self.tb, 1)

        # Button Area
        self.find_le = QLineEdit()

        self.prev_find_btn = QPushButton('<')
        self.prev_find_btn.pressed.connect(self.find_prev)
        self.prev_find_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.next_find_btn = QPushButton('>')
        self.next_find_btn.pressed.connect(self.find_next)
        self.next_find_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.prev_btn = QPushButton('Prev')
        self.prev_btn.pressed.connect(self.prev_logs)
        self.prev_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.log_cnt_le = QLineEdit()
        self.log_cnt_le.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.log_cnt_le.setText(str(self.log_cnt))

        self.next_btn = QPushButton('Next')
        self.next_btn.pressed.connect(self.next_logs)
        self.next_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btnbox = QHBoxLayout()
        btnbox.addWidget(self.find_le, 0)
        btnbox.addWidget(self.prev_find_btn, 1)
        btnbox.addWidget(self.next_find_btn, 2)
        btnbox.addWidget(self.prev_btn, 3)
        btnbox.addWidget(self.log_cnt_le, 4)
        btnbox.addWidget(self.next_btn, 5)

        vbox.addLayout(btnbox, 2)

        self.setLayout(vbox)

        self.show()

    def load_file(self, fname, pos):
        self.tb.clear()
        log_cnt_txt = self.log_cnt_le.text()
        try:
            self.log_cnt = int(log_cnt_txt)
        except ValueError:
            self.log_cnt_le.setText(str(self.log_cnt))

        ret = geolo_view.read_log(fname, pos, self.log_cnt, 
                date=self.filter_date.text(),
                lv=self.filter_lv.text(),
                qlabel=self.filter_qlabel.text(),
                md=self.filter_md.text(),
                msg=self.filter_msg.text())
        self.tb.append(ret["log"])
        return ret["pos"];

    def apply_filter(self):
        if self.fname != "":
            self.prev_pos = 0
            self.next_pos = self.load_file(self.fname, 0)
            scrollBar = self.tb.verticalScrollBar()
            scrollBar.setValue(0)

    def prev_logs(self):
        if self.fname != "":
            self.next_pos = self.load_file(self.fname, self.prev_pos)
            self.prev_pos = self.pos_list[-2]
            self.pos_list.pop()
            scrollBar = self.tb.verticalScrollBar()
            scrollBar.setValue(scrollBar.maximum())

    def next_logs(self):
        if self.fname != "":
            self.prev_pos = self.pos_list[-1]
            self.pos_list.append(self.next_pos)
            self.next_pos = self.load_file(self.fname, self.next_pos)
            scrollBar = self.tb.verticalScrollBar()
            scrollBar.setValue(0)

    def find_next(self):
        text = self.tb.toPlainText()
        query = self.find_le.text()
        pattern = re.compile(query,0)

        start = (self.find_pos_list[-1] + 1) if len(self.find_pos_list) != 0 else 0

        match = pattern.search(text,start)

        if match:
            start = match.start()
            end = match.end()

            c = self.tb.textCursor()
            c.setPosition(start)
            c.setPosition(end, QTextCursor.KeepAnchor)
            self.tb.setTextCursor(c)
            self.find_pos_list.append(start)
        else:
            self.tb.moveCursor(QTextCursor.End)

    def find_prev(self):
        text = self.tb.toPlainText()
        query = self.find_le.text()
        pattern = re.compile(query,0)

        self.find_pos_list.pop()
        start = (self.find_pos_list[-1]) if len(self.find_pos_list) != 0 else 0

        match = pattern.search(text,start)

        if match:
            start = match.start()
            end = match.end()

            c = self.tb.textCursor()
            c.setPosition(start)
            c.setPosition(end, QTextCursor.KeepAnchor)
            self.tb.setTextCursor(c)
        else:
            self.tb.moveCursor(QTextCursor.End)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_wg = MainWidget("")
        self.setCentralWidget(self.main_wg)

        # File chooser
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.showFileDlg)

        # Edit filter
        openEdit = QAction(QIcon('edit.png'), 'Edit filter', self)
        openEdit.setShortcut('Ctrl+E')
        openEdit.triggered.connect(self.showEditDlg)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(openEdit)

        self.setWindowTitle('earth log viewer')
        self.setGeometry(100, 300, 1200, 1000)
        self.show()

    def showFileDlg(self):
        fnames = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.main_wg.load_file(fnames[0], 0)
        self.main_wg.fname = fnames[0]

    def showEditDlg(self):
        filter_str = EditDialog.getFilter(self);
        self.main_wg.tb.append(filter_str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
