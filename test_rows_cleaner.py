"""Tests for rows_cleaner.py. Run from the project folder: python -m unittest -q test_rows_cleaner

Most inputs are real words and lines from chapters_rows/.
"""
import json
import tempfile
import unittest
from pathlib import Path

from rows_cleaner import clean_rows, clean_words, main


class CleanWordsTest(unittest.TestCase):
    def test_vowel_points_and_verse_end_are_removed(self):
        self.assertEqual(clean_words(["בְרָא", "אַרעָא׃", "ישׂראל"]), ["ברא", "ארעא", "ישראל"])

    def test_matches_cal_with_manuscript_variants_hidden(self):
        # Onkelos Genesis 1:2 as chapters_parser.py saved it, and as CAL shows it with
        # "Hide manuscript variants" (stripped of vowel points).
        line = ["וְאַרעָא", "הֲוָת", "צָדיָא", "וְרוֹקָניָא", "וַחֲשוֹכָא", "<פריש#3#>", "עַל", "אַפֵי",
                "תְהוֹמָא", "וְרוּחָא", "\\", "מִן", "קֳדָם", "יוי", "/דייי#3#/", "מְנַשבָא",
                "/מתנשבא#3#/", "עַל", "אַפֵי", "מַיָא׃"]
        expected = "וארעא הות צדיא ורוקניא וחשוכא פריש על אפי תהומא ורוחא מן קדם יוי מנשבא על אפי מיא"
        self.assertEqual(clean_words(line), expected.split())

    def test_chained_readings_are_removed(self):
        self.assertEqual(clean_words(["מְהַלֵיך", "/דמהליך#3#/דמדבר#3#/", "לְמַדִינחָא"]),
                         ["מהליך", "למדינחא"])

    def test_reading_of_several_words_is_removed(self):
        self.assertEqual(clean_words(["דְמֵיעַל", "/דמלעיל#3#/", "די", "מלעילי#3#/", "לִרקִיעָא"]),
                         ["דמיעל", "לרקיעא"])

    def test_chain_does_not_swallow_main_text_up_to_a_later_addition(self):
        # Onkelos Genesis 6:4 (shortened). Only "/די עלין#3#/" and "/מנהון#3#/" are variants:
        # CAL keeps "להון", the first reading of the editor's addition, in the text.
        line = ["דְעָלִין", "/די", "עלין#3#/", "בְנֵי", "רַברְבַיָא", "וְיָלְדָן", "<לְהוֹן#3#/מנהון#3#/>", "אִנוּן"]
        self.assertEqual(clean_words(line), ["דעלין", "בני", "רברביא", "וילדן", "להון", "אנון"])

    def test_reading_whose_tag_is_followed_by_a_space_is_removed(self):
        # Targum Jonathan, Joshua 6:3 (shortened): two readings of manuscript 3 for the three
        # words after "\", the first one closed by "#3# /" instead of "#3#/".
        line = ["כָל", "\\", "גֻברֵי", "עָבְדֵי", "קְרָבָא", "/גֻברֵי", "מגיחי", "קְרָבָא#3#", "/גיברי",
                "חילא", "דקרבא#3#/", "אַקֵיף"]
        self.assertEqual(clean_words(line), ["כל", "גברי", "עבדי", "קרבא", "אקיף"])

    def test_main_text_between_two_readings_is_kept(self):
        self.assertEqual(clean_words(["כהדן", "/כהדין#2#/", "קנדילה", "/קנתילא#2#/"]),
                         ["כהדן", "קנדילה"])

    def test_letter_variant_inside_a_word_is_removed(self):
        self.assertEqual(clean_words(["לא֗י/ו/֗", "מד!֗ו/ר/֗ח!קיה;"]), ["לאי", "מדוחקיה"])

    def test_deleted_text_is_removed_and_its_replacement_kept(self):
        # Deleted by the scribe, who wrote the replacement above the line.
        self.assertEqual(clean_words(["{{דהכן}}^דהדין^"]), ["דהדין"])
        # Deleted and corrected by the editor, following manuscript 03.
        self.assertEqual(clean_words(["{טיבא}<טבייא>#03#"]), ["טבייא"])
        self.assertEqual(clean_words(["ה{{ן}}<א>", "תנשיי{א}ן"]), ["הא", "תנשיין"])

    def test_deletion_spanning_several_words(self):
        self.assertEqual(clean_words(["{דלא", "אית}", "<דלית>"]), ["דלית"])

    def test_added_restored_and_interlinear_text_is_kept(self):
        self.assertEqual(clean_words(["[גר]מה", "ש<משא>", "ה^י^כא"]), ["גרמה", "שמשא", "היכא"])

    def test_marks_on_letters_are_removed_but_letters_kept(self):
        # Doubtful-letter dot, abbreviation mark, quotation marks, illegible-letter placeholder,
        # uncertain-letter ring.
        self.assertEqual(clean_words(["כהנ֗י֗", "אימ׳;", '"שחרית";', "ברי֗ש֗<א٠٠>", "שמ̊̊ואל"]),
                         ["כהני", "אימ", "שחרית", "ברישא", "שמואל"])

    def test_alternatives_that_cal_keeps_in_the_text_become_two_words(self):
        self.assertEqual(clean_words(["<גבר#3#/גִיבָר#3#>"]), ["גבר", "גיבר"])

    def test_maqaf_separates_words(self):
        self.assertEqual(clean_words(["כל־אנשא", "להו־;"]), ["כל", "אנשא", "להו"])

    def test_numbers_and_latin_are_removed(self):
        self.assertEqual(clean_words(["כה׳<25>", "F3", "#41ּ728#"]), ["כה"])

    def test_line_with_no_letters_becomes_empty(self):
        self.assertEqual(clean_words(["٠٠٠", "\\", "/#3#/"]), [])


class CleanRowsTest(unittest.TestCase):
    def test_keeps_labels_and_drops_lines_left_empty(self):
        rows = {"01:01 )1( ": ["בְרָא", "٠٠٠"], "01:02 )1( ": ["٠٠٠"], "01:03 )1( ": ["יוי"]}
        self.assertEqual(clean_rows(rows), {"01:01 )1( ": ["ברא"], "01:03 )1( ": ["יוי"]})


class MainTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.input_folder = Path(self.temp.name) / "rows"
        self.input_folder.mkdir()
        self.input_file = self.input_folder / "51001_ TgO Gn01.json"
        self.input_file.write_text(
            json.dumps({"01:01 )1( ": ["בְרָא", "/ברא#3#/"], "01:02 )1( ": ["٠٠٠"]}, ensure_ascii=False),
            encoding="utf-8")

    def test_writes_cleaned_file_with_same_name_and_leaves_input_alone(self):
        before = self.input_file.read_bytes()
        output_folder = self.input_folder / "clean"
        main(self.input_folder, output_folder)
        written = json.loads((output_folder / self.input_file.name).read_text(encoding="utf-8"))
        self.assertEqual(written, {"01:01 )1( ": ["ברא"]})
        self.assertEqual(self.input_file.read_bytes(), before)

    def test_refuses_to_write_into_the_input_folder(self):
        with self.assertRaises(SystemExit):
            main(self.input_folder, self.input_folder)

    def test_refuses_an_input_folder_without_json_files(self):
        empty = Path(self.temp.name) / "empty"
        empty.mkdir()
        with self.assertRaises(SystemExit):
            main(empty, Path(self.temp.name) / "out")


if __name__ == "__main__":
    unittest.main()
