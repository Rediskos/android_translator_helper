import sys
from PyQt5.QtWidgets import *
from Translator import *


class FileBrowserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Browser')

        # Line edits to display file paths
        self.le_blueprint_path = QLineEdit()
        self.le_translation_csv_path = QLineEdit()
        self.le_output_path = QLineEdit()

        # Buttons for browsing files
        self.btn_browse_blueprint = QPushButton('Browse')
        self.btn_browse_blueprint.clicked.connect(lambda: self.browse_file(self.le_blueprint_path))

        self.btn_browse_translation = QPushButton('Browse')
        self.btn_browse_translation.clicked.connect(lambda: self.browse_file(self.le_translation_csv_path))

        self.btn_output_path_browse = QPushButton("Browse")
        self.btn_output_path_browse.clicked.connect(lambda: self.browse_file(self.le_output_path))

        self.btn_translate = QPushButton("Translate")
        self.btn_translate.clicked.connect(lambda: self.translate_lang())

        self.lb_blueprint = QLabel()
        self.lb_blueprint.setText("файл xml со структурой перевода")
        self.lb_translation_file = QLabel()
        self.lb_translation_file.setText("файл csv с переводом")
        self.lb_output_path = QLabel()
        self.lb_output_path.setText("вывод")

        # Layout
        layout = QVBoxLayout()

        # File 1 layout
        blueprint_layout = QHBoxLayout()
        blueprint_layout.addWidget(self.lb_blueprint)
        blueprint_layout.addWidget(self.le_blueprint_path)
        blueprint_layout.addWidget(self.btn_browse_blueprint)

        # File 2 layout
        translation_layout = QHBoxLayout()
        translation_layout.addWidget(self.lb_translation_file)
        translation_layout.addWidget(self.le_translation_csv_path)
        translation_layout.addWidget(self.btn_browse_translation)

        # output layout
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.lb_output_path)
        output_layout.addWidget(self.le_output_path)
        output_layout.addWidget(self.btn_output_path_browse)

        layout.addLayout(blueprint_layout)
        layout.addLayout(translation_layout)
        layout.addLayout(output_layout)
        layout.addWidget(self.btn_translate)

        self.setLayout(layout)
        self.show()

    def browse_file(self, lineedit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            lineedit.setText(file_path)

    def translate_lang(self):
        translator_holder = TranslationsHolder(self.le_translation_csv_path.text())
        translator = AndroidXmlLanguageTranslator(self.le_blueprint_path.text(), translator_holder)
        translator.print_translated_xml(self.le_output_path.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileBrowserApp()
    sys.exit(app.exec_())
