import os
import datetime

SOURCE_DIR_DOC = os.path.join(os.getcwd(), "src", "data", "input", "docs")
SOURCE_DIR_WEB = os.path.join(os.getcwd(), "src", "data", "input", "websites")

EXPORT_DIR = os.path.join(os.getcwd(), "src", "data", "output", str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
EXTRACTOR_MODE_WEB = "web"
EXTRACTOR_MODE_DOC = "doc"