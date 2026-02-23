import re

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)

def extract_header(text: str):
    pattern = re.compile(r"^#{1,6}\s.*")
    return re.findall(pattern, text)

def extract_multiline_code(text: str):
    pattern = re.compile(r"^```\n.*```")
    return re.findall(pattern, text)

