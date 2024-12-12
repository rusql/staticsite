import unittest

from inline_markdown import (
    extract_markdown_links,
    split_nodes_delimiter,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


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
                TextNode(" standard ", TextType.TEXT),
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_match(self):
        markdown_images = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif"
        )  # missing close brace at end
        self.assertListEqual([], markdown_images)

    def test_single_match(self):
        markdown_images = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")], markdown_images
        )

    def test_dual_match(self):
        markdown_images = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            markdown_images,
        )

    def test_boot_dev(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_no_match(self):
        markdown_links = extract_markdown_links(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif"
        )  # missing close brace at end
        self.assertListEqual([], markdown_links)

    def test_single_match(self):
        markdown_links = extract_markdown_links(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")], markdown_links
        )

    def test_dual_match(self):
        markdown_links = extract_markdown_links(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            markdown_links,
        )

    def test_boot_dev(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_link_at_start(self):
        matches = extract_markdown_links(
            "[link at start](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link at start", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    class TestSplitNodes(unittest.TestCase):
        def test_split_image(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode(
                        "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                    ),
                ],
                new_nodes,
            )

        def test_split_image_single(self):
            node = TextNode(
                "![image](https://www.example.COM/IMAGE.PNG)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode(
                        "image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"
                    ),
                ],
                new_nodes,
            )

        def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode(
                        "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                    ),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image",
                        TextType.IMAGE,
                        "https://i.imgur.com/3elNhQu.png",
                    ),
                ],
                new_nodes,
            )

        def test_split_links(self):
            node = TextNode(
                "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                    TextNode(" with text that follows", TextType.TEXT),
                ],
                new_nodes,
            )


if __name__ == "__main__":
    unittest.main()
