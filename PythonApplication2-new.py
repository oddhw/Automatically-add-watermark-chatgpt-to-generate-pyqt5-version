import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QGridLayout, QSizePolicy, QRadioButton, QButtonGroup, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("添加水印")
        self.setWindowIcon(QIcon("path_to_your_icon.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setSpacing(0)

        self.watermark_path = ""
        self.image_paths = []
        self.output_folder = ""
        self.watermark_position = "education"

        self.buttonGroup = QButtonGroup(self)
        self.button1 = QRadioButton('教育')
        self.button1.setIcon(QIcon("path_to_button1_icon.png"))
        self.button1.setChecked(True)
        self.button1.toggled.connect(self.onClicked)
        self.layout.addWidget(self.button1, 0, 0)

        self.button2 = QRadioButton('餐饮')
        self.button2.setIcon(QIcon("path_to_button2_icon.png"))
        self.button2.toggled.connect(self.onClicked)
        self.layout.addWidget(self.button2, 0, 1)

        self.buttonGroup.addButton(self.button1)
        self.buttonGroup.addButton(self.button2)

        self.watermark_label = QLabel()
        self.layout.addWidget(self.watermark_label, 1, 0)

        self.watermark_button = QPushButton("选择水印图片")
        self.watermark_button.setIcon(QIcon("path_to_button3_icon.png"))
        self.watermark_button.clicked.connect(self.select_watermark)
        self.layout.addWidget(self.watermark_button, 2, 0)

        self.image_button = QPushButton("选择图片")
        self.image_button.setIcon(QIcon("path_to_button4_icon.png"))
        self.image_button.clicked.connect(self.select_images)
        self.layout.addWidget(self.image_button, 2, 1)

        self.folder_label = QLabel()
        self.layout.addWidget(self.folder_label, 3, 0)

        self.folder_button = QPushButton("选择输出文件夹")
        self.folder_button.setIcon(QIcon("path_to_button5_icon.png"))
        self.folder_button.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.folder_button, 4, 0)

        self.start_button = QPushButton("开始添加水印")
        self.start_button.setIcon(QIcon("path_to_button6_icon.png"))
        self.start_button.clicked.connect(self.start_watermarking)
        self.layout.addWidget(self.start_button, 4, 1)

        self.central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.watermark_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.folder_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.start_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.central_widget.setLayout(self.layout)
        self.setMinimumSize(500, 500)
        self.show()

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.watermark_position = radioButton.text()

    def select_watermark(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PNG files (*.png)")
        if file_dialog.exec():
            self.watermark_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(self.watermark_path)
            self.watermark_label.setPixmap(pixmap.scaled(128, 128, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

    def select_images(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Image files (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if file_dialog.exec():
            self.image_paths = file_dialog.selectedFiles()
            self.image_button.setIcon(QIcon('path_to_image_icon.ico'))

    def select_output_folder(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        if file_dialog.exec():
            self.output_folder = file_dialog.selectedFiles()[0]
            self.folder_button.setIcon(QIcon('path_to_folder_icon.ico'))
            self.folder_label.setText(self.output_folder)

    def start_watermarking(self):
        watermark = Image.open(self.watermark_path).convert("RGBA")
        for image_path in self.image_paths:
            base_image = Image.open(image_path).convert("RGBA")

            base_width, base_height = base_image.size
            watermark_width, watermark_height = watermark.size
            if self.watermark_position == "餐饮":
                scale = max(base_width / watermark_width / 5, base_height / watermark_height / 5)
            else:
                scale = max(base_width / watermark_width, base_height / watermark_height)
            watermark = watermark.resize((int(watermark_width * scale), int(watermark_height * scale)))

            if self.watermark_position == "教育":
                position = ((base_width - watermark.width) // 2, (base_height - watermark.height) // 2)
            else:
                position = ((base_width - watermark.width) // 2, int(base_height * 0.8) - (watermark.height // 2))

            base_image.paste(watermark, position, watermark)

            output_path = self.output_folder + "/" + image_path.split("/")[-1].split(".")[0] + "_watermarked.png"
            base_image.save(output_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
