import csv
import os.path
import xml.etree.ElementTree as ET
import re


class MyDialect(csv.Dialect):
    lineterminator = '\n'
    delimiter = ','
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL


class TranslationsHolder:
    translations_name_to_body = {}
    translations_body_to_body = {}
    available_langs = []

    def __init__(self, path_to_translations_file, default_lang="en", etalon_lang="ru"):
        self.lang = default_lang
        self.path_to_translations_file = path_to_translations_file
        self.etalon_lang = etalon_lang
        self._read_new_lang()

    def set_new_lang(self, new_lang):
        print(new_lang)
        if new_lang in self.available_langs:
            self.lang = new_lang
            self._read_new_lang()
        else:
            raise Exception("This lang not available")

    def new_translations_file(self, new_translations_file_path):
        self.path_to_translations_file = new_translations_file_path
        self._read_new_lang()

    def _read_new_lang(self):
        with open(self.path_to_translations_file, newline='', encoding='utf-8') as translationsFile:
            dialect = csv.Dialect
            dialect.delimiter = ';'
            self.translations_name_to_body = {}
            self.translations_body_to_body = {}
            pattern = r"#[A-Fa-f0-9]+"
            reader = csv.DictReader(translationsFile, dialect=MyDialect)
            self.available_langs = reader.fieldnames
            for row in reader:
                name = row["name"].replace(".", "_").replace("\"", "").replace(" ", "_")
                body = row[self.lang].replace(r"\'", r"'").replace(r"'", r"\'")
                color_match = re.findall(pattern, body)
                if color_match:
                    body = body.replace(color_match[0], "'{}'".format(color_match[0]))
                if name not in self.translations_name_to_body:
                    self.translations_name_to_body[name] = body

                etalon_body = row[self.etalon_lang].replace("\"", "").lower()
                if body and etalon_body not in self.translations_body_to_body:
                    self.translations_body_to_body[etalon_body] = body


class AndroidXmlLanguageTranslator:

    def __init__(self, path_to_xml_for_translating, translations_holder: TranslationsHolder):
        self.translationsHolder = translations_holder
        self.XmlForTranslationByLine = self.read_file_to_lines(path_to_xml_for_translating)
        self.defaultOutputFilePath = os.path.dirname(path_to_xml_for_translating)
        self.NOT_TRANSLATED = " <!--TODO: Not translated-->"

    def print_translated_xml(self, path_to_output_translation):
        with (open(path_to_output_translation, "w", encoding="utf-8") as new_file):
            for line in self.XmlForTranslationByLine:
                parsed = self.get_from_xml(line)

                if line == "":
                    new_file.write(line)
                    new_file.write("\n")
                    continue

                if parsed == False:
                    new_file.write(line)
                    if "<plurals" in line:
                        new_file.write(self.NOT_TRANSLATED)
                    new_file.write("\n")
                    continue

                try:
                    body = parsed.text.lower()
                except:
                    body = parsed.text

                try:
                    parsed.attrib["translatable"]
                    continue
                except:
                    pass

                try:
                    new_file.write(
                        "<string name=\"{}\">{}</string>".format(
                            parsed.attrib["name"],
                            self.translationsHolder.translations_body_to_body[body]
                        )
                    )
                except KeyError:
                    try:
                        new_file.write(
                            "<string name=\"{}\">{}</string>".format(
                                parsed.attrib["name"],
                                self.translationsHolder.translations_name_to_body[parsed.attrib["name"]]
                            )
                        )
                    except KeyError:
                        new_file.write(line)
                        if "item" not in line:
                            new_file.write(self.NOT_TRANSLATED)

                new_file.write("\n")

    def read_file_to_lines(self, path_to_file):
        print("reading " + path_to_file)
        with open(path_to_file, encoding="utf-8") as file:
            file_lines = [line.rstrip() for line in file]
        return file_lines

    def get_from_xml(self, string):
        try:
            return ET.fromstring(string)
        except:
            return False
