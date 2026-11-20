from pathlib import Path
import pprint

files = [f"raw_html_files/{f.name}" for f in Path("raw_html_files").iterdir() if f.is_file()]

# Prints valid Python list syntax formatted neatly
print("files =", pprint.pformat(files))

