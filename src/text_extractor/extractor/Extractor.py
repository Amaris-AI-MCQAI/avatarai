from abc import ABC, abstractmethod
from ..constants import (
    EXPORT_DIR,
    EXTRACTOR_MODE_DOC,
    SOURCE_DIR_DOC,
    SOURCE_DIR_WEB
)
import os
import re
import yaml

class Extractor(ABC):
    mode: str 
    @abstractmethod
    def read_input(self, filepath):
        pass

    def handle_file_paths_in_text_file(self, filename, source_dir, output_dict: dict) -> dict:
        output = []
        filepath_full = os.path.join(source_dir, filename)
        with open(filepath_full, "r") as stream:
            try:
                output = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        
        for path in output["paths"]:
            key = os.path.basename(path) if self.mode == EXTRACTOR_MODE_DOC else path.replace("/", "_")
            output_dict[key] = self.read_input(path)
        
        return output_dict

    def scrap_for_content(self) -> dict:
        source_path = SOURCE_DIR_DOC if self.mode == EXTRACTOR_MODE_DOC else SOURCE_DIR_WEB
        output_dict = {}
        for filename in os.listdir(source_path):
            if os.path.basename(filename) == "paths.yml":
                output_dict = self.handle_file_paths_in_text_file(filename, source_path, output_dict)
            else:
                key = os.path.basename(filename)
                output_dict[key] = self.read_input(filename)
            return output_dict

    def export_text(self):
        print(EXPORT_DIR)
        try:
            os.mkdir(EXPORT_DIR)
        except:
            pass
        for filename, text in self.scrap_for_content().items():
            output_filepath = os.path.join(EXPORT_DIR, "%s.txt" % filename)
            with open(output_filepath, "w") as stream:
                stream.write(text)

    @abstractmethod
    def process_raw_text(self, text):
        pass


