import unittest
import block_markdown as b


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(b.markdown_to_blocks(""), [])

    def test_single_line(self):
        self.assertListEqual(b.markdown_to_blocks("line 1"), ["line 1"])

    def test_double_lines(self):
        self.assertListEqual(b.markdown_to_blocks("line 1\nline 2"), ["line 1\nline 2"])

    def test_single_line_with_blank_rows(self):
        self.assertListEqual(b.markdown_to_blocks("\n\nline 1\n\n\n\n"), ["line 1"])

    def test_multiple_lines(self):
        markdown_text = "# This is a heading\n"
        markdown_text += "\n"
        markdown_text += "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
        markdown_text += "\n"
        markdown_text += "* This is the first list item in a list block\n"
        markdown_text += "* This is a list item\n"
        markdown_text += "* This is another list item\n"
        
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertListEqual(b.markdown_to_blocks(markdown_text), expected_blocks)
        
    def test_bootdev_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = b.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = b.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
        
        
if __name__ == "__main__":
    unittest.main()
