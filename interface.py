import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.setWindowTitle("Welcome Window")

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QtWidgets.QLabel("Select Input Data File:")
        self.file_path_label = QtWidgets.QLabel()
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)
        
        # add photo
        # self.image_label = QtWidgets.QLabel()
        # self.pixmap = QtGui.QPixmap("GroupProject/Trainers.png")
        # self.image_label.setPixmap(self.pixmap)
        
        self.image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("GroupProject/Trainers.jpg")
        self.image_label.setPixmap(pixmap)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.file_path_label)
        vbox.addWidget(self.browse_button)

        self.central_widget.setLayout(vbox)

    def browse(self):
        # file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "XLSX Files (*.xlsx)")
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(self.file_path)
            self.hide()
            self.function_window = FunctionWindow(self.file_path)
            self.function_window.show()

class FunctionWindow(QtWidgets.QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Function Window")
        self.file_path = file_path

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QtWidgets.QLabel(f"File Path: {self.file_path}")
        self.spatial_temporal_analysis_button = QtWidgets.QPushButton("Spatial Temporal Analysis")
        self.network_resilience_analysis_button = QtWidgets.QPushButton("Network Resilience Analysis")
        self.model_uncertainty_button = QtWidgets.QPushButton("Model Uncertainty")
        self.shortest_path_analysis_button = QtWidgets.QPushButton("Shortest Path Analysis")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.spatial_temporal_analysis_button)
        vbox.addWidget(self.network_resilience_analysis_button)
        vbox.addWidget(self.model_uncertainty_button)
        vbox.addWidget(self.shortest_path_analysis_button)

        self.central_widget.setLayout(vbox)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())

