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
        
        
class TestBlockToBlockType(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(b.block_to_block_type("a"), b.BlockType.PARAGRAPH)
        
    def test_headings(self):
        self.assertEqual(b.block_to_block_type('# aa\n# ff'), b.BlockType.HEADING1)
        self.assertEqual(b.block_to_block_type('## aa'), b.BlockType.HEADING2)
        self.assertEqual(b.block_to_block_type('### ss'), b.BlockType.HEADING3)
        self.assertEqual(b.block_to_block_type('#### aa'), b.BlockType.HEADING4)
        self.assertEqual(b.block_to_block_type('##### aa'), b.BlockType.HEADING5)
        self.assertEqual(b.block_to_block_type('###### aa'), b.BlockType.HEADING6)
        self.assertEqual(b.block_to_block_type('######aa'), b.BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(b.block_to_block_type('``` aa\n ff\n hhh\nbbb```'), b.BlockType.CODE)
        self.assertEqual(b.block_to_block_type('``` aa\n ff\n hhh\n```'), b.BlockType.CODE)
        self.assertEqual(b.block_to_block_type('``` \n ff\n hhh\n```'), b.BlockType.CODE)

    def test_quote(self):
        self.assertEqual(b.block_to_block_type('> aa\n> ff\n> hhh\n>bbb\n>```'), b.BlockType.QUOTE)
        self.assertEqual(b.block_to_block_type('> aa\n> ff\n> hhh\n>bbb\n```'), b.BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(b.block_to_block_type('* item1\n* item2\n* item3'), b.BlockType.UNORDERED_LIST)
        self.assertEqual(b.block_to_block_type('* item1\nitem2\n* item3'), b.BlockType.PARAGRAPH)
        
    def test_ordered_list(self):
        self.assertEqual(b.block_to_block_type('1. item1\n2. item2\n3. item3'), b.BlockType.ORDERED_LIST)
        self.assertEqual(b.block_to_block_type('1. item1\n4. item2\n3. item3'), b.BlockType.PARAGRAPH)
        self.assertEqual(b.block_to_block_type('1. item1'), b.BlockType.ORDERED_LIST)
        
if __name__ == "__main__":
    unittest.main()
