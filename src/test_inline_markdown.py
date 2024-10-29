import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_nodes_to_be_returned_as_is(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        split_nodes = split_nodes_delimiter([node, node], "*", TextType.BOLD)
        self.assertEqual([node, node], split_nodes)
        
    def test_single_delimited(self):
        # Test multiple words
        node = TextNode("*bold text*", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual([TextNode("bold text", TextType.BOLD)], split_nodes)

        # Test single words
        node = TextNode("*boldtext*", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual([TextNode("boldtext", TextType.BOLD)], split_nodes)

    def test_multiple_delimited1(self):
        node = TextNode(
            "standard text *some bold text* standard *bold_text* more_standard",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("standard text ", TextType.TEXT),
                TextNode("some bold text", TextType.BOLD),
                TextNode( " standard ", TextType.TEXT),
                TextNode("bold_text", TextType.BOLD),
                TextNode(" more_standard", TextType.TEXT),
            ],
            split_nodes,
        )
        
    def test_multiple_delimited2(self):
        node1 = TextNode(
            "standard text *some bold text* standard *bold_text* more_standard",
            TextType.TEXT,
        )
        node2 = TextNode(
            "standard text",
            TextType.TEXT,
        )
        node3 = TextNode(
            "standard text *some* *more bold*",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node1, node2, node3], "*", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("standard text ", TextType.TEXT),
                TextNode("some bold text", TextType.BOLD),
                TextNode(" standard ", TextType.TEXT),
                TextNode("bold_text", TextType.BOLD),
                TextNode(" more_standard", TextType.TEXT),
                TextNode("standard text", TextType.TEXT),
                TextNode("standard text ", TextType.TEXT),
                TextNode("some", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
            ],
            split_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
