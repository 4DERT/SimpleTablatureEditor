import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog, QMessageBox
from PyQt5 import QtCore
from ui_mainwindow import Ui_MainWindow

from GuitarProTools import GPTools

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = ""
        self.save_file_name = "Untilted"
        self.max_measure = 1

        self.check_boxes = []

        self.ui.button_ok.clicked.connect(lambda: self.load_gp_tools(True))
        self.ui.button_select.clicked.connect(self.load_file)
        self.ui.button_gp5.clicked.connect(lambda: self.save_file(False))
        self.ui.button_midi.clicked.connect(lambda: self.save_file(True))
        self.ui.button_external_editor.clicked.connect(self.open_in_external_editor)

        self.ui.spinBox_first.valueChanged.connect(self.update_measures_spinBoxes)
        self.ui.spinBox_second.valueChanged.connect(self.update_measures_spinBoxes)


    def create_error_dialog(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Something went wrong :(")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()


    def save_file(self, isMidi, fileName = None):
        m_start = self.ui.spinBox_first.value()
        m_stop = self.ui.spinBox_second.value()
        selected_tracks = []

        for i, box in self.check_boxes.items():
            if box.isChecked():
                selected_tracks.append(int(i))
        
        if selected_tracks == []:
            self.create_error_dialog("you have to choose tracks")
            return
        
        
        self.gp_tools.grep_track(*selected_tracks)
        self.gp_tools.grep_measures(m_start, m_stop)

        ext = ".midi" if isMidi else ".gp5"
        ext_filter = "Midi File (*.midi)" if isMidi else "Guitar Pro 5 File (*.gp5)"

        if fileName == None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",f"{self.save_file_name}{ext}",f"{ext_filter}", options=options)

        if fileName:
            if isMidi:
                self.gp_tools.save_as_midi(fileName, False)
            else:
                self.gp_tools.save_as_gp(fileName)
        self.load_gp_tools(False)
            

    def load_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","Guitar Pro 5 Files (*.gp5);;All Files (*)", options=options)
        if files:
            if len(files) == 1:
                self.ui.lineEdit_location.setText(files[0])
            else:
                self.create_error_dialog("Please selct only one file")
    

    def load_gp_tools(self, is_new = True):
        try:
            self.file = self.ui.lineEdit_location.text()
            self.gp_tools = GPTools(self.file)

            if is_new:
                # print information about song in main label
                info = self.gp_tools.get_song_info()
                info_msg = ""
                for name, spec in info.items():
                    if name == 'Tracks':
                        spec = len(spec)
                    info_msg += str(name) + ": " + str(spec) + "\n" if str(spec) != "" else ""
                self.ui.label_info.setText(info_msg)

                self.save_file_name = info['Title'] if info['Title'] != "" else "Untilted"

                self.create_check_boxes(info['Tracks'])
                self.max_measure = info['Measures']
                self.update_measures_spinBoxes()
                self.ui.spinBox_second.setValue(self.max_measure)
                self.ui.spinBox_first.setValue(1)
                self.ui.button_gp5.setEnabled(True)
                self.ui.button_midi.setEnabled(True)
                self.ui.button_external_editor.setEnabled(True)
                self.ui.spinBox_first.setEnabled(True)
                self.ui.spinBox_second.setEnabled(True)
            
        except ValueError:
            self.create_error_dialog("the file location is incorrect ")


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())


    def create_check_boxes(self, items: dict):
        self.clear_layout(self.ui.verticalLayout_2)
        self.check_boxes = {}

        box_select_all = QCheckBox(self.ui.widget_tracks)
        box_select_all.setText("Select all")
        box_select_all.stateChanged.connect(self.select_all_boxes)
        self.ui.verticalLayout_2.addWidget(box_select_all)

        for i, spec in items.items():
            title = str(i) + ". " + spec[0] + " (" + spec[1] + ")"
            check_box = QCheckBox(self.ui.widget_tracks)
            check_box.setText(title)
            self.check_boxes[i] = (check_box)
            self.ui.verticalLayout_2.addWidget(check_box)
        
        self.select_all_boxes(QtCore.Qt.Checked)
        box_select_all.setCheckState(QtCore.Qt.Checked)
    

    @QtCore.pyqtSlot(int)
    def select_all_boxes(self, state):
        block = False if state == QtCore.Qt.Checked else True
        for _, checkbox in self.check_boxes.items():
            checkbox.blockSignals(True)
            checkbox.setCheckState(state)
            checkbox.blockSignals(False)
            checkbox.setEnabled(block)
    

    def update_measures_spinBoxes(self):
        self.ui.spinBox_first.setMaximum(self.max_measure)
        self.ui.spinBox_second.setMaximum(self.max_measure)
        self.ui.spinBox_second.setMinimum(self.ui.spinBox_first.value())
        self.ui.spinBox_first.setMaximum(self.ui.spinBox_second.value())

    def open_in_external_editor(self):
        if sys.platform == "win32":
            path = "ste_tmp.gp5"
            opener = "start"
            shell = True
        else:   #linux
            path = "/tmp/ste_tmp.gp5"
            opener = "xdg-open"
            shell = False
        
        self.save_file(False, path)
        subprocess.call([opener, path], shell=shell)

def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()