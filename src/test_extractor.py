import unittest
from extractor import *

class TestTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll","https://i.imgur.com/aKaOqIh.gif"), ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll","https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev","https://www.boot.dev"), ("to youtube","https://www.youtube.com/@bootdotdev")])

    def test_extract_title_good(self):
        text = "# i am title"
        extracted = extract_title(text)
        self.assertEqual(extracted, "i am title")

    def test_extract_title_bad(self):
        text = "## i am title"
        with self.assertRaises(ValueError):
            extract_title(text)

if __name__ == "__main__":
    unittest.main()
