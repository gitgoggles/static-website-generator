import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode("p","i am node 1", None, {"href": "https://google.com"})
        html1 = ' href="https://google.com"'
        self.assertEqual(node1.props_to_html(), html1)

        node2 = HTMLNode("p","i am node 2", None, {"href": "https://google.com", "path": 'path/to/thing'})
        html2 = ' href="https://google.com" path="path/to/thing"'
        self.assertEqual(node2.props_to_html(), html2)

    def test_props_is_none(self):
        node3 = HTMLNode("p","i am node 3", None, None)
        html3 = ""
        self.assertEqual(node3.props_to_html(), html3)

class TestLeafNode(unittest.TestCase):
    def test_p_to_html(self):
        node = LeafNode("p","i am node")
        self.assertEqual(node.to_html(), "<p>i am node</p>")

    def test_href_to_html(self):
        node = LeafNode("a","i am node", {"href": "https://google.com/"})
        self.assertEqual(node.to_html(), '<a href="https://google.com/">i am node</a>')

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )


