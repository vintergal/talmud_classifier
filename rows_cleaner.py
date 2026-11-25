"""Stage 5: clean the rows dictionaries that chapters_parser.py wrote.

Every JSON file in the input folder maps a line label to the words of that line. The cleaned copy
keeps only the text of the main manuscript, written in plain letters: readings of other
manuscripts, text marked as deleted, and every sign that is not a Hebrew letter (vowel points,
editorial brackets, punctuation, digits) are removed, and lines left with no words are dropped.
What each sign means comes from CAL's table of text signs: https://cal.huc.edu/prova.html

python rows_cleaner.py input_folder_path output_folder_path
"""
import json
import re
import sys
from pathlib import Path

# A reading from another manuscript, "/text#source#/". Readings can be chained ("/a#3#/b#3#/") and
# can span several words ("/a#3#/ b c#3#/"). Every reading ends in its source tag and a slash, which
# is what tells it apart from main text that sits between two variants (some readings have a space
# before that slash: "/a#2# /b#3#/"). A reading after the first may not contain brackets or "\":
# those mean the chain is over, and what follows is main text.
VARIANT_READINGS = re.compile(r"/[^/#]*#[^#/\s]*#\s*/(?:[^/#<>{}\[\]\\]*#[^#/\s]*#\s*/)*")
# A variant of a few letters inside a word, with no source tag, as in "לא֗י/ו/֗".
LETTER_VARIANT = re.compile(r"/[^/#\s]*/")
# Text deleted by the scribe "{{...}}" or by the editor "{...}". The double braces go first, so that
# "{{x}}" is not left behind as "{}".
SCRIBE_DELETION = re.compile(r"\{\{[^{}]*\}\}")
EDITOR_DELETION = re.compile(r"\{[^{}]*\}")
# The source of text the editor added, as in "<פריש#3#>". The added text itself stays.
SOURCE_TAG = re.compile(r"#[^#\s]*#")
# Signs that stand between two words: the maqaf, CAL's word divider, and a slash left between two
# readings that CAL keeps in the text, as in "<גבר#3#/גיבר#3#>".
WORD_SEPARATORS = re.compile(r"[־|/]")
# Anything that is not a Hebrew letter (alef U+05D0 to tav U+05EA) or whitespace.
NOT_A_LETTER = re.compile(r"[^א-ת\s]")


def clean_words(words):
    """Return the cleaned words of one line, in order. The list is empty if no letters are left."""
    # Clean the line as one string, because brackets and variants can span several words.
    line = " ".join(words)
    # A removed reading becomes a space, so the words on either side of it stay apart.
    line = VARIANT_READINGS.sub(" ", line)
    line = LETTER_VARIANT.sub("", line)
    line = SCRIBE_DELETION.sub("", line)
    line = EDITOR_DELETION.sub("", line)
    line = SOURCE_TAG.sub("", line)
    line = WORD_SEPARATORS.sub(" ", line)
    line = NOT_A_LETTER.sub("", line)
    return line.split()


def clean_rows(rows):
    """Clean every line of one chapter, keeping its label and dropping lines left empty."""
    cleaned_rows = {}
    for name, words in rows.items():
        cleaned_words = clean_words(words)
        if cleaned_words:
            cleaned_rows[name] = cleaned_words
    return cleaned_rows


def read_rows(input_file):
    with open(input_file, "r", encoding="utf-8") as file_to_read:
        try:
            rows = json.load(file_to_read)
        except json.JSONDecodeError as error:
            sys.exit(f"error: {input_file} is not valid JSON ({error})")
    if not isinstance(rows, dict):
        sys.exit(f"error: {input_file} does not hold a rows dictionary")
    return rows


def main(input_folder_path, output_folder_path):
    input_folder = Path(input_folder_path)
    output_folder = Path(output_folder_path)
    # The parser's files must never be overwritten.
    if output_folder.resolve() == input_folder.resolve():
        sys.exit("error: the output folder must be different from the input folder")
    input_files = sorted(input_folder.glob("*.json"))
    if not input_files:
        sys.exit(f"error: no .json files in {input_folder}")
    output_folder.mkdir(parents=True, exist_ok=True)

    lines_before = lines_after = words_before = words_after = 0
    for input_file in input_files:
        rows = read_rows(input_file)
        cleaned_rows = clean_rows(rows)
        with open(output_folder / input_file.name, "w", encoding="utf-8") as file_to_write:
            json.dump(cleaned_rows, file_to_write, ensure_ascii=False, indent=2)
        lines_before += len(rows)
        lines_after += len(cleaned_rows)
        words_before += sum(len(words) for words in rows.values())
        words_after += sum(len(words) for words in cleaned_rows.values())

    print(f"cleaned {len(input_files)} files into {output_folder}")
    print(f"lines: {lines_before} -> {lines_after}, words: {words_before} -> {words_after}")


# python rows_cleaner.py input_folder_path output_folder_path
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python rows_cleaner.py input_folder_path output_folder_path")
    main(input_folder_path=sys.argv[1], output_folder_path=sys.argv[2])
