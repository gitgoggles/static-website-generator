from blocktype import BlockType
from extractor import *
from textnode import *
from htmlnode import *

def block_to_block_type(block: str):
    heading_pattern = re.compile(r"^#{1,6}\s.*")
    multiline_code_pattern = re.compile(r"^```\n.*\n```$", re.DOTALL)
    quote_pattern = re.compile(r"^>\s.*")
    unordered_list_pattern = re.compile(r"^-\s.*")
    ordered_list_pattern = re.compile(r"^\d\.\s.*")

    if re.search(heading_pattern, block):
        return BlockType.HEADING
    if re.search(multiline_code_pattern, block):
        return BlockType.CODE
    if re.search(quote_pattern, block):
        return BlockType.QUOTE
    if re.search(unordered_list_pattern, block):
        return BlockType.UNORDERED_LIST
    if re.search(ordered_list_pattern, block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return HTMLNode(None, text_node.text)
        case TextType.BOLD:
            return HTMLNode("b", text_node.text)
        case TextType.ITALIC:
            return HTMLNode("i", text_node.text)
        case TextType.CODE:
            return HTMLNode("code", text_node.text)
        case TextType.LINK:
            return HTMLNode("a", text_node.text, None, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return HTMLNode("img", None, None, {"src": f"{text_node.url}"})


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in matches:
            image_markdown = f"![{alt}]({url})"
            before, after = remaining_text.split(image_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in matches:
            link_markdown = f"[{alt}]({url})"
            before, after = remaining_text.split(link_markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining_text = after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_text_nodes(text: str):
    output_nodes = [TextNode(text, TextType.TEXT)]
    output_nodes = split_nodes_delimiter(output_nodes, "`", TextType.CODE)
    output_nodes = split_nodes_delimiter(output_nodes, "**", TextType.BOLD)
    output_nodes = split_nodes_delimiter(output_nodes, "_", TextType.ITALIC)
    output_nodes = split_nodes_image(output_nodes)
    output_nodes = split_nodes_link(output_nodes)

    return output_nodes

def markdown_to_blocks(text: str):
    return list(map(str.strip, text.split('\n\n')))

def markdown_to_html_node(markdown: str):
    block_list = markdown_to_blocks(markdown)
    root_children = []
    for block in block_list:
        if block == "":
            continue

        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                stripped_lines = list(map(lambda x: x.strip(), block.split('\n')))
                joined_lines = " ".join(stripped_lines)

                text_nodes = text_to_text_nodes(joined_lines)
                html_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
                root_children.append(ParentNode("p", html_nodes))
                continue
            case BlockType.HEADING:
                pattern = re.compile(r"^(#{1,6})\s.*")
                match = re.search(pattern, block)
                level = len(match.group(1))
                heading_text = block[level + 1:]

                text_nodes = text_to_text_nodes(heading_text)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                root_children.append(ParentNode(f"h{level}", html_nodes))
                continue
            case BlockType.CODE:
                lines = block.split('\n')
                code_text = "\n".join(lines[1:-1]) + "\n"
                code_node = ParentNode("code", [LeafNode(None, code_text)])
                root_children.append(ParentNode("pre", [code_node]))
                continue
            case BlockType.QUOTE:
                quote_lines = []
                for line in block.split('\n'):
                    quote_lines.append(line[2:])
                quote_text = " ".join(quote_lines)
                text_nodes = text_to_text_nodes(quote_text)
                html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                root_children.append(ParentNode("blockquote", html_nodes))
                continue
            case BlockType.UNORDERED_LIST:
                li_children = []
                for line in block.split('\n'):
                    _, text = line.split("- ", 1)
                    text_nodes = text_to_text_nodes(text)
                    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                    li_children.append(ParentNode("li", html_nodes))
                root_children.append(ParentNode("ul", li_children))
                continue
            case BlockType.ORDERED_LIST:
                li_children = []
                for line in block.split('\n'):
                    _, text = line.split(". ", 1)
                    text_nodes = text_to_text_nodes(text)
                    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
                    li_children.append(ParentNode("li", html_nodes))
                root_children.append(ParentNode("ol", li_children))
                continue


    return ParentNode('div', root_children)





