import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("你的应用名称")
        self.setWindowIcon(QIcon("path_to_your_icon.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setSpacing(0)  # 设置按钮之间的间距为0

        self.watermark_path = ""
        self.image_paths = []
        self.output_folder = ""

        button1 = QPushButton("选择水印图片")
        button1.clicked.connect(self.select_watermark)
        self.layout.addWidget(button1, 0, 0, 1, 1)  # 设置按钮占据第一行第一列的位置

        button2 = QPushButton("选择图片")
        button2.clicked.connect(self.select_images)
        self.layout.addWidget(button2, 0, 1, 1, 1)  # 设置按钮占据第一行第二列的位置

        button3 = QPushButton("选择输出文件夹")
        button3.clicked.connect(self.select_output_folder)
        self.layout.addWidget(button3, 1, 0, 1, 1)  # 设置按钮占据第二行第一列的位置

        button4 = QPushButton("开始添加水印")
        button4.clicked.connect(self.start_watermarking)
        self.layout.addWidget(button4, 1, 1, 1, 1)  # 设置按钮占据第二行第二列的位置

        # 设置按钮的高度和宽度均分整个页面的四分之一
        self.central_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.central_widget.setLayout(self.layout)
        self.setMinimumSize(500, 500)
        self.show()

    def select_watermark(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PNG files (*.png)")
        if file_dialog.exec_():
            self.watermark_path = file_dialog.selectedFiles()[0]

    def select_images(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            self.image_paths = file_dialog.selectedFiles()

    def select_output_folder(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        if file_dialog.exec_():
            self.output_folder = file_dialog.selectedFiles()[0]

    def start_watermarking(self):
        watermark = Image.open(self.watermark_path).convert("RGBA")
        for image_path in self.image_paths:
            base_image = Image.open(image_path).convert("RGBA")

            base_width, base_height = base_image.size
            watermark_width, watermark_height = watermark.size
            scale = max(base_width / watermark_width, base_height / watermark_height)
            watermark = watermark.resize((int(watermark_width * scale), int(watermark_height * scale)))

            position = ((base_width - watermark.width) // 2, (base_height - watermark.height) // 2)
            base_image.paste(watermark, position, watermark)

            output_path = self.output_folder + "/" + image_path.split("/")[-1].split(".")[0] + "_watermarked.png"
            base_image.save(output_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
