from textnode import *
from blocktype import BlockType
import unittest
from htmlnode import *
from conversion import *

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, test)

    def test_split_nodes_italics(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, test)

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, test)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(input)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_heading_block_type(self):
        heading1 = "# I am a heading block"
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)

        heading2 = "## I am a heading block"
        self.assertEqual(block_to_block_type(heading2), BlockType.HEADING)

        heading3 = "### I am a heading block"
        self.assertEqual(block_to_block_type(heading3), BlockType.HEADING)

        heading4 = "#### I am a heading block"
        self.assertEqual(block_to_block_type(heading4), BlockType.HEADING)

        heading5 = "##### I am a heading block"
        self.assertEqual(block_to_block_type(heading5), BlockType.HEADING)

        heading6 = "###### I am a heading block"
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)

        heading7 = "####### I am not a heading block"
        self.assertEqual(block_to_block_type(heading7), BlockType.PARAGRAPH)

    def test_block_to_code_block_type(self):
        code1 = "```\nI am a code block\n```"
        self.assertEqual(block_to_block_type(code1), BlockType.CODE)

        code2 = "```\nI am a\n code \nblock\n```"
        self.assertEqual(block_to_block_type(code2), BlockType.CODE)

        code3 = "```\nI am not a code block"
        self.assertEqual(block_to_block_type(code3), BlockType.PARAGRAPH)

    def test_block_to_quote_block_type(self):
        quote1 = "> I am a quote block"
        self.assertEqual(block_to_block_type(quote1), BlockType.QUOTE)

        quote2 = ">I am not a quote block"
        self.assertEqual(block_to_block_type(quote2), BlockType.PARAGRAPH)

        quote3 = ">> I am not a quote block"
        self.assertEqual(block_to_block_type(quote3), BlockType.PARAGRAPH)
    
    def test_block_to_unordered_list_block_type(self):
        unordered_list1 = "- I am a unordered_list block"
        self.assertEqual(block_to_block_type(unordered_list1), BlockType.UNORDERED_LIST)

        unordered_list2 = "-- I am not a unordered_list block"
        self.assertEqual(block_to_block_type(unordered_list2), BlockType.PARAGRAPH)

    def test_block_to_ordered_list_block_type(self):
        ordered_list1 = "1. I am a ordered_list block"
        self.assertEqual(block_to_block_type(ordered_list1), BlockType.ORDERED_LIST)

        ordered_list2 = "1.I am not a ordered_list block"
        self.assertEqual(block_to_block_type(ordered_list2), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
### IMPORTANT

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><h3>IMPORTANT</h3><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

#     def test_codeblock(self):
#         md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         print(html)
#         self.assertEqual(
#             html,
#             "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
#         )


if __name__ == "__main__":
    unittest.main()

