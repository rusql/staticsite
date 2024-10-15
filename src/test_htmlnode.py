import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_single_property(self):
        node = HTMLNode(props={"href": "http://www.test.com"})
        self.assertEqual(' href="http://www.test.com"', node.props_to_html())

    def test_props_to_html_with_multiple_properties(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_props_to_html_with_no_properties(self):
        node = HTMLNode()
        self.assertEqual(
            "", node.props_to_html()
        )
        
    def test_repr_with_nothing_set(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(tag=None, value=None, children=None, props=None)", node.__repr__())
    
    def test_repr_with_tag_set(self):
        node = HTMLNode(tag="div")
        self.assertEqual('HTMLNode(tag=div, value=None, children=None, props=None)', node.__repr__())

    def test_repr_with_value_set(self):
        node = HTMLNode(value="my value")
        self.assertEqual('HTMLNode(tag=None, value=my value, children=None, props=None)', node.__repr__())

    def test_repr_with_children_set(self):
        childNode = HTMLNode()
        node = HTMLNode(children=childNode)
        self.assertEqual('HTMLNode(tag=None, value=None, children=HTMLNode(tag=None, value=None, children=None, props=None), props=None)', node.__repr__())

    def test_repr_with_props_set(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }        
        node = HTMLNode(props=props)
        self.assertEqual("HTMLNode(tag=None, value=None, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})", node.__repr__())
