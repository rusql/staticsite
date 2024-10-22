import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_false3(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://test.test")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://test.test")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://test.test")
        self.assertEqual(
            "TextNode(This is a text node, text, https://test.test)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("my text", TextType.TEXT)
        self.assertEqual(LeafNode(value="my text"), text_node_to_html_node(text_node))

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("my text", TextType.BOLD)
        self.assertEqual(
            LeafNode(value="my text", tag="b"), text_node_to_html_node(text_node)
        )

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("my text", TextType.ITALIC)
        self.assertEqual(
            LeafNode(value="my text", tag="i"), text_node_to_html_node(text_node)
        )

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("my code", TextType.CODE)
        self.assertEqual(
            LeafNode(value="my code", tag="code"), text_node_to_html_node(text_node)
        )

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("my link", TextType.LINK, url="https://myurl.com")
        self.assertEqual(
            LeafNode(value="my link", tag="a", props={"href": "https://myurl.com"}),
            text_node_to_html_node(text_node),
        )

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("my image", TextType.IMAGE, url="https://myimageurl.com")
        leaf_node = LeafNode(
            value="",
            tag="img",
            props={
                "src": "https://myimageurl.com",
                "alt": "my image",
            },
        )
        self.assertEqual(
            leaf_node,
            text_node_to_html_node(text_node),
        )


if __name__ == "__main__":
    unittest.main()
