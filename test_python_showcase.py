import unittest

from python_showcase import analyze_text, extract_words


class TextAnalysisTests(unittest.TestCase):
    def test_extract_words_normalizes_case_and_punctuation(self) -> None:
        self.assertEqual(
            extract_words("Hello, WORLD! Don't forget Python."),
            ["hello", "world", "don't", "forget", "python"],
        )

    def test_analyze_text_returns_expected_statistics(self) -> None:
        stats = analyze_text("Python is great. Python is clear.")

        self.assertEqual(stats.words, 6)
        self.assertEqual(stats.unique_words, 4)
        self.assertEqual(stats.most_common_word, "is")

    def test_analyze_empty_text(self) -> None:
        stats = analyze_text("")

        self.assertEqual(stats.words, 0)
        self.assertEqual(stats.longest_word, "")
        self.assertEqual(stats.most_common_word, "")

    def test_analyze_text_rejects_non_string_input(self) -> None:
        with self.assertRaises(TypeError):
            analyze_text(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
