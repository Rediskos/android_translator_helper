import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from Translator import *


class FileBrowserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.translation_holder = None
        self.setWindowTitle('Translator')

        # Line edits to display file paths
        self.le_blueprint_path = QLineEdit()
        self.le_translation_csv_path = QLineEdit()
        self.le_output_path = QLineEdit()
        self.l_chosen_language = QLabel()
        self.l_chosen_language.setText("Chosen language: ")

        # Buttons for browsing files
        self.btn_browse_blueprint = QPushButton('Browse')
        self.btn_browse_blueprint.clicked.connect(lambda: self.browse_file(self.le_blueprint_path))

        self.btn_browse_translation = QPushButton('Browse')
        self.btn_browse_translation.clicked.connect(lambda: self._browse_translation_file(self.le_translation_csv_path))

        self.btn_output_path_browse = QPushButton("Browse")
        self.btn_output_path_browse.clicked.connect(lambda: self.browse_file(self.le_output_path))

        self.btn_translate = QPushButton("Translate")
        self.btn_translate.clicked.connect(lambda: self.translate_lang())

        self.btn_open_translated_file = QPushButton("Open file with translation")
        self.btn_open_translated_file.clicked.connect(lambda: os.startfile(self.le_output_path.text()))
        self.btn_open_translated_file.setVisible(False)

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

        # creating a QListWidget
        self.list_widget = QListWidget(self)

        self.list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Always show horizontal scrollbar
        self.list_widget.setFlow(QListWidget.LeftToRight)  # Set items flow from left to right
        self.list_widget.setWrapping(False)  # No wrapping
        self.list_widget.setResizeMode(QListWidget.Adjust)  # Adjust size to content

        layout.addLayout(blueprint_layout)
        layout.addLayout(translation_layout)
        layout.addWidget(self.l_chosen_language)
        layout.addWidget(self.list_widget)
        layout.addLayout(output_layout)
        layout.addWidget(self.btn_translate)
        layout.addWidget(self.btn_open_translated_file)

        self.setLayout(layout)
        self.setGeometry(600, 100, 400, 200)
        self.show()

    def browse_file(self, lineedit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            lineedit.setText(file_path)
            return True
        else:
            return False

    def _browse_translation_file(self, lineedit):
        if self.browse_file(lineedit):
            self.translation_holder = TranslationsHolder(self.le_translation_csv_path.text())
            self._validate_available_langs()

    def _validate_available_langs(self):
        self.list_widget.clear()
        for i in self.translation_holder.available_langs:
            item = QListWidgetItem(f"Item {i}")
            button = QPushButton()
            button.setText(i)
            button.clicked.connect(lambda _, new_lang=i: self._new_language_choosen(new_lang))
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, button)

    def translate_lang(self):
        translator = AndroidXmlLanguageTranslator(self.le_blueprint_path.text(), self.translation_holder)
        translator.print_translated_xml(self.le_output_path.text())
        self.btn_open_translated_file.setVisible(True)

    def _new_language_choosen(self, new_lang):
        self.translation_holder.set_new_lang(new_lang)
        self.l_chosen_language.setText(f"Chosen language: {new_lang}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileBrowserApp()
    sys.exit(app.exec_())
